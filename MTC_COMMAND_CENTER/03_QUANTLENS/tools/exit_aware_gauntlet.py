#!/usr/bin/env python
"""Exit-aware confirmation gauntlet for ONE pre-registered cell (2026-07-15).

Orchestrates the exit-aware primitives (cpcv_validator, probabilistic_pbo,
multiwindow_oos) for a single confirmation cell = (strategy, symbol, timeframe,
exit_mode, frozen primary params + literal star neighbours). It builds the
per-cell configuration x common-period return matrix that Gate-5 §G requires
for a valid PBO, threads exit_mode into every simulation, and applies the
pre-registered gate thresholds to emit one stamped verdict.

SAFETY: importing/unit-testing this module runs NO backtest. `run_cell` and
`main` call simulate_slice on real bars and therefore require Barış approval +
real data. Nothing here authorises a run. Default fixed_2R behaviour of the
underlying tools is unchanged (this module never runs unless invoked).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(TOOLS_DIR))

import mega_walk_forward as mw  # noqa: E402
import cpcv_validator as cpcv  # noqa: E402
import multiwindow_oos as mwin  # noqa: E402
import probabilistic_pbo as pbo  # noqa: E402


def _build_signals(strategy, df, params, symbol):
    dmap = None
    if strategy == "QL_2026-05-01_SWING_1H_DUAL_RSI_60_40_PULLBACK":
        maps = mw.build_daily_rsi(getattr(mw, "_MANIFEST", None), symbol)
        dmap = maps.get(int(params["rsi_len"])) if maps else None
    result = mw.build_signals(strategy, df, params, dmap)
    if isinstance(result, tuple) and len(result) == 3 and result[2] in {"long", "short"}:
        return result[0], result[1], result[2]
    return result[0], result[1], "long"


def build_config_matrix(cell: dict, df, configs: list[dict], n_groups: int = 6, exit_mode: str | None = None) -> dict:
    """Run each config across n_groups equal chronological periods, scoring with
    the cell's exit_mode -> the config x period return matrix (PBO input).

    All rows share ONE symbol + ONE exit_mode (this cell), so the matrix can
    never smuggle a cross-symbol/exit competitor — the Gate-5 §G defect.
    """
    em = exit_mode or cell.get("exit_mode") or mw.DEFAULT_EXIT_MODE
    groups = cpcv.contiguous_groups(len(df), n_groups)
    out = []
    for cfg in configs:
        params = cfg["params"]
        sig, stop, direction = _build_signals(cell["strategy"], df, params, cell["symbol"])
        rets = []
        for (s, e) in groups:
            st = mw.simulate_slice(df, sig, stop, cell["strategy"], s, e, direction=direction, exit_mode=em)
            rets.append(round(float(st.net_return_pct), 6))
        out.append({"params": params, "role": cfg.get("role", "star"), "returns_pct": rets})
    return {
        "cell": {**cell, "exit_mode": em},
        "period_labels": [f"G{i}" for i in range(len(groups))],
        "configs": out,
    }


def verdict(cpcv_res: dict, pbo_res: dict, mw_pos: int, mw_stable_pos: int, mw_stable_tot: int,
            *, cpcv_pass_rate_min: float = 0.70, pbo_max: float = 0.50,
            mw_windows_min: int = 3, mw_stable_min: float = 0.70) -> dict:
    """Pre-registered combined gate. Any missing/failed sub-gate => GAUNTLET_FAIL
    (Gate-5: a non-OK gauntlet is a failure, never a silent waiver)."""
    reasons = []
    cpcv_ok = cpcv_res.get("status") == "OK" and cpcv_res.get("pass_rate", 0.0) >= cpcv_pass_rate_min
    if not cpcv_ok:
        reasons.append(f"cpcv pass_rate {cpcv_res.get('pass_rate')} < {cpcv_pass_rate_min} or status {cpcv_res.get('status')}")
    pbo_val = pbo_res.get("pbo")
    pbo_ok = pbo_res.get("status") == "OK" and pbo_val is not None and pbo_val < pbo_max
    if not pbo_ok:
        reasons.append(f"pbo {pbo_val} !< {pbo_max} or status {pbo_res.get('status')}")
    mw_regime_ok = mw_pos >= mw_windows_min
    mw_stable_ok = mw_stable_tot > 0 and (mw_stable_pos / mw_stable_tot) >= mw_stable_min
    if not mw_regime_ok:
        reasons.append(f"multiwindow positive {mw_pos} < {mw_windows_min}")
    if not mw_stable_ok:
        reasons.append(f"neighbour-stable {mw_stable_pos}/{mw_stable_tot} < {mw_stable_min}")
    passed = cpcv_ok and pbo_ok and mw_regime_ok and mw_stable_ok
    return {
        "gauntlet_pass": bool(passed),
        "status": "PASS" if passed else "GAUNTLET_FAIL",
        "cpcv_ok": cpcv_ok, "pbo_ok": pbo_ok,
        "multiwindow_regime_ok": mw_regime_ok, "neighbour_stable_ok": mw_stable_ok,
        "reasons": reasons,
    }


def main() -> int:  # pragma: no cover - real-data entrypoint, run only under approval
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell", type=Path, required=True, help="JSON cell spec (frozen by the pre-registration)")
    parser.add_argument("--out-dir", type=Path, default=TOOLS_DIR / "gauntlet_runs")
    parser.add_argument("--n-groups", type=int, default=6)
    args = parser.parse_args()
    raise SystemExit("exit_aware_gauntlet.main is approval-gated; wire real data + thresholds from the pre-registration before enabling.")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
