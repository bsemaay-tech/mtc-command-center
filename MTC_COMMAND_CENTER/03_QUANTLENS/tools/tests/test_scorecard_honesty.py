"""Regression tests for computed and honestly propagated scorecard evidence."""

from copy import deepcopy
from dataclasses import asdict
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


PRIOR_GENERIC_POSITIVE_FIELDS = {
    "intake": (
        "entry_pseudo_present",
        "exit_pseudo_or_delegated",
        "direction_defined",
        "opposite_signal_behavior_present",
        "has_deterministic_rules",
        "codable",
        "not_manual_visual",
        "inputs_numeric_boolean",
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

PROPERTY_SPECIFIC_REPAIRS = {("intake", "inputs_numeric_boolean")}
NEUTRALIZED_EXISTENCE_ONLY_FIELDS = {
    block: tuple(
        field
        for field in fields
        if (block, field) not in PROPERTY_SPECIFIC_REPAIRS
    )
    for block, fields in PRIOR_GENERIC_POSITIVE_FIELDS.items()
}

DISTINCT_STAMP_FIXTURES = (
    {
        "strategy": "STAMP_TREND",
        "symbol": "BTCUSDT",
        "timeframe": "1h",
        "trades": 60,
        "regime_present": True,
        "best_params": {"length": 20, "enabled": True},
        "cost_bps": 8.0,
        "data_start": "2025-01-01T00:00:00Z",
        "data_end": "2025-12-31T23:00:00Z",
        "data_rows": 8760,
        "parity_status": "N_A",
    },
    {
        "strategy": "STAMP_HTF_TREND",
        "symbol": "ETHUSDT",
        "timeframe": "4h",
        "trades": 12,
        "regime_present": False,
        "best_params": {"fast": 12, "slow": 48, "use_filter": False},
        "cost_bps": 6.0,
        "data_start": "2025-02-01T00:00:00Z",
        "data_end": "2025-07-31T20:00:00Z",
        "data_rows": 1086,
        "parity_status": "WARNING",
    },
    {
        "strategy": "STAMP_DUAL_RSI",
        "symbol": "SOLUSDT",
        "timeframe": "15m",
        "trades": 31,
        "regime_present": True,
        "best_params": {"rsi_fast": 7, "rsi_slow": 21, "threshold": 55.5},
        "cost_bps": 10.0,
        "data_start": "2025-03-01T00:00:00Z",
        "data_end": "2025-05-31T23:45:00Z",
        "data_rows": 8832,
        "parity_status": "VERIFIED",
    },
    {
        "strategy": "STAMP_BREAKOUT",
        "symbol": "XRPUSDT",
        "timeframe": "30m",
        "trades": 45,
        "regime_present": False,
        "best_params": {"lookback": 55, "buffer": 0.002},
        "cost_bps": 12.0,
        "data_start": "2025-04-01T00:00:00Z",
        "data_end": "2025-09-30T23:30:00Z",
        "data_rows": 8784,
        "parity_status": "N_A",
    },
    {
        "strategy": "STAMP_MEAN_REVERSION",
        "symbol": "ADAUSDT",
        "timeframe": "2h",
        "trades": 29,
        "regime_present": True,
        "best_params": {"window": 40, "z_exit": 0.5},
        "cost_bps": 4.0,
        "data_start": "2025-05-01T00:00:00Z",
        "data_end": "2025-10-31T22:00:00Z",
        "data_rows": 2208,
        "parity_status": "WARNING",
    },
    {
        "strategy": "STAMP_VOLATILITY",
        "symbol": "DOGEUSDT",
        "timeframe": "5m",
        "trades": 120,
        "regime_present": True,
        "best_params": {"atr": 14, "multiplier": 2.2},
        "cost_bps": 14.0,
        "data_start": "2025-06-01T00:00:00Z",
        "data_end": "2025-06-30T23:55:00Z",
        "data_rows": 8640,
        "parity_status": "VERIFIED",
    },
    {
        "strategy": "STAMP_CHANNEL",
        "symbol": "AVAXUSDT",
        "timeframe": "1D",
        "trades": 8,
        "regime_present": False,
        "best_params": {"channel": 20, "enabled": False},
        "cost_bps": 7.0,
        "data_start": "2024-01-01T00:00:00Z",
        "data_end": "2025-12-31T00:00:00Z",
        "data_rows": 731,
        "parity_status": "N_A",
    },
    {
        "strategy": "STAMP_MOMENTUM",
        "symbol": "TRXUSDT",
        "timeframe": "4h",
        "trades": 75,
        "regime_present": True,
        "best_params": {"ema_fast": 9, "ema_slow": 30},
        "cost_bps": 9.0,
        "data_start": "2025-07-01T00:00:00Z",
        "data_end": "2025-12-31T20:00:00Z",
        "data_rows": 1104,
        "parity_status": "VERIFIED",
    },
    {
        "strategy": "STAMP_REVERSAL",
        "symbol": "BNBUSDT",
        "timeframe": "1h",
        "trades": 33,
        "regime_present": False,
        "best_params": {"mode": "fast", "cooldown": 3},
        "cost_bps": 11.0,
        "data_start": "2025-08-01T00:00:00Z",
        "data_end": "2025-11-30T23:00:00Z",
        "data_rows": 2928,
        "parity_status": "WARNING",
    },
)


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


def _evaluation_for_evidence(
    strategy: str = "TEST_STAMPS",
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    trades: int = 60,
    regime_present: bool = True,
    parity_status: str = "N_A",
) -> dict:
    return {
        "strategy_id": f"{strategy}|{symbol}|{timeframe}",
        "symbol": symbol,
        "timeframe": timeframe,
        "metrics": {
            "trades": {
                "status": "OK",
                "value": trades,
                "reason": "",
                "source_path": "test:computed_trades",
            }
        },
        "regime": {
            "regime_breakdown_present": {
                "status": "OK",
                "value": regime_present,
                "reason": "",
                "source_path": "test:computed_regime",
            }
        },
        "hard_flags": {"repaint_status": None, "overfit_suspect": None},
        "flags": {"parity_status": parity_status},
    }


def _mega_row_for_evidence(
    strategy: str = "TEST_STAMPS",
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    best_params: dict | None = None,
    data_start: str = "2025-01-01T00:00:00Z",
    data_end: str = "2025-12-31T23:00:00Z",
    data_rows: int = 8760,
) -> dict:
    return {
        "strategy": strategy,
        "symbol": symbol,
        "timeframe": timeframe,
        "data_start": data_start,
        "data_end": data_end,
        "data_rows": data_rows,
        "summary": {
            "best_params": (
                {"length": 20, "enabled": True}
                if best_params is None
                else best_params
            )
        },
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


def _slippage_probe_frame(n: int = 300) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "open": np.full(n, 100.0),
            "high": np.full(n, 100.12),
            "low": np.full(n, 99.97),
            "close": np.full(n, 100.0),
            "date": pd.date_range("2026-01-01", periods=n, freq="h", tz="UTC").date,
        }
    )


def _scorecard_from_slice_stats(stats: mega.SliceStats) -> tuple[dict, dict]:
    artifact = evaluation_builder.build_artifact(
        {
            "strategy": "TEST_QUEUE",
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "summary": {"lockbox_oos": asdict(stats)},
        },
        cpcv_row={"status": "OK", "pass_rate": 0.82},
        pbo=None,
        backtest_run_id="scorecard-honesty-test",
    )
    return artifact, score_all_gates.score_all_gates(artifact)


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


def test_prior_generic_positive_census_is_42_with_41_neutralized_fields():
    artifact = evidence_writer.enrich_artifact(
        _evaluation_for_evidence(),
        _mega_row_for_evidence(),
        {"generated_utc": "2026-08-29T00:00:00Z", "cost_bps": 8.0},
        "scorecard-honesty-test",
    )

    prior_generic_positive_fields = [
        artifact[block][field]
        for block, names in PRIOR_GENERIC_POSITIVE_FIELDS.items()
        for field in names
    ]
    neutralized_fields = [
        artifact[block][field]
        for block, names in NEUTRALIZED_EXISTENCE_ONLY_FIELDS.items()
        for field in names
    ]

    assert len(prior_generic_positive_fields) == 42
    assert len(neutralized_fields) == 41
    assert all(item["status"] == "NOT_COMPUTED" for item in neutralized_fields)
    assert all(item["value"] is None for item in neutralized_fields)
    assert artifact["intake"]["inputs_numeric_boolean"]["status"] == "OK"
    assert artifact["intake"]["inputs_numeric_boolean"]["value"] is True

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


def test_stamp_fixture_inputs_are_nine_distinct_records():
    assert len(DISTINCT_STAMP_FIXTURES) == 9
    assert len({json.dumps(item, sort_keys=True) for item in DISTINCT_STAMP_FIXTURES}) == 9
    assert len({item["symbol"] for item in DISTINCT_STAMP_FIXTURES}) == 9
    serialized_parameters = {
        json.dumps(item["best_params"], sort_keys=True)
        for item in DISTINCT_STAMP_FIXTURES
    }
    assert len(serialized_parameters) == 9
    assert len({item["cost_bps"] for item in DISTINCT_STAMP_FIXTURES}) == 9


@pytest.mark.parametrize(
    "fixture",
    DISTINCT_STAMP_FIXTURES,
    ids=[item["strategy"] for item in DISTINCT_STAMP_FIXTURES],
)
def test_stamp_neutralization_keeps_gate2_and_promotable_byte_identical(fixture):
    honest_artifact = evidence_writer.enrich_artifact(
        _evaluation_for_evidence(
            fixture["strategy"],
            fixture["symbol"],
            fixture["timeframe"],
            fixture["trades"],
            fixture["regime_present"],
            fixture["parity_status"],
        ),
        _mega_row_for_evidence(
            fixture["strategy"],
            fixture["symbol"],
            fixture["timeframe"],
            fixture["best_params"],
            fixture["data_start"],
            fixture["data_end"],
            fixture["data_rows"],
        ),
        {
            "generated_utc": "2026-08-29T00:00:00Z",
            "cost_bps": fixture["cost_bps"],
        },
        "scorecard-honesty-test",
    )
    stamped_variant = deepcopy(honest_artifact)
    for block, names in PRIOR_GENERIC_POSITIVE_FIELDS.items():
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


def test_zero_trade_slice_does_not_publish_default_slippage_as_computed():
    frame = _slippage_probe_frame()
    stats = mega.simulate_slice(
        frame,
        pd.Series(False, index=frame.index),
        pd.Series(99.94, index=frame.index),
        "TEST_QUEUE",
        0,
        len(frame),
    )
    artifact, scorecard = _scorecard_from_slice_stats(stats)

    assert stats.num_trades == 0
    assert "net_after_slippage_pct" not in scorecard["gate2"]["metrics"]
    assert artifact["metrics"]["net_after_slippage_pct"]["status"] != "OK"
    assert stats.net_after_slippage_pct is None


def test_computed_zero_slippage_is_still_published():
    frame = _slippage_probe_frame()
    signal = pd.Series(False, index=frame.index)
    signal.iloc[20] = True
    stats = mega.simulate_slice(
        frame,
        signal,
        pd.Series(99.94, index=frame.index),
        "TEST_QUEUE",
        0,
        len(frame),
    )
    artifact, scorecard = _scorecard_from_slice_stats(stats)

    assert stats.num_trades == 1
    assert stats.net_after_slippage_pct == 0.0
    assert artifact["metrics"]["net_after_slippage_pct"]["status"] == "OK"
    assert scorecard["gate2"]["metrics"]["net_after_slippage_pct"]["value"] == 0.0
