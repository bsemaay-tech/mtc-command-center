import math
from datetime import datetime

import pytest

from mtc_v2.core.config import (
    EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
    EXECUTION_PROFILE_RAW_CLOSE_ONLY,
    resolve_config,
    validate_config,
)
from mtc_v2.core.exits import (
    REASON_EXIT_BE,
    REASON_EXIT_SL_ATR,
    REASON_EXIT_SL_PERCENT,
    REASON_EXIT_SL_SWING_ATR,
    REASON_EXIT_TP1,
    REASON_EXIT_TP2,
    REASON_EXIT_TP_ATR,
    REASON_EXIT_TP_PERCENT,
    REASON_EXIT_TP_R,
    REASON_EXIT_TRAIL,
)
from mtc_v2.core.indicators import IndicatorSnapshot, SupertrendIndicatorSnapshot
from mtc_v2.core.instrument import InstrumentMetadata
from mtc_v2.core.position_sizer import PositionSizer
from mtc_v2.core.runner import (
    EXIT_BEFORE_ENTRY_PLACEHOLDER,
    FILL_POLICY_DECISION_BAR_CLOSE,
    REASON_EXIT_MARGIN_CALL,
    REASON_SIGNAL_CONFLICT,
    SAME_BAR_REENTRY_OWNER,
    Runner,
)
from mtc_v2.core.rounding import ceil_to_grid, floor_qty_to_step, floor_to_grid, round_half_up_to_grid
from mtc_v2.core.types import Bar, GateResult, RawSignal
from mtc_v2.signals.supertrend import (
    REASON_ST_DIRECTION_INIT,
    REASON_ST_FLIP_LONG,
    REASON_ST_FLIP_SHORT,
    REASON_ST_HA_NOT_SUPPORTED,
    REASON_ST_HOLD_LONG,
    REASON_ST_HOLD_SHORT,
    REASON_ST_INVALID_BAR,
    REASON_ST_WARMUP,
)


def _build_config(**overrides: object) -> dict[str, object]:
    config: dict[str, object] = {
        "enable_long": True,
        "enable_short": True,
        "allow_flip": True,
        "regime_lock": False,
        "max_entries": 1,
        "cooldown_bars": 0,
        "warmup_bars_override": None,
        "signal_mode": "Supertrend",
        "st_atr_len": 3,
        "st_factor": 1.0,
        "st_use_wicks": False,
        "st_use_ha": False,
        "instrument_symbol": "TEST",
        "instrument_point_value": 1.0,
        "instrument_price_tick": 0.25,
        "instrument_qty_step": 1.0,
        "instrument_min_qty": 0.0,
        "instrument_min_notional": 0.0,
        "instrument_contract_multiplier": 1.0,
        "initial_capital": 1000.0,
        "margin_long_pct": 100.0,
        "margin_short_pct": 100.0,
        "execution_profile_id": EXECUTION_PROFILE_RAW_CLOSE_ONLY,
        "risk_per_long_pct": 0.4,
        "risk_per_short_pct": 0.4,
        "fallback_size_pct": 10.1,
        "max_leverage_cap": 1.0,
        "equity_source": "Realized",
        "use_notional_assert": False,
        "use_sl": True,
        "use_sl_atr": True,
        "sl_atr_len": 1,
        "sl_atr_mult": 4.0,
        "tp_mode": "None",
        "tp_atr_len": 1,
        "tp_atr_mult": 4.0,
    }
    config.update(overrides)
    return config


def test_resolve_config_derives_margin_from_max_leverage_when_not_explicit() -> None:
    cfg = resolve_config({"max_leverage_cap": 5.0})
    assert cfg["margin_long_pct"] == pytest.approx(20.0)
    assert cfg["margin_short_pct"] == pytest.approx(20.0)


def test_resolve_config_preserves_explicit_margin_overrides() -> None:
    cfg = resolve_config(_build_config(max_leverage_cap=5.0, margin_long_pct=100.0, margin_short_pct=50.0))
    assert cfg["margin_long_pct"] == pytest.approx(100.0)
    assert cfg["margin_short_pct"] == pytest.approx(50.0)


def _build_transition_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 1, 1), 10.0, 10.0, 10.0, 10.0, 100, 0),
        Bar(datetime(2025, 1, 2), 10.0, 11.0, 9.8, 10.8, 120, 1),
        Bar(datetime(2025, 1, 3), 10.8, 11.2, 10.5, 11.0, 110, 2),
        Bar(datetime(2025, 1, 4), 11.0, 11.3, 10.7, 11.1, 130, 3),
        Bar(datetime(2025, 1, 5), 11.1, 11.2, 8.5, 9.0, 150, 4),
        Bar(datetime(2025, 1, 6), 9.0, 9.2, 8.8, 9.1, 90, 5),
        Bar(datetime(2025, 1, 7), 9.1, 12.5, 9.0, 12.0, 160, 6),
        Bar(datetime(2025, 1, 8), 12.0, 12.4, 11.7, 12.2, 140, 7),
    ]


def _build_invalid_start_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 2, 1), math.nan, math.nan, math.nan, math.nan, 100, 0),
        Bar(datetime(2025, 2, 2), 10.0, 10.0, 10.0, 10.0, 100, 1),
        Bar(datetime(2025, 2, 3), 10.0, 11.0, 9.5, 10.5, 100, 2),
        Bar(datetime(2025, 2, 4), 10.5, 10.8, 10.2, 10.6, 100, 3),
    ]


def _build_wicks_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 3, 1), 10.0, 10.2, 9.8, 10.0, 100, 0),
        Bar(datetime(2025, 3, 2), 10.0, 10.1, 9.0, 9.2, 100, 1),
        Bar(datetime(2025, 3, 3), 9.2, 9.3, 8.9, 9.0, 100, 2),
        Bar(datetime(2025, 3, 4), 9.0, 9.7, 8.95, 9.1, 100, 3),
        Bar(datetime(2025, 3, 5), 9.1, 9.2, 8.8, 9.0, 100, 4),
    ]


def _build_established_state_invalid_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 4, 1), 10.0, 10.0, 10.0, 10.0, 100, 0),
        Bar(datetime(2025, 4, 2), 10.0, 11.0, 9.8, 10.8, 120, 1),
        Bar(datetime(2025, 4, 3), 10.8, 11.2, 10.5, 11.0, 110, 2),
        Bar(datetime(2025, 4, 4), 11.0, 11.3, 10.7, 11.1, 130, 3),
        Bar(datetime(2025, 4, 5), math.nan, math.nan, math.nan, math.nan, 0, 4),
        Bar(datetime(2025, 4, 6), 11.1, 11.2, 8.5, 9.0, 150, 5),
    ]


def _build_entry_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 100.0, 100.5, 110, 1),
    ]


def _build_pyramid_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 100.0, 100.5, 110, 1),
        Bar(datetime(2025, 5, 3), 100.5, 101.0, 100.25, 100.75, 120, 2),
    ]


def _build_equity_snapshot_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 6, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 6, 2), 110.0, 111.0, 109.0, 110.5, 120, 1),
        Bar(datetime(2025, 6, 3), 110.5, 111.0, 109.5, 110.0, 120, 2),
    ]


def _instrument(**overrides: float) -> InstrumentMetadata:
    values = {
        "symbol": "TEST",
        "point_value": 1.0,
        "price_tick": 0.25,
        "qty_step": 0.1,
        "min_qty": 0.0,
        "min_notional": 0.0,
        "contract_multiplier": 1.0,
    }
    values.update(overrides)
    return InstrumentMetadata(**values)


def _build_stop_gap_long_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 99.0, 99.3, 98.5, 99.1, 110, 1),
    ]


def _build_stop_touch_long_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.0, 100.2, 99.2, 99.4, 110, 1),
    ]


def _build_stop_safe_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.3, 100.8, 99.4, 100.6, 110, 1),
    ]


def _build_tp_touch_long_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.4, 101.4, 100.2, 101.2, 110, 1),
    ]


def _build_tp_touch_short_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.1, 100.2, 99.0, 99.2, 110, 1),
    ]


def _build_tp_ambiguity_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.2, 101.4, 99.0, 100.3, 110, 1),
    ]


def _build_close_only_stop_probe_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.0, 100.2, 99.2, 99.6, 110, 1),
    ]


def _build_close_only_tp_probe_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.4, 101.4, 100.2, 100.8, 110, 1),
    ]


def _build_close_only_stop_break_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.0, 100.2, 99.2, 99.2, 110, 1),
    ]


def _build_close_only_tp_break_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        Bar(datetime(2025, 5, 2), 100.4, 101.6, 100.2, 101.4, 110, 1),
    ]


def _build_close_only_trailing_probe_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 10, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 10, 2), 100.2, 102.0, 100.4, 100.8, 100, 1),
        Bar(datetime(2025, 10, 3), 100.0, 100.2, 99.5, 99.8, 100, 2),
    ]


def _build_regime_lock_bars() -> list[Bar]:
    return [
        _build_entry_bars()[0],
        _build_stop_gap_long_bars()[1],
        Bar(datetime(2025, 5, 3), 99.1, 100.0, 98.9, 99.8, 120, 2),
        Bar(datetime(2025, 5, 4), 99.8, 100.1, 98.7, 99.0, 130, 3),
    ]


def _build_percent_exit_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 7, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 7, 2), 100.1, 102.5, 98.8, 101.0, 110, 1),
    ]


def _build_percent_tp_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 7, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 7, 2), 100.1, 102.5, 100.0, 101.0, 110, 1),
    ]


def _build_swing_entry_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 8, 1), 100.0, 100.5, 99.0, 100.0, 100, 0),
        Bar(datetime(2025, 8, 2), 100.0, 101.0, 99.5, 100.5, 100, 1),
        Bar(datetime(2025, 8, 3), 100.2, 100.6, 100.0, 100.0, 100, 2),
        Bar(datetime(2025, 8, 4), 99.2, 99.5, 98.4, 98.8, 100, 3),
    ]


def _build_break_even_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 9, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 9, 2), 100.2, 101.2, 100.3, 100.8, 100, 1),
        Bar(datetime(2025, 9, 3), 100.05, 100.2, 99.8, 100.0, 100, 2),
    ]


def _build_trailing_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 10, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 10, 2), 100.2, 102.0, 101.3, 101.8, 100, 1),
        Bar(datetime(2025, 10, 3), 100.3, 100.5, 99.8, 100.0, 100, 2),
    ]


class _StaticSignalProducer:
    def __init__(self, outputs: list[RawSignal], *, warmup_ready: bool = True) -> None:
        self._outputs = outputs
        self._index = 0
        self._warmup_ready = warmup_ready
        self.warmup_bars_required = 0
        self._snapshot = IndicatorSnapshot(
            supertrend=SupertrendIndicatorSnapshot(valid_bar=True, warmup_ready=warmup_ready)
        )

    def calculate(self, bar: Bar) -> RawSignal:
        raw = self._outputs[self._index]
        self._index += 1
        self._snapshot = IndicatorSnapshot(
            supertrend=SupertrendIndicatorSnapshot(
                line=raw.line,
                direction=raw.direction,
                valid_bar=True,
                warmup_ready=self._warmup_ready,
            )
        )
        return raw

    def indicator_snapshot(self) -> IndicatorSnapshot:
        return self._snapshot


def test_runner_smoke_supertrend_transition_contract() -> None:
    bars = _build_transition_bars()
    runner = Runner(_build_config())
    out = runner.run(bars)

    assert len(out) == 8
    assert all(not (signal.long and signal.short) for signal in out)
    assert [signal.reason for signal in out] == [
        REASON_ST_WARMUP,
        REASON_ST_WARMUP,
        REASON_ST_DIRECTION_INIT,
        REASON_ST_HOLD_LONG,
        REASON_ST_FLIP_SHORT,
        REASON_ST_HOLD_SHORT,
        REASON_ST_FLIP_LONG,
        REASON_ST_HOLD_LONG,
    ]
    assert [signal.direction for signal in out] == [None, None, 1, 1, -1, -1, 1, 1]

    pulse_indices = [idx for idx, signal in enumerate(out) if signal.long or signal.short]
    assert pulse_indices == [4, 6]
    assert sum(int(signal.long) + int(signal.short) for signal in out) == 2

    assert out[0].line is None
    assert out[1].line is None
    assert out[2].line == pytest.approx(10.216666666666667)
    assert out[4].line == pytest.approx(11.164814814814815)
    assert out[6].line == pytest.approx(8.91008230452675)

    formatted = Runner.format_raw_signals(out)
    assert formatted[2] == "02 | pulse=-     | dir= 1 | line= 10.2167 | reason=st_direction_init"
    assert formatted[4] == "04 | pulse=SHORT | dir=-1 | line= 11.1648 | reason=st_flip_short"
    assert formatted[6] == "06 | pulse=LONG  | dir= 1 | line=  8.9101 | reason=st_flip_long"

    parity_rows = runner.run_parity_rows(_build_transition_bars())
    assert parity_rows == [
        "00 | c=10.00 | d=na | L=0 | S=0 | r=st_warmup",
        "01 | c=10.80 | d=na | L=0 | S=0 | r=st_warmup",
        "02 | c=11.00 | d= 1 | L=0 | S=0 | r=st_direction_init",
        "03 | c=11.10 | d= 1 | L=0 | S=0 | r=st_hold_long",
        "04 | c= 9.00 | d=-1 | L=0 | S=1 | r=st_flip_short",
        "05 | c= 9.10 | d=-1 | L=0 | S=0 | r=st_hold_short",
        "06 | c=12.00 | d= 1 | L=1 | S=0 | r=st_flip_long",
        "07 | c=12.20 | d= 1 | L=0 | S=0 | r=st_hold_long",
    ]


def test_config_validation_and_execution_placeholders() -> None:
    validate_config(_build_config())
    validate_config(_build_config(enable_long=False, allow_flip=False, regime_lock=True))
    validate_config(_build_config(use_sl=False, use_sl_atr=True))
    validate_config(_build_config(use_sl=True, use_sl_atr=False, use_sl_percent=True, sl_percent=1.5))
    validate_config(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_swing_atr=True,
            sl_swing_basis="Wick",
            sl_swing_lookback=3,
        )
    )
    validate_config(_build_config(tp_mode="None"))
    validate_config(_build_config(tp_mode="ATR"))
    validate_config(_build_config(tp_mode="Percent"))
    validate_config(_build_config(tp_mode="R"))
    validate_config(_build_config(tp_mode="Multi-TP"))
    validate_config(_build_config(execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC))
    validate_config(_build_config(max_entries=2))
    validate_config(_build_config(cooldown_bars=2))
    validate_config(_build_config(initial_capital=100000.0, margin_long_pct=100.0, margin_short_pct=100.0))
    validate_config(_build_config(equity_source="Equity", use_notional_assert=True))
    validate_config(
        _build_config(
            tw_audit_semantics_mode="research",
            tw_reversal_reentry_mode="next_bar_open_after_protective_exit_signal",
            tw_reversal_reentry_delay_bars=1,
            tw_margin_call_mode="tradingview",
            tw_margin_call_split_entries=True,
            tw_be_semantics_mode="tradingview",
            tw_trailing_semantics_mode="tradingview",
        )
    )

    with pytest.raises(ValueError, match="Unknown config keys"):
        validate_config({"signal_mode": "Supertrend", "unknown_key": True})

    with pytest.raises(ValueError, match="execution_profile_id"):
        validate_config(_build_config(execution_profile_id="custom_profile"))

    with pytest.raises(ValueError, match="Exactly one SL mode must be selected"):
        validate_config(_build_config(use_sl=True, use_sl_atr=False))

    with pytest.raises(ValueError, match="tp1_close_pct must be between 0 and 100"):
        validate_config(_build_config(tp_mode="Multi-TP", tp1_close_pct=100.0))

    with pytest.raises(ValueError, match="equity_source must be one of"):
        validate_config(_build_config(equity_source="Marked"))

    with pytest.raises(ValueError, match="fixed_qty is inactive"):
        validate_config(_build_config(fixed_qty=2.0))

    with pytest.raises(ValueError, match="must be finite"):
        validate_config(_build_config(st_factor=math.nan))

    with pytest.raises(ValueError, match="must be finite"):
        validate_config(_build_config(instrument_qty_step=math.inf))

    with pytest.raises(ValueError, match="tw_audit_semantics_mode"):
        validate_config(_build_config(tw_audit_semantics_mode="invalid"))

    with pytest.raises(ValueError, match="tw_reversal_reentry_mode"):
        validate_config(_build_config(tw_reversal_reentry_mode="invalid"))

    runner = Runner(
        _build_config(
            instrument_symbol="TEST-PERP",
            instrument_point_value=1.0,
            instrument_price_tick=0.25,
            instrument_qty_step=0.1,
            instrument_min_qty=0.2,
            instrument_min_notional=10.0,
            instrument_contract_multiplier=1.0,
            initial_capital=100000.0,
            risk_per_long_pct=0.01,
            risk_per_short_pct=0.01,
            max_leverage_cap=1.0,
        )
    )
    runner.run(_build_transition_bars())

    assert runner.execution_profile_id == EXECUTION_PROFILE_RAW_CLOSE_ONLY
    assert runner.fill_policy_id == FILL_POLICY_DECISION_BAR_CLOSE
    assert runner.exit_before_entry_policy == EXIT_BEFORE_ENTRY_PLACEHOLDER
    assert runner.same_bar_reentry_owner == SAME_BAR_REENTRY_OWNER
    assert runner.tw_audit_semantics_mode == "off"
    assert runner.tw_reversal_reentry_mode == "local"
    assert runner.tw_reversal_reentry_delay_bars == 0
    assert runner.tw_margin_call_mode == "off"
    assert runner.tw_margin_call_split_entries is False
    assert runner.tw_be_semantics_mode == "local"
    assert runner.tw_trailing_semantics_mode == "local"
    assert runner.state.warmup_bars == 3
    assert runner.state.instrument.symbol == "TEST-PERP"
    assert runner.state.instrument.point_value == pytest.approx(1.0)
    assert runner.state.instrument.price_tick == pytest.approx(0.25)
    assert runner.state.instrument.qty_step == pytest.approx(0.1)
    assert runner.state.instrument.min_qty == pytest.approx(0.2)
    assert runner.state.instrument.min_notional == pytest.approx(10.0)
    assert runner.state.instrument.contract_multiplier == pytest.approx(1.0)
    assert runner.state.initial_capital == pytest.approx(100000.0)
    assert runner.state.equity == pytest.approx(
        runner.state.initial_capital + runner.state.realized_equity + runner.state.unrealized_pnl
    )
    assert runner.state.last_sizing_equity_snapshot > 0.0

    snapshot = runner.state.indicator_snapshot.supertrend
    assert snapshot.valid_bar is True
    assert snapshot.warmup_ready is True
    assert snapshot.direction == 1
    assert snapshot.line == pytest.approx(10.5900548696845)
    assert runner.state.block_new_entries_this_bar is False
    assert runner.state.position is None
    assert runner.state.total_entries == 0
    assert runner.state.total_exits == 0

    close_only_runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=False,
        )
    )
    close_only_runner.run(_build_transition_bars())
    assert close_only_runner.execution_profile_id == EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC


def test_runner_accepts_execution_parity_research_knobs_without_runtime_drift() -> None:
    cfg = _build_config(
        tw_audit_semantics_mode="research",
        tw_reversal_reentry_mode="delay_after_protective_exit",
        tw_reversal_reentry_delay_bars=1,
        tw_margin_call_mode="tradingview",
        tw_margin_call_split_entries=True,
        tw_be_semantics_mode="tradingview",
        tw_trailing_semantics_mode="tradingview",
    )
    runner = Runner(cfg)
    runner.run(_build_transition_bars())

    assert runner.tw_audit_semantics_mode == "research"
    assert runner.tw_reversal_reentry_mode == "delay_after_protective_exit"
    assert runner.tw_reversal_reentry_delay_bars == 1
    assert runner.tw_margin_call_mode == "tradingview"
    assert runner.tw_margin_call_split_entries is True
    assert runner.tw_be_semantics_mode == "tradingview"
    assert runner.tw_trailing_semantics_mode == "tradingview"


def test_rounding_helpers_use_parity_safe_contract() -> None:
    assert round_half_up_to_grid(100.025, 0.05) == pytest.approx(100.05)
    assert round_half_up_to_grid(100.024, 0.05) == pytest.approx(100.0)
    assert floor_to_grid(21311.827978514633, 0.1) == pytest.approx(21311.8)
    assert ceil_to_grid(21311.827978514633, 0.1) == pytest.approx(21311.9)
    assert floor_qty_to_step(1.29, 0.1) == pytest.approx(1.2)
    assert floor_qty_to_step(0.09, 0.1) == pytest.approx(0.0)


def test_position_sizer_l6_sl_on_long_and_short_qty_contract() -> None:
    sizer = PositionSizer(_build_config(risk_per_long_pct=2.0, risk_per_short_pct=1.0, max_leverage_cap=10.0))
    instrument = _instrument(qty_step=0.1)

    long_qty = sizer.calc_qty(100.0, 96.0, 1000.0, True, instrument)
    short_qty = sizer.calc_qty(100.0, 104.0, 1000.0, False, instrument)

    assert long_qty == pytest.approx(5.0)
    assert short_qty == pytest.approx(2.5)


def test_position_sizer_l6_sl_off_fallback_qty_contract() -> None:
    sizer = PositionSizer(_build_config(fallback_size_pct=25.0, max_leverage_cap=10.0))
    instrument = _instrument(qty_step=0.1)

    qty = sizer.calc_qty(100.0, None, 1000.0, True, instrument)

    assert qty == pytest.approx(2.5)


def test_position_sizer_l6_zero_equity_min_filters_leverage_and_rounding() -> None:
    sizer = PositionSizer(_build_config(risk_per_long_pct=10.0, max_leverage_cap=1.0))

    assert sizer.calc_qty(100.0, 96.0, 0.0, True, _instrument()) == pytest.approx(0.0)
    assert sizer.calc_qty(100.0, 96.0, -10.0, True, _instrument()) == pytest.approx(0.0)
    assert sizer.calc_qty(100.0, 96.0, 1000.0, True, _instrument(min_qty=11.0)) == pytest.approx(0.0)
    assert sizer.calc_qty(100.0, 96.0, 1000.0, True, _instrument(min_notional=1500.0)) == pytest.approx(0.0)
    assert sizer.calc_qty(100.0, 99.0, 1000.0, True, _instrument(qty_step=0.1)) == pytest.approx(10.0)
    assert sizer.calc_qty(100.0, 96.0, 1000.0, True, _instrument(qty_step=0.1),) == pytest.approx(10.0)


def test_position_sizer_l6_rounding_boundary_is_floor_based() -> None:
    sizer = PositionSizer(_build_config(risk_per_long_pct=0.5, max_leverage_cap=10.0))
    instrument = _instrument(qty_step=0.1)

    qty = sizer.calc_qty(100.25, 96.25, 1000.0, True, instrument)

    assert qty == pytest.approx(1.2)


def test_position_sizer_research_mode_uses_finer_qty_precision() -> None:
    local_sizer = PositionSizer(_build_config(risk_per_long_pct=10.0, max_leverage_cap=1.0))
    research_sizer = PositionSizer(
        _build_config(risk_per_long_pct=10.0, tw_audit_semantics_mode="research", max_leverage_cap=1.0)
    )
    instrument = _instrument(price_tick=0.01, qty_step=0.001, min_qty=0.001)

    local_qty = local_sizer.calc_qty(100.25, 99.25, 1000.0, True, instrument)
    research_qty = research_sizer.calc_qty(100.25, 99.25, 1000.0, True, instrument)

    assert local_qty == pytest.approx(9.975)
    assert research_qty == pytest.approx(9.975062, rel=1e-9)


def test_runner_l6_equity_source_override_is_ignored_and_sizing_stays_realized() -> None:
    bars = _build_equity_snapshot_bars()[:2]
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(False, True, "manual_short", direction=-1, line=9.0),
    ]

    realized_runner = Runner(
        _build_config(
            use_sl=False,
            allow_flip=True,
            fallback_size_pct=50.0,
            instrument_qty_step=0.01,
            equity_source="Realized",
        )
    )
    realized_runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    realized_runner.state.warmup_bars = 0
    realized_runner.run(bars)

    legacy_equity_runner = Runner(
        _build_config(
            use_sl=False,
            allow_flip=True,
            fallback_size_pct=50.0,
            instrument_qty_step=0.01,
            equity_source="Equity",
        )
    )
    legacy_equity_runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    legacy_equity_runner.state.warmup_bars = 0
    legacy_equity_runner.run(bars)

    assert realized_runner.state.position is not None
    assert realized_runner.state.position.side == "short"
    assert realized_runner.state.position.qty == pytest.approx(4.52)
    assert legacy_equity_runner.state.position is not None
    assert legacy_equity_runner.state.position.side == "short"
    assert legacy_equity_runner.state.position.qty == pytest.approx(realized_runner.state.position.qty)


def test_position_sizer_use_notional_assert_override_is_ignored() -> None:
    instrument = _instrument(price_tick=0.01, qty_step=0.001, min_qty=0.001)
    default_sizer = PositionSizer(_build_config(risk_per_long_pct=10.0, max_leverage_cap=1.0))
    legacy_override_sizer = PositionSizer(
        _build_config(risk_per_long_pct=10.0, max_leverage_cap=1.0, use_notional_assert=True)
    )

    default_qty = default_sizer.calc_qty(100.25, 99.25, 1000.0, True, instrument)
    legacy_override_qty = legacy_override_sizer.calc_qty(100.25, 99.25, 1000.0, True, instrument)

    assert default_qty == pytest.approx(9.975)
    assert legacy_override_qty == pytest.approx(default_qty)


def test_runner_smoke_supertrend_invalid_start_bar_does_not_advance_warmup() -> None:
    runner = Runner(_build_config(st_atr_len=2))
    bars = _build_invalid_start_bars()
    early = runner.run(bars[:2])

    assert [signal.reason for signal in early] == [
        REASON_ST_INVALID_BAR,
        REASON_ST_WARMUP,
    ]
    assert runner.state.indicator_snapshot.supertrend.warmup_ready is False
    assert runner.state.block_new_entries_this_bar is True

    out = early + runner.run(bars[2:])

    assert [signal.reason for signal in out] == [
        REASON_ST_INVALID_BAR,
        REASON_ST_WARMUP,
        REASON_ST_DIRECTION_INIT,
        REASON_ST_HOLD_LONG,
    ]
    assert [signal.direction for signal in out] == [None, None, 1, 1]
    assert all(not signal.long and not signal.short for signal in out)
    assert out[2].line == pytest.approx(9.5)
    assert out[3].line == pytest.approx(9.825)
    assert runner.state.indicator_snapshot.supertrend.warmup_ready is True
    assert runner.state.block_new_entries_this_bar is False


def test_runner_smoke_supertrend_ha_not_supported() -> None:
    out = Runner(_build_config(st_use_ha=True)).run(_build_transition_bars())

    assert len(out) == 8
    assert all(signal.reason == REASON_ST_HA_NOT_SUPPORTED for signal in out)
    assert all(not signal.long and not signal.short for signal in out)
    assert all(signal.direction is None for signal in out)
    assert all(signal.line is None for signal in out)


def test_runner_smoke_supertrend_invalid_bar_keeps_established_state() -> None:
    out = Runner(_build_config()).run(_build_established_state_invalid_bars())

    assert out[3].reason == REASON_ST_HOLD_LONG
    assert out[3].direction == 1
    assert out[3].line == pytest.approx(10.377777777777778)

    assert out[4].reason == REASON_ST_INVALID_BAR
    assert out[4].long is False
    assert out[4].short is False
    assert out[4].direction == out[3].direction
    assert out[4].line == pytest.approx(out[3].line)

    assert out[5].reason == REASON_ST_FLIP_SHORT
    assert out[5].short is True
    assert out[5].long is False
    assert out[5].direction == -1


def test_runner_smoke_supertrend_wicks_only_flip_changes_raw_pulses() -> None:
    bars = _build_wicks_bars()
    out_without_wicks = Runner(_build_config(st_atr_len=2, st_factor=0.5, st_use_wicks=False)).run(bars)
    out_with_wicks = Runner(_build_config(st_atr_len=2, st_factor=0.5, st_use_wicks=True)).run(bars)

    assert all(not (signal.long and signal.short) for signal in out_without_wicks)
    assert all(not (signal.long and signal.short) for signal in out_with_wicks)

    assert out_without_wicks[3].reason == REASON_ST_HOLD_SHORT
    assert out_without_wicks[3].direction == -1
    assert out_without_wicks[3].long is False
    assert out_without_wicks[3].short is False

    assert out_with_wicks[3].reason == REASON_ST_FLIP_LONG
    assert out_with_wicks[3].direction == 1
    assert out_with_wicks[3].long is True
    assert out_with_wicks[3].short is False


def test_runner_l3_no_signal_keeps_portfolio_flat() -> None:
    bars = _build_entry_bars()
    runner = Runner(_build_config(instrument_qty_step=0.1, instrument_min_qty=0.1))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "no_signal", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars)

    assert len(out) == 2
    assert runner.state.position is None
    assert runner.state.total_entries == 0
    assert runner.state.opened_this_bar_reason is None


def test_runner_l4_capital_gate_allows_entry_within_leverage_cap() -> None:
    # With max_leverage_cap=10.0 and equity=50, the allowed notional is 500.
    # A single entry at price≈100.25 with qty=1 (notional≈100.25) is well
    # within the leverage cap, so the capital gate must NOT block it.
    # (Old behaviour incorrectly compared required_margin against self.state.equity
    # instead of sizing_equity × max_leverage_cap — that was the _entry_blocked_by_capital bug.)
    bars = _build_entry_bars()
    runner = Runner(
        _build_config(
            initial_capital=50.0,
            margin_long_pct=100.0,
            risk_per_long_pct=8.0,
            max_leverage_cap=10.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    runner.state.warmup_bars = 0

    runner.run(bars[:1])

    # required_margin ≈ 100.25 < sizing_equity × max_leverage_cap = 50 × 10 = 500
    # → capital gate should NOT block the entry.
    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.total_entries == 1
    assert runner.state.equity == pytest.approx(50.0)


def test_runner_direction_gates_block_disabled_sides() -> None:
    bars = _build_entry_bars()

    long_disabled = Runner(_build_config(enable_long=False, use_sl=False))
    long_disabled.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    long_disabled.state.warmup_bars = 0
    long_disabled.run(bars[:1])
    assert long_disabled.state.position is None

    short_disabled = Runner(_build_config(enable_short=False, use_sl=False))
    short_disabled.signal_producer = _StaticSignalProducer(
        [RawSignal(False, True, "manual_short", direction=-1, line=9.0)]
    )
    short_disabled.state.warmup_bars = 0
    short_disabled.run(bars[:1])
    assert short_disabled.state.position is None


def test_runner_l3_warmup_block_prevents_raw_pulse_entry() -> None:
    bars = _build_entry_bars()
    runner = Runner(_build_config())
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)],
        warmup_ready=False,
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars[:1])

    assert len(out) == 1
    assert out[0].long is True
    assert runner.state.position is None
    assert runner.state.block_new_entries_this_bar is True
    assert runner.state.opened_this_bar_reason is None


def test_runner_l3_long_pulse_opens_long_at_bar_close() -> None:
    bars = _build_entry_bars()
    runner = Runner(
        _build_config(
            instrument_qty_step=0.1,
            instrument_min_qty=0.1,
            risk_per_long_pct=0.5,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars[:1])

    assert len(out) == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.position.entry_price == pytest.approx(bars[0].close)
    assert runner.state.position.avg_entry_price == pytest.approx(bars[0].close)
    assert runner.state.position.qty == pytest.approx(1.2)
    assert runner.state.position.entry_bar == bars[0].bar_index
    assert len(runner.state.position.entry_legs) == 1
    assert runner.state.position.lifecycle_id == 1
    assert runner.state.position.working_exit_reference_qty == pytest.approx(1.2)
    assert runner.state.position.working_exit_book_version == 1
    assert runner.state.position.initial_risk_per_unit == pytest.approx(4.0)
    assert runner.state.position.active_stop_price == pytest.approx(96.25)
    assert runner.state.opened_this_bar_reason == "manual_long"
    assert runner.state.total_entries == 1


def test_runner_l4_stop_prices_align_to_adverse_tick_grid() -> None:
    bars = _build_entry_bars()

    long_runner = Runner(_build_config(instrument_price_tick=0.1, risk_per_long_pct=0.41))
    long_runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    long_runner.state.warmup_bars = 0
    long_runner.run(bars[:1])
    assert long_runner.state.position is not None
    assert long_runner.state.position.active_stop_price == pytest.approx(96.2)

    short_runner = Runner(_build_config(instrument_price_tick=0.1, risk_per_short_pct=0.41))
    short_runner.signal_producer = _StaticSignalProducer(
        [RawSignal(False, True, "manual_short", direction=-1, line=9.0)]
    )
    short_runner.state.warmup_bars = 0
    short_runner.run(bars[:1])
    assert short_runner.state.position is not None
    assert short_runner.state.position.active_stop_price == pytest.approx(104.3)


def test_runner_use_sl_false_keeps_entry_open_without_stop() -> None:
    bars = _build_entry_bars()
    runner = Runner(_build_config(use_sl=False, use_sl_atr=True))
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    runner.state.warmup_bars = 0

    runner.run(bars[:1])

    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.position.active_stop_price is None
    assert runner.state.position.active_tp_price is None
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 0


def test_runner_l5_tp_disabled_keeps_l4_behavior_unchanged() -> None:
    bars = _build_stop_gap_long_bars()
    runner = Runner(_build_config(tp_mode="None", sl_atr_mult=1.0))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_price == pytest.approx(99.0)
    assert runner.state.last_exit_was_pessimistic is False


def test_runner_l5_tp_warmup_blocks_entry_until_target_is_seeded() -> None:
    bars = _build_transition_bars()
    runner = Runner(_build_config(use_sl=False, tp_mode="ATR", tp_atr_len=3))
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)] * len(bars)
    )
    runner.state.warmup_bars = 0

    runner.run(bars[:2])

    assert runner.state.position is None
    assert runner.state.indicator_snapshot.atr_tp.warmup_ready is False
    assert runner.state.block_new_entries_this_bar is True

    runner.run(bars[2:3])

    assert runner.state.position is not None
    assert runner.state.position.active_tp_price is not None


def test_runner_l5_long_tp_touch_closes_at_target_price() -> None:
    bars = _build_tp_touch_long_bars()
    runner = Runner(_build_config(use_sl=False, tp_mode="ATR", tp_atr_mult=1.0))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_ATR
    assert runner.state.last_exit_price == pytest.approx(101.25)
    assert runner.state.last_realized_pnl == pytest.approx(1.0)
    assert runner.state.total_exits == 1
    assert runner.state.last_exit_was_pessimistic is False


def test_runner_l5_short_tp_touch_closes_at_target_price() -> None:
    bars = _build_tp_touch_short_bars()
    runner = Runner(_build_config(use_sl=False, tp_mode="ATR", tp_atr_mult=1.0))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, True, "manual_short", direction=-1, line=9.0),
            RawSignal(False, False, "no_signal", direction=-1, line=8.9),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_ATR
    assert runner.state.last_exit_price == pytest.approx(99.25)
    assert runner.state.last_realized_pnl == pytest.approx(1.0)
    assert runner.state.total_exits == 1


def test_runner_l5_tp_close_blocks_same_bar_opp_signal_and_reopen() -> None:
    bars = _build_tp_touch_long_bars()
    runner = Runner(_build_config(use_sl=False, tp_mode="ATR", tp_atr_mult=1.0, allow_flip=True))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, True, "manual_short", direction=-1, line=9.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_ATR
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1
    assert runner.state.block_new_entries_this_bar is True


def test_runner_l5_stop_first_wins_when_tp_and_sl_hit_same_bar() -> None:
    bars = _build_tp_ambiguity_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=True,
            sl_atr_mult=1.0,
            tp_mode="ATR",
            tp_atr_mult=1.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_price == pytest.approx(99.25)
    assert runner.state.last_exit_was_pessimistic is True
    assert runner.state.total_exits == 1


def test_close_only_profile_ignores_intrabar_stop_touch_until_close_breaks_level() -> None:
    bars = _build_close_only_stop_probe_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=True,
            sl_atr_mult=1.0,
            tp_mode="None",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.total_exits == 0
    assert runner.state.closed_this_bar_reason is None


def test_close_only_profile_exits_stop_at_bar_close_price() -> None:
    bars = _build_close_only_stop_break_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=True,
            sl_atr_mult=1.0,
            tp_mode="None",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_price == pytest.approx(99.2)
    assert runner.state.last_exit_was_pessimistic is False


def test_close_only_profile_requires_close_for_target_hits() -> None:
    bars = _build_close_only_tp_probe_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=False,
            tp_mode="ATR",
            tp_atr_mult=1.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.total_exits == 0


def test_close_only_profile_exits_target_at_bar_close_price() -> None:
    bars = _build_close_only_tp_break_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=False,
            tp_mode="ATR",
            tp_atr_mult=1.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_ATR
    assert runner.state.last_exit_price == pytest.approx(101.4)


def test_close_only_profile_break_even_requires_close_trigger() -> None:
    bars = _build_break_even_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_break_even=True,
            be_trigger_r=1.0,
            be_buffer_r=0.1,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.be_active is False
    assert runner.state.closed_this_bar_reason is None


def test_close_only_profile_trailing_requires_close_trigger_and_anchor() -> None:
    bars = _build_close_only_trailing_probe_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_trailing=True,
            trail_atr_len=1,
            trail_start_r=1.0,
            trail_distance_atr_mult=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.trail_active is False
    assert runner.state.closed_this_bar_reason is None


def test_close_only_profile_multi_tp_runs_tp1_partial_on_close_only() -> None:
    bars = _build_percent_tp_bars()
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="Multi-TP",
            tp1_r_multiple=1.0,
            tp1_close_pct=50.0,
            tp2_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP1
    assert runner.state.last_exit_price == pytest.approx(101.0)
    assert runner.state.total_exits == 1
    assert runner.state.position.qty == pytest.approx(0.5)
    assert "TP1" in runner.state.position.completed_exit_ids


def test_close_only_profile_multi_tp_does_not_chain_tp2_same_bar() -> None:
    bars = [
        Bar(datetime(2025, 1, 1), 100.0, 100.0, 100.0, 100.0, 100, 0),
        Bar(datetime(2025, 1, 2), 100.0, 103.0, 99.5, 102.5, 100, 1),
    ]
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="Multi-TP",
            tp1_r_multiple=1.0,
            tp1_close_pct=50.0,
            tp2_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP1
    assert runner.state.total_exits == 1
    assert runner.state.position.qty == pytest.approx(0.5)
    assert len(runner.state.exit_events_this_bar) == 1
    assert runner.state.exit_events_this_bar[0].exit_reason == REASON_EXIT_TP1


def test_close_only_profile_multi_tp_disables_tp2_if_tp1_bar_already_closed_through_it() -> None:
    bars = [
        Bar(datetime(2025, 1, 1), 100.0, 100.0, 100.0, 100.0, 100, 0),
        Bar(datetime(2025, 1, 2), 100.0, 103.0, 99.5, 102.5, 100, 1),
        Bar(datetime(2025, 1, 3), 102.5, 103.5, 102.0, 103.0, 100, 2),
    ]
    runner = Runner(
        _build_config(
            execution_profile_id=EXECUTION_PROFILE_CLOSE_ONLY_DETERMINISTIC,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="Multi-TP",
            tp1_r_multiple=1.0,
            tp1_close_pct=50.0,
            tp2_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.closed_this_bar_reason is None
    assert runner.state.total_exits == 1
    assert runner.state.position.qty == pytest.approx(0.5)
    assert runner.state.position.active_tp_price is None
    assert all(
        not working_exit.active or working_exit.target_price is None
        for working_exit in runner.state.position.working_exits
    )


def test_runner_l3_short_pulse_opens_short_at_bar_close() -> None:
    bars = _build_entry_bars()
    runner = Runner(_build_config(risk_per_short_pct=0.8))
    runner.signal_producer = _StaticSignalProducer(
        [RawSignal(False, True, "manual_short", direction=-1, line=9.0)]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars[:1])

    assert len(out) == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_price == pytest.approx(bars[0].close)
    assert runner.state.position.avg_entry_price == pytest.approx(bars[0].close)
    assert runner.state.position.qty == pytest.approx(2.0)
    assert runner.state.position.entry_bar == bars[0].bar_index
    assert runner.state.position.active_stop_price == pytest.approx(104.25)
    assert runner.state.opened_this_bar_reason == "manual_short"
    assert runner.state.total_entries == 1


def test_runner_allow_flip_controls_same_bar_reverse_entry() -> None:
    bars = _build_entry_bars()
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(False, True, "manual_short", direction=-1, line=9.0),
    ]

    no_flip = Runner(_build_config(use_sl=False, allow_flip=False, cooldown_bars=10))
    no_flip.signal_producer = _StaticSignalProducer(list(raw_outputs))
    no_flip.state.warmup_bars = 0
    no_flip.run(bars)

    assert no_flip.state.position is None
    assert no_flip.state.closed_this_bar_reason == "opp_signal"
    assert no_flip.state.total_entries == 1
    assert no_flip.state.total_exits == 1

    with_flip = Runner(_build_config(use_sl=False, allow_flip=True, cooldown_bars=10))
    with_flip.signal_producer = _StaticSignalProducer(list(raw_outputs))
    with_flip.state.warmup_bars = 0
    with_flip.run(bars)

    assert with_flip.state.position is not None
    assert with_flip.state.position.side == "short"
    assert with_flip.state.position.entry_bar == bars[1].bar_index
    assert with_flip.state.closed_this_bar_reason == "opp_signal"
    assert with_flip.state.total_entries == 2
    assert with_flip.state.total_exits == 1


def test_runner_allow_flip_false_does_not_defer_gate_blocked_reverse_signal() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 99.75, 100.0, 110, 1),
        Bar(datetime(2025, 5, 3), 100.0, 100.25, 99.5, 99.9, 120, 2),
    ]
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(False, True, "manual_short_blocked", direction=-1, line=9.0),
        RawSignal(False, False, "no_signal", direction=0, line=9.0),
    ]
    runner = Runner(_build_config(use_sl=False, allow_flip=False, use_ma_filter=True))
    runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    runner.state.warmup_bars = 0

    def _gate_stub(**_: object) -> dict[str, GateResult]:
        short_ok = runner.state.current_bar_index != 1
        return {
            "ma_filter": GateResult("ma_filter", long_ok=True, short_ok=short_ok),
        }

    runner._evaluate_entry_gates = _gate_stub  # type: ignore[method-assign]
    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1


def test_runner_allow_flip_false_revalidates_deferred_reverse_signal() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 99.75, 100.0, 110, 1),
        Bar(datetime(2025, 5, 3), 100.0, 100.25, 99.5, 99.9, 120, 2),
    ]
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(False, True, "manual_short_allowed_then_deferred", direction=-1, line=9.0),
        RawSignal(False, False, "no_signal", direction=0, line=9.0),
    ]
    runner = Runner(_build_config(use_sl=False, allow_flip=False, use_ma_filter=True))
    runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    runner.state.warmup_bars = 0

    def _gate_stub(**_: object) -> dict[str, GateResult]:
        # Bar 1 allows the short that triggers opp-signal close.
        # Bar 2 blocks shorts, so the deferred replay must be dropped.
        short_ok = runner.state.current_bar_index == 1
        return {
            "ma_filter": GateResult("ma_filter", long_ok=True, short_ok=short_ok),
        }

    runner._evaluate_entry_gates = _gate_stub  # type: ignore[method-assign]
    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1


def test_runner_disabled_htf_override_does_not_block_deferred_flip_replay() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 99.75, 100.0, 110, 1),
        Bar(datetime(2025, 5, 3), 100.0, 100.25, 99.5, 99.9, 120, 2),
    ]
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(False, True, "manual_short_allowed_then_deferred", direction=-1, line=9.0),
        RawSignal(False, False, "no_signal", direction=0, line=9.0),
    ]
    runner = Runner(_build_config(use_sl=False, allow_flip=False))
    runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    runner.state.warmup_bars = 0
    runner.set_gate_overrides(htf_trend_line_map={2: 1000.0})

    def _gate_stub(**_: object) -> dict[str, GateResult]:
        return {
            "ma_filter": GateResult("ma_filter", long_ok=True, short_ok=True),
        }

    runner._evaluate_entry_gates = _gate_stub  # type: ignore[method-assign]
    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 2
    assert runner.state.total_entries == 2
    assert runner.state.total_exits == 1


def test_runner_ma_mtf_requires_ready_htf_data_and_does_not_fallback_to_ltf() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.25, 100, 0),
        Bar(datetime(2025, 5, 2), 100.25, 100.75, 100.0, 100.5, 110, 1),
        Bar(datetime(2025, 5, 3), 100.5, 101.0, 100.25, 100.75, 120, 2),
    ]
    raw_outputs = [
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
        RawSignal(True, False, "manual_long", direction=1, line=10.0),
    ]
    runner = Runner(_build_config(use_sl=False, use_ma_filter=True, use_ma_mtf=True, ma_length=1))
    runner.signal_producer = _StaticSignalProducer(list(raw_outputs))
    runner.state.warmup_bars = 0
    htf_data = {bar.timestamp: None for bar in bars}

    runner.run(bars, htf_data=htf_data)

    assert runner.ma_filter_tracker.line is None
    assert runner.state.position is None
    assert runner.state.total_entries == 0


def test_runner_can_carry_reversal_to_next_bar_after_protective_exit() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 5, 2), 99.0, 99.2, 95.0, 96.0, 110, 1),
        Bar(datetime(2025, 5, 3), 96.0, 96.5, 95.5, 96.0, 120, 2),
    ]
    runner = Runner(
        _build_config(
            allow_flip=True,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tw_audit_semantics_mode="research",
            tw_reversal_reentry_mode="carry_to_next_bar_after_protective_exit",
            tw_reversal_reentry_delay_bars=1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, True, "manual_short_after_sl", direction=-1, line=9.0),
            RawSignal(False, False, "no_signal", direction=0, line=9.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.total_entries == 2
    assert runner.state.total_exits == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 2
    assert runner.state.position.entry_price == pytest.approx(96.0)


def test_runner_can_fill_next_bar_open_after_protective_exit_signal() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 5, 2), 99.0, 99.2, 95.0, 96.0, 110, 1),
        Bar(datetime(2025, 5, 3), 96.0, 96.5, 95.5, 96.0, 120, 2),
        Bar(datetime(2025, 5, 4), 90.0, 90.4, 89.5, 90.2, 130, 3),
    ]
    runner = Runner(
        _build_config(
            allow_flip=True,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tw_audit_semantics_mode="research",
            tw_reversal_reentry_mode="next_bar_open_after_protective_exit_signal",
            tw_reversal_reentry_delay_bars=1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "flat_after_sl", direction=0, line=9.0),
            RawSignal(False, True, "manual_short_after_sl", direction=-1, line=9.0),
            RawSignal(False, False, "no_signal", direction=0, line=9.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.total_entries == 2
    assert runner.state.total_exits == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 3
    assert runner.state.position.entry_price == pytest.approx(90.0)


def test_runner_can_fill_next_bar_close_after_protective_exit_signal() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 5, 2), 99.0, 99.2, 95.0, 96.0, 110, 1),
        Bar(datetime(2025, 5, 3), 96.0, 96.5, 95.5, 96.0, 120, 2),
        Bar(datetime(2025, 5, 4), 90.0, 90.4, 89.5, 90.2, 130, 3),
    ]
    runner = Runner(
        _build_config(
            allow_flip=True,
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tw_audit_semantics_mode="research",
            tw_reversal_reentry_mode="next_bar_close_after_protective_exit_signal",
            tw_reversal_reentry_delay_bars=1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "flat_after_sl", direction=0, line=9.0),
            RawSignal(False, True, "manual_short_after_sl", direction=-1, line=9.0),
            RawSignal(False, False, "no_signal", direction=0, line=9.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.total_entries == 2
    assert runner.state.total_exits == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 3
    assert runner.state.position.entry_price == pytest.approx(90.2)


def test_runner_can_apply_tradingview_style_margin_call_partial_liquidation() -> None:
    bars = [
        Bar(datetime(2025, 5, 1), 100.0, 100.0, 100.0, 100.0, 100, 0),
        Bar(datetime(2025, 5, 2), 100.0, 100.4, 99.8, 100.1, 110, 1),
    ]
    runner = Runner(
        _build_config(
            use_sl=False,
            risk_per_long_pct=1.0,
            risk_per_short_pct=1.0,
            fallback_size_pct=100.0,
            tw_audit_semantics_mode="research",
            tw_margin_call_mode="tradingview",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, True, "manual_short", direction=-1, line=9.0),
            RawSignal(False, False, "no_signal", direction=0, line=9.0),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1
    assert runner.state.closed_this_bar_reason == REASON_EXIT_MARGIN_CALL
    assert runner.state.last_exit_was_partial is True
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.qty == pytest.approx(9.6812749, rel=1e-5)


def test_runner_regime_lock_blocks_same_side_reentry_until_opposite_pulse() -> None:
    bars = _build_regime_lock_bars()
    runner = Runner(_build_config(regime_lock=True, sl_atr_mult=1.0))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
            RawSignal(True, False, "manual_long_reentry", direction=1, line=10.2),
            RawSignal(False, True, "manual_short_unlock", direction=-1, line=9.8),
        ]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars)

    assert len(out) == 4
    assert runner.state.total_entries == 2
    assert runner.state.total_exits == 1
    assert runner.state.position is not None
    assert runner.state.position.side == "short"
    assert runner.state.position.entry_bar == 3


def test_runner_l6a_same_direction_add_updates_basket_state() -> None:
    bars = _build_entry_bars()
    runner = Runner(
        _build_config(
            allow_flip=False,
            regime_lock=False,
            max_entries=2,
            cooldown_bars=0,
            instrument_qty_step=0.1,
            margin_long_pct=10.0,
            sl_atr_mult=1.0,
            risk_per_long_pct=0.5,
            max_leverage_cap=10.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(True, False, "manual_long_again", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars)

    assert len(out) == 2
    assert out[0].long is True
    assert out[1].long is True
    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.position.entry_bar == bars[0].bar_index
    assert runner.state.position.entry_price == pytest.approx(bars[0].close)
    assert runner.state.position.avg_entry_price == pytest.approx(
        ((bars[0].close * 5.0) + (bars[1].close * 6.6)) / 11.6
    )
    assert runner.state.position.qty == pytest.approx(11.6)
    assert runner.state.position.active_stop_price == pytest.approx(99.75)
    assert len(runner.state.position.entry_legs) == 2
    assert runner.state.position.lifecycle_id == 1
    assert runner.state.position.working_exit_reference_qty == pytest.approx(11.6)
    assert runner.state.position.working_exit_book_version == 2
    assert runner.state.position.initial_risk_per_unit == pytest.approx(1.0)
    assert runner.state.total_entries == 2
    assert runner.state.opened_this_bar_reason == "manual_long_again"


def test_runner_l6a_max_entries_blocks_third_same_direction_add() -> None:
    bars = _build_pyramid_bars()
    runner = Runner(
        _build_config(
            regime_lock=False,
            max_entries=2,
            cooldown_bars=0,
            instrument_qty_step=0.1,
            margin_long_pct=10.0,
            sl_atr_mult=1.0,
            risk_per_long_pct=0.5,
            max_leverage_cap=10.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long_1", direction=1, line=10.0),
            RawSignal(True, False, "manual_long_2", direction=1, line=10.1),
            RawSignal(True, False, "manual_long_3", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.total_entries == 2
    assert len(runner.state.position.entry_legs) == 2
    assert runner.state.position.qty == pytest.approx(11.6)
    assert runner.state.opened_this_bar_reason is None


def test_runner_l6a_cooldown_blocks_next_bar_add_but_later_bar_can_add() -> None:
    bars = _build_pyramid_bars()
    runner = Runner(
        _build_config(
            regime_lock=False,
            max_entries=3,
            cooldown_bars=2,
            instrument_qty_step=0.1,
            margin_long_pct=10.0,
            sl_atr_mult=1.0,
            risk_per_long_pct=0.5,
            max_leverage_cap=10.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long_1", direction=1, line=10.0),
            RawSignal(True, False, "manual_long_2", direction=1, line=10.1),
            RawSignal(True, False, "manual_long_3", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.total_entries == 2
    assert len(runner.state.position.entry_legs) == 2
    assert runner.state.position.entry_legs[0].entry_bar == 0
    assert runner.state.position.entry_legs[1].entry_bar == 2
    assert runner.state.last_entry_bar_index == 2


def test_runner_l6a_opp_signal_close_uses_avg_entry_price() -> None:
    bars = _build_pyramid_bars()
    runner = Runner(
        _build_config(
            regime_lock=False,
            allow_flip=False,
            max_entries=2,
            cooldown_bars=0,
            instrument_qty_step=0.1,
            margin_long_pct=10.0,
            sl_atr_mult=1.0,
            risk_per_long_pct=0.5,
            max_leverage_cap=10.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long_1", direction=1, line=10.0),
            RawSignal(True, False, "manual_long_2", direction=1, line=10.1),
            RawSignal(False, True, "manual_short", direction=-1, line=9.9),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    avg_entry = ((bars[0].close * 5.0) + (bars[1].close * 6.6)) / 11.6
    expected_pnl = (bars[2].close - avg_entry) * 11.6

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == "opp_signal"
    assert runner.state.last_realized_pnl == pytest.approx(expected_pnl)
    assert runner.state.realized_equity == pytest.approx(expected_pnl)


def test_runner_l3_supertrend_short_entry_ignores_later_long_flip() -> None:
    runner = Runner(_build_config(allow_flip=False, sl_atr_mult=1.0))
    out = runner.run(_build_transition_bars())

    assert len(out) == 8
    assert out[4].short is True
    assert out[6].long is True
    assert runner.state.position is None
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1
    assert runner.state.last_exit_price == pytest.approx(11.75)


def test_runner_l4_stop_gap_hit_closes_long_at_bar_open() -> None:
    bars = _build_stop_gap_long_bars()
    runner = Runner(_build_config(sl_atr_mult=1.0, risk_per_long_pct=0.1))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    out = runner.run(bars)

    assert len(out) == 2
    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_price == pytest.approx(99.0)
    assert runner.state.last_realized_pnl == pytest.approx(-1.25)
    assert runner.state.realized_equity == pytest.approx(-1.25)
    assert runner.state.total_entries == 1
    assert runner.state.total_exits == 1
    assert runner.state.block_new_entries_this_bar is True


def test_runner_l4_stop_touch_hit_closes_long_at_stop_price() -> None:
    bars = _build_stop_touch_long_bars()
    runner = Runner(_build_config(sl_atr_mult=1.0, risk_per_long_pct=0.1))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_price == pytest.approx(99.25)
    assert runner.state.last_realized_pnl == pytest.approx(-1.0)
    assert runner.state.realized_equity == pytest.approx(-1.0)
    assert runner.state.total_exits == 1


def test_runner_l4_stop_not_hit_keeps_position_open() -> None:
    bars = _build_stop_safe_bars()
    runner = Runner(_build_config(sl_atr_mult=1.0, risk_per_long_pct=0.1))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.side == "long"
    assert runner.state.position.active_stop_price == pytest.approx(99.25)
    assert runner.state.closed_this_bar_reason is None
    assert runner.state.last_exit_price is None
    assert runner.state.realized_equity == pytest.approx(0.0)
    assert runner.state.total_exits == 0


def test_runner_l4_parity_rows_are_readable_and_deterministic() -> None:
    bars = _build_stop_gap_long_bars()
    runner = Runner(_build_config(sl_atr_mult=1.0, risk_per_long_pct=0.1))
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    parity_rows = runner.run_l4_parity_rows(bars)

    assert parity_rows == [
        "00 | ts=2025-05-01T00:00:00 | c=100.2500 | st=10.0000 | d= 1 | L=1 | S=0 | pos=long  | ep=100.2500 | aep=100.2500 | eb=00 | q=1.0000 | ec=1 | lc=1 | bv=1 | sp=99.2500 | tp=na | xr=na | xb=na | xp=na | ps=0",
        "01 | ts=2025-05-02T00:00:00 | c=99.1000 | st=10.1000 | d= 1 | L=0 | S=0 | pos=flat  | ep=na | aep=na | eb=na | q=0.0000 | ec=0 | lc=0 | bv=0 | sp=na | tp=na | xr=sl_atr_hit | xb=01 | xp=99.0000 | ps=0",
    ]


def test_runner_smoke_dual_true_conflict_is_zeroed() -> None:
    class ConflictProducer:
        def calculate(self, bar: Bar) -> RawSignal:
            return RawSignal(True, True, "manual_conflict", direction=1, line=10.0)

    runner = Runner(_build_config())
    runner.signal_producer = ConflictProducer()

    out = runner.run(_build_transition_bars()[:1])

    assert len(out) == 1
    assert out[0].reason == REASON_SIGNAL_CONFLICT
    assert out[0].long is False
    assert out[0].short is False
    assert out[0].direction == 1
    assert out[0].line == pytest.approx(10.0)


# ============================================================================
# L5 Architecture Compliance Tests
# ============================================================================


def test_l11_tp_config_parent_child_contract() -> None:
    """resolve_config derives the L11 TP radio flags from tp_mode."""
    from mtc_v2.core.config import resolve_config

    # tp_mode=None → use_tp=False, use_tp_single_atr=False
    cfg_off = resolve_config(_build_config(tp_mode="None"))
    assert cfg_off["use_tp"] is False
    assert cfg_off["use_tp_single_atr"] is False

    # tp_mode=ATR → use_tp=True, use_tp_single_atr=True
    cfg_on = resolve_config(_build_config(tp_mode="ATR"))
    assert cfg_on["use_tp"] is True
    assert cfg_on["use_tp_single_atr"] is True

    cfg_pct = resolve_config(_build_config(tp_mode="Percent"))
    assert cfg_pct["use_tp"] is True
    assert cfg_pct["use_tp_single_pct"] is True

    cfg_r = resolve_config(_build_config(tp_mode="R"))
    assert cfg_r["use_tp"] is True
    assert cfg_r["use_tp_single_r"] is True

    cfg_multi = resolve_config(_build_config(tp_mode="Multi-TP"))
    assert cfg_multi["use_tp"] is True
    assert cfg_multi["use_tp_multi"] is True


def test_l5_tp_rounding_uses_half_up_not_adverse() -> None:
    """Architecture: TP prices use round_half_up_to_grid, not directional ceil/floor."""
    bars = [Bar(datetime(2025, 5, 1), 100.0, 100.5, 99.5, 100.0, 100, 0)]

    # Long: raw TP = 100.0 + 1.04*1.0 = 101.04
    # round_half_up(101.04, 0.1) → 101.0  (ceil would give 101.1)
    long_runner = Runner(_build_config(
        use_sl=False, tp_mode="ATR", tp_atr_mult=1.04,
        instrument_price_tick=0.1,
    ))
    long_runner.signal_producer = _StaticSignalProducer(
        [RawSignal(True, False, "manual_long", direction=1, line=10.0)]
    )
    long_runner.state.warmup_bars = 0
    long_runner.run(bars)
    assert long_runner.state.position is not None
    assert long_runner.state.position.active_tp_price == pytest.approx(101.0)

    # Short: raw TP = 100.0 - 1.04*1.0 = 98.96
    # round_half_up(98.96, 0.1) → 99.0  (floor would give 98.9)
    short_runner = Runner(_build_config(
        use_sl=False, tp_mode="ATR", tp_atr_mult=1.04,
        instrument_price_tick=0.1,
    ))
    short_runner.signal_producer = _StaticSignalProducer(
        [RawSignal(False, True, "manual_short", direction=-1, line=9.0)]
    )
    short_runner.state.warmup_bars = 0
    short_runner.run(bars)
    assert short_runner.state.position is not None
    assert short_runner.state.position.active_tp_price == pytest.approx(99.0)


def test_l5_ambiguity_python_uses_pessimistic_sl_with_flag() -> None:
    """Python resolves SL+TP same-bar ambiguity as pessimistic SL; flag is set."""
    bars = _build_tp_ambiguity_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=True,
            sl_atr_mult=1.0,
            tp_mode="ATR",
            tp_atr_mult=1.0,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "no_signal", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    # Python uses pessimistic SL resolution — exit reason is SL, flag is set
    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_ATR
    assert runner.state.last_exit_was_pessimistic is True
    # Pine would export PRICE_AMBIGUOUS (code=4); Python keeps SL — expected divergence


def test_l10_percent_sl_closes_at_percent_stop() -> None:
    bars = _build_percent_exit_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_PERCENT
    assert runner.state.last_exit_price == pytest.approx(99.0)
    assert runner.state.realized_equity == pytest.approx(-1.0)


def test_l11_percent_tp_closes_at_percent_target() -> None:
    bars = _build_percent_tp_bars()
    runner = Runner(
        _build_config(
            use_sl=False,
            tp_mode="Percent",
            tp_percent=2.0,
            fallback_size_pct=10.0,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_PERCENT
    assert runner.state.last_exit_price == pytest.approx(102.0)


def test_l11_r_multiple_tp_uses_frozen_initial_risk() -> None:
    bars = _build_percent_tp_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="R",
            tp_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP_R
    assert runner.state.last_exit_price == pytest.approx(102.0)


def test_l10_swing_atr_stop_uses_prior_closed_bars() -> None:
    bars = _build_swing_entry_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_swing_atr=True,
            sl_swing_basis="Wick",
            sl_swing_lookback=2,
            sl_swing_atr_len=1,
            sl_swing_atr_mult=0.5,
            risk_per_long_pct=0.3,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "seed_0", direction=1, line=10.0),
            RawSignal(False, False, "seed_1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long", direction=1, line=10.2),
            RawSignal(False, False, "hold", direction=1, line=10.3),
        ]
    )
    runner.state.warmup_bars = 2

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_SL_SWING_ATR
    assert runner.state.last_exit_price == pytest.approx(98.7)


def test_l7_break_even_promotes_stop_owner_and_hits_on_gap() -> None:
    bars = _build_break_even_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_break_even=True,
            be_trigger_r=1.0,
            be_buffer_r=0.1,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_BE
    assert runner.state.last_exit_price == pytest.approx(100.05)


def test_l7_break_even_tradingview_mode_uses_close_trigger() -> None:
    bars = _build_break_even_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_break_even=True,
            be_trigger_r=1.0,
            be_buffer_r=0.1,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
            tw_audit_semantics_mode="research",
            tw_be_semantics_mode="tradingview",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert runner.state.position.be_active is False
    assert runner.state.closed_this_bar_reason is None


def test_l7_break_even_next_bar_confirmed_delays_activation() -> None:
    bars = _build_break_even_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_break_even=True,
            be_trigger_r=1.0,
            be_buffer_r=0.1,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
            tw_audit_semantics_mode="research",
            tw_be_semantics_mode="next_bar_confirmed",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_BE


def test_l8_trailing_stop_promotes_owner_and_hits_on_later_bar() -> None:
    bars = _build_trailing_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_trailing=True,
            trail_atr_len=1,
            trail_start_r=1.0,
            trail_distance_atr_mult=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TRAIL
    assert runner.state.last_exit_price == pytest.approx(100.3)


def test_l8_trailing_tradingview_mode_uses_close_trigger_and_anchor() -> None:
    bars = _build_trailing_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_trailing=True,
            trail_atr_len=1,
            trail_start_r=1.0,
            trail_distance_atr_mult=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
            tw_audit_semantics_mode="research",
            tw_trailing_semantics_mode="tradingview",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TRAIL


def test_l8_trailing_next_bar_confirmed_delays_owner_update_until_following_bar() -> None:
    bars = _build_trailing_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            use_trailing=True,
            trail_atr_len=1,
            trail_start_r=1.0,
            trail_distance_atr_mult=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
            tw_audit_semantics_mode="research",
            tw_trailing_semantics_mode="next_bar_confirmed",
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
            RawSignal(False, False, "hold", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TRAIL


def test_l6b_l9_multi_tp_runs_partial_then_remainder_close_same_bar() -> None:
    bars = _build_percent_tp_bars()
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="Multi-TP",
            tp1_r_multiple=1.0,
            tp1_close_pct=50.0,
            tp2_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long", direction=1, line=10.0),
            RawSignal(False, False, "hold", direction=1, line=10.1),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is None
    assert runner.state.total_exits == 2
    assert runner.state.closed_this_bar_reason == REASON_EXIT_TP2
    assert runner.state.last_exit_qty == pytest.approx(0.5)
    assert runner.state.realized_equity == pytest.approx(1.5)
    assert len(runner.state.exit_events_this_bar) == 2
    assert runner.state.exit_events_this_bar[0].exit_reason == REASON_EXIT_TP1
    assert runner.state.exit_events_this_bar[0].was_partial is True
    assert runner.state.exit_events_this_bar[1].exit_reason == REASON_EXIT_TP2
    assert runner.state.exit_events_this_bar[1].was_partial is False


def test_l6b_add_rebuild_preserves_completed_tp1() -> None:
    bars = [
        Bar(datetime(2025, 11, 1), 100.0, 100.2, 99.8, 100.0, 100, 0),
        Bar(datetime(2025, 11, 2), 100.1, 101.2, 100.2, 100.8, 100, 1),
        Bar(datetime(2025, 11, 3), 100.8, 101.0, 100.4, 100.6, 100, 2),
    ]
    runner = Runner(
        _build_config(
            use_sl=True,
            use_sl_atr=False,
            use_sl_percent=True,
            sl_percent=1.0,
            tp_mode="Multi-TP",
            tp1_r_multiple=1.0,
            tp1_close_pct=50.0,
            tp2_r_multiple=2.0,
            risk_per_long_pct=0.1,
            max_leverage_cap=10.0,
            max_entries=2,
            instrument_price_tick=0.1,
            instrument_qty_step=0.1,
        )
    )
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(True, False, "manual_long_1", direction=1, line=10.0),
            RawSignal(False, False, "hold_after_tp1", direction=1, line=10.1),
            RawSignal(True, False, "manual_long_add", direction=1, line=10.2),
        ]
    )
    runner.state.warmup_bars = 0

    runner.run(bars)

    assert runner.state.position is not None
    assert "TP1" in runner.state.position.completed_exit_ids
    assert all(working_exit.exit_id != "TP1" for working_exit in runner.state.position.working_exits if working_exit.active)
    assert runner.state.position.working_exit_reference_qty > runner.state.position.qty
