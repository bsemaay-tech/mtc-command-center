from __future__ import annotations

import json
from pathlib import Path

from mtc_compatible_risk_adapter import RiskConfig, run_visual_debug_trades
from python_signal_model import SIGNAL_FIELDS, SignalConfig, compute_signals, load_ohlcv_csv, write_csv


def main() -> None:
    config_path = Path("config.example.json")
    if Path("config.json").exists():
        config_path = Path("config.json")
    cfg_raw = json.loads(config_path.read_text(encoding="utf-8"))
    rows = load_ohlcv_csv(cfg_raw["input_csv"])
    signal_config = SignalConfig(
        warmup_bars=int(cfg_raw.get("warmup_bars", 50)),
        vwap_guard_lookback=int(cfg_raw.get("vwap_guard_lookback", 8)),
        vwap_guard_ratio=float(cfg_raw.get("vwap_guard_ratio", 0.75)),
        slope_lookback=int(cfg_raw.get("slope_lookback", 12)),
        range_lookback=int(cfg_raw.get("range_lookback", 20)),
        breakout_lookback=int(cfg_raw.get("breakout_lookback", 10)),
        atr_lookback=int(cfg_raw.get("atr_lookback", 14)),
        volume_lookback=int(cfg_raw.get("volume_lookback", 20)),
        capitulation_volume_mult=float(cfg_raw.get("capitulation_volume_mult", 2.0)),
        capitulation_range_atr_mult=float(cfg_raw.get("capitulation_range_atr_mult", 1.5)),
        capitulation_vwap_distance_pct=float(cfg_raw.get("capitulation_vwap_distance_pct", 1.5)),
        compression_lookback=int(cfg_raw.get("compression_lookback", 20)),
        compression_width_pct=float(cfg_raw.get("compression_width_pct", 1.2)),
        enable_long=bool(cfg_raw.get("enable_long", True)),
        enable_short=bool(cfg_raw.get("enable_short", True)),
    )
    signals = compute_signals(rows, signal_config)
    risk_config = RiskConfig(
        enable_long=bool(cfg_raw.get("enable_long", True)),
        enable_short=bool(cfg_raw.get("enable_short", True)),
        fixed_qty=float(cfg_raw.get("fixed_qty", 1)),
        time_exit_bars=int(cfg_raw.get("time_exit_bars", 20)),
        cost_bps=float(cfg_raw.get("cost_bps", 0)),
    )
    trades, equity = run_visual_debug_trades(signals, risk_config)
    out_dir = Path(cfg_raw.get("output_dir", "outputs"))
    write_csv(out_dir / "signals_debug.csv", signals, SIGNAL_FIELDS)
    write_csv(out_dir / "trades_debug.csv", trades, ["entry_time", "exit_time", "side", "entry_price", "exit_price", "qty", "pnl_points", "exit_reason"])
    write_csv(out_dir / "equity_debug.csv", equity, ["timestamp", "position", "active_stop", "realized_points", "unrealized_points", "debug_total_points"])
    print(f"wrote {len(signals)} signal rows, {len(trades)} debug trades to {out_dir}")


if __name__ == "__main__":
    main()
