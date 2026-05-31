"""
Trade Microscope -- Per-bar exit trace for a specific trade.

PURPOSE: Diagnose exit timing divergence between Python and TradingView.
TARGET: TV Trade #232 (SHORT, entry ~Oct 10 22:30, exit TRAIL Jan 13 22:00)

This script:
  1. Runs the full backtest (Jul 2025 - Jan 2026, warmup_only parity mode)
  2. Finds the Python SHORT trade matching TV #232 entry time
  3. Re-runs just that trade's bar range with per-bar instrumentation
  4. Exports debug/debug_exit_trace_trade232.csv with:
     - OHLC + HA OHLC
     - All exit levels: sl_price, tp1_price, tp2_price, be_price, trail_stop
     - All hit flags: sl_hit, tp1_hit, tp2_hit, be_hit, trail_hit
     - Conflict resolution: high_first, tp_first_if_conflict
     - Chosen exit + fill price
     - Position state: qty, be_triggered, trailing_active, highest, lowest

Usage:
    cd C:\\LAB\\tradingview-lab\\mtc_backtest
    python -m scripts.trade_microscope
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

import pandas as pd
import numpy as np

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config.defaults import MTCConfig
from src.engine.mtc_runner import MTCRunner
from src.engine.mtc_state import Direction, ExitReason


# -- Config ------------------------------------------------------------------
CASE_FILE = Path(__file__).resolve().parent.parent / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
TV_TRADE_ENTRY_TIME = "2025-10-10 22:30"   # TV #232 entry
TV_TRADE_EXIT_TIME = "2026-01-13 22:00"    # TV #232 exit (TRAIL)
TV_TRADE_DIRECTION = "short"
TV_TRADE_ENTRY_PRICE = 111242.6
OUTPUT_CSV = Path(__file__).resolve().parent.parent / "debug" / "debug_exit_trace_trade232.csv"


def load_case(case_path: Path) -> dict:
    """Load case JSON."""
    with open(case_path) as f:
        return json.load(f)


def load_dataset(case: dict) -> pd.DataFrame:
    """Load parquet dataset."""
    data_dir = Path(__file__).resolve().parent.parent / "data"
    dataset_path = data_dir / case["dataset"]
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    df = pd.read_parquet(dataset_path)
    print(f"Loaded {len(df)} bars from {dataset_path.name}")
    return df


def build_config(case: dict) -> MTCConfig:
    """Build MTCConfig from case JSON."""
    return MTCConfig.model_validate(case["config"])


def find_matching_trade(runner: MTCRunner, target_entry_ts: str, target_direction: str):
    """Find the Python trade closest to the TV entry timestamp & direction."""
    target_ts = pd.Timestamp(target_entry_ts, tz="UTC")
    target_dir = Direction.LONG if target_direction == "long" else Direction.SHORT

    best_trade = None
    best_delta = pd.Timedelta(days=9999)

    for t in runner.state.trades:
        if t.direction != target_dir:
            continue
        if t.entry_time is None:
            continue
        t_ts = pd.Timestamp(t.entry_time)
        t_ts = t_ts.tz_localize("UTC") if t_ts.tzinfo is None else t_ts.tz_convert("UTC")
        delta = abs(t_ts - target_ts)
        if delta < best_delta:
            best_delta = delta
            best_trade = t

    return best_trade, best_delta


def run_microscope():
    """Run the trade microscope for TV #232."""
    print("=" * 70)
    print("TRADE MICROSCOPE -- TV Trade #232 (SHORT Oct 10 -> Jan 13)")
    print("=" * 70)

    # Load case
    case = load_case(CASE_FILE)
    df = load_dataset(case)
    config = build_config(case)

    # Parse eval window
    eval_start = datetime.fromisoformat(case["start_date"])
    eval_end = datetime.fromisoformat(case["end_date"])
    warmup_bars = case.get("warmup_bars", 200)

    print(f"\nConfig: signal_mode={config.signal_mode}, parity.fill_contract={config.parity.fill_contract}")
    print(f"Eval window: {eval_start} -> {eval_end}")
    print(f"Warmup bars: {warmup_bars}, Preroll days: {config.parity.preroll_days}")
    print(f"Preroll mode: {config.parity.preroll_mode}")

    # Run full backtest
    print("\n-- Phase 1: Running full backtest --")
    runner = MTCRunner(config)
    results = runner.run(
        df,
        warmup_bars=warmup_bars,
        eval_start=eval_start,
        eval_end=eval_end,
    )

    all_trades = results.get("trades_all", results.get("trades", []))
    eval_trades = results["trades"]
    print(f"Total trades (all): {len(all_trades)}")
    print(f"Eval trades: {len(eval_trades)}")

    # Find matching Python trade
    print(f"\n-- Phase 2: Finding Python match for TV #232 --")
    print(f"Target: {TV_TRADE_DIRECTION.upper()} entry @ {TV_TRADE_ENTRY_TIME}")

    best_trade, best_delta = find_matching_trade(runner, TV_TRADE_ENTRY_TIME, TV_TRADE_DIRECTION)

    if best_trade is None:
        print("ERROR: No matching SHORT trade found!")
        # List nearby trades
        print("\nNearby SHORT trades around Oct 2025:")
        for t in all_trades:
            if t.direction == Direction.SHORT and t.entry_time is not None:
                ts = pd.Timestamp(t.entry_time)
                if pd.Timestamp("2025-10-01", tz="UTC") <= ts <= pd.Timestamp("2025-11-01", tz="UTC"):
                    print(f"  #{t.trade_id}: entry={t.entry_time} @ {t.entry_price:.1f}, "
                          f"exit={t.exit_time} reason={t.exit_reason.value}")
        return

    print(f"MATCH: Trade #{best_trade.trade_id}")
    print(f"  Entry: {best_trade.entry_time} @ {best_trade.entry_price:.1f}")
    print(f"  Exit:  {best_trade.exit_time} @ {best_trade.exit_price:.1f} ({best_trade.exit_reason.value})")
    print(f"  Bars held: {best_trade.bars_held}")
    print(f"  PnL: {best_trade.pnl:.2f} ({best_trade.pnl_pct:.2f}%)")
    print(f"  Delta from TV entry: {best_delta}")

    # Phase 3: Re-run with per-bar instrumentation
    print(f"\n-- Phase 3: Per-bar exit trace (bars {best_trade.entry_bar} -> {best_trade.exit_bar}) --")

    trace_rows = run_instrumented_trace(
        df, config, warmup_bars, eval_start, eval_end,
        best_trade.entry_bar, best_trade.exit_bar + 50  # +50 bars buffer to see what happens after
    )

    # Export
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    trace_df = pd.DataFrame(trace_rows)
    trace_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nExported {len(trace_rows)} rows -> {OUTPUT_CSV}")

    # Summary stats
    if len(trace_rows) > 0:
        print(f"\n-- Phase 4: Trace Summary --")
        in_pos_rows = [r for r in trace_rows if r.get("in_position")]
        sl_hits = sum(1 for r in trace_rows if r.get("sl_hit"))
        tp1_hits = sum(1 for r in trace_rows if r.get("tp1_hit"))
        tp2_hits = sum(1 for r in trace_rows if r.get("tp2_hit"))
        trail_hits = sum(1 for r in trace_rows if r.get("trail_hit"))
        be_triggers = sum(1 for r in trace_rows if r.get("be_newly_triggered"))
        trail_activations = sum(1 for r in trace_rows if r.get("trail_newly_activated"))

        print(f"  Bars in position: {len(in_pos_rows)}")
        print(f"  SL hit bars: {sl_hits}")
        print(f"  TP1 hit bars: {tp1_hits}")
        print(f"  TP2/TP hit bars: {tp2_hits}")
        print(f"  Trail hit bars: {trail_hits}")
        print(f"  BE triggered: {be_triggers}")
        print(f"  Trail activated: {trail_activations}")

        # Find first SL hit
        for r in trace_rows:
            if r.get("sl_hit") and r.get("in_position"):
                print(f"\n  FIRST SL HIT: bar {r['bar_index']} @ {r['timestamp']}")
                print(f"    SL price: {r['sl_price']}, Bar high: {r['high']}, Bar low: {r['low']}")
                break

        # Find first trail hit
        for r in trace_rows:
            if r.get("trail_hit") and r.get("in_position"):
                print(f"\n  FIRST TRAIL HIT: bar {r['bar_index']} @ {r['timestamp']}")
                print(f"    Trail stop: {r['trail_stop']}, Bar high: {r['high']}, Close: {r['close']}")
                break

    # TV comparison
    print(f"\n-- TV vs Python Comparison --")
    print(f"  TV #232:  entry={TV_TRADE_ENTRY_TIME} @ {TV_TRADE_ENTRY_PRICE:.1f}")
    print(f"            exit={TV_TRADE_EXIT_TIME} (TRAIL)")
    print(f"  PY #{best_trade.trade_id}: entry={best_trade.entry_time} @ {best_trade.entry_price:.1f}")
    print(f"            exit={best_trade.exit_time} ({best_trade.exit_reason.value})")

    if best_trade.exit_time:
        py_exit_ts = pd.Timestamp(best_trade.exit_time)
        tv_exit_ts = pd.Timestamp(TV_TRADE_EXIT_TIME, tz="UTC")
        py_exit_ts = py_exit_ts.tz_localize("UTC") if py_exit_ts.tzinfo is None else py_exit_ts.tz_convert("UTC")
        exit_delta = py_exit_ts - tv_exit_ts
        print(f"  Exit time delta: {exit_delta}")
        if py_exit_ts < tv_exit_ts:
            print(f"  WARNING:  Python exits EARLIER by {abs(exit_delta)}")
        elif py_exit_ts > tv_exit_ts:
            print(f"  WARNING:  Python exits LATER by {abs(exit_delta)}")
        else:
            print(f"  OK: Exit times match!")


def run_instrumented_trace(
    df: pd.DataFrame,
    config: MTCConfig,
    warmup_bars: int,
    eval_start: datetime,
    eval_end: datetime,
    trace_start_bar: int,
    trace_end_bar: int,
) -> List[Dict]:
    """
    Re-run backtest with per-bar instrumentation for the trace window.

    Instead of modifying MTCRunner, we replicate the critical exit logic
    and capture intermediate state at each bar.
    """
    from src.engine.indicators import atr as calc_atr
    from src.modules.signals.supertrend import SupertrendSignal
    from src.modules.risk.sl_calculator import SLCalculator
    from src.modules.risk.tp_calculator import TPCalculator, BreakEvenCalculator, TrailingStopCalculator
    from src.modules.risk.position_sizer import PositionSizer

    # Create a runner and run the full backtest to get correct state
    runner = MTCRunner(config)
    results = runner.run(
        df, warmup_bars=warmup_bars,
        eval_start=eval_start, eval_end=eval_end,
    )

    # Now we need per-bar exit details. The cleanest approach:
    # Re-run the backtest but this time capture exit trace data at each bar.
    # We'll use a monkey-patched version of _process_exits.

    trace_rows: List[Dict] = []
    mintick = 0.1

    # Create a fresh runner for the instrumented run
    runner2 = MTCRunner(config)

    # Store original _process_exits
    original_process_exits = runner2._process_exits

    def instrumented_process_exits(bar, df_arg, bar_idx, long_signal, short_signal,
                                     long_raw=False, short_raw=False):
        """Wrapper that captures exit trace data before delegating."""
        pos = runner2.state.position
        if pos is None:
            return original_process_exits(bar, df_arg, bar_idx, long_signal, short_signal,
                                          long_raw=long_raw, short_raw=short_raw)

        is_long = pos.is_long()
        side = "long" if is_long else "short"
        high = bar['high']
        low = bar['low']
        close = bar['close']

        # Capture pre-exit state
        row = {
            "bar_index": bar_idx,
            "timestamp": runner2.state.current_time,
            "open": bar['open'],
            "high": high,
            "low": low,
            "close": close,
            "in_position": True,
            "direction": pos.direction.value,
            "entry_price": pos.entry_price,
            "entry_bar": pos.entry_bar,
            "quantity": pos.quantity,
            "initial_quantity": pos.initial_quantity,

            # Exit levels
            "sl_price": pos.sl_price,
            "sl_base_price": pos.sl_base_price,
            "tp_price": pos.tp_price,
            "tp1_price": pos.tp1_price,
            "tp2_price": pos.tp2_price,
            "tp1_filled": pos.tp1_filled,

            # BE state
            "be_triggered": pos.be_triggered,
            "be_price": pos.sl_price if pos.be_triggered else None,

            # Trailing state
            "trailing_active": pos.trailing_active,
            "trail_stop": pos.trailing_stop,
            "highest_price": pos.highest_price,
            "lowest_price": pos.lowest_price,

            # R-distance
            "r_distance": pos.r_distance,
        }

        # Compute hit flags (BEFORE any exit processing)
        # SL hit
        if pos.sl_price and config.stop_loss.enabled:
            if is_long:
                row["sl_hit"] = runner2._long_stop_hit(low, close, pos.sl_price)
            else:
                row["sl_hit"] = runner2._short_stop_hit(high, close, pos.sl_price)
        else:
            row["sl_hit"] = False

        # TP1 hit
        if config.multi_tp.enabled and not pos.tp1_filled and pos.tp1_price:
            if is_long:
                row["tp1_hit"] = runner2._long_tp_hit(high, close, pos.tp1_price)
            else:
                row["tp1_hit"] = runner2._short_tp_hit(low, close, pos.tp1_price)
        else:
            row["tp1_hit"] = False

        # TP2/TP hit
        tp_check_price = pos.tp2_price if pos.tp1_filled else pos.tp_price
        if tp_check_price and config.take_profit.enabled:
            if is_long:
                row["tp2_hit"] = runner2._long_tp_hit(high, close, tp_check_price)
            else:
                row["tp2_hit"] = runner2._short_tp_hit(low, close, tp_check_price)
        else:
            row["tp2_hit"] = False

        # Trail hit
        if pos.trailing_active and pos.trailing_stop:
            if is_long:
                row["trail_hit"] = runner2._long_stop_hit(low, close, pos.trailing_stop)
            else:
                row["trail_hit"] = runner2._short_stop_hit(high, close, pos.trailing_stop)
        else:
            row["trail_hit"] = False

        # Conflict resolution
        high_first = runner2._tv_high_first(bar)
        tp_first_if_conflict = (is_long and high_first) or ((not is_long) and (not high_first))
        row["high_first"] = high_first
        row["tp_first_if_conflict"] = tp_first_if_conflict
        row["sl_deferred"] = row["sl_hit"] and row.get("tp1_hit", False) and tp_first_if_conflict

        # BE trigger check (would it trigger this bar?)
        be_would_trigger = False
        if not pos.be_triggered and runner2.be_calc.enabled and not pos.trailing_active:
            check_price = high if is_long else low
            be_would_trigger = runner2.be_calc.should_trigger(
                pos.entry_price, pos.sl_base_price or pos.sl_price,
                check_price, side
            )
        row["be_would_trigger"] = be_would_trigger

        # Trail activation check (would it activate this bar?)
        trail_would_activate = False
        if runner2.trail_calc.enabled and not pos.trailing_active:
            check_price = high if is_long else low
            trail_would_activate = runner2.trail_calc.should_activate(
                pos.entry_price, pos.sl_base_price or pos.sl_price,
                check_price, side
            )
        row["trail_would_activate"] = trail_would_activate

        # Hypothetical trail stop if trailing were active
        if not pos.trailing_active and pos.sl_base_price:
            hyp_trail = runner2.trail_calc.calculate_trailing_stop(
                pos.entry_price, pos.sl_base_price,
                pos.highest_price, pos.lowest_price, side
            )
            row["hypothetical_trail_stop"] = hyp_trail
        else:
            row["hypothetical_trail_stop"] = None

        # Unrealized PnL
        row["unrealized_pnl"] = pos.unrealized_pnl(close)
        if pos.r_distance > 0:
            row["unrealized_r"] = pos.unrealized_pnl_r(close)
        else:
            row["unrealized_r"] = 0.0

        # Distance from extremes
        if is_long:
            row["dist_to_sl_pct"] = ((close - pos.sl_price) / close * 100) if pos.sl_price else None
        else:
            row["dist_to_sl_pct"] = ((pos.sl_price - close) / close * 100) if pos.sl_price else None

        # Now run the actual exit processing
        exit_result = original_process_exits(bar, df_arg, bar_idx, long_signal, short_signal,
                                              long_raw=long_raw, short_raw=short_raw)

        # Post-exit state
        row["exit_result"] = exit_result
        row["position_closed"] = (exit_result is not None and not runner2.state.in_position)
        row["partial_close"] = (exit_result is not None and runner2.state.in_position)

        # Capture post-exit state
        pos_after = runner2.state.position
        if pos_after:
            row["be_triggered_after"] = pos_after.be_triggered
            row["trailing_active_after"] = pos_after.trailing_active
            row["trail_stop_after"] = pos_after.trailing_stop
            row["sl_price_after"] = pos_after.sl_price
            row["qty_after"] = pos_after.quantity
            row["highest_after"] = pos_after.highest_price
            row["lowest_after"] = pos_after.lowest_price
            row["be_newly_triggered"] = (not row["be_triggered"]) and pos_after.be_triggered
            row["trail_newly_activated"] = (not row["trailing_active"]) and pos_after.trailing_active
        else:
            row["be_triggered_after"] = None
            row["trailing_active_after"] = None
            row["trail_stop_after"] = None
            row["sl_price_after"] = None
            row["qty_after"] = 0.0
            row["highest_after"] = None
            row["lowest_after"] = None
            row["be_newly_triggered"] = False
            row["trail_newly_activated"] = False

        # Only record rows in the trace window
        if trace_start_bar <= bar_idx <= trace_end_bar:
            trace_rows.append(row)

        return exit_result

    # Monkey-patch
    runner2._process_exits = instrumented_process_exits

    # Also capture bars where we're NOT in position (for context)
    # We'll add a post-loop hook via the signal recording

    # Run the instrumented backtest
    print(f"Running instrumented backtest (tracing bars {trace_start_bar} - {trace_end_bar})...")
    results2 = runner2.run(
        df, warmup_bars=warmup_bars,
        eval_start=eval_start, eval_end=eval_end,
    )

    # Add flat bars in trace window that weren't captured
    captured_bars = {r["bar_index"] for r in trace_rows}
    _ts_series = pd.to_datetime(df['timestamp'], utc=True) if 'timestamp' in df.columns else None
    for i in range(max(trace_start_bar, warmup_bars), min(trace_end_bar + 1, len(df))):
        if i not in captured_bars:
            trace_rows.append({
                "bar_index": i,
                "timestamp": _ts_series.iloc[i] if _ts_series is not None else None,
                "open": df['open'].iloc[i],
                "high": df['high'].iloc[i],
                "low": df['low'].iloc[i],
                "close": df['close'].iloc[i],
                "in_position": False,
                "direction": "FLAT",
                "exit_result": None,
            })

    # Sort by bar_index
    trace_rows.sort(key=lambda r: r["bar_index"])

    return trace_rows


if __name__ == "__main__":
    run_microscope()
