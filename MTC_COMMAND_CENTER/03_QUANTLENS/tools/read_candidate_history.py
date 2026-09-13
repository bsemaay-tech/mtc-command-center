#!/usr/bin/env python3
"""Read legacy candidate records and print one mapping report to stdout.

This reader has no output-file option and opens every repository input read-only.
It does not create a lifecycle ledger or assign current lifecycle status.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


COMMAND_CENTER = Path(__file__).resolve().parents[2]
REGISTRY = COMMAND_CENTER / "05_REGISTRY"
STRATEGIES = COMMAND_CENTER / "03_QUANTLENS" / "strategies"
STATUS = COMMAND_CENTER / "03_STATUS"

REGISTER_PATHS = (
    REGISTRY / "STRATEGY_RESEARCH_REGISTRY.json",
    REGISTRY / "TRIAGE_CANDIDATE_REGISTRY.json",
    REGISTRY / "AI_QUANTLENS_VERDICT_REGISTRY.json",
    REGISTRY / "VARIANT_LOG_REGISTRY.json",
    REGISTRY / "PROMOTION_REGISTRY.json",
    REGISTRY / "STRATEGY_REGISTRY.json",
)

# WAYFINDER_LIFECYCLE_FOLD_2026-08-23.md section 4a.
OLD_STATUS_MAP = {
    "REJECTED": ("REJECTED", ()),
    "KEEP_AS_RESEARCH_NOTE": ("PARKED", ("legacy:research_note",)),
    "PROMOTE_TO_SANDBOX": ("CANDIDATE", ("legacy:sandbox",)),
    "PROMOTE_TO_FORWARD_PAPER_TRADE": (
        "CANDIDATE",
        ("legacy:forward_paper_aspirant",),
    ),
    "MTC_ENGINE_VALIDATED": ("CANDIDATE", ("legacy:mtc_engine_validated",)),
    "PROMOTE_TO_PARITY_CANDIDATE": (
        "CANDIDATE",
        ("legacy:parity_candidate",),
    ),
    "APPROVED_FOR_MTC_V2_INTEGRATION": (
        "CANDIDATE",
        ("legacy:approved_v2_integration",),
    ),
}

# Owner decision 115 applies these four current_status values only.
CURRENT_STATUS_TO_CAPTURED = {
    "RESEARCH_BATCH",
    "READY_FOR_DETERMINISTIC_REVIEW",
    "READY_FOR_PYTHON_PROTOTYPE",
    "TRIAGED",
}

DIAGNOSTIC_LABELS = {
    "TRUE_ALPHA_CANDIDATE",
    "BENCHMARK_BEATER",
    "BETA_DISGUISED_AS_ALPHA",
    "REGIME_SPECIFIC_EDGE",
    "OVERFIT_SUSPECT",
    "STATISTICALLY_UNCONFIRMED",
    "INSUFFICIENT_TRADES",
    "NO_DATA",
    "REJECTED",
}

ADVISORY_TAGS = {
    "NEEDS_CLARIFICATION": "advisory:needs_clarification",
    "RESEARCH_ONLY": "advisory:research_only",
    "SALVAGE": "advisory:salvage",
}

RANKING_REASON = (
    "The recorded rule requires the missing written state ranking; no ranking was invented."
)


class Refusal(RuntimeError):
    """Raised when a declared input cannot be read without guessing."""


@dataclass
class Projection:
    state: str | None = None
    labels: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)


@dataclass
class Outcome:
    source: str
    record_id: str
    disposition: str
    mapped_state: str | None
    labels: list[str]
    effects: list[str]
    reasons: list[str]


def _relative(path: Path) -> str:
    return path.relative_to(COMMAND_CENTER).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"{_relative(path)} is unreadable JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise Refusal(f"{_relative(path)} must contain one JSON object")
    return value


def _list_field(document: dict[str, Any], key: str, source: str) -> list[Any]:
    value = document.get(key)
    if not isinstance(value, list):
        raise Refusal(f"{source}.{key} must be an array")
    return value


def _string_field(document: dict[str, Any], key: str, source: str) -> str:
    value = document.get(key)
    if not isinstance(value, str) or not value:
        raise Refusal(f"{source}.{key} must be a non-empty string")
    return value


def _unique(rows: Iterable[dict[str, Any]], key: str, source: str) -> None:
    values = [_string_field(row, key, source) for row in rows]
    duplicates = sorted(value for value, count in collections.Counter(values).items() if count > 1)
    if duplicates:
        raise Refusal(f"{source}.{key} contains duplicate values: {duplicates}")


def _discover_inputs() -> tuple[list[Path], list[Path], list[Path]]:
    specs = sorted(STRATEGIES.glob("STG*/producer_spec.json"))
    scorecards = sorted(STATUS.rglob("*.scorecard.json"))
    inputs = sorted((*REGISTER_PATHS, *specs, *scorecards), key=_relative)
    missing = [path for path in inputs if not path.is_file()]
    if missing:
        raise Refusal("declared input is missing: " + ", ".join(map(str, missing)))
    return inputs, specs, scorecards


def _file_hashes(paths: Iterable[Path]) -> dict[str, str]:
    return {_relative(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def _manifest_hash(hashes: dict[str, str]) -> str:
    manifest = "\n".join(f"{path} {digest}" for path, digest in sorted(hashes.items()))
    return hashlib.sha256(manifest.encode("utf-8")).hexdigest()


def _map_current_status(row: dict[str, Any], source: str) -> Projection:
    value = _string_field(row, "current_status", source)
    if "|" in value:
        parts = value.split("|")
        if any(not part for part in parts):
            raise Refusal(f"{source}.current_status has an empty composite component")
        return Projection(labels=parts, reasons=[RANKING_REASON])
    if value in CURRENT_STATUS_TO_CAPTURED:
        return Projection(
            state="CAPTURED",
            labels=[value],
            notes=[f'Original current_status kept visibly as "{value}".'],
        )
    if value in OLD_STATUS_MAP:
        state, tags = OLD_STATUS_MAP[value]
        return Projection(state=state, labels=[value], tags=list(tags))
    return Projection(
        labels=[value],
        reasons=[f'No recorded mapping exists for current_status "{value}".'],
    )


def _map_promotion_status(spec: dict[str, Any], source: str) -> Projection:
    if "promotion_status" not in spec:
        return Projection(
            state="CAPTURED",
            notes=["promotion_status is missing and is marked missing."],
        )
    values = spec["promotion_status"]
    if not isinstance(values, list):
        raise Refusal(f"{source}.promotion_status must be an array when present")
    if any(not isinstance(value, str) or not value for value in values):
        raise Refusal(f"{source}.promotion_status must contain only non-empty strings")
    if not values:
        return Projection(
            state="CAPTURED",
            notes=["promotion_status is empty and is marked missing."],
        )
    if len(values) > 1:
        return Projection(labels=list(values), reasons=[RANKING_REASON])
    value = values[0]
    if value not in OLD_STATUS_MAP:
        return Projection(
            labels=[value],
            reasons=[f'No recorded promotion_status mapping exists for "{value}".'],
        )
    state, tags = OLD_STATUS_MAP[value]
    return Projection(state=state, labels=[value], tags=list(tags))


def _map_classification(spec: dict[str, Any], source: str) -> Projection:
    lockbox = spec.get("metrics_lockbox")
    if lockbox is None:
        return Projection()
    if not isinstance(lockbox, dict):
        raise Refusal(f"{source}.metrics_lockbox must be an object when present")
    if "classification" not in lockbox:
        return Projection()
    value = lockbox["classification"]
    if not isinstance(value, str) or not value:
        raise Refusal(f"{source}.metrics_lockbox.classification must be a non-empty string")
    if value not in DIAGNOSTIC_LABELS:
        return Projection(
            labels=[value],
            reasons=[f'No recorded diagnostic-label mapping exists for "{value}".'],
        )
    return Projection(labels=[value], tags=[f"label:{value.lower()}"])


def _strategy_outcomes(
    rows: list[dict[str, Any]], specs_by_path: dict[str, dict[str, Any]]
) -> list[Outcome]:
    outcomes: list[Outcome] = []
    used_specs: set[str] = set()
    for row in rows:
        strategy_id = _string_field(row, "strategy_id", "strategy record")
        source_folder = _string_field(row, "source_folder", strategy_id).replace("\\", "/")
        spec_path = f"{source_folder.rstrip('/')}/producer_spec.json"
        if spec_path not in specs_by_path:
            raise Refusal(
                f"{strategy_id}.source_folder does not contain a discovered producer_spec.json"
            )
        used_specs.add(spec_path)
        spec = specs_by_path[spec_path]
        current = _map_current_status(row, strategy_id)
        promotion = _map_promotion_status(spec, spec_path)
        classification = _map_classification(spec, spec_path)
        parts = (current, promotion, classification)
        reasons = [reason for part in parts for reason in part.reasons]
        states = {part.state for part in parts if part.state is not None}
        raw_conflict = bool(promotion.labels) and current.labels != promotion.labels
        if len(states) > 1:
            reasons.append(
                "MIGRATED_CONFLICT: source values project to different states; both values are "
                "kept and neither wins silently."
            )
        effects = [*current.tags, *promotion.tags, *classification.tags]
        effects.extend(note for part in parts for note in part.notes)
        if raw_conflict:
            effects.append("migrated-conflict: both source values retained")
        labels = [*current.labels, *promotion.labels, *classification.labels]
        disposition = "UNPLACED" if reasons else "MAPPED"
        outcomes.append(
            Outcome(
                source="strategy + producer_spec",
                record_id=strategy_id,
                disposition=disposition,
                mapped_state=None if reasons else next(iter(states), None),
                labels=labels,
                effects=effects,
                reasons=list(dict.fromkeys(reasons)),
            )
        )
    unused = sorted(set(specs_by_path) - used_specs)
    if unused:
        raise Refusal("producer specs are not named by strategy source_folder: " + ", ".join(unused))
    return outcomes


def _triage_outcomes(rows: list[dict[str, Any]]) -> list[Outcome]:
    outcomes = []
    for row in rows:
        candidate_id = _string_field(row, "candidate_id", "triage record")
        effects = ["may be reviewed again later"]
        if row.get("eligible_for_retriage") is True:
            effects.append("legacy:retriage_eligible")
        elif row.get("eligible_for_retriage") not in (True, False):
            raise Refusal(f"{candidate_id}.eligible_for_retriage must be true or false")
        outcomes.append(
            Outcome("triage registry", candidate_id, "MAPPED", "CAPTURED", [], effects, [])
        )
    return outcomes


def _advisory_outcomes(rows: list[dict[str, Any]]) -> list[Outcome]:
    outcomes = []
    for row in rows:
        strategy_id = _string_field(row, "strategy_id", "advisory record")
        decision = _string_field(row, "decision", strategy_id)
        tag = ADVISORY_TAGS.get(decision)
        if tag is None:
            outcomes.append(
                Outcome(
                    "advisory registry",
                    strategy_id,
                    "UNPLACED",
                    None,
                    [decision],
                    [],
                    [f'No recorded advisory mapping exists for "{decision}".'],
                )
            )
        else:
            outcomes.append(
                Outcome("advisory registry", strategy_id, "MAPPED", None, [decision], [tag], [])
            )
    return outcomes


def _variant_outcomes(rows: list[dict[str, Any]]) -> list[Outcome]:
    outcomes = []
    for row in rows:
        variant_id = _string_field(row, "variant_id", "variant record")
        promotable = row.get("promotable")
        if not isinstance(promotable, bool):
            raise Refusal(f"{variant_id}.promotable must be true or false")
        if not promotable:
            outcomes.append(
                Outcome("variant registry", variant_id, "MAPPED", None, ["false"], ["no effect"], [])
            )
        elif not isinstance(row.get("family_id"), str) or not row["family_id"]:
            outcomes.append(
                Outcome(
                    "variant registry",
                    variant_id,
                    "UNPLACED",
                    None,
                    ["true"],
                    [],
                    ["promotable is true but no recorded family_id exists; no family was invented."],
                )
            )
        else:
            outcomes.append(
                Outcome(
                    "variant registry",
                    variant_id,
                    "MAPPED",
                    None,
                    ["true"],
                    ["legacy:promotable"],
                    [],
                )
            )
    return outcomes


def _escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _histogram(values: Iterable[object]) -> str:
    counts = collections.Counter(values)
    return ", ".join(f"{_escape(value)} x{count}" for value, count in sorted(counts.items(), key=lambda x: str(x[0])))


def _render_report(
    documents: dict[str, dict[str, Any]],
    outcomes: list[Outcome],
    scorecards: list[Path],
    before: dict[str, str],
    after: dict[str, str],
    spec_count: int,
) -> str:
    strategy_rows = _list_field(documents["research"], "strategies", "research registry")
    triage_rows = _list_field(documents["triage"], "candidates", "triage registry")
    advisory_rows = _list_field(documents["advisory"], "entries", "advisory registry")
    variant_rows = _list_field(documents["variants"], "variants", "variant registry")
    promotion_rows = _list_field(documents["promotions"], "promotions", "promotion registry")
    old_strategy_rows = _list_field(documents["old_strategy"], "candidates", "strategy registry")
    mapped = [item for item in outcomes if item.disposition == "MAPPED"]
    unplaced = [item for item in outcomes if item.disposition == "UNPLACED"]
    read_count = len(outcomes) + len(scorecards)
    if len(mapped) + len(unplaced) + len(scorecards) != read_count:
        raise AssertionError("report categories do not balance")

    lines = [
        "# Candidate-history reading and mapping report",
        "",
        "This is a read-only projection, not a lifecycle history book and not a statement of any "
        "candidate's current status. `UNPLACED` is a report disposition, not a lifecycle state.",
        "",
        "## Measured inputs",
        "",
        "| Source | Source units read | Measured values |",
        "|---|---:|---|",
        f"| Strategy research registry joined to its recorded producer file | {len(strategy_rows)} | "
        f"current_status: {_histogram(row.get('current_status') for row in strategy_rows)}; "
        f"producer files: {spec_count} |",
        f"| Triage candidate registry | {len(triage_rows)} | summary.total: "
        f"{_escape(documents['triage'].get('summary', {}).get('total'))} |",
        f"| Advisory verdict registry | {len(advisory_rows)} | decisions: "
        f"{_histogram(row.get('decision') for row in advisory_rows)} |",
        f"| Variant registry | {len(variant_rows)} | promotable: "
        f"{_histogram(row.get('promotable') for row in variant_rows)} |",
        f"| Retired promotion registry | {len(promotion_rows)} | deliberately not mapped; retired from service |",
        f"| Retired strategy registry | {len(old_strategy_rows)} | deliberately not mapped; retired from service |",
        f"| Observed `03_STATUS/**/*.scorecard.json` evidence files | {len(scorecards)} | deliberately excluded; this observed set is not claimed as an owner-ratified complete corpus |",
        "",
        "## Applied mappings",
        "",
        "| Old value or source case | Report result |",
        "|---|---|",
        "| RESEARCH_BATCH, READY_FOR_DETERMINISTIC_REVIEW, READY_FOR_PYTHON_PROTOTYPE, or TRIAGED in current_status | CAPTURED; original literal remains visible |",
        "| PROMOTE_TO_FORWARD_PAPER_TRADE | CANDIDATE + legacy:forward_paper_aspirant |",
        "| Composite current_status | UNPLACED: highest-ranked rule needs the missing written ranking |",
        "| Multi-label promotion_status array | UNPLACED: lowest-ranked rule needs the missing written ranking |",
        "| Missing promotion_status | CAPTURED and marked missing |",
        "| FORWARD_PAPER_CANDIDATE or RESEARCH_GRADE in promotion_status | UNPLACED: no recorded mapping |",
        "| Recognised diagnostic classification | label:<lowercased>; never a state |",
        "| PASS or STRONG_PASS diagnostic classification | UNPLACED: no recorded diagnostic-label mapping |",
        "| Every triage candidate | CAPTURED; visibly marked as reviewable later |",
        "| NEEDS_CLARIFICATION, RESEARCH_ONLY, or SALVAGE advisory verdict | corresponding advisory:* tag; never a state |",
        "| promotable=false variant | resolved no-effect |",
        "| scorecard evidence file | DELIBERATELY_EXCLUDED; remains readable in place |",
        "",
        "No tag token was invented for the owner's phrases `original label`, `marked missing`, or "
        "`may be reviewed again later`; those phrases are shown literally in this report.",
        "",
        "## UNPLACED records",
        "",
        "| Source | Record | Source labels kept | Exact reason |",
        "|---|---|---|---|",
    ]
    for item in unplaced:
        lines.append(
            f"| {_escape(item.source)} | {_escape(item.record_id)} | "
            f"{_escape(', '.join(item.labels) or '-')} | {_escape(' '.join(item.reasons))} |"
        )

    lines.extend(
        [
            "",
            "## Deliberately excluded sources",
            "",
            "The two retired registers contain zero rows. The following observed scorecard evidence "
            "files were counted but not mapped, copied, moved, or changed:",
            "",
        ]
    )
    lines.extend(f"- `{_relative(path)}`" for path in scorecards)

    changed = sorted(path for path in before.keys() | after.keys() if before.get(path) != after.get(path))
    lines.extend(
        [
            "",
            "## Read-only proof",
            "",
            f"Each of {len(before)} input files was hashed individually. The displayed digest hashes "
            "the sorted `relative path + file SHA-256` manifest.",
            "",
            f"- Before: `{_manifest_hash(before)}`",
            f"- After: `{_manifest_hash(after)}`",
            f"- Changed inputs: {len(changed)}",
            f"- Result: {'UNCHANGED' if not changed else 'CHANGED - REFUSE THIS REPORT'}",
            "",
            "## Final counts",
            "",
            f"READ={read_count} MAPPED={len(mapped)} UNPLACED={len(unplaced)} "
            f"DELIBERATELY_EXCLUDED={len(scorecards)}",
            f"Balance: {len(mapped)} + {len(unplaced)} + {len(scorecards)} = {read_count}",
        ]
    )
    if changed:
        lines.extend(["", "Changed paths:", *[f"- `{path}`" for path in changed]])
    return "\n".join(lines) + "\n"


def build_report() -> str:
    before_paths, specs, scorecards = _discover_inputs()
    before = _file_hashes(before_paths)
    documents = {
        "research": _load_json(REGISTER_PATHS[0]),
        "triage": _load_json(REGISTER_PATHS[1]),
        "advisory": _load_json(REGISTER_PATHS[2]),
        "variants": _load_json(REGISTER_PATHS[3]),
        "promotions": _load_json(REGISTER_PATHS[4]),
        "old_strategy": _load_json(REGISTER_PATHS[5]),
    }
    strategy_rows = _list_field(documents["research"], "strategies", "research registry")
    triage_rows = _list_field(documents["triage"], "candidates", "triage registry")
    advisory_rows = _list_field(documents["advisory"], "entries", "advisory registry")
    variant_rows = _list_field(documents["variants"], "variants", "variant registry")
    for rows, key, source in (
        (strategy_rows, "strategy_id", "research registry"),
        (triage_rows, "candidate_id", "triage registry"),
        (advisory_rows, "strategy_id", "advisory registry"),
        (variant_rows, "variant_id", "variant registry"),
    ):
        if any(not isinstance(row, dict) for row in rows):
            raise Refusal(f"{source} contains a non-object row")
        _unique(rows, key, source)

    specs_by_path = {_relative(path): _load_json(path) for path in specs}
    outcomes = [
        *_strategy_outcomes(strategy_rows, specs_by_path),
        *_triage_outcomes(triage_rows),
        *_advisory_outcomes(advisory_rows),
        *_variant_outcomes(variant_rows),
    ]
    after_paths, after_specs, after_scorecards = _discover_inputs()
    if [*_map_relative(before_paths)] != [*_map_relative(after_paths)]:
        raise Refusal("the input file set changed while the report was being built")
    after = _file_hashes(after_paths)
    return _render_report(documents, outcomes, after_scorecards, before, after, len(after_specs))


def _map_relative(paths: Iterable[Path]) -> Iterable[str]:
    return map(_relative, paths)


def self_check() -> int:
    modified_copy = {"strategy_id": "STG-MODIFIED"}
    try:
        _map_current_status(modified_copy, "modified copy")
    except Refusal as exc:
        print(f"DETECTED refusal: {exc}")
    else:
        print("NOT DETECTED: modified copy without current_status was accepted", file=sys.stderr)
        return 1
    control = _map_current_status(
        {"current_status": "RESEARCH_BATCH"}, "accepted control"
    )
    if control.state != "CAPTURED" or control.reasons:
        print("NOT DETECTED: accepted control did not map to CAPTURED", file=sys.stderr)
        return 1
    print("accepted control: RESEARCH_BATCH -> CAPTURED")
    composite = _map_current_status(
        {"current_status": "PROMOTE_TO_FORWARD_PAPER_TRADE|PROMOTE_TO_PARITY_CANDIDATE"},
        "ranking check",
    )
    if composite.state is not None or RANKING_REASON not in composite.reasons:
        print("NOT DETECTED: missing ranking did not leave the composite UNPLACED", file=sys.stderr)
        return 1
    array = _map_promotion_status(
        {
            "promotion_status": [
                "PROMOTE_TO_FORWARD_PAPER_TRADE",
                "PROMOTE_TO_PARITY_CANDIDATE",
            ]
        },
        "ranking check",
    )
    if array.state is not None or RANKING_REASON not in array.reasons:
        print("NOT DETECTED: missing ranking did not leave the array UNPLACED", file=sys.stderr)
        return 1
    print("DETECTED missing ranking: composite and array remain UNPLACED")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="run the in-memory modified-copy refusal check instead of reading repository inputs",
    )
    args = parser.parse_args(argv)
    if args.self_check:
        return self_check()
    try:
        report = build_report()
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    print(report, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
