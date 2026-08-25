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
    cases: list[tuple[str, Callable[[Path], None], bool]] = [
        ("family_04_bug_value", tamper_family_04_bug_value, False),
        ("family_06_fabricated_citations", tamper_family_06_citations, False),
        ("family_04_incoherent_risk", tamper_family_04_incoherent_risk, False),
        ("family_05_incoherent_accept", tamper_family_05_incoherent_accept, False),
        ("family_24_duplicate_effects", tamper_family_24_duplicate_effects, False),
        ("manifest_built_count_normal", tamper_manifest_built_count, False),
        ("manifest_built_count_optimized", tamper_manifest_built_count, True),
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
        for index, (name, mutate, optimized) in enumerate(cases, start=1):
            case_dir = temp_path / f"case_{index:02d}"
            shutil.copytree(FIXTURE_DIR, case_dir)
            mutate(case_dir)
            result = run_verifier(
                verifier,
                case_dir,
                temp_path / f"case_{index:02d}_output",
                optimized=optimized,
            )
            was_rejected = result.returncode != 0
            rejected += int(was_rejected)
            print(
                f"TAMPER name={name} optimized={str(optimized).lower()} "
                f"rc={result.returncode} rejected={str(was_rejected).lower()} "
                f"detail={reason_line(result)}"
            )

    passed = baseline_clean and rejected == len(cases)
    print(
        f"VERIFIER_REGRESSION_SUMMARY baseline_clean={int(baseline_clean)} "
        f"tamper_rejected={rejected}/{len(cases)} result={'PASS' if passed else 'FAIL'}"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
