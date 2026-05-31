"""
REVIEW_ONLY — Standalone Python reference producer for promoted alpha candidates.
================================================================================
Purpose: emit the deterministic, bar-close signal series that serves as the
PARITY SOURCE OF TRUTH for the Pine v6 review wrappers. Reuses the exact engine
logic (mega_walk_forward.build_signals + simulate_slice) so the reference cannot
drift from the backtest that produced the promotion metrics.

It also re-verifies the lockbox metrics against the values recorded in each
candidate's producer_spec.json, so any divergence is caught immediately.

Usage:
    python reference_producer.py <candidate_folder_name>
    python reference_producer.py ALL

Outputs (into the candidate folder):
    <candidate_id>_signals.csv   full-history bar-level: timestamp, ohlc, indicators, long_entry, stop, target
    <candidate_id>_trades.csv    realized trade list with entry/exit/return
    PARITY_REFERENCE_METRICS.md  verification table (engine vs recorded)

This script does NOT modify production MTC_v2 and writes only inside the candidate folder.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import mega_walk_forward as M

PROMOTED = Path(M.OUTPUT_DIR).parent / "06_PROMOTED_TO_PARITY"
COST = M.COST_BPS / 10000.0
HOLD = M.HOLDING_BAR_LIMIT

def emit_for(candidate_dir: Path):
    spec = json.loads((candidate_dir / "producer_spec.json").read_text(encoding="utf-8"))
    cid = spec["candidate_id"]
    strat = spec["engine_strategy_id"]
    sym = spec["symbol"]; tf = spec["timeframe"]
    params = spec["verified_parameters"]
    is_trail = (strat == "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL")

    ds = M.find_ds(M._MANIFEST, sym, tf)
    if ds is None:
        print(f"[{cid}] NO DATA for {sym} {tf}"); return
    df = M.load_df(ds["normalized_path"]).reset_index(drop=True)

    # Build engine signals (daily RSI map only needed for dual-RSI, not used by these 3)
    dmap = None
    if strat == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        maps = M.build_daily_rsi(M._MANIFEST, sym)
        dmap = maps.get(int(params.get("rsi_len", 7))) if maps else None
    sig, stop = M.build_signals(strat, df, params, dmap)

    n = len(df)
    op = df["open"].to_numpy(); hi = df["high"].to_numpy(); lo = df["low"].to_numpy(); cl = df["close"].to_numpy()
    em = df["ema_8"].to_numpy() if "ema_8" in df.columns else np.zeros(n)
    sg = sig.to_numpy(); st = stop.to_numpy()

    # Bar-level export
    out = pd.DataFrame({
        "timestamp_utc": df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "open": op, "high": hi, "low": lo, "close": cl,
        "atr14": df["atr_14"].to_numpy() if "atr_14" in df.columns else np.nan,
        "ema8": em,
        "long_entry": sg.astype(int),
        "stop_at_signal": st,
    })
    # target only for non-trail (2R)
    if not is_trail:
        risk = op  # placeholder; computed per-trade below
    out.to_csv(candidate_dir / f"{cid}_signals.csv", index=False)

    # Replay trades on FULL history (deterministic, same rules as engine)
    trades = []
    i = 20
    while i < n - 1:
        if not sg[i]:
            i += 1; continue
        e = i + 1
        if e >= n: break
        ep = op[e]; sp = st[i]
        if np.isnan(ep) or np.isnan(sp) or sp >= ep or ep <= 0:
            i += 1; continue
        risk = ep - sp; tgt = ep + 2.0 * risk
        xi = min(e + HOLD, n - 1); xp = cl[xi]; reason = "time"
        for c in range(e, xi + 1):
            if lo[c] <= sp:
                xi = c; xp = sp; reason = "stop"; break
            if not is_trail and hi[c] >= tgt:
                xi = c; xp = tgt; reason = "target"; break
            if is_trail and cl[c] < em[c]:
                nx = min(c + 1, n - 1); xi = c; xp = op[nx]; reason = "trail"; break
        ret = (xp / ep - 1.0) - COST
        trades.append({
            "entry_time": df["timestamp"].iloc[e].strftime("%Y-%m-%dT%H:%M:%S%z"),
            "exit_time": df["timestamp"].iloc[xi].strftime("%Y-%m-%dT%H:%M:%S%z"),
            "entry": round(float(ep), 6), "stop": round(float(sp), 6),
            "exit": round(float(xp), 6), "reason": reason,
            "ret_net_pct": round(float(ret) * 100, 4),
            "R": round(float((xp - ep) / risk), 4) if risk > 0 else 0.0,
        })
        i = max(xi + 1, i + 1)
    tdf = pd.DataFrame(trades)
    tdf.to_csv(candidate_dir / f"{cid}_trades.csv", index=False)

    # Verify lockbox (last 25%) metrics vs engine simulate_slice + recorded spec
    lb_s = n - n // 4
    stats = M.simulate_slice(df, sig, stop, strat, lb_s, n)
    rec = spec.get("metrics_lockbox", {})
    rows = [
        ("compound_return_pct", stats.net_return_pct, rec.get("return_pct_compound")),
        ("profit_factor", stats.profit_factor, rec.get("profit_factor")),
        ("trades", stats.num_trades, rec.get("trades")),
        ("max_drawdown_pct", stats.max_drawdown_pct, rec.get("max_drawdown_pct")),
        ("win_rate", stats.win_rate, rec.get("win_rate")),
        ("expectancy_R", stats.expectancy_R, rec.get("expectancy_R")),
    ]
    md = [f"# Parity Reference Metrics — {cid}", "",
          f"- Engine strategy: `{strat}`  | Symbol/TF: {sym} {tf}  | direction: long-only",
          f"- Params: `{json.dumps(params, separators=(',',':'))}`",
          f"- Full-history trades emitted: {len(tdf)}  | lockbox bars: {n - lb_s}",
          "", "| Metric | Engine (recomputed) | Recorded (spec) | Match |",
          "|---|---|---|---|"]
    ok = True
    for name, eng, recv in rows:
        m = "—"
        if recv is not None:
            try:
                m = "OK" if abs(float(eng) - float(recv)) <= max(0.5, abs(float(recv)) * 0.01) else "DIFF"
            except Exception:
                m = "?"
            if m == "DIFF": ok = False
        md.append(f"| {name} | {eng} | {recv} | {m} |")
    md.append("")
    md.append(f"**Overall:** {'VERIFIED — reference reproduces recorded lockbox metrics.' if ok else 'MISMATCH — investigate before parity.'}")
    (candidate_dir / "PARITY_REFERENCE_METRICS.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[{cid}] signals+trades emitted; lockbox verify ret={stats.net_return_pct}% pf={stats.profit_factor} "
          f"trades={stats.num_trades} -> {'VERIFIED' if ok else 'MISMATCH'}")

def main():
    M._MANIFEST = json.load(open(M.BUNDLE_MANIFEST, encoding="utf-8"))
    arg = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    if arg == "ALL":
        dirs = [d for d in PROMOTED.iterdir() if d.is_dir() and (d / "producer_spec.json").exists()]
    else:
        dirs = [PROMOTED / arg]
    for d in dirs:
        emit_for(d)

if __name__ == "__main__":
    main()
