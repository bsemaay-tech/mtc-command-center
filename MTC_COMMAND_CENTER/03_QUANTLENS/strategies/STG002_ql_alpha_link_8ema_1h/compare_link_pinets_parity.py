"""
REVIEW_ONLY — Exact PineTS vs Python producer parity comparator for LINK 8EMA.
------------------------------------------------------------------------------
Loads:
  - link_pinets_signals.json     (PineTS producer output: longSig/ema8/atr14)
  - the SAME mock bars PineTS used (_pinets_mock/*.json)  -> Python producer input
Runs the Python producer (mega_walk_forward.build_signals, same engine that produced
the promotion metrics) on the identical bars and scores bar-for-bar agreement.

Both sides therefore consume byte-identical OHLCV -> any disagreement is a true
logic difference, not a data-feed artifact.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[1] / "tools"   # 06_QUANTLENS_LAB/tools
sys.path.insert(0, str(TOOLS))
import mega_walk_forward as M

STRAT = "QL_2026-05-01_US_EQUITIES_INTRADAY_8EMA_EXIT_TRAIL"
PARAMS = {"pullback_atr": 0.5, "impulse_atr": 1.6, "slope_window": 3}
WARMUP = 100  # exclude initial bars where Pine RMA-ATR seeding vs pandas differ

def main():
    sig_blob = json.loads((HERE / "link_pinets_signals.json").read_text(encoding="utf-8"))
    pine = pd.DataFrame(sig_blob["rows"])
    mock_bars = json.loads(Path(sig_blob["mock_file"]).read_text(encoding="utf-8"))

    # Python side: identical bars -> df with engine column names
    df = pd.DataFrame(mock_bars)
    df["timestamp"] = pd.to_datetime(df["openTime"], unit="ms", utc=True)
    df["date"] = df["timestamp"].dt.date
    df = df[["timestamp", "date", "open", "high", "low", "close"]].copy()

    sig, stop = M.build_signals(STRAT, df, PARAMS, None)
    py = pd.DataFrame({
        "ts": df["openTime"] if "openTime" in df else (df["timestamp"].astype("int64") // 10**6),
        "py_long": sig.astype(int).to_numpy(),
        "py_ema8": df["ema_8"].to_numpy(),
        "py_atr14": df["atr_14"].to_numpy(),
        "py_stop": stop.to_numpy(),
    })
    py["ts"] = (df["timestamp"].astype("int64") // 10**6).to_numpy()

    m = pine.merge(py, on="ts", how="inner")
    m = m.iloc[WARMUP:].reset_index(drop=True)
    n = len(m)

    # Signal agreement
    agree = (m["longSig"].fillna(0).astype(int) == m["py_long"].astype(int))
    agree_pct = 100.0 * agree.mean()
    pine_longs = int((m["longSig"] == 1).sum())
    py_longs = int((m["py_long"] == 1).sum())
    both = int(((m["longSig"] == 1) & (m["py_long"] == 1)).sum())
    only_pine = int(((m["longSig"] == 1) & (m["py_long"] == 0)).sum())
    only_py = int(((m["longSig"] == 0) & (m["py_long"] == 1)).sum())

    # Indicator parity (relative)
    def reldiff(a, b):
        a = pd.to_numeric(a, errors="coerce"); b = pd.to_numeric(b, errors="coerce")
        denom = b.abs().replace(0, np.nan)
        return (np.abs(a - b) / denom).replace([np.inf, -np.inf], np.nan)
    ema_rel = reldiff(m["ema8"], m["py_ema8"]).max()
    atr_rel = reldiff(m["atr14"], m["py_atr14"]).max()

    report = {
        "bars_compared": n,
        "signal_agreement_pct": round(float(agree_pct), 4),
        "pine_long_signals": pine_longs,
        "python_long_signals": py_longs,
        "long_both": both,
        "long_only_pine": only_pine,
        "long_only_python": only_py,
        "ema8_max_rel_diff": None if pd.isna(ema_rel) else round(float(ema_rel), 8),
        "atr14_max_rel_diff": None if pd.isna(atr_rel) else round(float(atr_rel), 8),
        "warmup_excluded": WARMUP,
        "verdict": "PASS" if agree_pct >= 99.0 else "REVIEW",
    }
    out = HERE / "PINETS_PARITY_RESULT.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nWrote {out}")

if __name__ == "__main__":
    main()
