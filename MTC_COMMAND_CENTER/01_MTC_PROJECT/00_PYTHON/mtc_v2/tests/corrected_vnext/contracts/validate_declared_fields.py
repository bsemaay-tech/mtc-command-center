from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


CONTRACTS_DIR = Path(__file__).resolve().parent
MTC_V2_ROOT = CONTRACTS_DIR.parents[2]
MANIFEST_PATH = CONTRACTS_DIR / "CONTRACT_TABLES_MANIFEST.json"
ANCHOR_PATH = CONTRACTS_DIR / "implementation_anchor.json"
REGISTRY_PATH = CONTRACTS_DIR / "declared_field_registry.json"
SEMANTIC_REVIEW_PATH = CONTRACTS_DIR / "semantic_coverage_review.json"
REGISTRY_SCHEMA = "P012_DECLARED_FIELD_REGISTRY_V1"
REPORT_SCHEMA = "P012_DECLARED_FIELD_VALIDATION_REPORT_V1"
DISPOSITIONS = frozenset({"ENFORCED", "CROSS_CHECKED", "HISTORICAL", "DECLARED_ONLY"})
DESIGN_VERSION_RE = re.compile(r"\bDesign (v[0-9]+\.[0-9]+)\s*$")
CHANGELOG_RE = re.compile(
    r"^###\s+\d+(?:\.\d+)*\s+(v[0-9]+\.[0-9]+)\s+change log(?:\s|$)",
    re.IGNORECASE,
)
PATH_COUNT_RE = re.compile(
    r"\b([0-9]+)\s+paths?\s+under\s+`?tests/corrected_vnext/?`?",
    re.IGNORECASE,
)
PRESENT_TENSE_RE = re.compile(r"\b(?:now tracks|run this session)\b", re.IGNORECASE)
HISTORICAL_MARKER_RE = re.compile(
    r"\b(?:historical|captured[-_ ]at|as[-_ ]of|measured[-_ ]at)\b", re.IGNORECASE
)
HISTORICAL_MARKER_KEYS = frozenset(
    {
        "historical",
        "historical_label",
        "captured_at",
        "captured_at_utc",
        "as_of",
        "as_of_utc",
        "measured_at",
        "measured_at_utc",
    }
)
# The record already has a convention for dating a snapshot, and it puts the date in the
# KEY NAME: design.heading_line_map_measured_at_reseal17 plus four
# heading_line_map_addition_measured_at_reseal{25,26,28,30} siblings. Five uses, and it is
# the reason that map was eventually recognised as a snapshot at all -- its own name said so.
#
# The first version of this file did not accept that convention. It recognised "historical",
# "captured_at" and "as_of" -- three spellings this record has never used -- and omitted the
# one it does use. So the check would have demanded a NEW way of saying "true on a date"
# while a working one sat five keys away. That is the same error as the original
# HEADING_MAP_ACCURATE: a checker asserting how the record ought to look instead of reading
# what the record means.
HISTORICAL_MARKER_KEY_RE = re.compile(r"measured[-_ ]at|_at_reseal\d+", re.IGNORECASE)


@dataclass(frozen=True)
class Refusal:
    code: str
    path: str
    detail: str

    def line(self) -> str:
        return f"{self.code} {self.path} {self.detail}"


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON token: {value}")


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_exact(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_pairs,
        parse_constant=_reject_constant,
    )


def _repo_root(start: Path = CONTRACTS_DIR) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise OSError(f"repository root not found above {start}")


def _path_values(documents: Mapping[str, Any], dotted_path: str) -> list[Any]:
    parts = dotted_path.split(".")
    if not parts or parts[0] not in documents:
        return []
    values = [documents[parts[0]]]
    for part in parts[1:]:
        next_values: list[Any] = []
        for value in values:
            candidates = value if type(value) is list else [value]
            for candidate in candidates:
                if type(candidate) is dict and part in candidate:
                    next_values.append(candidate[part])
        values = next_values
        if not values:
            break
    return values


def _registry_entries(registry: Any) -> tuple[list[dict[str, Any]], list[Refusal]]:
    if type(registry) is not dict or registry.get("schema") != REGISTRY_SCHEMA:
        return [], [Refusal("REGISTRY_INVALID", "registry.schema", f"expected {REGISTRY_SCHEMA}")]
    if set(registry) != {"schema", "entries"} or type(registry.get("entries")) is not list:
        return [], [Refusal("REGISTRY_INVALID", "registry", "expected only schema and entries")]

    entries: list[dict[str, Any]] = []
    refusals: list[Refusal] = []
    seen: set[str] = set()
    extra_key = {
        "ENFORCED": "enforced_at",
        "CROSS_CHECKED": "rule",
        "HISTORICAL": "rule",
        "DECLARED_ONLY": "reason",
    }
    for index, entry in enumerate(registry["entries"]):
        location = f"registry.entries.{index}"
        if type(entry) is not dict:
            refusals.append(Refusal("REGISTRY_INVALID", location, "entry must be an object"))
            continue
        path = entry.get("path")
        disposition = entry.get("disposition")
        if type(path) is not str or not path or path in seen:
            refusals.append(Refusal("REGISTRY_INVALID", location, "path must be non-empty and unique"))
            continue
        seen.add(path)
        if disposition not in DISPOSITIONS:
            refusals.append(Refusal("REGISTRY_INVALID", path, "unknown disposition"))
            continue
        expected_keys = {"path", "note", "disposition", extra_key[disposition]}
        if set(entry) != expected_keys or any(
            type(entry.get(key)) is not str or not entry[key].strip()
            for key in expected_keys - {"disposition"}
        ):
            refusals.append(
                Refusal(
                    "REGISTRY_INVALID",
                    path,
                    f"{disposition} entry must contain exactly {sorted(expected_keys)} with non-empty strings",
                )
            )
            continue
        entries.append(entry)
    return entries, refusals


def _validate_registry_coverage(
    documents: Mapping[str, Any], entries: Sequence[Mapping[str, Any]]
) -> list[Refusal]:
    refusals: list[Refusal] = []
    registered = {entry["path"] for entry in entries}
    for document_name in ("manifest", "anchor"):
        document = documents.get(document_name)
        if type(document) is not dict:
            refusals.append(Refusal("INPUT_INVALID", document_name, "document must be an object"))
            continue
        for field in sorted(document):
            path = f"{document_name}.{field}"
            if path not in registered:
                refusals.append(Refusal("UNREGISTERED_FIELD", path, "top-level field is not registered"))
    for entry in entries:
        path = entry["path"]
        if not _path_values(documents, path):
            refusals.append(Refusal("MISSING_DECLARED_FIELD", path, "registered field is absent"))
    return refusals


def _validate_enforced_claims(
    entries: Sequence[Mapping[str, Any]], mtc_v2_root: Path = MTC_V2_ROOT
) -> list[Refusal]:
    refusals: list[Refusal] = []
    root = mtc_v2_root.resolve()
    for entry in entries:
        if entry["disposition"] != "ENFORCED":
            continue
        file_text, separator, line_text = entry["enforced_at"].rpartition(":")
        try:
            line_number = int(line_text) if separator else 0
            file_path = (root / file_text).resolve()
            file_path.relative_to(root)
            lines = file_path.read_text(encoding="utf-8").splitlines()
            line = lines[line_number - 1] if 1 <= line_number <= len(lines) else ""
        except (OSError, ValueError):
            line = ""
        field_name = entry["path"].rsplit(".", 1)[-1]
        quoted_field = re.compile(rf"(['\"]){re.escape(field_name)}\1")
        if not line or quoted_field.search(line) is None:
            refusals.append(
                Refusal(
                    "ENFORCED_CLAIM_UNPROVEN",
                    entry["path"],
                    f"{entry['enforced_at']} lacks a quoted reference to {field_name}",
                )
            )
    return refusals


def _version_tuple(version: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"v([0-9]+)\.([0-9]+)", version)
    return (int(match.group(1)), int(match.group(2))) if match else None


def _read_design_text(manifest: Mapping[str, Any]) -> tuple[str | None, str]:
    design = manifest.get("design")
    design_file = design.get("file") if type(design) is dict else None
    if type(design_file) is not str or not design_file:
        return None, "manifest.design.file is missing or invalid"
    try:
        return Path(design_file).read_text(encoding="utf-8"), design_file
    except (OSError, UnicodeError) as exc:
        return None, f"{design_file}: {exc}"


def _validate_design(
    manifest: Mapping[str, Any], design_text: str | None = None
) -> list[Refusal]:
    refusals: list[Refusal] = []
    design = manifest.get("design")
    if type(design) is not dict:
        detail = "manifest.design is not an object"
        return [
            Refusal(code, "manifest.design", detail)
            for code in (
                "DESIGN_VERSION_MATCHES_BYTES",
                "DESIGN_CHANGELOG_ADOPTED",
                "HEADING_MAP_HISTORICAL_CONSISTENT",
            )
        ]
    if design_text is None:
        design_text, detail = _read_design_text(manifest)
        if design_text is None:
            return [
                Refusal(code, "manifest.design.file", detail)
                for code in (
                    "DESIGN_VERSION_MATCHES_BYTES",
                    "DESIGN_CHANGELOG_ADOPTED",
                    "HEADING_MAP_HISTORICAL_CONSISTENT",
                )
            ]

    lines = design_text.splitlines()
    title_match = DESIGN_VERSION_RE.search(lines[0]) if lines else None
    title_version = title_match.group(1) if title_match else None
    if title_version is None or design.get("version") != title_version:
        refusals.append(
            Refusal(
                "DESIGN_VERSION_MATCHES_BYTES",
                "manifest.design.version",
                f"declared={design.get('version')!r} line1={title_version!r}",
            )
        )

    changelog_versions = [
        match.group(1)
        for line in lines
        if (match := CHANGELOG_RE.match(line)) is not None
    ]
    newest = max(changelog_versions, key=_version_tuple) if changelog_versions else None
    title_tuple = _version_tuple(title_version) if title_version is not None else None
    newest_tuple = _version_tuple(newest) if newest is not None else None
    if title_tuple is None or newest_tuple is None or newest_tuple > title_tuple:
        refusals.append(
            Refusal(
                "DESIGN_CHANGELOG_ADOPTED",
                "manifest.design.version",
                f"line1={title_version!r} newest_changelog={newest!r}",
            )
        )

    heading_map = design.get("heading_line_map_measured_at_reseal17")
    if type(heading_map) is not dict:
        refusals.append(
            Refusal(
                "HEADING_MAP_HISTORICAL_CONSISTENT",
                "manifest.design.heading_line_map_measured_at_reseal17",
                "heading map is not an object",
            )
        )
    else:
        actual_headings: dict[str, list[int]] = {}
        for number, line in enumerate(lines, 1):
            match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
            if match is not None:
                actual_headings.setdefault(match.group(1), []).append(number)
        # This map is a DATED SNAPSHOT: its name is `..._measured_at_reseal17`, and the
        # design block records later additions in sibling
        # `heading_line_map_addition_measured_at_reseal{25,26,28,30}` keys rather than
        # rewriting this one. So the design is append-only and these line numbers are
        # expected to drift as content is inserted above them.
        #
        # Comparing a reseal-17 snapshot against CURRENT line numbers is therefore a
        # category error. An earlier version of this check did exactly that and produced
        # 8 false refusals; correcting the entries to current lines would have falsified a
        # dated historical record — the same defect repaired in commit 2f1008ab.
        #
        # What IS soundly checkable about a historical snapshot:
        #   * every declared heading still exists in the design (a vanished heading is real);
        #   * drift is non-negative — a heading moving EARLIER means content was deleted
        #     above it, which an append-only design should never do.
        drifts: list[tuple[str, int, int]] = []
        for heading, declared_line in heading_map.items():
            if type(heading) is not str:
                refusals.append(
                    Refusal(
                        "HEADING_MAP_HISTORICAL_CONSISTENT",
                        "manifest.design.heading_line_map_measured_at_reseal17",
                        f"non-string heading key {heading!r}",
                    )
                )
                continue
            if type(declared_line) is not int or type(declared_line) is bool:
                refusals.append(
                    Refusal(
                        "HEADING_MAP_HISTORICAL_CONSISTENT",
                        f"manifest.design.heading_line_map_measured_at_reseal17.{heading}",
                        f"declared line is not an int: {declared_line!r}",
                    )
                )
                continue
            actual_lines = actual_headings.get(heading, [])
            if not actual_lines:
                refusals.append(
                    Refusal(
                        "HEADING_MAP_HISTORICAL_CONSISTENT",
                        f"manifest.design.heading_line_map_measured_at_reseal17.{heading}",
                        f"declared={declared_line} but the heading no longer exists in the design",
                    )
                )
                continue
            drift = actual_lines[0] - declared_line
            if drift < 0:
                refusals.append(
                    Refusal(
                        "HEADING_MAP_HISTORICAL_CONSISTENT",
                        f"manifest.design.heading_line_map_measured_at_reseal17.{heading}",
                        f"declared={declared_line} actual={actual_lines[0]} drift={drift} "
                        "(negative drift means content was deleted above an append-only design)",
                    )
                )
                continue
            drifts.append((heading, declared_line, drift))
    return refusals


def _chain_refusals(
    path: str,
    history: Any,
    old_field: str,
    new_field: str,
    live_value: Any,
) -> list[Refusal]:
    if type(history) is not list or not history:
        return [Refusal("RESEAL_CHAIN_CONTINUOUS", path, "history must be a non-empty list")]
    refusals: list[Refusal] = []
    for index in range(len(history) - 1):
        current = history[index]
        following = history[index + 1]
        current_new = current.get(new_field) if type(current) is dict else None
        following_old = following.get(old_field) if type(following) is dict else None
        # A transition whose predecessor field is ABSENT is not a contradiction -- it is
        # unexaminable. Early entries of an append-only history can predate a field's
        # introduction (base_repin_history entries 1-4 carry no old_core_tree_oid_at_base;
        # the field starts at entry 5). Reporting those as a chain "break" would claim a
        # contradiction that has not been shown.
        #
        # The distinction is the whole point: the Lead's own chain walk SKIPPED these and
        # then reported "zero breaks", which conflated *nothing contradicts* with
        # *verified*. Both are worth reporting, under different codes.
        if type(following) is dict and old_field not in following:
            refusals.append(
                Refusal(
                    "CHAIN_UNVERIFIABLE",
                    f"{path}.{index}->{index + 1}",
                    f"{new_field}={current_new!r} but {old_field} is absent from entry "
                    f"{index + 1}, so this transition cannot be checked in either direction",
                )
            )
        elif current_new != following_old:
            refusals.append(
                Refusal(
                    "RESEAL_CHAIN_CONTINUOUS",
                    f"{path}.{index}->{index + 1}",
                    f"{new_field}={current_new!r} but {old_field}={following_old!r}",
                )
            )
    final = history[-1]
    final_new = final.get(new_field) if type(final) is dict else None
    if final_new != live_value:
        refusals.append(
            Refusal(
                "RESEAL_CHAIN_CONTINUOUS",
                f"{path}.{len(history) - 1}",
                f"final {new_field}={final_new!r} but live={live_value!r}",
            )
        )
    return refusals


def _orphan_refusals(
    path: str, history: Any, old_field: str, new_field: str
) -> list[Refusal]:
    if type(history) is not list:
        return []
    produced = {
        entry[new_field]
        for entry in history
        if type(entry) is dict and new_field in entry
    }
    refusals: list[Refusal] = []
    for index, entry in enumerate(history[1:], 1):
        if type(entry) is not dict or old_field not in entry:
            continue
        predecessor = entry[old_field]
        if predecessor not in produced:
            refusals.append(
                Refusal(
                    "ORPHAN_PREDECESSOR",
                    f"{path}.{index}.{old_field}",
                    f"{predecessor!r} does not appear as any {new_field}",
                )
            )
    return refusals


def _tracked_path_count(repo_root: Path) -> int:
    relative = CONTRACTS_DIR.parent.resolve().relative_to(repo_root.resolve()).as_posix()
    output = subprocess.check_output(
        ["git", "-C", str(repo_root), "ls-files", "--", relative],
        text=True,
        stderr=subprocess.STDOUT,
    )
    return len(output.splitlines())


def _semantic_review_is_validating(review: Any) -> bool:
    if type(review) is not dict or review.get("schema") != "P012_SEMANTIC_COVERAGE_REVIEW_V2":
        return False
    items = review.get("items")
    if type(items) is not dict or set(items) != {str(number) for number in range(1, 7)}:
        return False
    accepted = {"ACCEPTED", "ACCEPTED_WITH_RESIDUAL_RISK", "PASS", "PASS-WITH-NITS"}
    if any(type(item) is not dict or item.get("disposition") not in accepted for item in items.values()):
        return False
    return (
        review.get("unresolved_items") == []
        and type(review.get("signed_at")) is str
        and bool(review["signed_at"])
        and type(review.get("owner_ratification")) is dict
        and review["owner_ratification"].get("ratified") is True
    )


def _has_historical_marker(value: Any) -> bool:
    if type(value) is dict:
        if any(key.casefold() in HISTORICAL_MARKER_KEYS and bool(member) for key, member in value.items()):
            return True
        # A date carried in the key name discharges it too -- that is this record's own
        # convention, used five times in the design block.
        if any(
            HISTORICAL_MARKER_KEY_RE.search(key) is not None and bool(member)
            for key, member in value.items()
        ):
            return True
        return any(_has_historical_marker(member) for member in value.values())
    if type(value) is list:
        return any(_has_historical_marker(member) for member in value)
    return type(value) is str and HISTORICAL_MARKER_RE.search(value) is not None


def _contains_present_tense(value: Any) -> bool:
    if type(value) is dict:
        return any(_contains_present_tense(member) for member in value.values())
    if type(value) is list:
        return any(_contains_present_tense(member) for member in value)
    return type(value) is str and PRESENT_TENSE_RE.search(value) is not None


def _live_identity(repo_root: Path) -> dict[str, str]:
    head = subprocess.check_output(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()
    core = subprocess.check_output(
        [
            "git",
            "-C",
            str(repo_root),
            "rev-parse",
            "HEAD:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2/core",
        ],
        text=True,
        stderr=subprocess.STDOUT,
    ).strip()
    return {"worktree": str(repo_root.resolve()), "head_commit": head, "mtc_v2_core_tree_oid": core}


def _historical_label_refusals(
    documents: Mapping[str, Any],
    entries: Sequence[Mapping[str, Any]],
    repo_root: Path,
) -> list[Refusal]:
    try:
        live = _live_identity(repo_root)
    except (OSError, subprocess.CalledProcessError) as exc:
        return [Refusal("HISTORICAL_LABELLED", "repository", f"live identity unavailable: {exc}")]
    refusals: list[Refusal] = []
    for entry in entries:
        if entry["disposition"] != "HISTORICAL":
            continue
        for value in _path_values(documents, entry["path"]):
            if type(value) is not dict:
                continue
            mismatches: list[str] = []
            for field, live_value in live.items():
                if field not in value:
                    continue
                recorded = value[field]
                if field == "worktree":
                    try:
                        differs = Path(recorded).resolve() != Path(live_value).resolve()
                    except (OSError, TypeError):
                        differs = True
                else:
                    differs = recorded != live_value
                if differs:
                    mismatches.append(field)
            if mismatches and (not _has_historical_marker(value) or _contains_present_tense(value)):
                refusals.append(
                    Refusal(
                        "HISTORICAL_LABELLED",
                        entry["path"],
                        f"stale identities={','.join(mismatches)} marker={_has_historical_marker(value)} present_tense={_contains_present_tense(value)}",
                    )
                )
    return refusals


def _validate_cross_checks(
    manifest: Mapping[str, Any],
    anchor: Mapping[str, Any],
    entries: Sequence[Mapping[str, Any]],
    repo_root: Path,
    *,
    design_text: str | None = None,
    tracked_path_count: int | None = None,
    semantic_review: Any = None,
    baseline_digest: str | None = None,
) -> list[Refusal]:
    refusals: list[Refusal] = []
    seal_state = manifest.get("seal_state")
    seal = manifest.get("seal")
    seal_state = seal_state if type(seal_state) is dict else {}
    seal = seal if type(seal) is dict else {}

    if seal_state.get("EXPECTED_SEAL_SHA") != seal.get("EXPECTED_SEAL_SHA"):
        refusals.append(
            Refusal(
                "SEAL_STATE_SEAL_AGREE",
                "manifest.seal_state.EXPECTED_SEAL_SHA",
                f"seal_state={seal_state.get('EXPECTED_SEAL_SHA')!r} seal={seal.get('EXPECTED_SEAL_SHA')!r}",
            )
        )
    bases = (
        seal_state.get("IMPLEMENTATION_BASE_SHA"),
        seal.get("IMPLEMENTATION_BASE_SHA"),
        anchor.get("IMPLEMENTATION_BASE_SHA"),
    )
    if not (bases[0] == bases[1] == bases[2]):
        refusals.append(
            Refusal(
                "SEAL_STATE_BASE_AGREE",
                "manifest.seal_state.IMPLEMENTATION_BASE_SHA",
                f"seal_state={bases[0]!r} seal={bases[1]!r} anchor={bases[2]!r}",
            )
        )

    chain_specs = (
        (
            "manifest.reseal_history",
            manifest.get("reseal_history"),
            "old_EXPECTED_SEAL_SHA",
            "new_EXPECTED_SEAL_SHA",
            seal.get("EXPECTED_SEAL_SHA"),
        ),
        (
            "anchor.reseal_history",
            anchor.get("reseal_history"),
            "old_EXPECTED_SEAL_SHA",
            "new_EXPECTED_SEAL_SHA",
            anchor.get("EXPECTED_SEAL_SHA"),
        ),
        (
            "anchor.base_repin_history.base_commit",
            anchor.get("base_repin_history"),
            "old_IMPLEMENTATION_BASE_SHA",
            "new_IMPLEMENTATION_BASE_SHA",
            anchor.get("IMPLEMENTATION_BASE_SHA"),
        ),
        (
            "anchor.base_repin_history.core_tree",
            anchor.get("base_repin_history"),
            "old_core_tree_oid_at_base",
            "new_core_tree_oid_at_base",
            anchor.get("core_tree_oid_at_base"),
        ),
    )
    for path, history, old_field, new_field, live_value in chain_specs:
        refusals.extend(_chain_refusals(path, history, old_field, new_field, live_value))
        refusals.extend(_orphan_refusals(path, history, old_field, new_field))

    refusals.extend(_validate_design(manifest, design_text))

    provenance = manifest.get("expected_value_provenance")
    statement = provenance.get("statement") if type(provenance) is dict else None
    if type(statement) is not str:
        refusals.append(
            Refusal(
                "PATH_COUNT_ACCURATE",
                "manifest.expected_value_provenance.statement",
                "statement is not a string",
            )
        )
    else:
        try:
            measured_count = _tracked_path_count(repo_root) if tracked_path_count is None else tracked_path_count
            for match in PATH_COUNT_RE.finditer(statement):
                declared_count = int(match.group(1))
                if declared_count != measured_count:
                    refusals.append(
                        Refusal(
                            "PATH_COUNT_ACCURATE",
                            "manifest.expected_value_provenance.statement",
                            f"declared={declared_count} measured={measured_count}",
                        )
                    )
        except (OSError, ValueError, subprocess.CalledProcessError) as exc:
            refusals.append(
                Refusal(
                    "PATH_COUNT_ACCURATE",
                    "manifest.expected_value_provenance.statement",
                    f"tracked path count unavailable: {exc}",
                )
            )

    if semantic_review is None:
        try:
            semantic_review = load_json_exact(SEMANTIC_REVIEW_PATH)
        except (OSError, ValueError, json.JSONDecodeError):
            semantic_review = None
    section = manifest.get("section_16_review")
    status = section.get("status") if type(section) is dict else None
    section_statement = section.get("statement") if type(section) is dict else None
    says_unperformed = (
        type(status) is str
        and re.search(r"PENDING|UNPERFORMED|NOT[^A-Z0-9]*PERFORMED", status, re.IGNORECASE) is not None
    ) or (
        type(section_statement) is str
        and re.search(r"\b(?:has\s+)?NOT\s+(?:been\s+)?performed\b", section_statement, re.IGNORECASE)
        is not None
    )
    if _semantic_review_is_validating(semantic_review) and says_unperformed:
        refusals.append(
            Refusal(
                "SECTION16_STATUS_CONSISTENT",
                "manifest.section_16_review.status",
                f"declared={status!r} while a validating semantic_coverage_review.json is installed",
            )
        )

    pin = manifest.get("legacy_event_order_map_pin")
    baseline = pin.get("baseline_manifest") if type(pin) is dict else None
    if type(baseline) is not dict:
        refusals.append(
            Refusal(
                "BASELINE_PIN_CURRENT_OR_LABELLED",
                "manifest.legacy_event_order_map_pin.baseline_manifest",
                "baseline_manifest is not an object",
            )
        )
    else:
        recorded_digest = baseline.get("sha256")
        baseline_path = baseline.get("path")
        try:
            if baseline_digest is None:
                actual_digest = hashlib.sha256(Path(baseline_path).read_bytes()).hexdigest()
            else:
                actual_digest = baseline_digest
        except (OSError, TypeError) as exc:
            actual_digest = f"unavailable:{exc}"
        if recorded_digest != actual_digest and not _has_historical_marker(baseline):
            refusals.append(
                Refusal(
                    "BASELINE_PIN_CURRENT_OR_LABELLED",
                    "manifest.legacy_event_order_map_pin.baseline_manifest",
                    f"recorded={recorded_digest!r} actual={actual_digest!r} and no explicit historical label",
                )
            )

    refusals.extend(_historical_label_refusals({"manifest": manifest, "anchor": anchor}, entries, repo_root))
    return refusals


def validate_documents(
    manifest: Mapping[str, Any],
    anchor: Mapping[str, Any],
    registry: Mapping[str, Any],
    *,
    repo_root: Path | None = None,
    mtc_v2_root: Path = MTC_V2_ROOT,
    design_text: str | None = None,
    tracked_path_count: int | None = None,
    semantic_review: Any = None,
    baseline_digest: str | None = None,
) -> list[Refusal]:
    entries, refusals = _registry_entries(registry)
    documents = {"manifest": manifest, "anchor": anchor}
    if refusals:
        return refusals
    refusals.extend(_validate_registry_coverage(documents, entries))
    refusals.extend(_validate_enforced_claims(entries, mtc_v2_root))
    try:
        resolved_repo_root = _repo_root() if repo_root is None else repo_root
    except OSError as exc:
        refusals.append(Refusal("INPUT_INVALID", "repository", str(exc)))
        return refusals
    if type(manifest) is dict and type(anchor) is dict:
        refusals.extend(
            _validate_cross_checks(
                manifest,
                anchor,
                entries,
                resolved_repo_root,
                design_text=design_text,
                tracked_path_count=tracked_path_count,
                semantic_review=semantic_review,
                baseline_digest=baseline_digest,
            )
        )
    return refusals


def _write_report(path: Path, refusals: Sequence[Refusal]) -> None:
    report = {
        "schema": REPORT_SCHEMA,
        "status": "REFUSE" if refusals else "PASS",
        "refusal_count": len(refusals),
        "refusals": [asdict(refusal) for refusal in refusals],
    }
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate all registered P0-12 declared fields.")
    parser.add_argument("--json", type=Path, help="write a machine-readable validation report")
    args = parser.parse_args(argv)
    try:
        manifest = load_json_exact(MANIFEST_PATH)
        anchor = load_json_exact(ANCHOR_PATH)
        registry = load_json_exact(REGISTRY_PATH)
        refusals = validate_documents(manifest, anchor, registry)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        refusals = [Refusal("INPUT_INVALID", "input", str(exc))]
    for refusal in refusals:
        print(refusal.line())
    if not refusals:
        print("PASS")
    if args.json is not None:
        _write_report(args.json, refusals)
    return 1 if refusals else 0


if __name__ == "__main__":
    raise SystemExit(main())
