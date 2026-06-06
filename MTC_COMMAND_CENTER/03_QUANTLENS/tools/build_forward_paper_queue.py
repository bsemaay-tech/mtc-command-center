"""
build_forward_paper_queue.py

Reads scorecard_v2/*.scorecard.json from all backtest runs.
Identifies FORWARD_PAPER candidates: Gate2=PASS + cpcv_pass_ratio>=0.7 + net_after_slippage_pct > 0
Outputs: MTC_COMMAND_CENTER/03_QUANTLENS/05_BACKTEST_RESULTS/FORWARD_PAPER_QUEUE.md
"""

from pathlib import Path
import json
from datetime import datetime

MCC_ROOT = Path(__file__).resolve().parents[2]
BACKTEST_ROOT = MCC_ROOT / "03_QUANTLENS" / "05_BACKTEST_RESULTS"
STATUS_ROOT = MCC_ROOT / "03_STATUS"
OUTPUT_FILE = BACKTEST_ROOT / "FORWARD_PAPER_QUEUE.md"

CPCV_THRESHOLD = 0.70
SLIPPAGE_NET_MIN = 0.0  # must be positive after slippage


def load_scorecards() -> list[dict]:
    """Load all scorecard_v2 JSON files from BACKTEST_ROOT and STATUS_ROOT."""
    cards = []
    search_roots = [BACKTEST_ROOT, STATUS_ROOT]
    for root in search_roots:
        if not root.exists():
            continue
        for sc_file in root.rglob("scorecard_v2/*.scorecard.json"):
            try:
                data = json.loads(sc_file.read_text(encoding="utf-8"))
                data["_source_file"] = str(sc_file.relative_to(MCC_ROOT))
                cards.append(data)
            except Exception as e:
                print(f"[WARN] Could not parse {sc_file}: {e}")
    return cards


def is_forward_paper_candidate(card: dict) -> tuple[bool, list[str]]:
    """
    Returns (is_candidate, reasons_list).
    Candidate if: Gate2=PASS AND cpcv_pass_ratio>=0.7 AND net_after_slippage_pct>0
    """
    reasons = []
    gate2 = card.get("gate2", {})
    metrics = gate2.get("metrics", {})

    gate2_pass = gate2.get("pass", False)
    if not gate2_pass:
        return False, ["Gate2 not PASS"]

    cpcv = metrics.get("cpcv_pass_ratio", {})
    cpcv_val = cpcv.get("value") if isinstance(cpcv, dict) else cpcv
    if cpcv_val is None or cpcv_val < CPCV_THRESHOLD:
        return False, [f"CPCV {cpcv_val} < {CPCV_THRESHOLD}"]

    slip = metrics.get("net_after_slippage_pct", {})
    slip_val = slip.get("value") if isinstance(slip, dict) else slip
    if slip_val is None or slip_val <= SLIPPAGE_NET_MIN:
        return False, [f"Net slippage return {slip_val} <= {SLIPPAGE_NET_MIN}"]

    reasons.append(f"Gate2=PASS, CPCV={cpcv_val:.2f}, NetSlip={slip_val:.1f}%")

    # Bonus: note if gate_summary says promotable
    if card.get("gate_summary", {}).get("promotable"):
        reasons.append("PROMOTABLE=true")
    else:
        reasons.append("Gate3 still incomplete (paper-trade evidence needed)")

    return True, reasons


def build_queue():
    cards = load_scorecards()
    print(f"Loaded {len(cards)} scorecards from {BACKTEST_ROOT} + {STATUS_ROOT}")

    candidates = []
    for card in cards:
        is_cand, reasons = is_forward_paper_candidate(card)
        if is_cand:
            gate2 = card.get("gate2", {})
            metrics = gate2.get("metrics", {})

            def mval(key):
                v = metrics.get(key, {})
                return v.get("value") if isinstance(v, dict) else v

            candidates.append({
                "strategy_id": card.get("strategy_id", "unknown"),
                "symbol": card.get("symbol", ""),
                "timeframe": card.get("timeframe", ""),
                "gate2_score": gate2.get("score"),
                "cpcv": mval("cpcv_pass_ratio"),
                "pbo": mval("pbo"),
                "net_slippage": mval("net_after_slippage_pct"),
                "sharpe": mval("sharpe"),
                "sortino": mval("sortino"),
                "promotable": card.get("gate_summary", {}).get("promotable", False),
                "reasons": reasons,
                "source": card.get("_source_file", ""),
            })

    candidates.sort(key=lambda c: (not c["promotable"], -(c["cpcv"] or 0)))

    lines = [
        "# FORWARD_PAPER_QUEUE",
        f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} — {len(candidates)} candidates_",
        "",
        "## Criteria",
        f"- Gate2 = PASS",
        f"- CPCV pass ratio ≥ {CPCV_THRESHOLD}",
        f"- Net after slippage > {SLIPPAGE_NET_MIN}%",
        "",
        "## Candidates",
        "",
    ]

    if not candidates:
        lines.append("_No candidates meet all criteria._")
    else:
        lines.append("| # | Strategy | Symbol | TF | Gate2 | CPCV | PBO | Net% | Sharpe | Promotable |")
        lines.append("|---|----------|--------|-----|-------|------|-----|------|--------|------------|")
        for i, c in enumerate(candidates, 1):
            promo = "YES" if c["promotable"] else "no"
            lines.append(
                f"| {i} | {c['strategy_id']} | {c['symbol']} | {c['timeframe']} "
                f"| {c['gate2_score']} | {c['cpcv']:.2f} | {c['pbo'] or 'N/A'} "
                f"| {c['net_slippage']:.1f} | {c['sharpe'] or 'N/A'} | {promo} |"
            )
        lines.append("")
        for c in candidates:
            lines.append(f"### {c['strategy_id']} | {c['symbol']} {c['timeframe']}")
            for r in c["reasons"]:
                lines.append(f"- {r}")
            lines.append(f"- Source: `{c['source']}`")
            lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {OUTPUT_FILE}")
    print(f"Total candidates: {len(candidates)}")
    return candidates


if __name__ == "__main__":
    build_queue()
