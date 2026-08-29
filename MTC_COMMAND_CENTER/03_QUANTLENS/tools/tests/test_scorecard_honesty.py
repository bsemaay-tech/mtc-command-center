"""Regression tests for computed and honestly propagated scorecard evidence."""

from copy import deepcopy
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest


TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import build_all_gate_evidence as evidence_writer  # noqa: E402
import build_evaluation_artifact as evaluation_builder  # noqa: E402
import build_forward_paper_queue as forward_queue  # noqa: E402
import mega_walk_forward as mega  # noqa: E402
import score_all_gates  # noqa: E402
import score_gate2  # noqa: E402


EXISTENCE_ONLY_FIELDS = {
    "intake": (
        "entry_pseudo_present",
        "exit_pseudo_or_delegated",
        "direction_defined",
        "opposite_signal_behavior_present",
        "has_deterministic_rules",
        "codable",
        "not_manual_visual",
        "state_machine_definable",
        "not_closed_source",
        "signal_from_closed_bar",
        "htf_lookahead_safe",
        "no_risky_structure",
        "entry_signal_clear",
        "exit_or_delegated_clear",
        "opposite_signal_clear",
        "reentry_policy_clear",
        "state_model_clear",
        "backtest_exit_model_chosen",
        "required_data_available",
        "granularity_available",
        "indicators_computable",
        "cost_model_addable",
        "order_type_clear",
        "entry_timing_clear",
        "spread_slippage_estimable",
        "no_anti_liquidity_assumption",
        "intrabar_uncertainty_manageable",
        "no_extreme_latency_dependence",
        "strategy_thesis_present",
    ),
    "feasibility": (
        "signal_reducible",
        "entry_vs_full_clear",
        "alert_convertible",
        "state_machine_definable",
    ),
    "signal_contract": (
        "emits_long_short_close_flat",
        "signal_timing_defined",
        "signal_uniquely_identifiable",
        "entry_logical_exit_separable",
    ),
    "risk_engine_compat": ("no_conflicting_order_logic",),
    "monitoring": ("carries_version",),
    "reproducibility": ("version_pinned", "rerun_reproducible"),
}


def _regime_frame(n: int = 300) -> pd.DataFrame:
    close = np.linspace(100.0, 160.0, n) + np.sin(np.arange(n) / 5.0)
    return pd.DataFrame(
        {
            "open": close - 0.1,
            "high": close + 1.0,
            "low": close - 1.0,
            "close": close,
        }
    )


def _artifact_with_regime(regime: dict) -> dict:
    return evaluation_builder.build_artifact(
        mega_row={
            "strategy": "TEST_REGIME",
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "summary": {
                "lockbox_oos": {},
                "regime_analysis": regime,
            },
        },
        cpcv_row=None,
        pbo=None,
        backtest_run_id="scorecard-honesty-test",
    )


def _regime_breakdown_subscore(scored: dict) -> dict:
    return next(
        item
        for item in scored["gate2"]["sub_scores"]
        if item["criterion"] == "regime_breakdown"
    )


def _evaluation_for_evidence(strategy: str = "TEST_STAMPS") -> dict:
    return {
        "strategy_id": f"{strategy}|BTCUSDT|1h",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "metrics": {
            "trades": {
                "status": "OK",
                "value": 60,
                "reason": "",
                "source_path": "test:computed_trades",
            }
        },
        "regime": {
            "regime_breakdown_present": {
                "status": "OK",
                "value": True,
                "reason": "",
                "source_path": "test:computed_regime",
            }
        },
        "hard_flags": {"repaint_status": None, "overfit_suspect": None},
        "flags": {"parity_status": "N_A"},
    }


def _mega_row_for_evidence(strategy: str = "TEST_STAMPS") -> dict:
    return {
        "strategy": strategy,
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "data_start": "2025-01-01T00:00:00Z",
        "data_end": "2025-12-31T23:00:00Z",
        "data_rows": 8760,
        "summary": {"best_params": {"length": 20, "enabled": True}},
    }


def _mega_row_for_queue_metric(net_after_slippage_pct=None) -> dict:
    lockbox = {}
    if net_after_slippage_pct is not None:
        lockbox["net_after_slippage_pct"] = net_after_slippage_pct
    return {
        "strategy": "TEST_QUEUE",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "summary": {"lockbox_oos": lockbox},
    }


def test_absent_regime_coverage_is_false_and_removes_four_gate2_points():
    regime = mega.compute_regime_analysis(
        _regime_frame(),
        [{"entry_idx": 50, "net": 0.02}],
        lockbox_start=200,
        lockbox_end=300,
    )

    assert regime["regime_coverage_count"] == 0
    assert regime["regime_breakdown_present"] is False

    artifact = _artifact_with_regime(regime)
    flag = artifact["regime"]["regime_breakdown_present"]
    assert flag["status"] == "OK"
    assert flag["value"] is False

    without_coverage = score_gate2.score_gate2(artifact)
    assert _regime_breakdown_subscore(without_coverage)["points_awarded"] == 0.0

    unchecked_variant = deepcopy(artifact)
    unchecked_variant["regime"]["regime_breakdown_present"]["value"] = True
    with_unchecked_points = score_gate2.score_gate2(unchecked_variant)

    assert with_unchecked_points["gate2"]["score"] - without_coverage["gate2"]["score"] == pytest.approx(4.0)


def test_populated_regime_coverage_keeps_the_four_gate2_points():
    regime = mega.compute_regime_analysis(
        _regime_frame(),
        [{"entry_idx": 250, "net": 0.02}],
        lockbox_start=200,
        lockbox_end=300,
    )

    assert regime["regime_coverage_count"] > 0
    assert regime["regime_breakdown_present"] is True

    artifact = _artifact_with_regime(regime)
    flag = artifact["regime"]["regime_breakdown_present"]
    assert flag["status"] == "OK"
    assert flag["value"] is True
    assert _regime_breakdown_subscore(score_gate2.score_gate2(artifact))[
        "points_awarded"
    ] == 4.0


def test_row_existence_alone_leaves_41_rubric_fields_not_computed():
    artifact = evidence_writer.enrich_artifact(
        _evaluation_for_evidence(),
        _mega_row_for_evidence(),
        {"generated_utc": "2026-08-29T00:00:00Z", "cost_bps": 8.0},
        "scorecard-honesty-test",
    )

    fields = [
        artifact[block][field]
        for block, names in EXISTENCE_ONLY_FIELDS.items()
        for field in names
    ]
    assert len(fields) == 41
    assert all(item["status"] == "NOT_COMPUTED" for item in fields)
    assert all(item["value"] is None for item in fields)

    scorecard = score_all_gates.score_all_gates(artifact)
    assert scorecard["gate1"]["status"] == "INCOMPLETE"
    assert scorecard["gate1B"]["status"] == "INCOMPLETE"


def test_input_type_evidence_reads_each_best_parameter_value():
    numeric = evidence_writer.build_intake(
        _evaluation_for_evidence(),
        _mega_row_for_evidence(),
        {"cost_bps": 8.0},
        "scorecard-honesty-test",
    )["inputs_numeric_boolean"]

    mixed_row = _mega_row_for_evidence()
    mixed_row["summary"]["best_params"]["mode"] = "fast"
    mixed = evidence_writer.build_intake(
        _evaluation_for_evidence(),
        mixed_row,
        {"cost_bps": 8.0},
        "scorecard-honesty-test",
    )["inputs_numeric_boolean"]

    assert numeric["status"] == "OK" and numeric["value"] is True
    assert mixed["status"] == "OK" and mixed["value"] is False


@pytest.mark.parametrize("fixture_number", range(1, 10))
def test_stamp_neutralization_keeps_gate2_and_promotable_byte_identical(fixture_number):
    strategy = f"STAMP_FIXTURE_{fixture_number:02d}"
    honest_artifact = evidence_writer.enrich_artifact(
        _evaluation_for_evidence(strategy),
        _mega_row_for_evidence(strategy),
        {"generated_utc": "2026-08-29T00:00:00Z", "cost_bps": 8.0},
        "scorecard-honesty-test",
    )
    stamped_variant = deepcopy(honest_artifact)
    for block, names in EXISTENCE_ONLY_FIELDS.items():
        for field in names:
            stamped_variant[block][field] = evidence_writer.OK(
                True, "modified-copy", "pre-fix existence stamp"
            )

    honest_scorecard = score_all_gates.score_all_gates(honest_artifact)
    stamped_scorecard = score_all_gates.score_all_gates(stamped_variant)

    assert json.dumps(honest_scorecard["gate2"], sort_keys=True) == json.dumps(
        stamped_scorecard["gate2"], sort_keys=True
    )
    assert honest_scorecard["gate_summary"]["promotable"] is False
    assert stamped_scorecard["gate_summary"]["promotable"] is False


def test_scorecard_copies_computed_queue_metrics_from_upstream_envelopes():
    artifact = evaluation_builder.build_artifact(
        _mega_row_for_queue_metric(net_after_slippage_pct=6.25),
        cpcv_row={"status": "OK", "pass_rate": 0.82},
        pbo=None,
        backtest_run_id="scorecard-honesty-test",
    )
    scorecard = score_all_gates.score_all_gates(artifact)

    assert scorecard["gate2"]["metrics"]["cpcv_pass_ratio"] == artifact[
        "metrics"
    ]["cpcv_pass_ratio"]
    assert scorecard["gate2"]["metrics"]["net_after_slippage_pct"] == artifact[
        "metrics"
    ]["net_after_slippage_pct"]
    assert scorecard["gate2"]["metrics"]["cpcv_pass_ratio"]["source_path"] == "cpcv:pass_rate"
    assert (
        scorecard["gate2"]["metrics"]["net_after_slippage_pct"]["source_path"]
        == "mega:summary.lockbox_oos.net_after_slippage_pct"
    )

    queue_probe = deepcopy(scorecard)
    queue_probe["gate2"]["pass"] = True
    accepted, _ = forward_queue.is_forward_paper_candidate(queue_probe)
    assert accepted is True


def test_scorecard_does_not_fabricate_queue_metrics_when_computations_did_not_run():
    artifact = evaluation_builder.build_artifact(
        _mega_row_for_queue_metric(),
        cpcv_row=None,
        pbo=None,
        backtest_run_id="scorecard-honesty-test",
    )
    scorecard = score_all_gates.score_all_gates(artifact)

    assert "metrics" not in scorecard["gate2"]
