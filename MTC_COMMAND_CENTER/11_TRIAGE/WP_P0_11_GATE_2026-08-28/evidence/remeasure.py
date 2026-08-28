from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


GATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GATE_DIR.parents[2]
ANCHOR_PATH = Path(r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v1.owner-signed.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=True,
    ).stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run1", required=True, type=Path)
    parser.add_argument("--run2", required=True, type=Path)
    args = parser.parse_args()
    run1 = args.run1.resolve()
    run2 = args.run2.resolve()
    fixture = REPO_ROOT / "IBKR_PAPER_BRIDGE" / "tests" / "fixtures" / "BTC_1h_real.csv"
    legacy = load(GATE_DIR / "p011_legacy_manifest.json")
    schema = load(GATE_DIR / "P011_OBSERVATION_SCHEMA_v1.json")
    matrix_path = GATE_DIR / "evidence" / "discrimination_matrix" / "discrimination_matrix.json"
    matrix = load(matrix_path)
    structural_path = GATE_DIR / "evidence" / "structural_mutations.json"
    structural = load(structural_path)
    receipt_path = GATE_DIR / "P011_GATE_RECEIPT.json"
    receipt = load(receipt_path)
    anchor = load(ANCHOR_PATH)
    row_evidence = load(run1 / "row_corroboration.json")
    baseline_manifest = load(run1 / "baseline_manifest.json")

    with fixture.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        fixture_count = 0
        first_fixture_row = None
        last_fixture_row = None
        for row in reader:
            fixture_count += 1
            first_fixture_row = first_fixture_row or row
            last_fixture_row = row

    observations: Counter[str] = Counter()
    events: Counter[str] = Counter()
    unique_keys: set[tuple[str, int, str]] = set()
    first_keys: dict[str, tuple[str, int, str]] = {}
    last_keys: dict[str, tuple[str, int, str]] = {}
    with (run1 / "mtc_v2_legacy_sequence.jsonl").open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            profile_id = str(record["profile_id"])
            key = (profile_id, int(record["bar_index"]), str(record["timestamp"]))
            if key in unique_keys:
                raise SystemExit(f"duplicate observation key: {key}")
            unique_keys.add(key)
            observations[profile_id] += 1
            events[profile_id] += len(record["events"])
            first_keys.setdefault(profile_id, key)
            last_keys[profile_id] = key

    profile_paths = sorted((GATE_DIR / "profiles").glob("*.json"))
    artifact_names = ["mtc_v2_legacy_sequence.jsonl", "final_states.json", "row_corroboration.json", "baseline_manifest.json"]
    result = {
        "git": {
            "head": git("rev-parse", "HEAD"),
            "a_tree_oid": git("rev-parse", "5c560306:MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2"),
            "controller_freeze_commit": git("rev-parse", "legacy/pine-controller/2026-08-25^{commit}"),
            "b_freeze_commit": git("rev-parse", "legacy/02-mtc-backtest/2026-08-25^{commit}"),
        },
        "fixture": {
            "sha256": sha256_file(fixture),
            "header": header,
            "data_rows": fixture_count,
            "first_timestamp": first_fixture_row[0] if first_fixture_row else None,
            "last_timestamp": last_fixture_row[0] if last_fixture_row else None,
        },
        "profiles": {
            path.name: {
                "sha256": sha256_file(path),
                "resolved_key_count": len(load(path)["resolved_config"]),
            }
            for path in profile_paths
        },
        "legacy_manifest": {
            "sha256": sha256_file(GATE_DIR / "p011_legacy_manifest.json"),
            "rows": len(legacy["rows"]),
            "dispositions": dict(sorted(Counter(item["disposition"] for item in legacy["rows"]).items())),
        },
        "schema": {
            "sha256": sha256_file(GATE_DIR / "P011_OBSERVATION_SCHEMA_v1.json"),
            "fields": len(schema["field_catalog"]),
            "state_digest_components": len(schema["digest_catalog"]["state_digest_components"]),
            "event_components": len(schema["digest_catalog"]["event_component_paths"]),
        },
        "sequence": {
            "bytes": (run1 / "mtc_v2_legacy_sequence.jsonl").stat().st_size,
            "sha256": sha256_file(run1 / "mtc_v2_legacy_sequence.jsonl"),
            "run2_sha256": sha256_file(run2 / "mtc_v2_legacy_sequence.jsonl"),
            "observations": dict(sorted(observations.items())),
            "events": dict(sorted(events.items())),
            "unique_keys": len(unique_keys),
            "first_keys": first_keys,
            "last_keys": last_keys,
        },
        "artifacts": {
            name: {
                "run1_sha256": sha256_file(run1 / name),
                "run2_sha256": sha256_file(run2 / name),
                "byte_identical": sha256_file(run1 / name) == sha256_file(run2 / name),
            }
            for name in artifact_names
        },
        "adapter": {
            "tool_sha256": sha256_file(GATE_DIR / "p011_gate.py"),
            "baseline_manifest_tool_sha256": baseline_manifest["adapters"]["observation_adapter"]["sha256"],
        },
        "row_arm": row_evidence["counts"],
        "matrix": {
            "sha256": sha256_file(matrix_path),
            "transcript_sha256": sha256_file(matrix_path.parent / "mutation_transcript.jsonl"),
            "rows": matrix["matrix_row_count"],
            "red": matrix["red_count"],
            "restored_green": matrix["restored_green_count"],
            "digest_components": matrix["digest_component_count"],
            "event_components": matrix["event_component_count"],
        },
        "structural_mutations": {
            "sha256": sha256_file(structural_path),
            "rows": len(structural["mutations"]),
            "unique_mutation_ids": len({item["mutation_id"] for item in structural["mutations"]}),
            "red_as_expected": sum(bool(item["red"].get("as_expected")) for item in structural["mutations"]),
            "restored_as_expected": sum(
                bool(item["restoration_green"].get("as_expected")) for item in structural["mutations"]
            ),
            "failures": [
                item["mutation_id"]
                for item in structural["mutations"]
                if not item["red"].get("as_expected")
                or not item["restoration_green"].get("as_expected")
            ],
        },
        "receipt_anchor": {
            "receipt_state": receipt["receipt_state"],
            "receipt_sha256": sha256_file(receipt_path),
            "anchor_receipt_match": anchor["receipt_sha256"] == sha256_file(receipt_path),
            "anchor_legacy_match": anchor["legacy_manifest_sha256"] == sha256_file(GATE_DIR / "p011_legacy_manifest.json"),
            "subject_runs": anchor["subject_runs_at_signature"],
        },
    }
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False, default=list))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
