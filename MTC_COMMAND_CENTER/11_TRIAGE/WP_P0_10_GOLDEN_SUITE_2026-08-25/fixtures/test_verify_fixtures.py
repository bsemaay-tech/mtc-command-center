"""Executable tamper regressions for the WP-P0-10 fixture verifier."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable


FIXTURE_DIR = Path(__file__).resolve().parent


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def fixture(path: Path, number: int) -> tuple[Path, dict[str, Any]]:
    fixture_path = path / f"family_{number:02d}.json"
    return fixture_path, json.loads(fixture_path.read_text(encoding="utf-8"))


def assertion(data: dict[str, Any], target: str) -> dict[str, Any]:
    return next(
        item
        for item in data["expected_output"]["assertions"]
        if item["path"] == target
    )


def recompute_internal_hashes(data: dict[str, Any]) -> None:
    expected = {
        item["path"]: item["value"]
        for item in data["expected_output"]["assertions"]
    }
    state = {key: value for key, value in expected.items() if key.startswith("state.")}
    data["expected_output"]["sha256"] = hashlib.sha256(
        canonical_bytes(expected)
    ).hexdigest()
    data["expected_output"]["final_state_sha256"] = hashlib.sha256(
        canonical_bytes(state)
    ).hexdigest()


def write_fixture_with_manifest_hash(
    path: Path,
    number: int,
    fixture_path: Path,
    data: dict[str, Any],
) -> None:
    write_json(fixture_path, data)
    manifest_path = path / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_item = next(
        item for item in manifest["families"] if item["number"] == number
    )
    manifest_item["fixture_contract_sha256"] = hashlib.sha256(
        canonical_bytes(data)
    ).hexdigest()
    write_json(manifest_path, manifest)


def tamper_family_04_bug_value(path: Path) -> None:
    fixture_path, data = fixture(path, 4)
    assertion(data, "resolution.proposed_qty")["value"] = "20"
    data["deliberate_mutation"]["from"] = "20"
    data["deliberate_mutation"]["to"] = "2"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_06_citations(path: Path) -> None:
    fixture_path, data = fixture(path, 6)
    fabricated = (
        "MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_09_CAPABILITY_TABLE_2026-08-25/"
        "CAPABILITY_CANONICALIZATION_TABLE.md:99999-99999 "
        "(C99/GF-99)"
    )
    for item in data["expected_output"]["assertions"]:
        item["citations"] = [fabricated]
    data["expected_output"]["sha256_citations"] = [fabricated]
    data["expected_output"]["final_state_sha256_citations"] = [fabricated]
    data["deliberate_mutation"]["citation"] = fabricated
    data["companion_scenarios"][0]["source"] = fabricated
    write_json(fixture_path, data)


def tamper_family_04_incoherent_risk(path: Path) -> None:
    fixture_path, data = fixture(path, 4)
    assertion(data, "resolution.per_unit_risk")["value"] = "25"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_05_incoherent_accept(path: Path) -> None:
    fixture_path, data = fixture(path, 5)
    assertion(data, "decision.outcome")["value"] = "ACCEPT"
    data["deliberate_mutation"]["from"] = "ACCEPT"
    data["deliberate_mutation"]["to"] = "REJECT"
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_family_24_duplicate_effects(path: Path) -> None:
    fixture_path, data = fixture(path, 24)
    assertion(data, "economic_effects.count")["value"] = 2
    assertion(data, "state.position.qty")["value"] = "2"
    data["deliberate_mutation"]["from"] = 2
    data["deliberate_mutation"]["to"] = 1
    recompute_internal_hashes(data)
    write_json(fixture_path, data)


def tamper_manifest_built_count(path: Path) -> None:
    manifest_path = path / "manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["built_count"] = 22
    write_json(manifest_path, data)


def tamper_family_03_absent_undeclared_input(path: Path) -> None:
    fixture_path, data = fixture(path, 3)
    scenario = data["companion_scenarios"][0]
    del scenario["config"]["tw_qty_precision_mode"]
    del scenario["assertion_inputs"]["legacy_precision.research_qty"]
    write_fixture_with_manifest_hash(path, 3, fixture_path, data)


def run_verifier(
    verifier: Path,
    fixture_dir: Path,
    output_dir: Path,
    optimized: bool = False,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(verifier), str(fixture_dir), str(output_dir)])
    return subprocess.run(
        command,
        cwd=Path.cwd(),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def reason_line(result: subprocess.CompletedProcess[str]) -> str:
    lines = [
        line.strip()
        for line in (result.stderr + "\n" + result.stdout).splitlines()
        if line.strip()
    ]
    named = next((line for line in lines if line.startswith("VERIFY_FAIL reason=")), None)
    if named:
        return named
    return "no_named_rejection" if result.returncode == 0 else "unnamed_nonzero_rejection"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verifier", type=Path, default=FIXTURE_DIR / "verify_fixtures.py")
    args = parser.parse_args()
    verifier = args.verifier.resolve()
    cases: list[tuple[str, Callable[[Path], None], bool, str | None]] = [
        ("family_04_bug_value", tamper_family_04_bug_value, False, None),
        ("family_06_fabricated_citations", tamper_family_06_citations, False, None),
        ("family_04_incoherent_risk", tamper_family_04_incoherent_risk, False, None),
        ("family_05_incoherent_accept", tamper_family_05_incoherent_accept, False, None),
        ("family_24_duplicate_effects", tamper_family_24_duplicate_effects, False, None),
        (
            "family_03_absent_undeclared_input",
            tamper_family_03_absent_undeclared_input,
            False,
            "VERIFY_FAIL reason=family=03 assertion_input_source_undeclared "
            "path=legacy_precision.research_qty",
        ),
        ("manifest_built_count_normal", tamper_manifest_built_count, False, None),
        ("manifest_built_count_optimized", tamper_manifest_built_count, True, None),
    ]

    with tempfile.TemporaryDirectory(prefix="wp_p010_verifier_regression_") as temp:
        temp_path = Path(temp)
        baseline_output = temp_path / "baseline_output"
        baseline = run_verifier(verifier, FIXTURE_DIR, baseline_output)
        baseline_clean = baseline.returncode == 0
        print(
            f"BASELINE rc={baseline.returncode} clean={str(baseline_clean).lower()} "
            f"detail={reason_line(baseline)}"
        )

        rejected = 0
        for index, (name, mutate, optimized, expected_reason) in enumerate(
            cases, start=1
        ):
            case_dir = temp_path / f"case_{index:02d}"
            shutil.copytree(FIXTURE_DIR, case_dir)
            mutate(case_dir)
            result = run_verifier(
                verifier,
                case_dir,
                temp_path / f"case_{index:02d}_output",
                optimized=optimized,
            )
            detail = reason_line(result)
            was_rejected = result.returncode != 0 and (
                expected_reason is None or expected_reason in detail
            )
            rejected += int(was_rejected)
            print(
                f"TAMPER name={name} optimized={str(optimized).lower()} "
                f"rc={result.returncode} rejected={str(was_rejected).lower()} "
                f"detail={detail}"
            )

    passed = baseline_clean and rejected == len(cases)
    print(
        f"VERIFIER_REGRESSION_SUMMARY baseline_clean={int(baseline_clean)} "
        f"tamper_rejected={rejected}/{len(cases)} result={'PASS' if passed else 'FAIL'}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
