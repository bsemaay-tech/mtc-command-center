from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


EXPECTED_ROWS = {
    "C01": ("C01-LEGACY-001", "C01-GF8-MUT-001"),
    "C02": ("C02-LEGACY-001", "C02-GF8-MUT-001"),
    "C03": ("C03-LEGACY-001", "C03-GF8-MUT-001"),
    "C04": ("C04-LEGACY-001", "C04-GF8-MUT-001"),
    "C05": ("C05-LEGACY-001", "C05-GF8-MUT-001"),
    "C06": ("C06-LEGACY-001", "C06-GF8-MUT-001"),
    "C07": ("C07-LEGACY-001", "C07-GF8-MUT-001"),
    "C08": ("C08-LEGACY-001", "C08-GF8-MUT-001"),
    "C09": ("C09-LEGACY-001", "C09-GF8-MUT-001"),
    "C10": ("C10-LEGACY-001", "C10-GF8-MUT-001"),
    "C11": ("C11-LEGACY-001", "C11-GF8-MUT-001"),
    "C12": ("C12-LEGACY-001", "C12-GF8-MUT-001"),
    "C13": ("C13-LEGACY-001", "C13-GF8-MUT-001"),
    "C14": ("C14-LEGACY-001", "C14-GF8-MUT-001"),
    "C15": ("C15-LEGACY-001", "C15-GF8-MUT-001"),
    "C16": ("C16-LEGACY-001", "C16-GF8-MUT-001"),
    "C17": ("C17-LEGACY-001", "C17-GF8-MUT-001"),
    "C18": ("C18-LEGACY-001", "C18-GF8-MUT-001"),
    "C19": ("C19-LEGACY-001", "C19-GF8-MUT-001"),
    "C20": ("C20-LEGACY-001", "C20-GF8-MUT-001"),
    "C21": ("C21-LEGACY-001", "C21-GF8-MUT-001"),
    "C22": ("C22-LEGACY-001", "C22-GF8-MUT-001"),
    "C23": ("C23-LEGACY-001", "C23-GF8-MUT-001"),
    "C24": ("C24-LEGACY-001", "C24-GF8-MUT-001"),
    "C26": ("C26-LEGACY-001", "C26-GF8-MUT-001"),
    "C31": ("C31-LEGACY-001", "C31-GF8-MUT-001"),
    "C33": ("C33-LEGACY-001", "C33-GF8-MUT-001"),
    "C36": ("C36-LEGACY-001", "C36-GF8-MUT-001"),
    "C37": ("C37-LEGACY-001", "C37-GF8-MUT-001"),
    "C38": ("C38-LEGACY-001", "C38-GF8-MUT-001"),
    "C39": ("C39-LEGACY-001", "C39-GF8-MUT-001"),
    "C40": ("C40-LEGACY-001", "C40-GF8-MUT-001"),
    "C41": ("C41-LEGACY-001", "C41-GF8-MUT-001"),
}
UNRESOLVED_AUTHORITY_ROWS = {"C32", "C34", "C35", "C42"}
UNRESOLVED_PRODUCER_ROWS = {"C28", "C29", "C30"}
UNRESOLVED_ROWS = UNRESOLVED_AUTHORITY_ROWS | UNRESOLVED_PRODUCER_ROWS
EXPECTED_RESULT_ORDER = sorted([*EXPECTED_ROWS, *UNRESOLVED_ROWS])
EXPECTED_A_COMMIT = "5c5603065c994d545c0eaa8c137fa9edd5cdfc28"
EXPECTED_A_TREE = "7aa6f867d821df08a00358adf2dd4400b9c719e8"
EXPECTED_CONTROLLER_COMMIT = "77a10e6573d93f8aaf777010ea507bbec0a7668b"
EXPECTED_CONTROLLER_TREE = "a14d071e3a6ee93735d6c2fc458f16b9f8d19a22"
EXPECTED_B_COMMIT = "b5ed1afadcff09b69e36b72affeb23de51d84c14"
EXPECTED_B_TREE = "e8c4f06ba0fc74ce03f195fd946004ae9b458b37"
EXPECTED_MASTER = "85c3e17f97efa1ba83ef9c679de319a50ad3be04"
EXPECTED_P009_BLOB = "1c39ab939dfcf5589e5ec8fba4af8966947a67fc"
EXPECTED_P009_SHA256 = "7d48871a3e45dab118e97969d701912edb5d7c16a4d822d816beca1d03a42249"
EXPECTED_GATE_VERSION = "P011-LC-GATE-v2"
EXPECTED_MANIFEST_SHA256 = "1bc01646e9a00a4ee62c22c6ce1416ed03648e97351e792ae82bbbaff95f52d7"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
    ).encode("utf-8")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(
            handle,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def behavior_signature(record: dict[str, Any]) -> dict[str, Any]:
    if record.get("status") == "GREEN_AFTER_RED":
        return {
            "green_output": record.get("green", {}).get("parsed_output"),
            "green_return_code": record.get("green", {}).get("return_code"),
            "mutation_application": record.get("mutation", {}).get("application"),
            "mutation_id": record.get("mutation", {}).get("mutation_id"),
            "red_output": record.get("mutation", {}).get("red", {}).get("parsed_output"),
            "red_return_code": record.get("mutation", {}).get("red", {}).get("return_code"),
            "row_id": record.get("row_id"),
            "scenario_id": record.get("scenario_id"),
            "status": record.get("status"),
        }
    return {
        key: record.get(key)
        for key in (
            "actual",
            "clean_authority_inspection",
            "comparison",
            "expected",
            "mutation",
            "reason",
            "row_id",
            "scenario_id",
            "status",
        )
    } | {
        "clean_probe_output": record.get("clean_authority_probe", {}).get("parsed_output"),
        "clean_probe_return_code": record.get("clean_authority_probe", {}).get("return_code"),
    }


def disposition_signature(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row.get(key)
        for key in (
            "producer_execution",
            "producer_mutation",
            "row_id",
            "scenario_ids",
            "status",
            "stop_reason",
        )
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Independent WP-P0-11 row-arm remeasurement")
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--prior-evidence", required=True)
    parser.add_argument("--prior-ref", required=True)
    args = parser.parse_args()

    evidence = Path(args.evidence).resolve()
    prior_evidence = Path(args.prior_evidence).resolve()
    manifest_path = Path(args.manifest).resolve()
    gate_dir = manifest_path.parent
    repo_root = gate_dir.parents[2]
    p009_rel = Path(
        "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
        "CAPABILITY_CANONICALIZATION_TABLE.md"
    )
    p009_path = repo_root / p009_rel

    require(sha256_file(manifest_path) == EXPECTED_MANIFEST_SHA256, "legacy manifest hash differs")
    manifest = load_json(manifest_path)
    require(manifest.get("gate_version") == EXPECTED_GATE_VERSION, "manifest gate version differs")
    require(
        [row.get("row_id") for row in manifest.get("rows", [])]
        == [f"C{index:02d}" for index in range(1, 43)],
        "manifest row identities differ",
    )
    applicable = sum(row.get("disposition") == "APPLICABLE" for row in manifest["rows"])
    policy_only = sum(
        row.get("disposition") == "NOT_A_LEGACY_REPRODUCTION_ROW" for row in manifest["rows"]
    )
    require((applicable, policy_only) == (40, 2), "manifest dispositions differ")

    require(sha256_file(p009_path) == EXPECTED_P009_SHA256, "P0-09 SHA-256 differs")
    p009_blob = subprocess.run(
        ["git", "hash-object", "--", p009_rel.as_posix()],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    require(p009_blob == EXPECTED_P009_BLOB, "P0-09 blob OID differs")
    ancestry = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_MASTER, "HEAD"],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    require(ancestry.returncode == 0, "required master commit is not an ancestor")

    results_path = evidence / "row_results.jsonl"
    raw_lines = results_path.read_bytes().splitlines(keepends=True)
    require(raw_lines and all(line.endswith(b"\n") for line in raw_lines), "JSONL newline contract differs")
    records = [json.loads(line) for line in raw_lines]
    require([record.get("row_id") for record in records] == EXPECTED_RESULT_ORDER, "executed row order differs")
    prior_evidence_rel = prior_evidence.relative_to(repo_root).as_posix()
    prior_results = subprocess.run(
        ["git", "show", f"{args.prior_ref}:{prior_evidence_rel}/row_results.jsonl"],
        cwd=repo_root,
        capture_output=True,
        check=True,
    ).stdout.splitlines()
    prior_records = [json.loads(line) for line in prior_results]
    require(
        [behavior_signature(record) for record in records]
        == [behavior_signature(record) for record in prior_records],
        "one or more row behaviors differ from the recorded v1 state",
    )

    clean_green = 0
    mutation_red = 0
    expected_leaves = 0
    compared_leaves = 0
    red_mismatch_count = 0
    for record in records:
        row_id = record["row_id"]
        unhashed = dict(record)
        recorded_hash = unhashed.pop("record_sha256")
        require(sha256_bytes(canonical_bytes(unhashed)) == recorded_hash, f"{row_id} record hash differs")
        if row_id in UNRESOLVED_ROWS:
            if row_id in UNRESOLVED_AUTHORITY_ROWS:
                require(record.get("status") == "UNRESOLVED_AUTHORITY_CONTRADICTION", f"{row_id} unresolved status differs")
                require(record.get("mutation") == "NOT_RUN_NO_AUTHORITY_ESTABLISHED_EXPECTED_ROUTE", f"{row_id} mutation must not run")
                require(bool(record.get("comparison", {}).get("mismatches")), f"{row_id} contradiction mismatch absent")
                require(record.get("clean_authority_probe", {}).get("return_code") == 0, f"{row_id} clean probe failed")
            else:
                require(record.get("status") == "UNRESOLVED_PRODUCER_EXECUTION", f"{row_id} producer status differs")
                require(record.get("mutation") == "NOT_RUN_NO_EXECUTABLE_PINE_PRODUCER_IN_AUTHORIZED_LANE", f"{row_id} mutation must not run")
                require(all(record.get("clean_authority_inspection", {}).values()), f"{row_id} source inspection differs")
            continue
        scenario_id, mutation_id = EXPECTED_ROWS[row_id]
        require(record.get("scenario_id") == scenario_id, f"{row_id} scenario identity differs")
        require(record.get("status") == "GREEN_AFTER_RED", f"{row_id} status differs")
        require(record.get("mutation", {}).get("mutation_id") == mutation_id, f"{row_id} mutation identity differs")
        expected_commit, expected_tree = EXPECTED_A_COMMIT, EXPECTED_A_TREE
        if row_id in {"C38", "C39"}:
            expected_commit, expected_tree = EXPECTED_B_COMMIT, EXPECTED_B_TREE
        require(record.get("authority", {}).get("commit") == expected_commit, f"{row_id} authority commit differs")
        require(record.get("authority", {}).get("tree_oid") == expected_tree, f"{row_id} authority tree differs")
        require(bool(record.get("authority", {}).get("citations")), f"{row_id} citations absent")
        require(all(record.get("contract_binding", {}).values()), f"{row_id} contract binding differs")

        red = record["mutation"]["red"]
        red_output = red.get("parsed_output") or {}
        require(red.get("return_code") == 1, f"{row_id} RED rc differs")
        require(red_output.get("outcome") == "FAIL", f"{row_id} RED outcome differs")
        require(bool(red_output.get("comparison", {}).get("mismatches")), f"{row_id} RED has no mismatch")
        mutation_red += 1
        red_mismatch_count += len(red_output["comparison"]["mismatches"])

        green = record["green"]
        green_output = green.get("parsed_output") or {}
        comparison = green_output.get("comparison", {})
        require(green.get("return_code") == 0, f"{row_id} GREEN rc differs")
        require(green_output.get("outcome") == "PASS", f"{row_id} GREEN outcome differs")
        require(comparison.get("mismatches") == [], f"{row_id} GREEN has mismatches")
        require(
            comparison.get("expected_leaf_count") == comparison.get("compared_expected_leaf_count"),
            f"{row_id} expected leaf conservation differs",
        )
        clean_green += 1
        expected_leaves += comparison["expected_leaf_count"]
        compared_leaves += comparison["compared_expected_leaf_count"]

    corroboration_path = evidence / "row_corroboration.json"
    corroboration = load_json(corroboration_path)
    require(corroboration.get("gate_version") == EXPECTED_GATE_VERSION, "corroboration gate version differs")
    rows = corroboration.get("rows", [])
    require([row.get("row_id") for row in rows] == [f"C{index:02d}" for index in range(1, 43)], "corroboration row order differs")
    independently_counted = {
        "green": sum(row.get("status") == "GREEN" for row in rows),
        "not_applicable": sum(row.get("status") == "NOT_A_LEGACY_REPRODUCTION_ROW" for row in rows),
        "stop": sum(row.get("status") == "STOP" for row in rows),
        "total": len(rows),
    }
    require(independently_counted == {"green": 33, "not_applicable": 2, "stop": 7, "total": 42}, "corroboration counts differ")
    require(corroboration.get("counts") == independently_counted, "reported corroboration counts differ")
    require(corroboration.get("outcome") == "STOP", "partial arm did not remain STOP")
    prior_corroboration = json.loads(
        subprocess.run(
            ["git", "show", f"{args.prior_ref}:{prior_evidence_rel}/row_corroboration.json"],
            cwd=repo_root,
            capture_output=True,
            check=True,
        ).stdout
    )
    require(
        [disposition_signature(row) for row in rows]
        == [disposition_signature(row) for row in prior_corroboration.get("rows", [])],
        "one or more C01-C42 dispositions differ from the recorded v1 state",
    )

    batch_path = evidence / "batch_manifest.json"
    batch = load_json(batch_path)
    require(batch.get("gate_version") == EXPECTED_GATE_VERSION, "batch gate version differs")
    require(batch.get("legacy_manifest_sha256") == EXPECTED_MANIFEST_SHA256, "batch manifest pin differs")
    require(batch.get("authority", {}).get("a_commit") == EXPECTED_A_COMMIT, "batch A commit differs")
    require(batch.get("authority", {}).get("a_tree_oid") == EXPECTED_A_TREE, "batch A tree differs")
    require(batch.get("authority", {}).get("merged_master_commit") == EXPECTED_MASTER, "batch master pin differs")
    require(batch.get("authority", {}).get("p009_blob_oid") == EXPECTED_P009_BLOB, "batch P0-09 blob differs")
    require(batch.get("authority", {}).get("p009_sha256") == EXPECTED_P009_SHA256, "batch P0-09 hash differs")
    require(batch.get("artifacts", {}).get("row_results.jsonl") == sha256_file(results_path), "results hash differs")
    require(batch.get("artifacts", {}).get("row_corroboration.json") == sha256_file(corroboration_path), "corroboration hash differs")
    unresolved_path = evidence / "unresolved_rows.json"
    require(batch.get("artifacts", {}).get("unresolved_rows.json") == sha256_file(unresolved_path), "unresolved hash differs")
    require(batch.get("counts", {}).get("clean_green") == 33, "batch GREEN count differs")
    require(batch.get("counts", {}).get("unresolved_authority_contradiction") == 4, "batch unresolved count differs")
    require(batch.get("counts", {}).get("unresolved_producer_execution") == 3, "batch producer STOP count differs")

    output = {
        "artifact_hashes": {
            "batch_manifest.json": sha256_file(batch_path),
            "row_corroboration.json": sha256_file(corroboration_path),
            "row_results.jsonl": sha256_file(results_path),
            "unresolved_rows.json": sha256_file(unresolved_path),
        },
        "compared_expected_leaves": compared_leaves,
        "counts": {
            "applicable": applicable,
            "clean_green": clean_green,
            "green": independently_counted["green"],
            "mutation_red": mutation_red,
            "not_applicable": policy_only,
            "red_mismatches": red_mismatch_count,
            "stop": independently_counted["stop"],
            "total": independently_counted["total"],
        },
        "expected_leaves": expected_leaves,
        "behavior_identical_to_prior": True,
        "dispositions_identical_to_prior": True,
        "outcome": "PASS",
        "prior_ref": args.prior_ref,
        "p009_blob_oid": p009_blob,
        "p009_sha256": sha256_file(p009_path),
        "rows": EXPECTED_RESULT_ORDER,
        "unresolved_rows": sorted(UNRESOLVED_ROWS),
        "unresolved_authority_rows": sorted(UNRESOLVED_AUTHORITY_ROWS),
        "unresolved_producer_rows": sorted(UNRESOLVED_PRODUCER_ROWS),
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
