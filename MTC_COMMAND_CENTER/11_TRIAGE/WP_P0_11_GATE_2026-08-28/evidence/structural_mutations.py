from __future__ import annotations

import copy
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


GATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GATE_DIR.parents[2]
sys.path.insert(0, str(GATE_DIR))
import p011_gate as gate


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("wb") as handle:
        for record in records:
            handle.write(gate.canonical_bytes(record, pretty=False))


def normalize_evidence(value: str, replacements: dict[str, str]) -> str:
    for original, replacement in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        value = value.replace(original, replacement)
        value = value.replace(json.dumps(original)[1:-1], replacement)
    value = re.sub(
        r"(?i)[A-Z]:\\\\(?:[^\\\"\r\n]+\\\\)*p011_structural_[^\\\"\r\n]+",
        "<SCRATCH>",
        value,
    )
    value = re.sub(
        r"(?i)[A-Z]:\\(?:[^\\\"\r\n]+\\)*p011_structural_[^\\\"\r\n]+",
        "<SCRATCH>",
        value,
    )
    return value


def run(command: list[str], expected_rc: int, replacements: dict[str, str]) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        check=False,
        timeout=300,
    )
    normalized_command = [normalize_evidence(argument, replacements) for argument in command]
    normalized_stdout = normalize_evidence(completed.stdout.rstrip("\r\n"), replacements)
    normalized_stderr = normalize_evidence(completed.stderr.rstrip("\r\n"), replacements)
    evidence = (normalized_stdout + normalized_stderr).encode("utf-8")
    return {
        "command_argv": normalized_command,
        "expected_return_code": expected_rc,
        "return_code": completed.returncode,
        "stdout": normalized_stdout,
        "stderr": normalized_stderr,
        "evidence_sha256": hashlib.sha256(evidence).hexdigest(),
        "as_expected": completed.returncode == expected_rc,
    }


def self_test_command(expected: Path, actual: Path, ledger: Path) -> list[str]:
    return [
        sys.executable,
        "-I",
        str(GATE_DIR / "p011_gate.py"),
        "self-test-compare",
        "--expected",
        str(expected),
        "--actual",
        str(actual),
        "--mismatch-ledger",
        str(ledger),
    ]


def refresh_digest(record: dict[str, Any]) -> None:
    record["state_digest"] = gate.state_digest(
        record["events"],
        record["position"],
        record["gate_readiness"],
        record["account"],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="WP-P0-11 executed structural mutations")
    parser.add_argument("--baseline", required=True, type=Path)
    args = parser.parse_args()
    baseline = args.baseline.resolve()
    sequence = baseline / "mtc_v2_legacy_sequence.jsonl"
    first = gate.representative_observation(sequence)
    second = copy.deepcopy(first)
    second["bar_index"] += 1
    second["timestamp"] = (datetime.fromisoformat(second["timestamp"]) + timedelta(hours=1)).isoformat()
    second["events"] = []
    second["position"]["entry_bar"] = second["bar_index"]
    second["position"]["entry_legs"][0]["entry_bar"] = second["bar_index"]
    refresh_digest(second)
    expected_records = [first, second]
    results: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="p011_structural_") as scratch_text:
        scratch = Path(scratch_text)
        replacements = {
            str(scratch): "<SCRATCH>",
            str(REPO_ROOT): "<REPO_ROOT>",
            sys.executable: "<PYTHON>",
        }
        expected = scratch / "expected.jsonl"
        actual = scratch / "actual.jsonl"
        ledger = scratch / "ledger.json"
        write_jsonl(expected, expected_records)

        cases: list[tuple[str, str, list[dict[str, Any]] | bytes, int]] = []
        cases.append(("missing_first_observation", "missing first key is named without cascade", [second], 1))
        cases.append(("duplicate_observation_identity", "duplicate key is rejected instead of overwritten", [first, first, second], 1))
        cases.append(("reordered_observations", "order mismatch is reported", [second, first], 1))

        undeclared = copy.deepcopy(expected_records)
        undeclared[0]["undeclared_child"] = "forbidden"
        cases.append(("undeclared_observation_child", "closed schema rejects the child", undeclared, 1))

        duplicate_ordinal = copy.deepcopy(expected_records)
        duplicate_ordinal[0]["events"].append(copy.deepcopy(duplicate_ordinal[0]["events"][0]))
        duplicate_ordinal[0]["events"][1]["event_ordinal"] = 0
        refresh_digest(duplicate_ordinal[0])
        cases.append(("duplicate_event_ordinal", "event shape fails", duplicate_ordinal, 1))

        deleted_event = copy.deepcopy(expected_records)
        deleted_event[0]["events"] = []
        refresh_digest(deleted_event[0])
        cases.append(("deleted_event", "ordered event comparison fails", deleted_event, 1))

        added_event = copy.deepcopy(expected_records)
        extra = copy.deepcopy(added_event[0]["events"][0])
        extra["event_ordinal"] = 1
        extra["event_kind"] = "EXIT"
        extra["exit_id"] = "EXTRA"
        extra["realized_pnl"] = float(0.0).hex()
        added_event[0]["events"].append(extra)
        refresh_digest(added_event[0])
        cases.append(("unexpected_event", "ordered event comparison fails", added_event, 1))

        inverted_side = copy.deepcopy(expected_records)
        inverted_side[0]["events"][0]["side"] = "short"
        refresh_digest(inverted_side[0])
        cases.append(("inverted_event_side", "side comparison fails", inverted_side, 1))

        changed_state = copy.deepcopy(expected_records)
        changed_state[0]["position"]["qty"] = float(3.0).hex()
        refresh_digest(changed_state[0])
        cases.append(("changed_first_observation_position_state", "first-observation position projection and digest differ", changed_state, 1))

        moved_event = copy.deepcopy(expected_records)
        moved_event[1]["events"] = moved_event[0]["events"]
        moved_event[0]["events"] = []
        refresh_digest(moved_event[0])
        refresh_digest(moved_event[1])
        cases.append(("event_shifted_to_next_bar", "missing N event and unexpected N+1 event are named", moved_event, 1))

        changed_input = copy.deepcopy(expected_records)
        changed_input[0]["input"]["close"] = float(999.0).hex()
        cases.append(("changed_ohlcv_value", "input value differs", changed_input, 1))
        cases.append(("parser_failure_before_observation", "invalid JSON is inability to evaluate", b"{not-json}\n", 3))

        for case_id, protected_class, payload, expected_rc in cases:
            if isinstance(payload, bytes):
                actual.write_bytes(payload)
            else:
                write_jsonl(actual, payload)
            red = run(self_test_command(expected, actual, ledger), expected_rc, replacements)
            green = run(self_test_command(expected, expected, ledger), 0, replacements)
            results.append(
                {
                    "mutation_id": case_id,
                    "protected_class": protected_class,
                    "red": red,
                    "restoration_green": green,
                }
            )

        receipt = gate.load_json(GATE_DIR / "P011_GATE_RECEIPT.json")
        tampered_receipt = copy.deepcopy(receipt)
        tampered_receipt["source_identities"]["implementation_a"]["tree_oid"] = "0" * 40
        tampered_receipt_path = scratch / "tampered_receipt.json"
        tampered_receipt_path.write_bytes(gate.canonical_bytes(tampered_receipt))
        compare_command = [
            sys.executable,
            "-I",
            str(GATE_DIR / "p011_gate.py"),
            "compare",
            "--receipt",
            str(tampered_receipt_path),
            "--baseline",
            str(baseline),
            "--subject-mode",
            "LEGACY_COMPATIBLE",
            "--mismatch-ledger",
            str(ledger),
        ]
        results.append(
            {
                "mutation_id": "coordinated_local_receipt_rehash",
                "protected_class": "external receipt pin rejects locally rehashed provenance",
                "red": run(compare_command, 1, replacements),
                "restoration_green": run(
                    [
                        sys.executable,
                        "-I",
                        str(GATE_DIR / "p011_gate.py"),
                        "compare",
                        "--receipt",
                        str(GATE_DIR / "P011_GATE_RECEIPT.json"),
                        "--baseline",
                        str(baseline),
                        "--subject-mode",
                        "LEGACY_COMPATIBLE",
                        "--mismatch-ledger",
                        str(ledger),
                    ],
                    3,
                    replacements,
                ),
            }
        )

        wrong_baseline = scratch / "wrong_producer_baseline"
        wrong_baseline.mkdir()
        manifest = gate.load_json(baseline / "baseline_manifest.json")
        manifest["source"]["commit"] = "0" * 40
        (wrong_baseline / "baseline_manifest.json").write_bytes(gate.canonical_bytes(manifest))
        wrong_command = compare_command.copy()
        wrong_command[wrong_command.index(str(tampered_receipt_path))] = str(GATE_DIR / "P011_GATE_RECEIPT.json")
        wrong_command[wrong_command.index(str(baseline))] = str(wrong_baseline)
        results.append(
            {
                "mutation_id": "wrong_sequence_producer_identity",
                "protected_class": "producer provenance differs before comparison",
                "red": run(wrong_command, 1, replacements),
                "restoration_green": run(
                    [
                        sys.executable,
                        "-I",
                        str(GATE_DIR / "p011_gate.py"),
                        "compare",
                        "--receipt",
                        str(GATE_DIR / "P011_GATE_RECEIPT.json"),
                        "--baseline",
                        str(baseline),
                        "--subject-mode",
                        "LEGACY_COMPATIBLE",
                        "--mismatch-ledger",
                        str(ledger),
                    ],
                    3,
                    replacements,
                ),
            }
        )

        manifest = gate.load_json(GATE_DIR / "p011_legacy_manifest.json")
        manifest["rows"] = manifest["rows"][1:]
        tampered_manifest = scratch / "tampered_legacy_manifest.json"
        tampered_manifest.write_bytes(gate.canonical_bytes(manifest))
        build_common = [
            sys.executable,
            "-I",
            str(GATE_DIR / "p011_gate.py"),
            "build-baseline",
            "--source-commit",
            gate.SOURCE_COMMIT,
            "--producer",
            "A",
            "--data",
            str(REPO_ROOT / "IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv"),
            "--profile",
            str(GATE_DIR / "profiles/mtc_v2_legacy_supertrend_default_v1.json"),
            "--profile",
            str(GATE_DIR / "profiles/mtc_v2_legacy_range_filter_default_v1.json"),
            "--legacy-manifest",
            str(tampered_manifest),
            "--out",
            str(scratch / "must_not_be_created_manifest"),
        ]
        results.append(
            {
                "mutation_id": "deleted_applicable_c_row",
                "protected_class": "external legacy-manifest pin rejects coverage loss",
                "red": run(build_common, 1, replacements),
                "restoration_green": run(
                    build_common[:-4]
                    + [
                        "--legacy-manifest",
                        str(GATE_DIR / "p011_legacy_manifest.json"),
                        "--out",
                        str(scratch / "restored_manifest_build"),
                    ],
                    3,
                    replacements,
                ),
            }
        )

        tampered_profile = gate.load_json(GATE_DIR / "profiles/mtc_v2_legacy_supertrend_default_v1.json")
        tampered_profile["resolved_config"]["st_factor"] = 4.5
        tampered_profile_path = scratch / "tampered_profile.json"
        tampered_profile_path.write_bytes(gate.canonical_bytes(tampered_profile))
        profile_command = build_common.copy()
        profile_command[profile_command.index(str(GATE_DIR / "profiles/mtc_v2_legacy_supertrend_default_v1.json"))] = str(tampered_profile_path)
        profile_command[profile_command.index(str(tampered_manifest))] = str(GATE_DIR / "p011_legacy_manifest.json")
        profile_command[profile_command.index(str(scratch / "must_not_be_created_manifest"))] = str(scratch / "must_not_be_created_profile")
        results.append(
            {
                "mutation_id": "changed_resolved_config_and_local_hash",
                "protected_class": "full resolved snapshot differs from frozen resolve_config",
                "red": run(profile_command, 1, replacements),
                "restoration_green": run(
                    build_common[:-4]
                    + [
                        "--legacy-manifest",
                        str(GATE_DIR / "p011_legacy_manifest.json"),
                        "--out",
                        str(scratch / "restored_profile_build"),
                    ],
                    3,
                    replacements,
                ),
            }
        )

        source_fixture = REPO_ROOT / "IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv"
        tampered_data = scratch / "tampered_data.csv"
        data = bytearray(source_fixture.read_bytes())
        offset = data.index(ord("1"), data.index(b"\n") + 1)
        data[offset] = ord("2")
        tampered_data.write_bytes(data)
        data_command = build_common.copy()
        data_command[data_command.index(str(source_fixture))] = str(tampered_data)
        data_command[data_command.index(str(tampered_manifest))] = str(GATE_DIR / "p011_legacy_manifest.json")
        data_command[data_command.index(str(scratch / "must_not_be_created_manifest"))] = str(scratch / "must_not_be_created_data")
        results.append(
            {
                "mutation_id": "changed_data_byte",
                "protected_class": "pinned data hash differs before strategy execution",
                "red": run(data_command, 1, replacements),
                "restoration_green": run(
                    build_common[:-4]
                    + [
                        "--legacy-manifest",
                        str(GATE_DIR / "p011_legacy_manifest.json"),
                        "--out",
                        str(scratch / "restored_data_build"),
                    ],
                    3,
                    replacements,
                ),
            }
        )

    failures = [
        item["mutation_id"]
        for item in results
        if not item["red"].get("as_expected") or not item["restoration_green"].get("as_expected")
    ]
    output = {
        "artifact_schema_version": "P011_STRUCTURAL_MUTATIONS_v1",
        "gate_version": gate.GATE_VERSION,
        "outcome": "PASS" if not failures else "STOP",
        "mutation_count": len(results),
        "expected_results": sum(item["red"].get("as_expected", False) for item in results),
        "restored_results": sum(item["restoration_green"].get("as_expected", False) for item in results),
        "failures": failures,
        "evidence_normalization": {
            "purpose": "remove machine- and run-specific path prefixes from durable command/output evidence",
            "tokens": ["<PYTHON>", "<REPO_ROOT>", "<SCRATCH>"],
            "semantic_values_and_return_codes_unchanged": True,
        },
        "mutations": results,
        "explicitly_not_executed": [
            "4 authority-contradictory row-producer mutations (C32, C34, C35, C42)",
            "independent-subject import/delegation classification mutation",
            "P0-10 round-4d mutations (NONE_DIRECT_BUILD)",
            "missing external anchor path mutation (the authoritative anchor was not moved)",
        ],
    }
    output_path = Path(__file__).with_name("structural_mutations.json")
    output_path.write_bytes(gate.canonical_bytes(output))
    print(json.dumps({"outcome": output["outcome"], "mutations": len(results), "expected_results": output["expected_results"], "restored_results": output["restored_results"], "sha256": gate.sha256_file(output_path)}, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 3


if __name__ == "__main__":
    raise SystemExit(main())
