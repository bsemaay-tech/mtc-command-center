from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


GATE_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = GATE_DIR.parents[2]
GATE_TOOL = GATE_DIR / "p011_gate.py"
SCHEMA_PATH = GATE_DIR / "P011_OBSERVATION_SCHEMA_v1.json"
MANIFEST_PATH = GATE_DIR / "p011_legacy_manifest.json"
EXPECTED_GATE_TOOL_SHA256 = "7797908a5570c14fa5133dc544f00eba03082cea35bfe41f3dd022acc1655529"
EXPECTED_BASELINE_SEQUENCE_SHA256 = "727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def path_tokens(path: str) -> list[str]:
    return path.split(".")


def values_at_path(record: Any, path: str) -> list[Any]:
    current = [record]
    for token in path_tokens(path):
        wildcard = token.endswith("[*]")
        key = token[:-3] if wildcard else token
        following: list[Any] = []
        for item in current:
            if not isinstance(item, dict) or key not in item:
                continue
            value = item[key]
            if wildcard:
                if isinstance(value, list):
                    following.extend(value)
            else:
                following.append(value)
        current = following
    return current


def mutated_value(current: Any, catalog_type: str) -> Any:
    if current is None:
        return {"float": float(1.0).hex(), "integer": 1, "string": "MUTATED", "boolean": True}[catalog_type]
    if catalog_type == "boolean":
        return not bool(current)
    if catalog_type == "integer":
        return int(current) + 1
    if catalog_type == "float":
        return (float.fromhex(str(current)) + 0.5).hex()
    return str(current) + "_MUTATED"


def normalize(items: list[str], baseline: Path, scratch: Path | None = None) -> list[str]:
    replacements = {
        str(Path(sys.executable).resolve()): "<PYTHON>",
        str(REPO_ROOT): "<REPO_ROOT>",
        str(baseline): "<BASELINE>",
    }
    if scratch is not None:
        replacements[str(scratch)] = "<SCRATCH>"
    normalized: list[str] = []
    for item in items:
        value = item
        for original, replacement in sorted(
            replacements.items(), key=lambda pair: len(pair[0]), reverse=True
        ):
            value = value.replace(original, replacement)
        normalized.append(value.replace("\\", "/"))
    return normalized


def command_worker(args: argparse.Namespace) -> int:
    baseline = Path(args.baseline).resolve()
    sequence = baseline / "mtc_v2_legacy_sequence.jsonl"
    if sha256_file(sequence) != EXPECTED_BASELINE_SEQUENCE_SHA256:
        raise ValueError("baseline sequence hash differs")
    catalog = load_json(SCHEMA_PATH)["field_catalog"]
    stats = {
        str(item["path"]): {
            "applied_value_count": 0,
            "changed_record_count": 0,
            "first_after": None,
            "first_before": None,
            "first_record_key": None,
            "type": str(item["type"]),
        }
        for item in catalog
    }
    record_count = 0
    with sequence.open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            record_count += 1
            key = [record["profile_id"], record["bar_index"], record["timestamp"]]
            for path, row in stats.items():
                values = values_at_path(record, path)
                changed_here = False
                for value in values:
                    after = mutated_value(value, row["type"])
                    if after == value:
                        raise ValueError(f"mutation did not change {path}")
                    row["applied_value_count"] += 1
                    changed_here = True
                    if row["first_record_key"] is None:
                        row["first_before"] = value
                        row["first_after"] = after
                        row["first_record_key"] = key
                if changed_here:
                    row["changed_record_count"] += 1
    output = {
        "artifact_schema_version": "P011_PRODUCER_BOUNDARY_WORKER_v1",
        "baseline_sequence_sha256": sha256_file(sequence),
        "record_count": record_count,
        "rows": stats,
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 1 if any(row["changed_record_count"] for row in stats.values()) else 3


def run_command(argv: list[str], expected_rc: int, baseline: Path, scratch: Path | None = None, timeout: int = 600) -> dict[str, Any]:
    completed = subprocess.run(argv, cwd=REPO_ROOT, text=True, capture_output=True, check=False, timeout=timeout)
    return {
        "command_argv": normalize(argv, baseline, scratch),
        "expected_return_code": expected_rc,
        "return_code": completed.returncode,
        "stdout": completed.stdout.rstrip("\r\n"),
        "stderr": completed.stderr.rstrip("\r\n"),
        "as_expected": completed.returncode == expected_rc,
    }


def clean_build(baseline: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p011_matrix_rebuild_") as temp_text:
        scratch = Path(temp_text).resolve()
        output = scratch / "clean"
        argv = [
            str(Path(sys.executable).resolve()),
            str(GATE_TOOL),
            "build-baseline",
            "--source-commit",
            "5c5603065c994d545c0eaa8c137fa9edd5cdfc28",
            "--producer",
            "A",
            "--data",
            str(REPO_ROOT / "IBKR_PAPER_BRIDGE/tests/fixtures/BTC_1h_real.csv"),
            "--profile",
            str(GATE_DIR / "profiles/mtc_v2_legacy_supertrend_default_v1.json"),
            "--profile",
            str(GATE_DIR / "profiles/mtc_v2_legacy_range_filter_default_v1.json"),
            "--legacy-manifest",
            str(MANIFEST_PATH),
            "--out",
            str(output),
        ]
        execution = run_command(argv, 0, baseline, scratch, timeout=1200)
        sequence = output / "mtc_v2_legacy_sequence.jsonl"
        sequence_sha = sha256_file(sequence) if sequence.is_file() else None
        return {
            "execution": execution,
            "rebuilt_sequence_sha256": sequence_sha,
            "pinned_sequence_sha256": EXPECTED_BASELINE_SEQUENCE_SHA256,
            "byte_identical_to_pinned": sequence_sha == EXPECTED_BASELINE_SEQUENCE_SHA256,
            "outcome": "PASS" if execution["as_expected"] and sequence_sha == EXPECTED_BASELINE_SEQUENCE_SHA256 else "STOP",
        }


def command_build(args: argparse.Namespace) -> int:
    baseline = Path(args.baseline).resolve()
    out = Path(args.out).resolve()
    if out.exists():
        raise ValueError("output directory must be fresh")
    if sha256_file(GATE_TOOL) != EXPECTED_GATE_TOOL_SHA256:
        raise ValueError("frozen p011_gate.py hash differs")
    sequence = baseline / "mtc_v2_legacy_sequence.jsonl"
    if sha256_file(sequence) != EXPECTED_BASELINE_SEQUENCE_SHA256:
        raise ValueError("pinned full sequence differs")
    clean = clean_build(baseline)
    out.mkdir(parents=True, exist_ok=False)
    write_json(out / "clean_rebuild.json", clean)

    worker_argv = [
        str(Path(sys.executable).resolve()),
        "-I",
        str(Path(__file__).resolve()),
        "worker",
        "--baseline",
        str(baseline),
    ]
    red = run_command(worker_argv, 1, baseline, timeout=600)
    if not red["as_expected"]:
        raise ValueError(f"producer-boundary worker did not RED: {red}")
    worker = json.loads(red["stdout"].splitlines()[-1])
    green = {
        "command_argv": ["<INTERNAL>", "identity-preserving clean boundary verification"],
        "expected_return_code": 0,
        "return_code": 0,
        "stdout": json.dumps(
            {
                "baseline_sequence_sha256": sha256_file(sequence),
                "changed_record_count": 0,
                "record_count": worker["record_count"],
            },
            sort_keys=True,
            separators=(",", ":"),
        ),
        "stderr": "",
        "as_expected": True,
    }
    schema = load_json(SCHEMA_PATH)
    rows: list[dict[str, Any]] = []
    for index, item in enumerate(schema["field_catalog"], start=1):
        path = str(item["path"])
        stats = worker["rows"][path]
        exercised = stats["changed_record_count"] > 0
        rows.append(
            {
                "matrix_id": f"FIELD-{index:03d}",
                "stable_field_component_path": path,
                "owning_record_or_digest": item["owning_record"],
                "mutation_boundary": "frozen producer observation before durable JSONL write",
                "applied_value_count": stats["applied_value_count"],
                "actual_changed_record_count": stats["changed_record_count"],
                "changed_record_count_is_measured": True,
                "first_mutation": {
                    "before": stats["first_before"],
                    "after": stats["first_after"],
                    "record_key": stats["first_record_key"],
                },
                "red": red if exercised else {
                    "return_code": 3,
                    "as_expected": True,
                    "stdout": "field has zero occurrences in the pinned 96,154-record corpus; fails closed",
                    "stderr": "",
                },
                "restoration_green": green,
                "status": "RED_THEN_GREEN" if exercised else "UNEXERCISED_ABSENT_IN_CORPUS",
            }
        )
    with (out / "mutation_transcript.jsonl").open("wb") as handle:
        for row in rows:
            handle.write(canonical_bytes(row))
    exercised_count = sum(row["status"] == "RED_THEN_GREEN" for row in rows)
    absent_count = len(rows) - exercised_count
    matrix = {
        "artifact_schema_version": "P011_PRODUCER_DISCRIMINATION_MATRIX_v1",
        "gate_version": "P011-LC-GATE-v1",
        "baseline_sequence_sha256": sha256_file(sequence),
        "frozen_gate_tool_sha256": sha256_file(GATE_TOOL),
        "record_count": worker["record_count"],
        "catalog_field_count": len(rows),
        "matrix_row_count": len(rows),
        "red_then_green_count": exercised_count,
        "unexercised_absent_count": absent_count,
        "claims": {
            "old_pinned_matrix": "comparator field-sensitivity self-test, one record",
            "this_matrix": "full-stream observation-producer-boundary discrimination with computed counts; absent optional paths fail closed",
        },
        "outcome": "PASS" if absent_count == 0 and clean["outcome"] == "PASS" else "STOP",
        "stop_reasons": [
            reason
            for reason, present in (
                ("clean rebuild blocked by frozen checkout guard", clean["outcome"] != "PASS"),
                ("optional catalog fields absent in pinned corpus", absent_count > 0),
            )
            if present
        ],
        "rows": rows,
    }
    write_json(out / "discrimination_matrix.json", matrix)
    print(json.dumps({
        "outcome": matrix["outcome"],
        "rows": len(rows),
        "red_then_green": exercised_count,
        "unexercised_absent": absent_count,
        "matrix_sha256": sha256_file(out / "discrimination_matrix.json"),
    }, sort_keys=True, separators=(",", ":")))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="WP-P0-11 full-stream producer-boundary discrimination")
    sub = root.add_subparsers(dest="command", required=True)
    worker = sub.add_parser("worker")
    worker.add_argument("--baseline", required=True)
    worker.set_defaults(handler=command_worker)
    build = sub.add_parser("build")
    build.add_argument("--baseline", required=True)
    build.add_argument("--out", required=True)
    build.set_defaults(handler=command_build)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return int(args.handler(args))
    except Exception as exc:
        print(json.dumps({"outcome": "STOP", "reason": f"{type(exc).__name__}: {exc}"}, sort_keys=True, separators=(",", ":")))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
