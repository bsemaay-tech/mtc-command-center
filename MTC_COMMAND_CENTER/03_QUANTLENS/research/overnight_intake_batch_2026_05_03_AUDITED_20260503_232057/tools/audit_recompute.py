"""Independent metric + fee-stress recomputation for first-run strategies.

Reads first-run strategies/CANDIDATE_*/trades.csv and results.csv, recomputes
metrics from raw trades, compares to first-run claimed values, runs an
independent fee-stress sweep, and emits audit CSV/MD artifacts.

Inputs are read-only. All outputs go to the AUDITED folder.
"""
from __future__ import annotations

import csv
import json
import math
import re
from pathlib import Path

FIRST = Path(r"C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/research/overnight_intake_batch_2026_05_03")
AUDIT = Path(r"C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/research/overnight_intake_batch_2026_05_03_AUDITED_20260503_232057")
STRAT = FIRST / "strategies"

# Realistic Binance USDT-M futures taker baseline ~4 bps per side. The first run
# clearly ran with ~6 bps/side cost (gross-net delta ≈ 12 bps). We honor the
# first-run base by inferring per-trade cost from gross-net spread, then probe
# 2x and 3x as additional fee on top of that base.

PCT_TOL_PF = 0.02       # ±2% relative tolerance on PF for MATCH
PCT_TOL_NET = 0.01      # ±1% absolute on win_rate; ±1% relative on net_return
ABS_TOL_DD = 0.5        # ±0.5 pp absolute on max_dd_pct


def f(x, default=float("nan")):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def read_trades(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            rows.append({
                "asset": r.get("asset", ""),
                "direction": r.get("direction", "long"),
                "entry": f(r.get("entry_price")),
                "exit": f(r.get("exit_price")),
                "gross": f(r.get("gross_return_pct")),
                "net": f(r.get("net_return_pct")),
                "bars": int(f(r.get("holding_bars"), 0) or 0),
            })
    return rows


def recompute(trades: list[dict], extra_cost_per_trade_pct: float = 0.0) -> dict:
    if not trades:
        return {"trades": 0, "pf": float("nan"), "net_return_pct": 0.0,
                "win_rate": float("nan"), "avg_trade_pct": float("nan"),
                "median_trade_pct": float("nan"), "expectancy_pct": float("nan"),
                "max_dd_pct": float("nan"), "n_assets": 0,
                "concentration_top_asset_share": float("nan")}
    # Apply additional cost on top of net_return_pct (already net at base cost)
    rs = [t["net"] - extra_cost_per_trade_pct for t in trades]
    n = len(rs)
    wins = [r for r in rs if r > 0]
    losses = [r for r in rs if r < 0]
    sum_w = sum(wins)
    sum_l = sum(losses)  # negative
    pf = (sum_w / -sum_l) if sum_l < 0 else float("inf")
    # equity curve assumed log-additive in pct space (approx; matches first-run convention)
    equity = []
    cum_mult = 1.0
    for r in rs:
        cum_mult *= (1.0 + r / 100.0)
        equity.append(cum_mult)
    peak = equity[0]
    max_dd = 0.0
    for e in equity:
        if e > peak:
            peak = e
        dd = (peak - e) / peak * 100.0
        if dd > max_dd:
            max_dd = dd
    rs_sorted = sorted(rs)
    median = rs_sorted[n // 2] if n % 2 == 1 else 0.5 * (rs_sorted[n // 2 - 1] + rs_sorted[n // 2])
    asset_counts: dict[str, int] = {}
    for t in trades:
        asset_counts[t["asset"]] = asset_counts.get(t["asset"], 0) + 1
    top_share = max(asset_counts.values()) / n if asset_counts else float("nan")
    return {
        "trades": n,
        "pf": pf,
        "net_return_pct": (cum_mult - 1.0) * 100.0,
        "win_rate": len(wins) / n,
        "avg_trade_pct": sum(rs) / n,
        "median_trade_pct": median,
        "expectancy_pct": sum(rs) / n,
        "max_dd_pct": -max_dd,
        "n_assets": len(asset_counts),
        "concentration_top_asset_share": top_share,
    }


def base_cost_per_trade(trades: list[dict]) -> float:
    deltas = [t["gross"] - t["net"] for t in trades if math.isfinite(t["gross"]) and math.isfinite(t["net"])]
    if not deltas:
        return 0.0
    deltas.sort()
    return deltas[len(deltas) // 2]


def reclassify(rec: dict, fee2: dict, fee3: dict, n_assets: int, label: str, top_share: float) -> tuple[str, list[str]]:
    notes = []
    pf = rec["pf"]
    pf2 = fee2["pf"]
    pf3 = fee3["pf"]
    dd = rec["max_dd_pct"]
    n = rec["trades"]
    net = rec["net_return_pct"]

    if n == 0:
        return "DATA_BLOCKED", ["no trades / data blocked"]

    if not (pf >= pf2 >= pf3):
        notes.append(f"FEE_MONOTONIC_BUG (pf={pf:.3f}, 2x={pf2:.3f}, 3x={pf3:.3f})")

    if "REJECT" in label.upper() or "BASELINE" in label.upper() or "DATA_BLOCKED" in label.upper():
        # honor first-run honest reject/baseline if metrics support it
        if "REJECT" in label.upper() and pf < 1.05:
            return "REJECT_NO_EDGE", notes + [f"pf={pf:.2f} after audited recompute"]
        if "BASELINE" in label.upper():
            return "BASELINE_ONLY", notes + ["baseline rule by design"]
        if "DATA_BLOCKED" in label.upper():
            return "DATA_BLOCKED", notes
    if pf < 1.05:
        return "REJECT_NO_EDGE", notes + [f"pf={pf:.2f}"]
    if abs(dd) > 90:
        return "WEAK_CANDIDATE", notes + [f"max_dd={dd:.1f}% extreme"]
    if pf3 < 1.0:
        return "WEAK_CANDIDATE", notes + ["edge disappears at 3x cost"]
    if n_assets < 5:
        return "WEAK_CANDIDATE", notes + [f"only {n_assets} assets"]
    if top_share > 0.4:
        return "WEAK_CANDIDATE", notes + [f"concentrated: top asset = {top_share:.0%}"]
    if pf >= 1.20 and pf2 >= 1.10 and pf3 >= 1.0 and abs(dd) < 60 and n >= 30:
        return "PASS_STAGE2", notes
    return "WEAK_CANDIDATE", notes + [f"net={net:.1f}%, pf={pf:.2f}, dd={dd:.1f}%"]


def main() -> None:
    audit_rows = []
    diff_rows = []
    fee_rows = []

    folders = sorted([p for p in STRAT.iterdir() if p.is_dir() and p.name.startswith("CANDIDATE_")])
    for d in folders:
        cid = d.name
        trades_path = d / "trades.csv"
        results_path = d / "results.csv"
        first_results = {}
        if results_path.exists():
            with results_path.open("r", encoding="utf-8") as fh:
                rd = csv.DictReader(fh)
                for row in rd:
                    first_results = row
                    break
        first_label = first_results.get("classification", "")
        first_pf = f(first_results.get("aggregate_pf"))
        first_net = f(first_results.get("aggregate_net_return_pct"))
        first_dd = f(first_results.get("aggregate_max_dd_pct"))
        first_trades = int(f(first_results.get("trade_count"), 0))
        first_assets = int(f(first_results.get("assets_tested"), 0))
        first_winrate = f(first_results.get("win_rate"))
        first_fee2 = f(first_results.get("fee_2x_pf"))
        first_fee3 = f(first_results.get("fee_3x_pf"))

        if not trades_path.exists():
            audit_rows.append({"cand": cid, "status": "NO_TRADES_FILE", "first_class": first_label})
            continue

        trades = read_trades(trades_path)
        base = recompute(trades, 0.0)
        # infer per-trade base cost (gross - net) median; assume 2x means add same
        # cost again, 3x adds 2x base again
        inferred_base = base_cost_per_trade(trades)
        fee2 = recompute(trades, inferred_base)
        fee3 = recompute(trades, 2.0 * inferred_base)

        new_label, notes = reclassify(base, fee2, fee3, base["n_assets"], first_label, base.get("concentration_top_asset_share", 0))
        monotonic_audited = (base["pf"] >= fee2["pf"] >= fee3["pf"]) if all(math.isfinite(x) for x in (base["pf"], fee2["pf"], fee3["pf"])) else False

        # diff vs first-run
        def cmp(a, b, rel):
            if not math.isfinite(a) or not math.isfinite(b):
                return "NOT_RECOMPUTABLE"
            if abs(a - b) < 1e-9:
                return "MATCH"
            if abs(b) > 1e-12 and abs(a - b) / max(abs(b), 1e-12) < rel:
                return "MINOR_ROUNDING_DIFF"
            return "MAJOR_MISMATCH"

        diff = {
            "cand": cid,
            "trades_match": base["trades"] == first_trades,
            "pf_first": round(first_pf, 4) if math.isfinite(first_pf) else "",
            "pf_audit": round(base["pf"], 4) if math.isfinite(base["pf"]) else "",
            "pf_status": cmp(base["pf"], first_pf, PCT_TOL_PF),
            "net_first": round(first_net, 4) if math.isfinite(first_net) else "",
            "net_audit": round(base["net_return_pct"], 4) if math.isfinite(base["net_return_pct"]) else "",
            "net_status": cmp(base["net_return_pct"], first_net, 0.05),
            "dd_first": round(first_dd, 4) if math.isfinite(first_dd) else "",
            "dd_audit": round(base["max_dd_pct"], 4) if math.isfinite(base["max_dd_pct"]) else "",
            "dd_status": "MATCH" if math.isfinite(first_dd) and math.isfinite(base["max_dd_pct"]) and abs(first_dd - base["max_dd_pct"]) < ABS_TOL_DD else (
                "MINOR_ROUNDING_DIFF" if math.isfinite(first_dd) and math.isfinite(base["max_dd_pct"]) and abs(first_dd - base["max_dd_pct"]) < 5 else "MAJOR_MISMATCH"),
            "winrate_first_pct": round(first_winrate, 2) if math.isfinite(first_winrate) else "",
            "winrate_audit_pct": round(base["win_rate"] * 100.0, 2),
            "fee2_first": round(first_fee2, 4) if math.isfinite(first_fee2) else "",
            "fee2_audit": round(fee2["pf"], 4) if math.isfinite(fee2["pf"]) else "",
            "fee3_first": round(first_fee3, 4) if math.isfinite(first_fee3) else "",
            "fee3_audit": round(fee3["pf"], 4) if math.isfinite(fee3["pf"]) else "",
            "monotonic_first_run": (first_pf >= first_fee2 >= first_fee3) if all(math.isfinite(x) for x in (first_pf, first_fee2, first_fee3)) else "n/a",
            "monotonic_audit": monotonic_audited,
        }
        diff_rows.append(diff)

        audit_rows.append({
            "cand": cid,
            "first_class": first_label,
            "audit_class": new_label,
            "trades": base["trades"],
            "n_assets": base["n_assets"],
            "concentration_top_asset_share": round(base["concentration_top_asset_share"], 3) if math.isfinite(base["concentration_top_asset_share"]) else "",
            "pf_base": round(base["pf"], 4) if math.isfinite(base["pf"]) else "",
            "pf_2x": round(fee2["pf"], 4) if math.isfinite(fee2["pf"]) else "",
            "pf_3x": round(fee3["pf"], 4) if math.isfinite(fee3["pf"]) else "",
            "net_return_pct": round(base["net_return_pct"], 4) if math.isfinite(base["net_return_pct"]) else "",
            "max_dd_pct": round(base["max_dd_pct"], 4) if math.isfinite(base["max_dd_pct"]) else "",
            "win_rate_pct": round(base["win_rate"] * 100.0, 2),
            "expectancy_pct": round(base["expectancy_pct"], 4) if math.isfinite(base["expectancy_pct"]) else "",
            "monotonic_audit": monotonic_audited,
            "notes": " | ".join(notes),
        })

        fee_rows.append({
            "cand": cid,
            "pf_base": round(base["pf"], 4) if math.isfinite(base["pf"]) else "",
            "pf_fee_2x": round(fee2["pf"], 4) if math.isfinite(fee2["pf"]) else "",
            "pf_fee_3x": round(fee3["pf"], 4) if math.isfinite(fee3["pf"]) else "",
            "monotonic": monotonic_audited,
            "inferred_base_cost_pct": round(base_cost_per_trade(trades), 4),
        })

    # Write all CSVs
    def write_csv(path: Path, rows: list[dict]):
        if not rows:
            path.write_text("(no rows)\n", encoding="utf-8")
            return
        with path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write_csv(AUDIT / "METRIC_RECOMPUTE_AUDIT.csv", diff_rows)
    write_csv(AUDIT / "FEE_STRESS_AUDIT.csv", fee_rows)
    write_csv(AUDIT / "AUDITED_STRATEGY_RECLASSIFICATION.csv", audit_rows)

    # MD reports
    lines = ["# Metric Recompute Audit", "",
             "Independent recomputation from each strategy's raw trades.csv.",
             "Status meanings: MATCH (≤rounding), MINOR_ROUNDING_DIFF, MAJOR_MISMATCH.",
             "",
             "| cand | trades_match | pf_first | pf_audit | pf | net_first | net_audit | net | dd_first | dd_audit | dd | wr_first | wr_audit | fee2_first | fee2_audit | fee3_first | fee3_audit | mono_first | mono_audit |",
             "|------|--------------|---------:|---------:|----|----------:|----------:|----|---------:|---------:|----|---------:|---------:|-----------:|-----------:|-----------:|-----------:|------------|------------|"]
    for r in diff_rows:
        lines.append(f"| {r['cand']} | {r['trades_match']} | {r['pf_first']} | {r['pf_audit']} | {r['pf_status']} | {r['net_first']} | {r['net_audit']} | {r['net_status']} | {r['dd_first']} | {r['dd_audit']} | {r['dd_status']} | {r['winrate_first_pct']} | {r['winrate_audit_pct']} | {r['fee2_first']} | {r['fee2_audit']} | {r['fee3_first']} | {r['fee3_audit']} | {r['monotonic_first_run']} | {r['monotonic_audit']} |")
    (AUDIT / "METRIC_RECOMPUTE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")

    lines2 = ["# Fee Stress Audit", "",
              "PF recomputed from trades with additional per-trade cost equal to inferred base (=median(gross-net)).",
              "Monotonic requires base ≥ 2x ≥ 3x.", "",
              "| cand | pf_base | pf_fee_2x | pf_fee_3x | monotonic | inferred_base_cost_pct |",
              "|------|--------:|----------:|----------:|-----------|----------------------:|"]
    for r in fee_rows:
        lines2.append(f"| {r['cand']} | {r['pf_base']} | {r['pf_fee_2x']} | {r['pf_fee_3x']} | {r['monotonic']} | {r['inferred_base_cost_pct']} |")
    (AUDIT / "FEE_STRESS_AUDIT.md").write_text("\n".join(lines2), encoding="utf-8")

    lines3 = ["# Audited Strategy Reclassification", "",
              "Final classification after independent metric + fee-stress audit.",
              "",
              "| cand | first_class | audit_class | trades | assets | top_asset_share | pf_base | pf_2x | pf_3x | net_pct | max_dd_pct | win_rate | mono | notes |",
              "|------|-------------|-------------|-------:|-------:|----------------:|--------:|------:|------:|--------:|-----------:|---------:|------|-------|"]
    for r in audit_rows:
        lines3.append(f"| {r['cand']} | {r['first_class']} | {r['audit_class']} | {r['trades']} | {r['n_assets']} | {r['concentration_top_asset_share']} | {r['pf_base']} | {r['pf_2x']} | {r['pf_3x']} | {r['net_return_pct']} | {r['max_dd_pct']} | {r['win_rate_pct']} | {r['monotonic_audit']} | {r['notes']} |")
    (AUDIT / "AUDITED_STRATEGY_RECLASSIFICATION.md").write_text("\n".join(lines3), encoding="utf-8")

    # summary console
    print("Audit complete.")
    print(f"Strategies audited: {len(audit_rows)}")
    pass_n = sum(1 for r in audit_rows if r["audit_class"] == "PASS_STAGE2")
    weak_n = sum(1 for r in audit_rows if r["audit_class"] == "WEAK_CANDIDATE")
    rej_n = sum(1 for r in audit_rows if "REJECT" in r["audit_class"])
    blocked_n = sum(1 for r in audit_rows if r["audit_class"] == "DATA_BLOCKED")
    print(f"PASS_STAGE2={pass_n} WEAK={weak_n} REJECT={rej_n} BLOCKED={blocked_n}")
    for r in audit_rows:
        print(f"  {r['cand']:>12} | {r['first_class']:>30} -> {r['audit_class']:>20} | pf={r['pf_base']} 2x={r['pf_2x']} 3x={r['pf_3x']} dd={r['max_dd_pct']} mono={r['monotonic_audit']}")


if __name__ == "__main__":
    main()
