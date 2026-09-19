#!/usr/bin/env python3
"""Deterministic read-only reproducer for P014 small report."""

from __future__ import annotations

import ast
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LEDGER_PATH = ROOT / "fixture-ledger.sqlite"
RESTORED_LEDGER_PATH = ROOT / "fixture-ledger.restored.sqlite"
BACKUP_LEDGER_PATH = ROOT / "fixture-ledger.backup.sqlite"
STATUS_REPORT_PATH = ROOT / "fixture-status-report.json"
SCOPE_PATH = ROOT / "P031_M1_SCOPE_AND_STATUS.md"
LEDGER_READER_PATH = ROOT / "p031_lifecycle_ledger.py"
TRIAL_CATALOG_PATH = ROOT / "trial_catalog.py"
TRIAL_TEST_PATH = ROOT / "test_trial_catalog_types.py"
CONTRACT_ROOT = Path(r"C:\tmp\P013_CONTRACT_V2_20260912")
CONTRACT_WRITE_TARGETS = {
    "trades.parquet",
    "equity.parquet",
    "intents.jsonl",
    "levels.parquet",
}


def md_cell(value: object) -> str:
    return str(value).replace("|", "\\|")


def check_set_purpose(
    event_type: str, previous_state: str | None, writer_class: str | None
) -> str | None:
    if event_type in {"TRIAGED", "DECLINED"}:
        return "worthiness"
    if event_type == "SHADOW_ELIGIBLE":
        return "shadow_eligibility"
    if event_type == "PAPER_ELIGIBLE":
        return "paper_eligibility"
    if event_type == "TESTNET_ELIGIBLE":
        return "testnet_live_candidate_eligibility"
    if event_type == "LIVE_CANDIDATE":
        return "live_candidate_eligibility"
    if event_type == "ADMISSION_WITHHELD_CAPACITY":
        return "shadow_eligibility" if previous_state == "FROZEN" else None
    if event_type == "PROMOTED" or (
        event_type == "RESUMED" and writer_class == "PROMOTION_AUTHORITY"
    ):
        return "promotion"
    if event_type in {"SUSPENDED", "RETIRED"} or (
        event_type == "RESUMED" and writer_class == "MULTI_WORKER_SUPERVISOR"
    ):
        return "supervisor"
    return None


def load_ledger_state(path: Path):
    conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM lifecycle_events ORDER BY global_sequence"
        ).fetchall()
        current_rows = conn.execute(
            "SELECT * FROM lifecycle_current ORDER BY candidate_id"
        ).fetchall()
    finally:
        conn.close()

    events = []
    for row in rows:
        event = json.loads(bytes(row["canonical_event"]))
        evidence = json.loads(bytes(row["canonical_evidence"]))
        events.append(
            {
                "candidate_id": event["candidate_id"],
                "global_sequence": row["global_sequence"],
                "event_type": event["event_type"],
                "previous_state": event["previous_state"],
                "next_state": event["next_state"],
                "reason": event.get("reason"),
                "timestamp": event["timestamp"],
                "writer_class": event["writer_class"],
                "writer_id": event["writer_id"],
                "source_kind": evidence.get("source_kind"),
                "check_set_version": evidence.get("check_set_version"),
                "evaluation_run_hash": evidence.get("evaluation_run_hash"),
                "failing_checks": evidence.get("failing_checks", []),
                "evidence_keys": sorted(evidence.keys()),
                "check_set_purpose_persisted": "check_set_purpose" in evidence,
            }
        )

    # check_set_purpose is not persisted in this fixture evidence; derive from event shape.
    for item in events:
        item["check_set_purpose"] = check_set_purpose(
            item["event_type"], item["previous_state"], item["writer_class"]
        )

    latest_by_candidate = {e["candidate_id"]: e for e in events}
    return events, current_rows, latest_by_candidate


def locate_json_array(path: Path, key: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines, start=1):
        if f'"{key}"' in line:
            start = i
            stripped = line.strip()
            if stripped.endswith("]") or stripped.endswith("],"):
                return f"{path}:{i}"
            for j in range(i + 1, len(lines) + 1):
                if lines[j - 1].strip() in ("]", "],"):
                    return f"{path}:{start}-{j}"
            return f"{path}:{start}"
    return str(path)


def read_unresolved_lifecycle_contracts_json() -> tuple[list[str], str]:
    payload = json.loads(STATUS_REPORT_PATH.read_text(encoding="utf-8"))
    unresolved = payload.get("unresolved_lifecycle_contracts")
    items = [str(x) for x in unresolved] if isinstance(unresolved, list) else []
    return items, locate_json_array(STATUS_REPORT_PATH, "unresolved_lifecycle_contracts")


def read_unresolved_lifecycle_contracts_reader() -> tuple[list[str], str]:
    text = LEDGER_READER_PATH.read_text(encoding="utf-8")
    mod = ast.parse(text)
    for node in mod.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name != "_render_status_report":
            continue
        for child in ast.walk(node):
            if not isinstance(child, ast.Dict):
                continue
            for key, value in zip(child.keys, child.values):
                if not isinstance(key, ast.Constant):
                    continue
                if key.value != "unresolved_lifecycle_contracts":
                    continue
                if not isinstance(value, ast.List):
                    continue
                items = [
                    elt.value
                    for elt in value.elts
                    if isinstance(elt, ast.Constant)
                ]
                end = value.end_lineno or value.lineno
                return items, f"{LEDGER_READER_PATH}:{value.lineno}-{end}"
    return [], f"{LEDGER_READER_PATH}:NOT FOUND"


def contract_type_rows() -> list[dict[str, str]]:
    text = TRIAL_CATALOG_PATH.read_text(encoding="utf-8")
    source_lines = text.splitlines()
    mod = ast.parse(text)

    all_public = []
    for node in mod.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
        ):
            for element in node.value.elts:
                if isinstance(element, ast.Constant) and isinstance(element.value, str):
                    all_public.append(element.value)
            break

    alias_map = {}
    classes = {}
    for node in mod.body:
        if isinstance(node, ast.ClassDef):
            classes[node.name] = node
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Name):
                alias_map[target.id] = (node.value.id, node.lineno)

    rows = []
    for name in all_public:
        if name in classes:
            cls = classes[name]
            is_enum = any(
                isinstance(base, ast.Name) and base.id == "Enum"
                or isinstance(base, ast.Attribute) and base.attr == "Enum"
                for base in cls.bases
            )
            fields = []
            for node in cls.body:
                if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                    fields.append(
                        f"{node.target.id}:{ast.unparse(node.annotation)}"
                        f'{"" if node.value is None else f"={ast.unparse(node.value)}"}'
                    )
                elif is_enum and isinstance(node, ast.Assign) and len(node.targets) == 1:
                    target = node.targets[0]
                    if isinstance(target, ast.Name):
                        fields.append(f"{target.id}={ast.unparse(node.value)}")
            rows.append(
                {
                    "name": name,
                    "kind": "enum" if is_enum else "class",
                    "fields": ", ".join(fields),
                    "doc": (ast.get_docstring(cls) or "").replace("\n", " ").strip(),
                    "source": f"{TRIAL_CATALOG_PATH}:{cls.lineno}",
                }
            )
        elif name in alias_map:
            target, lineno = alias_map[name]
            doc = f"Compatibility alias for {target}"
            if lineno >= 2:
                prev = source_lines[lineno - 2].strip()
                if prev.startswith("#"):
                    doc = prev[1:].strip()
            rows.append(
                {
                    "name": name,
                    "kind": "alias",
                    "fields": f"alias_of={target}",
                    "doc": doc,
                    "source": f"{TRIAL_CATALOG_PATH}:{lineno}",
                }
            )

    return rows


def refusal_reasons() -> list[str]:
    rows = contract_type_rows()
    reasons = []
    for row in rows:
        if row["name"] != "BoundaryRefusalReason":
            continue
        if row["kind"] != "enum":
            continue
        for entry in row["fields"].split(", "):
            if entry:
                reasons.append(entry.split("=")[0])
        break
    return reasons


def test_metrics() -> dict[str, object]:
    text = TRIAL_TEST_PATH.read_text(encoding="utf-8")
    mod = ast.parse(text)
    defs = [
        node
        for node in mod.body
        if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
    ]
    member_count = None
    for node in mod.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name != "_completed_run_members":
            continue
        for child in node.body:
            if isinstance(child, ast.Return) and isinstance(child.value, ast.Dict):
                member_count = len(child.value.keys)
    parametrized = []
    for node in defs:
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call):
                continue
            func = dec.func
            if not (isinstance(func, ast.Attribute) and func.attr == "parametrize"):
                continue
            cases = None
            if len(dec.args) >= 2:
                arg = dec.args[1]
                if isinstance(arg, (ast.List, ast.Tuple)):
                    cases = len(arg.elts)
                elif (
                    isinstance(arg, ast.Call)
                    and isinstance(arg.func, ast.Name)
                    and arg.func.id == "sorted"
                    and member_count is not None
                ):
                    cases = member_count
            parametrized.append((node.name, cases, node.lineno))
            break
    def_count = len(defs)
    case_total = sum(cases for _, cases, _ in parametrized if cases is not None)
    collection = def_count - len(parametrized) + case_total
    return {
        "def_count": def_count,
        "parametrized": parametrized,
        "collection_if_imported": collection,
        "source": f"{TRIAL_TEST_PATH}",
    }


def test_count() -> int:
    return int(test_metrics()["def_count"])


def search_contract_data_files() -> list[str]:
    if not CONTRACT_ROOT.exists():
        return []
    hits = []
    for name in sorted(CONTRACT_WRITE_TARGETS):
        for path in CONTRACT_ROOT.rglob(name):
            if path.is_file():
                hits.append(str(path))
    return sorted(hits)


EVENT_COUNT_SQL = (
    "SELECT json_extract(canonical_event, '$.next_state') AS next_state, "
    "COUNT(*) FROM lifecycle_events GROUP BY 1"
)


def event_state_counts(path: Path) -> dict[str, int]:
    conn = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        rows = conn.execute(EVENT_COUNT_SQL).fetchall()
    finally:
        conn.close()
    return {str(state): int(count) for state, count in rows}


def main() -> None:
    events, current_rows, latest_by_candidate = load_ledger_state(LEDGER_PATH)
    counts = event_state_counts(LEDGER_PATH)
    sql_events = (
        f"SELECT * FROM lifecycle_events ORDER BY global_sequence "
        f"on file:{LEDGER_PATH.as_posix()}?mode=ro"
    )
    sql_counts = (
        f"{EVENT_COUNT_SQL} "
        f"on file:{LEDGER_PATH.as_posix()}?mode=ro"
    )

    print("# Q-A. Fixture lifecycle report")
    print(
        "| candidate / family | current lifecycle state | last transition | "
        "check_set_purpose | failing_checks / rejection reason | source (file:line or command) |"
    )
    print("| --- | --- | --- | --- | --- | --- |")
    for candidate in sorted(latest_by_candidate):
        latest = latest_by_candidate[candidate]
        current = next(
            row for row in current_rows if row["candidate_id"] == candidate
        )
        if latest["check_set_purpose_persisted"]:
            purpose_cell = latest["check_set_purpose"]
        else:
            purpose_cell = "not persisted in this fixture evidence"
        failure_payload = json.dumps(latest["failing_checks"], ensure_ascii=False)
        last_transition = (
            f"{latest['timestamp']} {latest['event_type']} "
            f"(writer={latest['writer_class']})"
        )
        source = sql_events
        print(
            "| "
            f"{md_cell(candidate)} | "
            f"{md_cell(current['current_state'])} | "
            f"{md_cell(last_transition)} | "
            f"{md_cell(purpose_cell)} | "
            f"{md_cell(failure_payload)} | "
            f"{md_cell(source)} |"
        )

    print("\nQ-A event_counts_per_state:")
    print(f"command: {sql_counts}")
    for state, count in sorted(counts.items()):
        print(f"- {state}: {count}")

    json_items, json_src = read_unresolved_lifecycle_contracts_json()
    reader_items, reader_src = read_unresolved_lifecycle_contracts_reader()
    print("\nQ-A unresolved_lifecycle_contracts JSON snapshot (older demo run):")
    print(f"source: {json_src}")
    for item in json_items:
        print(f"- {item}")
    print(
        "\nQ-A unresolved_lifecycle_contracts current reader source "
        "(_render_status_report; this is the current reader's list):"
    )
    print(f"source: {reader_src}")
    for item in reader_items:
        print(f"- {item}")
    print(
        "Q-A reader CLI: not executed from this directory; "
        f"{LEDGER_READER_PATH}:25 imports mtc_contracts "
        "(ModuleNotFoundError: No module named 'mtc_contracts')"
    )

    print("\n# Q-B. Contract/type scan")
    print("| name | fields | purpose from docstring | source |")
    print("| --- | --- | --- | --- |")
    type_rows = contract_type_rows()
    for row in type_rows:
        print(
            f"| {md_cell(row['name'])} | {md_cell(row['fields'])} | "
            f"{md_cell(row['doc'])} | {md_cell(row['source'])} |"
        )

    reasons = refusal_reasons()
    metrics = test_metrics()
    print(f"\nQ-B public_type_count: {len(type_rows)}")
    print(f"Q-B refusal_reasons: {', '.join(reasons) if reasons else 'NONE'}")
    print(f"Q-B test_count: {metrics['def_count']}")
    print(
        "Q-B test_count_basis: top-level def test_* via ast "
        f"(file {metrics['source']}); suite was not collected"
    )
    print(
        "Q-B parametrized_defs: "
        + ", ".join(
            f"{name}:{cases}@{lineno}"
            for name, cases, lineno in metrics["parametrized"]
        )
    )
    print(
        "Q-B pytest_collection_if_imported: "
        f"{metrics['collection_if_imported']} "
        "(not collected; mtc_contracts missing)"
    )
    print("Q-B catalog_data_exists:")
    catalog_hits = search_contract_data_files()
    print(
        f"search: rglob of {sorted(CONTRACT_WRITE_TARGETS)} under {CONTRACT_ROOT}"
    )
    if catalog_hits:
        for hit in catalog_hits:
            print(f"- {hit}")
    else:
        print("- NONE FOUND")

    print("\n# Appendix")
    print(
        f"Q-A fixture inputs: {LEDGER_PATH}, {RESTORED_LEDGER_PATH}, "
        f"{BACKUP_LEDGER_PATH}, {STATUS_REPORT_PATH}"
    )
    print(f"Q-B test file: {TRIAL_TEST_PATH}")
    print(f"P0-31 scope/status source: {SCOPE_PATH}")
    print(f"P0-31 ledger reader source: {LEDGER_READER_PATH}")


if __name__ == "__main__":
    main()
