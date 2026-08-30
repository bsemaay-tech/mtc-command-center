"""Report-only promotion diagnostic behavior at its public evaluator/CLI seams."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import promotion_gates_report as report  # noqa: E402


NAMED_PRODUCERS = ("mega_walk_forward.py", "finalize_bootstrap_bh.py")


def candidate_fixture(producer: str) -> dict:
    return {
        "strategy": f"FIXTURE_{producer.removesuffix('.py').upper()}",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "classification": "PASS",
        "dsr_p_value": 0.94,
        "dsr_robust": False,
        "boot_p_value": 0.01,
        "bh_fdr_survivor": True,
        "robust_final": False,
        "summary": {
            "lockbox_oos": {"net_return_pct": 3.0},
            "buy_hold_lockbox": {"buy_hold_return_pct": 1.0},
        },
        "promotion_report_bindings": {
            "strategy": {
                "symbol": "BTCUSDT",
                "timeframe": "1h",
                "window": {"start": "2025-10-01T00:00:00Z", "end": "2025-12-31T23:00:00Z"},
                "cost_assumptions": {"cost_bps": 8.0},
                "provenance": producer,
            },
            "buy_and_hold": {
                "symbol": "BTCUSDT",
                "timeframe": "1h",
                "window": {"start": "2025-10-01T00:00:00Z", "end": "2025-12-31T23:00:00Z"},
                "cost_assumptions": {"cost_bps": 8.0},
                "provenance": producer,
            },
        },
    }


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_dsr_coherent_below_threshold_is_fail_for_named_producers(producer: str) -> None:
    evaluated = report.evaluate_candidate(
        candidate_fixture(producer),
        evidence_prefix=f"fixture:{producer}#/results/0",
    )

    assert evaluated["checks"]["dsr"] == {
        "status": "FAIL",
        "reason": {
            "code": "DSR_BELOW_THRESHOLD",
            "message": "dsr_p_value is below 0.95 and dsr_robust is false",
        },
        "values": {"dsr_p_value": 0.94, "dsr_robust": False},
        "evidence_source_paths": [
            f"fixture:{producer}#/results/0/dsr_p_value",
            f"fixture:{producer}#/results/0/dsr_robust",
        ],
    }


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_dsr_disagreement_is_typed_stop_for_named_producers(producer: str) -> None:
    candidate = candidate_fixture(producer)
    candidate["dsr_robust"] = True

    dsr = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["dsr"]

    assert dsr["status"] == "STOP"
    assert dsr["reason"]["code"] == "DSR_VALUE_FLAG_DISAGREEMENT"
    assert dsr["values"]["dsr_p_value"] == 0.94


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_dsr_at_threshold_with_true_flag_is_pass_for_named_producers(producer: str) -> None:
    candidate = candidate_fixture(producer)
    candidate["dsr_p_value"] = 0.95
    candidate["dsr_robust"] = True

    dsr = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["dsr"]

    assert dsr["status"] == "PASS"
    assert dsr["values"] == {"dsr_p_value": 0.95, "dsr_robust": True}


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_missing_dsr_value_is_typed_stop_without_a_number(producer: str) -> None:
    candidate = candidate_fixture(producer)
    del candidate["dsr_p_value"]

    dsr = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["dsr"]

    assert dsr["status"] == "STOP"
    assert dsr["reason"]["code"] == "DSR_P_VALUE_MISSING"
    assert dsr["values"]["dsr_p_value"] is None


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_bh_is_stop_even_when_partial_producer_flag_says_survivor(producer: str) -> None:
    evaluated = report.evaluate_candidate(
        candidate_fixture(producer),
        evidence_prefix=f"fixture:{producer}#/results/0",
    )

    assert evaluated["checks"]["bh_fdr"] == {
        "status": "STOP",
        "reason": {
            "code": "BH_COMPLETE_FAMILY_MANIFEST_MISSING",
            "message": "no complete independently enumerated BH family manifest exists",
        },
        "values": {"boot_p_value": 0.01, "bh_fdr_survivor": True},
        "evidence_source_paths": [
            f"fixture:{producer}#/results/0/boot_p_value",
            f"fixture:{producer}#/results/0/bh_fdr_survivor",
        ],
    }


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_robust_final_is_stop_when_bh_evidence_is_stopped(producer: str) -> None:
    evaluated = report.evaluate_candidate(
        candidate_fixture(producer),
        evidence_prefix=f"fixture:{producer}#/results/0",
    )

    robust = evaluated["checks"]["robust_final"]
    assert robust["status"] == "STOP"
    assert robust["reason"]["code"] == "ROBUST_FINAL_DEPENDENCY_STOP"
    assert robust["values"] == {
        "robust_final": False,
        "classification": "PASS",
        "dsr_status": "FAIL",
        "bh_fdr_status": "STOP",
    }


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_missing_robust_final_is_typed_stop(producer: str) -> None:
    candidate = candidate_fixture(producer)
    del candidate["robust_final"]

    robust = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["robust_final"]

    assert robust["status"] == "STOP"
    assert robust["reason"]["code"] == "ROBUST_FINAL_MISSING_OR_INVALID"
    assert robust["values"]["robust_final"] is None


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_raw_excess_stops_when_identity_bindings_differ(producer: str) -> None:
    candidate = deepcopy(candidate_fixture(producer))
    candidate["promotion_report_bindings"]["buy_and_hold"]["symbol"] = "ETHUSDT"

    evaluated = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )

    raw_excess = evaluated["checks"]["positive_raw_lockbox_excess"]
    assert raw_excess["status"] == "STOP"
    assert raw_excess["reason"]["code"] == "RAW_EXCESS_BINDING_MISMATCH"
    assert raw_excess["values"] == {
        "strategy_return_pct": 3.0,
        "buy_hold_return_pct": 1.0,
        "raw_excess_pct": None,
    }


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_raw_excess_strict_positive_and_zero_boundary_are_measured(producer: str) -> None:
    positive = candidate_fixture(producer)
    zero = deepcopy(positive)
    zero["summary"]["lockbox_oos"]["net_return_pct"] = 1.0

    positive_check = report.evaluate_candidate(
        positive,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["positive_raw_lockbox_excess"]
    zero_check = report.evaluate_candidate(
        zero,
        evidence_prefix=f"fixture:{producer}#/results/1",
    )["checks"]["positive_raw_lockbox_excess"]

    assert (positive_check["status"], positive_check["values"]["raw_excess_pct"]) == ("PASS", 2.0)
    assert (zero_check["status"], zero_check["values"]["raw_excess_pct"]) == ("FAIL", 0.0)


@pytest.mark.parametrize("producer", NAMED_PRODUCERS)
def test_missing_buy_hold_return_is_typed_stop_without_excess_number(producer: str) -> None:
    candidate = candidate_fixture(producer)
    del candidate["summary"]["buy_hold_lockbox"]["buy_hold_return_pct"]

    raw_excess = report.evaluate_candidate(
        candidate,
        evidence_prefix=f"fixture:{producer}#/results/0",
    )["checks"]["positive_raw_lockbox_excess"]

    assert raw_excess["status"] == "STOP"
    assert raw_excess["reason"]["code"] == "RAW_EXCESS_RETURN_MISSING_OR_NOT_FINITE"
    assert raw_excess["values"]["raw_excess_pct"] is None


def test_report_has_machine_counts_patterns_and_a_human_table() -> None:
    mega_candidate = candidate_fixture("mega_walk_forward.py")
    finalized_candidate = candidate_fixture("finalize_bootstrap_bh.py")
    finalized_candidate["dsr_p_value"] = 0.95
    finalized_candidate["dsr_robust"] = True
    finalized_candidate["summary"]["lockbox_oos"]["net_return_pct"] = 1.0

    built = report.build_report(
        {"results": [mega_candidate, finalized_candidate]},
        source_path="fixture:two-named-producers",
    )

    assert built["counts"]["candidates"] == 2
    assert built["counts"]["checks"] == {
        "dsr": {"PASS": 1, "FAIL": 1, "STOP": 0},
        "bh_fdr": {"PASS": 0, "FAIL": 0, "STOP": 2},
        "robust_final": {"PASS": 0, "FAIL": 0, "STOP": 2},
        "positive_raw_lockbox_excess": {"PASS": 1, "FAIL": 1, "STOP": 0},
    }
    assert built["counts"]["patterns"] == {
        "DSR=FAIL|BH_FDR=STOP|ROBUST_FINAL=STOP|POSITIVE_RAW_LOCKBOX_EXCESS=PASS": 1,
        "DSR=PASS|BH_FDR=STOP|ROBUST_FINAL=STOP|POSITIVE_RAW_LOCKBOX_EXCESS=FAIL": 1,
    }
    assert "| Candidate | DSR | BH-FDR | robust_final | Positive raw lockbox excess |" in built[
        "human_readable_table"
    ]
    assert "DSR_BELOW_THRESHOLD" in built["human_readable_table"]
    assert "p=0.94" in built["human_readable_table"]
    assert "BH_COMPLETE_FAMILY_MANIFEST_MISSING" in built["human_readable_table"]
    assert "raw_excess_pp=2.0" in built["human_readable_table"]
    assert all(row["evidence_source_paths"] for row in built["rows"])
    assert {row["measurement_label"] for row in built["rows"]} == {
        "MEASURED_REPORT_ONLY_DIAGNOSTIC"
    }


def test_cli_writes_only_the_requested_machine_and_human_report(tmp_path: Path) -> None:
    input_path = tmp_path / "candidate_fixture.json"
    output_path = tmp_path / "promotion_gates_report.json"
    input_path.write_text(
        json.dumps({"results": [candidate_fixture("mega_walk_forward.py")]}),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "promotion_gates_report.py"),
            "--input",
            str(input_path),
            "--output",
            str(output_path),
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    artifact = json.loads(output_path.read_text(encoding="utf-8"))
    assert artifact["report_kind"] == "promotion_gates_report_only"
    assert artifact["effect"] == "DISPLAY_ONLY_NO_ENFORCEMENT"
    assert artifact["counts"]["candidates"] == 1
    assert "| Candidate | DSR | BH-FDR |" in artifact["human_readable_table"]
    assert sorted(path.name for path in tmp_path.iterdir()) == [
        "candidate_fixture.json",
        "promotion_gates_report.json",
    ]


def test_cli_refuses_every_fenced_target_without_writing(tmp_path: Path) -> None:
    input_path = tmp_path / "candidate_fixture.json"
    input_path.write_text(
        json.dumps({"results": [candidate_fixture("finalize_bootstrap_bh.py")]}),
        encoding="utf-8",
    )
    simulated_repo = tmp_path / "MTC_COMMAND_CENTER"
    targets = [
        simulated_repo / "03_QUANTLENS" / "tools" / "score_all_gates.py",
        simulated_repo / "03_QUANTLENS" / "tools" / "build_forward_paper_queue.py",
        simulated_repo / "03_QUANTLENS" / "tools" / "build_strategy_research_registry.py",
        simulated_repo / "03_QUANTLENS" / "06_PROMOTED_TO_PARITY" / "PROMOTION_INDEX.md",
        simulated_repo / "05_REGISTRY" / "PROMOTION_REGISTRY.json",
        simulated_repo / "03_QUANTLENS" / "strategies" / "STG_FIXTURE" / "producer_spec.json",
        simulated_repo / "06_SCHEMAS" / "promotion_gates_report.json",
        simulated_repo / "03_QUANTLENS" / "strategies" / "STG_FIXTURE" / "promotion_gates_report.json",
        simulated_repo / "05_REGISTRY" / "promotion_gates_report.json",
        simulated_repo / "03_QUANTLENS" / "06_PROMOTED_TO_PARITY" / "promotion_gates_report.json",
    ]

    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "promotion_gates_report.py"),
                "--input",
                str(input_path),
                "--output",
                str(target),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        assert completed.returncode == 2, target
        assert "REFUSED:" in completed.stderr
        assert not target.exists(), target
