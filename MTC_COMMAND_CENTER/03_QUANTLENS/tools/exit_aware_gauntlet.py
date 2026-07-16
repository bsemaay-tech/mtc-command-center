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
import os
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


def run_cell(cell: dict, manifest: dict, out_dir: Path, *, n_groups: int = 6,
             test_groups: int = 2, embargo_pct: float = 0.01, min_trades: int = 30,
             min_pf: float = 1.0, max_dd_floor: float = -50.0,
             max_combinations: int = 100000) -> dict:
    """End-to-end exit-aware gauntlet for ONE frozen confirmation cell.

    cell = {strategy, symbol, timeframe, exit_mode, primary_params, star_params[]}.
    `exit_mode` must be EXPLICIT — a confirmation may never fall back to the
    default silently (substitution guard). Persists the config-matrix artifact
    and the stamped verdict JSON into out_dir; returns the verdict dict.
    """
    for key in ("strategy", "symbol", "timeframe", "exit_mode", "primary_params"):
        if not cell.get(key):
            raise ValueError(f"cell is missing required field {key!r} — confirmation cells must be fully explicit")
    stars = cell.get("star_params") or []
    if len(stars) < 1:
        raise ValueError("cell needs >= 1 literal star neighbour for PBO/stability")
    out_dir.mkdir(parents=True, exist_ok=True)
    exit_mode = cell["exit_mode"]

    # 1) exit-aware CPCV on the FROZEN primary config only
    class _CpcvArgs:
        pass
    ca = _CpcvArgs()
    ca.n_groups, ca.test_groups, ca.embargo_pct = n_groups, test_groups, embargo_pct
    ca.min_trades, ca.min_pf, ca.max_dd_floor = min_trades, min_pf, max_dd_floor
    row = {"strategy": cell["strategy"], "symbol": cell["symbol"], "timeframe": cell["timeframe"],
           "exit_mode": exit_mode, "classification": "STRONG_PASS",
           "summary": {"best_params": cell["primary_params"]}}
    cpcv_res = cpcv.validate_candidate(row, manifest, ca)
    if cpcv_res.get("exit_mode") != exit_mode:
        raise RuntimeError("exit_mode stamp missing from CPCV output — substitution guard tripped")

    # 2) config x period matrix (primary + literal stars) -> PBO/CSCV
    ds = mw.find_ds(manifest, cell["symbol"], cell["timeframe"])
    if ds is None:
        raise ValueError(f"no dataset for {cell['symbol']} {cell['timeframe']} in manifest")
    df = mw.load_df(ds["normalized_path"])
    configs = [{"params": cell["primary_params"], "role": "primary"}] + \
              [{"params": p, "role": "star"} for p in stars]
    matrix_art = build_config_matrix(cell, df, configs, n_groups=n_groups, exit_mode=exit_mode)
    matrix_path = out_dir / "config_matrix.json"
    matrix_path.write_text(json.dumps(matrix_art, indent=2), encoding="utf-8")
    try:
        ids, matrix = pbo.load_config_matrix(matrix_path)
        pbo_res = pbo.estimate_pbo(ids, matrix, max_combinations)
    except ValueError as exc:
        pbo_res = {"status": "INSUFFICIENT_DATA", "pbo": None, "reason": str(exc)}

    # 3) strict multiwindow: regime placement + literal-neighbour stability
    sig, stop, direction = _build_signals(cell["strategy"], df, cell["primary_params"], cell["symbol"])
    n = len(df)
    wins = mwin.windows(n)
    seed = abs(hash((cell["strategy"], cell["symbol"], cell["timeframe"], exit_mode))) % (2 ** 31)
    wres = {name: mwin.score_window(df, sig, stop, cell["strategy"], s, e, seed + i, exit_mode=exit_mode)
            for i, (name, (s, e)) in enumerate(wins.items())}
    mw_pos = sum(1 for w in wres.values() if w["trades"] >= mwin.MIN_TR and w["ret"] > 0)
    lb_s = n - (n // 4)
    stable_pos, stable_tot = mwin.neighbor_stability(
        cell["strategy"], df, cell["primary_params"], cell["symbol"], lb_s, n,
        exit_mode=exit_mode, literal_neighbors=stars, strict=True)

    # 4) combined pre-registered verdict (any missing gate = GAUNTLET_FAIL)
    v = verdict(cpcv_res, pbo_res, mw_pos, stable_pos, stable_tot)
    result = {
        "cell": {k: cell[k] for k in ("strategy", "symbol", "timeframe", "exit_mode")},
        "primary_params": cell["primary_params"],
        "star_params": stars,
        "exit_mode": exit_mode,
        "cpcv": {k: cpcv_res.get(k) for k in ("status", "exit_mode", "pass_count", "splits", "pass_rate",
                                              "return_median_pct", "trades_median")},
        "pbo": {k: pbo_res.get(k) for k in ("status", "pbo", "cscv_combinations", "candidate_count", "reason")
                if k in pbo_res},
        "multiwindow": {"windows_positive": mw_pos, "window_results": {k: wres[k] for k in wres},
                        "neighbour_stable": [stable_pos, stable_tot], "strict": True},
        "verdict": v,
    }
    (out_dir / "gauntlet_result.json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
    return result


def main() -> int:  # pragma: no cover - real-data entrypoint, run only under approval
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cell", type=Path, required=True, help="JSON cell spec (frozen by the pre-registration)")
    parser.add_argument("--out-dir", type=Path, default=TOOLS_DIR / "gauntlet_runs")
    parser.add_argument("--n-groups", type=int, default=6)
    parser.add_argument("--max-combinations", type=int, default=100000)
    parser.add_argument("--i-have-approval", action="store_true")
    args = parser.parse_args()
    if not args.i_have_approval:
        raise SystemExit(
            "REFUSED: exit_aware_gauntlet is approval-gated. It may only run after the "
            "pre-registration passes independent Gate-5 AND Barış approves it in writing."
        )
    manifest_path = os.environ.get("MEGA_BUNDLE_MANIFEST", "")
    if not manifest_path or not Path(manifest_path).exists():
        raise SystemExit("ABORT: MEGA_BUNDLE_MANIFEST must resolve to an existing manifest")
    mw._MANIFEST = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    cell = json.loads(args.cell.read_text(encoding="utf-8"))
    result = run_cell(cell, mw._MANIFEST, args.out_dir, n_groups=args.n_groups,
                      max_combinations=args.max_combinations)
    print(json.dumps(result["verdict"], indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
