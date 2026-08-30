from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


GATE_DIR = Path(__file__).resolve().parents[1]
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

import p011_gate


HISTORICAL_SCHEMA_SHA256 = (
    "c18fb1622ab38b374d65a1304994f0e9f5d8993f948e75d99694bdfceb5fdb2e"
)
HISTORICAL_BASELINE_SHA256 = (
    "727e438181bf1cd74ae0a90774afddf963ff03a382ee0646eaf2bb6d6010086e"
)
HISTORICAL_RECORD_COUNT = 96154
HISTORICAL_MATRIX_ROWS = 76
HISTORICAL_DETECTED_COUNT = 68
HISTORICAL_ABSENT_PATHS = (
    "position.working_exits[*].exit_id",
    "position.working_exits[*].kind",
    "position.working_exits[*].target_price",
    "position.working_exits[*].stop_price",
    "position.working_exits[*].qty_fraction",
    "position.working_exits[*].book_version",
    "position.working_exits[*].active",
    "position.completed_exit_ids[*]",
)
V2_RECEIPT_PATH = GATE_DIR / "P011_GATE_RECEIPT.json"
V2_ANCHOR_PATH = Path(
    r"C:\LAB\P011_TRUST_ANCHORS\P011-LC-GATE-v2.owner-signed.json"
)


class MatrixEvidenceError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )


def path_tokens(path: str) -> list[tuple[str, bool]]:
    return [
        (token[:-3], True) if token.endswith("[*]") else (token, False)
        for token in path.split(".")
    ]


def mutated_value(value: Any, catalog_type: str) -> Any:
    if value is None:
        return {
            "boolean": True,
            "float": float(1.0).hex(),
            "integer": 1,
            "string": "P011_STAGE3_MUTATED",
        }[catalog_type]
    if catalog_type == "boolean":
        return not value
    if catalog_type == "integer":
        return value + 1
    if catalog_type == "float":
        return (float.fromhex(value) + 0.5).hex()
    if catalog_type == "string":
        return value + "__P011_STAGE3_MUTATED"
    raise MatrixEvidenceError(f"unsupported catalog type: {catalog_type}")


def mutate_every_occurrence(record: dict[str, Any], path: str, catalog_type: str) -> int:
    tokens = path_tokens(path)

    def visit(current: Any, index: int) -> int:
        key, wildcard = tokens[index]
        if not isinstance(current, dict) or key not in current:
            return 0
        value = current[key]
        if index == len(tokens) - 1:
            if wildcard:
                if not isinstance(value, list):
                    return 0
                for item_index, item in enumerate(value):
                    value[item_index] = mutated_value(item, catalog_type)
                return len(value)
            current[key] = mutated_value(value, catalog_type)
            return 1
        if wildcard:
            if not isinstance(value, list):
                return 0
            return sum(visit(item, index + 1) for item in value)
        return visit(value, index + 1)

    return visit(record, 0)


def write_mutated_actual(
    expected_path: Path,
    actual_path: Path,
    *,
    field_path: str,
    catalog_type: str,
    recompute_state_digest: bool,
) -> tuple[int, int, int, list[Any] | None]:
    changed_records = 0
    changed_occurrences = 0
    record_count = 0
    first_changed_key: list[Any] | None = None
    with (
        expected_path.open("r", encoding="utf-8") as source,
        actual_path.open("wb") as target,
    ):
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            record_count += 1
            record = json.loads(line)
            occurrences = mutate_every_occurrence(record, field_path, catalog_type)
            if occurrences and recompute_state_digest:
                record["state_digest"] = p011_gate.state_digest(
                    record["events"],
                    record["position"],
                    record["gate_readiness"],
                    record["account"],
                )
            changed_occurrences += occurrences
            changed_records += occurrences > 0
            if occurrences and first_changed_key is None:
                first_changed_key = [
                    record.get("profile_id"),
                    record.get("bar_index"),
                    record.get("timestamp"),
                ]
            target.write(canonical_bytes(record))
    return record_count, changed_records, changed_occurrences, first_changed_key


def _first_changed_key(ledger: list[dict[str, Any]]) -> list[Any] | None:
    if not ledger:
        return None
    first = ledger[0]
    return [first.get("profile_or_row"), first.get("bar"), first.get("timestamp")]


def _authenticated_historical_prior() -> dict[str, Any]:
    authenticated = False
    receipt_values: dict[str, Any] = {}
    if V2_RECEIPT_PATH.is_file() and V2_ANCHOR_PATH.is_file():
        receipt = load_json(V2_RECEIPT_PATH)
        anchor = load_json(V2_ANCHOR_PATH)
        authenticated = anchor.get("receipt_sha256") == sha256_file(V2_RECEIPT_PATH)
        receipt_values = {
            "matrix_rows": (receipt.get("baseline_outputs", {}).get("discrimination_matrix", {})).get("matrix_rows"),
            "record_count": (receipt.get("baseline_outputs", {}).get("conservation", {})).get("total_observations"),
        }
    receipt_matrix_rows = receipt_values.get("matrix_rows")
    receipt_record_count = receipt_values.get("record_count")
    return {
        "receipt_anchor_hash_match": authenticated,
        "expected_absent_paths": list(HISTORICAL_ABSENT_PATHS),
        "expected_baseline_sha256": HISTORICAL_BASELINE_SHA256,
        "expected_detected_count": HISTORICAL_DETECTED_COUNT,
        "expected_matrix_rows": (
            receipt_matrix_rows if authenticated and type(receipt_matrix_rows) is int else None
        ),
        "expected_record_count": (
            receipt_record_count if authenticated and type(receipt_record_count) is int else None
        ),
        "expected_schema_sha256": HISTORICAL_SCHEMA_SHA256,
        "receipt_values": receipt_values,
        "comparison_sources": {
            "absent_paths": "MODULE_CONSTANT_HISTORICAL_ABSENT_PATHS",
            "detected_count": "MODULE_CONSTANT_HISTORICAL_DETECTED_COUNT",
            "matrix_rows": "ANCHOR_HASH_MATCHED_V2_RECEIPT_FIELD",
            "record_count": "ANCHOR_HASH_MATCHED_V2_RECEIPT_FIELD",
        },
    }


def build_matrix(
    *, expected_path: Path, schema_path: Path, output_dir: Path
) -> tuple[Path, Path]:
    expected_path = expected_path.resolve()
    schema_path = schema_path.resolve()
    output_dir = output_dir.resolve()
    if not expected_path.is_file() or not schema_path.is_file():
        raise MatrixEvidenceError("expected sequence or schema is absent")
    schema = load_json(schema_path)
    catalog = schema.get("field_catalog")
    if not isinstance(catalog, list) or not catalog:
        raise MatrixEvidenceError("schema field catalog is absent")
    expected_sha256 = sha256_file(expected_path)
    schema_sha256 = sha256_file(schema_path)
    digest_paths = set(
        (schema.get("digest_catalog") or {}).get("state_digest_components", [])
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    transcript_path = output_dir / "comparator_transcript.jsonl"
    matrix_path = output_dir / "discrimination_matrix.json"
    transcript_records: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    observed_record_count: int | None = None
    with tempfile.TemporaryDirectory(prefix="p011_stage3_matrix_") as temp_name:
        scratch = Path(temp_name).resolve()
        for index, field in enumerate(catalog, start=1):
            matrix_id = f"FIELD-{index:03d}"
            actual_path = scratch / f"{matrix_id}.actual.jsonl"
            (
                record_count,
                mutated_records,
                mutated_occurrences,
                writer_first_changed_key,
            ) = write_mutated_actual(
                expected_path,
                actual_path,
                field_path=field["path"],
                catalog_type=field["type"],
                recompute_state_digest=field["path"] in digest_paths,
            )
            if observed_record_count is None:
                observed_record_count = record_count
            elif observed_record_count != record_count:
                raise MatrixEvidenceError("record count changed between path variants")
            comparator_error = None
            try:
                ledger, comparator_changed_records = p011_gate.compare_sequence_files(
                    expected_path,
                    actual_path,
                    f"producer-discrimination:{matrix_id}:{field['path']}",
                )
            except (p011_gate.GateFail, p011_gate.GateStop) as exc:
                ledger = []
                comparator_changed_records = mutated_records
                comparator_error = f"{type(exc).__name__}: {exc}"
            actual_sha256 = sha256_file(actual_path)
            return_code = 1 if comparator_changed_records or comparator_error else 0
            status = (
                "DETECTED"
                if mutated_occurrences > 0
                and (comparator_changed_records > 0 or comparator_error is not None)
                else (
                    "UNEXERCISED_ABSENT_IN_CORPUS"
                    if mutated_occurrences == 0 and comparator_changed_records == 0
                    else "MATRIX_PROBE_INCONSISTENT"
                )
            )
            transcript = {
                "actual_sha256": actual_sha256,
                "changed_record_count": comparator_changed_records,
                "comparator": "p011_gate.compare_sequence_files",
                "comparator_error": comparator_error,
                "changed_record_count_source": (
                    "COMPARATOR"
                    if comparator_error is None
                    else "FRESH_ACTUAL_WRITER_AFTER_COMPARATOR_REFUSAL"
                ),
                "expected_sha256": expected_sha256,
                "first_changed_key": _first_changed_key(ledger)
                or writer_first_changed_key,
                "ledger": ledger,
                "matrix_id": matrix_id,
                "mutated_occurrence_count": mutated_occurrences,
                "mutated_record_count": mutated_records,
                "path": field["path"],
                "return_code": return_code,
                "status": status,
            }
            transcript_records.append(transcript)
            rows.append(
                {
                    "actual_sha256": actual_sha256,
                    "changed_record_count": comparator_changed_records,
                    "expected_sha256": expected_sha256,
                    "first_changed_key": transcript["first_changed_key"],
                    "matrix_id": matrix_id,
                    "mutated_occurrence_count": mutated_occurrences,
                    "mutated_record_count": mutated_records,
                    "owning_record": field["owning_record"],
                    "path": field["path"],
                    "return_code": return_code,
                    "status": status,
                }
            )
    transcript_path.write_bytes(
        b"".join(canonical_bytes(record) for record in transcript_records)
    )
    detected = sum(row["status"] == "DETECTED" for row in rows)
    absent_paths = [
        row["path"]
        for row in rows
        if row["status"] == "UNEXERCISED_ABSENT_IN_CORPUS"
    ]
    inconsistent = [
        row["matrix_id"] for row in rows if row["status"] == "MATRIX_PROBE_INCONSISTENT"
    ]
    historical = _authenticated_historical_prior()
    comparable = (
        expected_sha256 == historical["expected_baseline_sha256"]
        and schema_sha256 == historical["expected_schema_sha256"]
    )
    historical_reproduced = (
        comparable
        and observed_record_count == historical["expected_record_count"]
        and len(rows) == historical["expected_matrix_rows"]
        and detected == historical["expected_detected_count"]
        and absent_paths == historical["expected_absent_paths"]
    )
    outcome = "PASS" if not absent_paths and not inconsistent else "STOP"
    reason = None
    if not comparable or (comparable and not historical_reproduced):
        outcome = "STOP"
        reason = "STOP_HISTORICAL_EXPECTATION_NOT_REPRODUCED"
    elif absent_paths:
        reason = "STOP_UNEXERCISED_ABSENT_IN_CORPUS"
    elif inconsistent:
        reason = "STOP_MATRIX_PROBE_INCONSISTENT"
    restoration_path = output_dir / "writer_integrity_identity_copy.jsonl"
    shutil.copyfile(expected_path, restoration_path)
    restoration_ledger, restoration_changed = p011_gate.compare_sequence_files(
        expected_path, restoration_path, "writer-integrity-only"
    )
    matrix = {
        "absent_count": len(absent_paths),
        "absent_paths": absent_paths,
        "artifact_schema_version": "P011_DISCRIMINATION_MATRIX_v2",
        "baseline_sequence_sha256": expected_sha256,
        "catalog_field_count": len(catalog),
        "comparator_transcript": {
            "path": transcript_path.name,
            "sha256": sha256_file(transcript_path),
        },
        "detected_count": detected,
        "descriptive_arithmetic_only": {
            "detected_plus_absent": detected + len(absent_paths),
            "matrix_rows": len(rows),
            "acceptance_credit": 0,
        },
        "historical_prior": {
            **historical,
            "comparable": comparable,
            "reproduced": historical_reproduced,
        },
        "matrix_row_count": len(rows),
        "outcome": outcome,
        "reason": reason,
        "record_count": observed_record_count or 0,
        "rows": rows,
        "schema_sha256": schema_sha256,
        "writer_integrity_restoration": {
            "actual_sha256": sha256_file(restoration_path),
            "changed_record_count": restoration_changed,
            "closure_credit": 0,
            "expected_sha256": expected_sha256,
            "independence": "NON_INDEPENDENT_WRITER_INTEGRITY_ONLY",
            "ledger": restoration_ledger,
            "return_code": 0 if restoration_changed == 0 else 1,
        },
    }
    write_json(matrix_path, matrix)
    return matrix_path, transcript_path


def validate_matrix_against_transcript(
    matrix_path: Path, transcript_path: Path
) -> dict[str, Any]:
    matrix = load_json(matrix_path)
    transcripts = [
        json.loads(line)
        for line in transcript_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    transcript_by_id = {item.get("matrix_id"): item for item in transcripts}
    rows = matrix.get("rows")
    if not isinstance(rows, list) or len(rows) != len(transcripts):
        raise MatrixEvidenceError("matrix/transcript row count differs")
    if matrix.get("comparator_transcript", {}).get("sha256") != sha256_file(
        transcript_path
    ):
        raise MatrixEvidenceError("matrix transcript hash differs")
    mirrored = (
        "actual_sha256",
        "changed_record_count",
        "expected_sha256",
        "first_changed_key",
        "matrix_id",
        "mutated_occurrence_count",
        "mutated_record_count",
        "path",
        "return_code",
        "status",
    )
    for row in rows:
        transcript = transcript_by_id.get(row.get("matrix_id"))
        if transcript is None:
            raise MatrixEvidenceError("matrix row has no comparator transcript")
        if any(row.get(key) != transcript.get(key) for key in mirrored):
            raise MatrixEvidenceError(
                f"matrix claim differs from transcript: {row.get('matrix_id')}"
            )
    detected = sum(row["status"] == "DETECTED" for row in rows)
    absent_paths = [
        row["path"]
        for row in rows
        if row["status"] == "UNEXERCISED_ABSENT_IN_CORPUS"
    ]
    if matrix.get("detected_count") != detected:
        raise MatrixEvidenceError("matrix detected count differs from rows")
    if matrix.get("absent_count") != len(absent_paths):
        raise MatrixEvidenceError("matrix absent count differs from rows")
    if matrix.get("absent_paths") != absent_paths:
        raise MatrixEvidenceError("matrix absent list differs from rows")
    expected_outcome = "STOP" if absent_paths or matrix.get("reason") else "PASS"
    if matrix.get("outcome") != expected_outcome:
        raise MatrixEvidenceError("matrix outcome differs from terminal evidence")
    return {
        "agreement": "PASS",
        "matrix_outcome": matrix["outcome"],
        "matrix_row_count": len(rows),
        "transcript_sha256": sha256_file(transcript_path),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P0-11 per-path producer discrimination")
    parser.add_argument("--expected", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--out-dir", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    matrix_path, transcript_path = build_matrix(
        expected_path=Path(args.expected),
        schema_path=Path(args.schema),
        output_dir=Path(args.out_dir),
    )
    matrix = load_json(matrix_path)
    print(
        json.dumps(
            {
                "absent_count": matrix["absent_count"],
                "detected_count": matrix["detected_count"],
                "matrix": str(matrix_path),
                "outcome": matrix["outcome"],
                "reason": matrix["reason"],
                "record_count": matrix["record_count"],
                "transcript": str(transcript_path),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0 if matrix["outcome"] == "PASS" else 3


if __name__ == "__main__":
    raise SystemExit(main())
