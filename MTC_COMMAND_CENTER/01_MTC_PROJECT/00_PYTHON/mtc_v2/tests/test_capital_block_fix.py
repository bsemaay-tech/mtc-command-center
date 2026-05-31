"""
Tests for _entry_blocked_by_capital fix.

Root cause: _entry_blocked_by_capital used self.state.equity (post-close realized
equity) as the threshold, but qty is sized from sizing_equity_snapshot (pre-close
frozen equity) and is already capped by max_leverage_cap via PositionSizer.
This caused false capital blocks on:
  - Flip entries where the closing loss reduced equity below the margin required
    by qty that was sized from the pre-loss sizing_equity_snapshot (AUTO_010/014)
  - Fresh entries where risk-based qty × price > equity, but max_leverage_cap > 1.0
    allows the position notional (AUTO_015)

Fix: pass sizing_equity_snapshot to _entry_blocked_by_capital and use
     sizing_equity * max_leverage_cap as the threshold.
"""
from __future__ import annotations

from datetime import datetime

from mtc_v2.core.indicators import IndicatorSnapshot, SupertrendIndicatorSnapshot
from mtc_v2.core.runner import Runner
from mtc_v2.core.types import Bar, RawSignal


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class _StaticSignalProducer:
    """Injects pre-defined RawSignals, bypassing the real Supertrend calculation."""

    def __init__(self, outputs: list[RawSignal]) -> None:
        self._outputs = outputs
        self._index = 0
        self.warmup_bars_required = 0
        self._snapshot = IndicatorSnapshot(
            supertrend=SupertrendIndicatorSnapshot(valid_bar=True, warmup_ready=True)
        )

    def calculate(self, bar: Bar) -> RawSignal:
        raw = self._outputs[self._index]
        self._index += 1
        self._snapshot = IndicatorSnapshot(
            supertrend=SupertrendIndicatorSnapshot(
                line=raw.line,
                direction=raw.direction,
                valid_bar=True,
                warmup_ready=True,
            )
        )
        return raw

    def indicator_snapshot(self) -> IndicatorSnapshot:
        return self._snapshot


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
        "instrument_price_tick": 0.01,
        "instrument_qty_step": 0.001,
        "instrument_min_qty": 0.0,
        "instrument_min_notional": 0.0,
        "instrument_contract_multiplier": 1.0,
        "initial_capital": 100.0,
        "margin_long_pct": 100.0,
        "margin_short_pct": 100.0,
        "risk_per_long_pct": 1.0,
        "risk_per_short_pct": 1.0,
        "fallback_size_pct": 100.0,   # default: fallback = 1× equity / price
        "max_leverage_cap": 1.0,
        "equity_source": "Realized",
        "use_notional_assert": False,
        # Disable SL so close happens via opp_signal only (no price_exit_blocks_entry)
        "use_sl": False,
        "use_sl_atr": False,
        "sl_atr_len": 1,
        "sl_atr_mult": 4.0,
        "tp_mode": "None",
        "tp_atr_len": 1,
        "tp_atr_mult": 4.0,
    }
    config.update(overrides)
    return config


# ---------------------------------------------------------------------------
# Scenario 1 — AUTO_010/014 pattern: flip SHORT blocked after LONG closing loss
#
# Mechanics (use_sl=False → fallback qty; max_leverage_cap=1.0):
#   Bar 0: no signal  (flat warmup)
#   Bar 1: LONG signal → entry at close=10.0
#           sizing_equity = 100.0, fallback_size_pct=100 → raw_qty = 10.0
#           leverage_cap_qty = 100.0 / 10.0 = 10.0  → qty = 10.0
#   Bar 2: SHORT signal → LONG closes via opp_signal at close=9.9 (a loss)
#           Loss = (9.9 - 10.0) × 10.0 = -1.0  → post_close_equity = 99.0
#           SHORT sizing: sizing_equity_snapshot = 100.0 (pre-close, frozen)
#           fallback_qty = 100.0 / 9.9 = 10.101  → floor = 10.101 (qty_step=0.001)
#           leverage_cap_qty = 100.0 / 9.9 = 10.101 → qty = 10.101
#           required_margin = 9.9 × 10.101 × 1.0 × (100/100) ≈ 99.999
#
#   BUG:  state.equity = 99.0 < required_margin ≈ 99.999 → BLOCKED
#   FIX:  threshold = sizing_equity × max_leverage_cap = 100.0 × 1.0 = 100.0
#         100.0 < 99.999 → False → NOT blocked ✓
# ---------------------------------------------------------------------------

def _make_flip_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 1, 1), 10.0, 10.0, 10.0, 10.0, 100, 0),  # warmup
        Bar(datetime(2025, 1, 2), 10.0, 10.0, 10.0, 10.0, 100, 1),  # LONG entry
        Bar(datetime(2025, 1, 3),  9.9,  9.9,  9.9,  9.9, 100, 2),  # flip bar (loss)
        Bar(datetime(2025, 1, 4),  9.9,  9.9,  9.9,  9.9, 100, 3),  # hold short
    ]


def test_flip_short_not_blocked_after_long_closes_at_loss():
    """
    After a LONG closes at a loss on bar 2, the SHORT flip on the same bar
    must NOT be blocked by the capital check.

    Before fix: _entry_blocked_by_capital uses self.state.equity (= 99.0 post-loss),
                which is < required_margin ≈ 99.999 (sized from pre-loss equity=100).
    After fix:  threshold = sizing_equity_snapshot × max_leverage_cap = 100 × 1.0 = 100.0,
                which is ≥ required_margin ≈ 99.999 → entry allowed.
    """
    config = _build_config(
        initial_capital=100.0,
        fallback_size_pct=100.0,  # fallback qty = equity / price → hits leverage cap
        max_leverage_cap=1.0,
    )
    runner = Runner(config)
    runner.state.warmup_bars = 0
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "no_signal", direction=0, line=10.0),
            RawSignal(True,  False, "long",       direction=1, line=10.0),
            RawSignal(False, True,  "short_flip", direction=-1, line=9.9),
            RawSignal(False, False, "hold",       direction=-1, line=9.9),
        ]
    )

    runner.run(_make_flip_bars())

    # Before fix: total_entries=1 (SHORT flip blocked).
    # After fix:  total_entries=2 (LONG + SHORT flip).
    assert runner.state.total_entries >= 2, (
        f"SHORT flip was falsely blocked by capital check; "
        f"total_entries={runner.state.total_entries} (expected 2)"
    )
    assert runner.state.position is not None
    assert runner.state.position.side == "short", (
        f"Expected SHORT after flip; got side={runner.state.position.side}"
    )


# ---------------------------------------------------------------------------
# Scenario 2 — AUTO_015 pattern: fresh SHORT blocked with leverage_cap > 1
#
# Mechanics (use_sl=False, max_leverage_cap=2.0, fallback_size_pct=200):
#   Bar 0: no signal
#   Bar 1: SHORT signal → fresh entry at close=10.0 (no prior position)
#           sizing_equity = 100.0
#           fallback_qty = 200/100 × 100/10 = 20.0
#           leverage_cap_qty = (100 × 2.0) / 10.0 = 20.0 → qty = 20.0
#           required_margin = 10.0 × 20.0 × 1.0 × (100/100) = 200.0
#
#   BUG:  state.equity = 100.0 < required_margin = 200.0 → BLOCKED
#   FIX:  threshold = sizing_equity × max_leverage_cap = 100.0 × 2.0 = 200.0
#         200.0 < 200.0 → False → NOT blocked ✓
# ---------------------------------------------------------------------------

def _make_short_bars() -> list[Bar]:
    return [
        Bar(datetime(2025, 2, 1), 10.0, 10.0, 10.0, 10.0, 100, 0),  # warmup
        Bar(datetime(2025, 2, 2), 10.0, 10.0, 10.0, 10.0, 100, 1),  # SHORT entry
        Bar(datetime(2025, 2, 3),  9.9,  9.9,  9.9,  9.9, 100, 2),  # hold
    ]


def test_fresh_short_not_blocked_when_leverage_cap_allows_it():
    """
    With max_leverage_cap=2.0, a fresh SHORT entry whose notional (2×equity) exceeds
    the current equity (1×equity) must NOT be blocked — the leverage cap explicitly
    permits this 2× notional.

    Before fix: threshold = self.state.equity = 100.0 < required_margin = 200.0 → BLOCKED.
    After fix:  threshold = sizing_equity × max_leverage_cap = 100.0 × 2.0 = 200.0;
                200.0 < 200.0 is False → NOT blocked.
    """
    config = _build_config(
        initial_capital=100.0,
        fallback_size_pct=200.0,   # fallback qty = 2× equity/price → hits leverage_cap=2×
        max_leverage_cap=2.0,
    )
    runner = Runner(config)
    runner.state.warmup_bars = 0
    runner.signal_producer = _StaticSignalProducer(
        [
            RawSignal(False, False, "no_signal", direction=0, line=10.0),
            RawSignal(False, True,  "short",     direction=-1, line=10.0),
            RawSignal(False, False, "hold",      direction=-1, line=9.9),
        ]
    )

    runner.run(_make_short_bars())

    # Before fix: total_entries=0 (SHORT blocked because 100 < 200).
    # After fix:  total_entries=1 (entry allowed because 200 ≥ 200).
    assert runner.state.total_entries >= 1, (
        f"SHORT entry was falsely blocked by capital check with max_leverage_cap=2×; "
        f"total_entries={runner.state.total_entries} (expected 1)"
    )
    assert runner.state.position is not None
    assert runner.state.position.side == "short", (
        f"Expected SHORT position; got position={runner.state.position}"
    )
    # Verify qty is at the leverage cap (2× equity / price = 20 units)
    expected_qty = 20.0
    assert abs(runner.state.position.qty - expected_qty) < 0.01, (
        f"Expected qty≈{expected_qty}; got qty={runner.state.position.qty}"
    )
