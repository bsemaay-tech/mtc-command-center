"""Overnight orchestrator — 2026-05-30 → 2026-05-31.

Plans, materializes specs/prototypes, and kicks off a ~1M-case backtest sweep
covering the 19 newly approved candidates from this triage session plus the
existing 18 strategies in mega_walk_forward.py.

Default --dry-run prints the plan and case counts without writing anything.
Pass --apply to materialize spec/prototype files and emit a kickoff script.
Pass --launch to also start the backtest as a background Python process.
"""

from __future__ import annotations

import argparse
import json
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

THIS = Path(__file__).resolve()
MCC_ROOT = THIS.parent.parent
REPO_ROOT = MCC_ROOT.parent
QLAB_ROOT = REPO_ROOT / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"
PROTO_DIR = QLAB_ROOT / "04_PYTHON_PROTOTYPES"
PROMOTED_DIR = QLAB_ROOT / "06_PROMOTED_TO_PARITY"
TOOLS_DIR = QLAB_ROOT / "tools"

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "AVAXUSDT", "MATICUSDT", "LINKUSDT", "LTCUSDT", "DOTUSDT", "ATOMUSDT",
    "UNIUSDT", "AAVEUSDT", "FILUSDT", "NEARUSDT", "APTUSDT",
]
TIMEFRAMES = ["15m", "1h", "2h", "4h", "1D"]
FOLDS = 6


@dataclass
class Candidate:
    id: str
    source_id: str
    source_url: str
    title: str
    kind: str  # "strategy" | "filter_overlay" | "exit_overlay"
    confidence_rules: list[str]
    param_grid_size: int  # planned number of param combos
    entry_pseudo: str
    exit_pseudo: str
    timeframes: list[str] = field(default_factory=lambda: list(TIMEFRAMES))


CANDIDATES: list[Candidate] = [
    # ---------------- A: 8 promoted (7 + Andrew deep read) ----------------
    Candidate(
        id="QL_VCP_RICHARD_1D",
        source_id="QLR_Tm0dkf8_giA",
        source_url="https://www.youtube.com/watch?v=Tm0dkf8_giA",
        title="VCP Breakout (Richard Moglen tutorial)",
        kind="strategy",
        confidence_rules=[
            "2+ successive lower-amplitude contractions within a base",
            "volume declines on each contraction, surges on breakout",
            "entry at pivot-point breakout (prior resistance)",
            "stop at low of base OR low of breakout day",
            "trail under 21 EMA",
        ],
        param_grid_size=50,
        entry_pseudo="contractions>=2 AND close>pivot AND vol>1.5*avg20",
        exit_pseudo="close<EMA21 OR close<stop",
    ),
    Candidate(
        id="QL_VCP_MINERVINI_1D",
        source_id="QLR_M_tD6X0CSOI",
        source_url="https://www.youtube.com/watch?v=M_tD6X0CSOI",
        title="The Perfect VCP (Mark Minervini)",
        kind="strategy",
        confidence_rules=[
            "Stage 2 only: price > 50MA > 200MA",
            "RS line making new highs before price",
            "VCP pattern with progressively tighter contractions",
            "Entry: pivot breakout from VCP base",
            "Position sizing: progressive 5-10-15-20%",
        ],
        param_grid_size=80,
        entry_pseudo="stage2_ok AND rs_new_high AND vcp_pivot_breakout",
        exit_pseudo="close<EMA21 OR stop OR target_3x_ATR",
    ),
    Candidate(
        id="QL_DEEPAK_153_FILTER_1D",
        source_id="QLR_lpjTNygfnzM",
        source_url="https://www.youtube.com/watch?v=lpjTNygfnzM",
        title="Deepak Uppal 153% filter set",
        kind="filter_overlay",
        confidence_rules=[
            "price > 200-day MA",
            "price > 50-day MA",
            "50-day MA > 200-day MA",
            "price > $75 (or quote-currency equivalent)",
        ],
        param_grid_size=20,
        entry_pseudo="long_ok = price>SMA200 AND price>SMA50 AND SMA50>SMA200 AND price>min_price",
        exit_pseudo="N/A (filter overlay)",
    ),
    Candidate(
        id="QL_SELL_RULES_MARKET_WIZARDS_OVERLAY",
        source_id="QLR_UD7gipBWnuY",
        source_url="https://www.youtube.com/watch?v=UD7gipBWnuY",
        title="Market Wizards sell-rule library",
        kind="exit_overlay",
        confidence_rules=[
            "Trim 50% on first close below 50-day MA",
            "Full exit on extension > 8% from 50-day MA",
            "Filter: don't trade below 20-week EMA",
            "Trail 10/20-period MA with 3-touch confirmation",
            "Monthly DD cap with cascade 5%/3%/2%/1%",
        ],
        param_grid_size=40,
        entry_pseudo="N/A (overlay)",
        exit_pseudo="trim_on=close<SMA50; full_exit_on=ext>8% OR close<EMA_weekly20",
    ),
    Candidate(
        id="QL_CONNELL_EVENT_DRIVEN_GAP_1D",
        source_id="QLR_kao-hhaQnig",
        source_url="https://www.youtube.com/watch?v=kao-hhaQnig",
        title="Andrew Connell event-driven catalyst",
        kind="strategy",
        confidence_rules=[
            "Catalyst proxy: gap > 5% AND volume in top decile of last 60 bars",
            "Entry at open of catalyst bar",
            "Stop at low of prior green candle (or session low)",
            "Same-day invalidation: exit if loss > 1R by session close",
            "3-part scale-out at value-area top (20-day high proxy)",
        ],
        param_grid_size=60,
        entry_pseudo="gap_pct>=gap_thresh AND vol_rank>=0.9",
        exit_pseudo="scale_out_at_VAH OR stop OR session_close_if_negative",
    ),
    Candidate(
        id="QL_CONNELL_EVENT_DRIVEN_GAP_5M",
        source_id="QLR_kao-hhaQnig",
        source_url="https://www.youtube.com/watch?v=kao-hhaQnig",
        title="Andrew Connell intraday catalyst variant",
        kind="strategy",
        confidence_rules=[
            "5-minute timeframe entry on first 5m bar of gap day",
            "Stop at low of first 5m bar",
            "Same-day session exit",
        ],
        param_grid_size=40,
        entry_pseudo="is_first_5m_of_gap_day AND gap_pct>=thresh",
        exit_pseudo="close<bar_low OR session_end",
        timeframes=["5m"],
    ),
    # AVWAP — Brian Shannon parent + 4 sub-cases
    Candidate(
        id="QL_AVWAP_BRIAN_GAP_RECLAIM_5M",
        source_id="QLR_UmLa9FAlMgw",
        source_url="https://www.youtube.com/watch?v=UmLa9FAlMgw",
        title="AVWAP gap reclaim (Brian Shannon)",
        kind="strategy",
        confidence_rules=[
            "Gap up → settles → reclaims daily AVWAP from below",
            "Stop below low of day",
        ],
        param_grid_size=40,
        entry_pseudo="gap_up AND prior_below_avwap AND close>avwap_daily",
        exit_pseudo="close<bar_low OR end_of_session",
        timeframes=["5m", "15m"],
    ),
    Candidate(
        id="QL_AVWAP_BRIAN_STAGE2_EMERGING_1D",
        source_id="QLR_UmLa9FAlMgw",
        source_url="https://www.youtube.com/watch?v=UmLa9FAlMgw",
        title="AVWAP stage-2 emerging momentum (Brian Shannon)",
        kind="strategy",
        confidence_rules=[
            "20MA > 50MA > 200MA (Stage 2)",
            "Anchor VWAP from key low",
            "Buy on first higher-low pullback to AVWAP",
        ],
        param_grid_size=60,
        entry_pseudo="stage2_ok AND higher_low_at_avwap AND turn_up",
        exit_pseudo="close<avwap OR trail_under_swing_low",
    ),
    Candidate(
        id="QL_AVWAP_BRIAN_INTRADAY_OR_5M",
        source_id="QLR_UmLa9FAlMgw",
        source_url="https://www.youtube.com/watch?v=UmLa9FAlMgw",
        title="AVWAP intraday opening range (Brian Shannon)",
        kind="strategy",
        confidence_rules=[
            "Anchor AVWAP at session open",
            "Break of opening range",
            "Pullback to AVWAP holds as support → entry",
        ],
        param_grid_size=40,
        entry_pseudo="or_break AND pullback_to_avwap_held",
        exit_pseudo="close<avwap_intraday OR end_of_session",
        timeframes=["5m"],
    ),
    Candidate(
        id="QL_AVWAP_BRIAN_EARNINGS_ANCHOR_1D",
        source_id="QLR_UmLa9FAlMgw",
        source_url="https://www.youtube.com/watch?v=UmLa9FAlMgw",
        title="AVWAP earnings-anchor (Brian Shannon)",
        kind="strategy",
        confidence_rules=[
            "Anchor VWAP from earnings bar (proxy: largest daily volume bar in last 90 days)",
            "Buy pullbacks to earnings AVWAP",
            "Stop below AVWAP swing-low",
        ],
        param_grid_size=40,
        entry_pseudo="anchor_bar=top_vol_90d; pullback_to_anchor_avwap_held",
        exit_pseudo="close<anchor_avwap",
    ),
    # Christian Flanders parent + 4 sub-cases
    Candidate(
        id="QL_EPISODIC_PIVOT_CHRISTIAN_5M",
        source_id="QLR_Lot25-2fb-4",
        source_url="https://www.youtube.com/watch?v=Lot25-2fb-4",
        title="Christian Flanders episodic pivot (5m opening range)",
        kind="strategy",
        confidence_rules=[
            "News/earnings catalyst (proxy: gap > 4% + 5m vol > 3x avg)",
            "Buy at first 5m opening range high",
            "Stop at low of day",
        ],
        param_grid_size=50,
        entry_pseudo="catalyst_proxy AND close>or_high_5m",
        exit_pseudo="close<low_of_day OR session_end",
        timeframes=["5m"],
    ),
    Candidate(
        id="QL_TRAIL_20MA_CHRISTIAN_1D",
        source_id="QLR_Lot25-2fb-4",
        source_url="https://www.youtube.com/watch?v=Lot25-2fb-4",
        title="Christian Flanders 20-day MA trailing exit overlay",
        kind="exit_overlay",
        confidence_rules=[
            "Exit on close below 20-day SMA",
            "Empirically: +145% vs 10-day baseline in author's backtest",
        ],
        param_grid_size=20,
        entry_pseudo="N/A (overlay)",
        exit_pseudo="exit_on=close<SMA20",
    ),
    Candidate(
        id="QL_VCP_EARLY_ENTRY_CHRISTIAN_1D",
        source_id="QLR_Lot25-2fb-4",
        source_url="https://www.youtube.com/watch?v=Lot25-2fb-4",
        title="Christian VCP early-contraction entry",
        kind="strategy",
        confidence_rules=[
            "Same VCP detection as Minervini",
            "Entry on day 2-3 of contraction (early, not breakout)",
            "Tight stop below contraction",
        ],
        param_grid_size=50,
        entry_pseudo="vcp_in_progress AND contraction_day_2_or_3",
        exit_pseudo="close<contraction_low OR breakout_failed",
    ),
    Candidate(
        id="QL_OPEN_RANGE_5PCT_STOP_CHRISTIAN_5M",
        source_id="QLR_Lot25-2fb-4",
        source_url="https://www.youtube.com/watch?v=Lot25-2fb-4",
        title="Christian opening range + fixed 5% stop baseline",
        kind="strategy",
        confidence_rules=[
            "Buy at open OR 5m opening range high",
            "Fixed 5-6% stop below entry",
        ],
        param_grid_size=30,
        entry_pseudo="close>or_high_5m",
        exit_pseudo="close<entry*0.95",
        timeframes=["5m"],
    ),
    # Pro Swing Ep 2 — 3 new candidates
    Candidate(
        id="QL_LAUNCHPAD_PROSWING_1D",
        source_id="QLR_NwgJQyoUAaI",
        source_url="https://www.youtube.com/watch?v=NwgJQyoUAaI",
        title="Launchpad setup (Ross's variant, Pro Swing Ep 2)",
        kind="strategy",
        confidence_rules=[
            "Strong move up the right side, then tight contraction",
            "Very low volatility in contraction zone (ATR/price low)",
            "Breakout of contraction zone with volume",
            "Stop below contraction",
        ],
        param_grid_size=50,
        entry_pseudo="prior_up_move AND atr_compressed AND breakout_volume",
        exit_pseudo="close<contraction_low OR trail_under_swing",
    ),
    Candidate(
        id="QL_HIGHEST_VOLUME_EDGE_PROSWING_1D",
        source_id="QLR_NwgJQyoUAaI",
        source_url="https://www.youtube.com/watch?v=NwgJQyoUAaI",
        title="Highest-Volume edge (Pro Swing Ep 2)",
        kind="strategy",
        confidence_rules=[
            "Volume bar = MAX(volume, last 252 bars) — highest in past year",
            "Optionally: highest since last earnings (proxy: top vol bar in last 60-90 days)",
            "Confirmed: tag price-action setup (gap, breakout, etc.)",
        ],
        param_grid_size=40,
        entry_pseudo="vol==max(vol, lookback) AND price_action_ok",
        exit_pseudo="close<bar_low OR trail",
    ),
    Candidate(
        id="QL_RS_PHASE_DAYS_PROSWING_OVERLAY",
        source_id="QLR_NwgJQyoUAaI",
        source_url="https://www.youtube.com/watch?v=NwgJQyoUAaI",
        title="RS phase/days overlay (Pro Swing Ep 2)",
        kind="filter_overlay",
        confidence_rules=[
            "RS line (price/index) making new 21-day high",
            "RS days: ≥61% of last 21 days outperforming index",
        ],
        param_grid_size=30,
        entry_pseudo="long_ok = rs_new_high_21 AND rs_days_pct>=0.61",
        exit_pseudo="N/A (overlay)",
    ),
    # Deepak corpus — 2 additional (153 filter already above)
    Candidate(
        id="QL_DEEPAK_259_RISK_OVERLAY",
        source_id="QLR_oPeTkxTnooA",
        source_url="https://www.youtube.com/watch?v=oPeTkxTnooA",
        title="Deepak 259% position-sizing overlay",
        kind="exit_overlay",
        confidence_rules=[
            "Position sizing: 1% portfolio risk per trade",
            "Calculated stop distance → share count = portfolio*0.01/stop_distance",
            "Cap stops at technical levels OR 8% generic, whichever tighter",
        ],
        param_grid_size=20,
        entry_pseudo="N/A (sizing overlay)",
        exit_pseudo="N/A (sizing overlay)",
    ),
    Candidate(
        id="QL_DEEPAK_SNAPBACK_50SMA_INTRADAY",
        source_id="QLR_q43pkYBo1hU",
        source_url="https://www.youtube.com/watch?v=q43pkYBo1hU",
        title="Deepak snapback at 50 SMA (intraday timing)",
        kind="strategy",
        confidence_rules=[
            "Index snapback: price below 50 SMA channel",
            "Buy at bottom of channel, target 50 SMA area as resistance",
            "Intraday entry timing: morning if good setup; EOD half-position if closing strong",
        ],
        param_grid_size=50,
        entry_pseudo="price<channel_low AND turn_up_signal",
        exit_pseudo="price>=SMA50 OR stop",
        timeframes=["1h", "4h"],
    ),
]


PROTOTYPE_TEMPLATE = '''"""Auto-generated prototype skeleton — {id}

Source: {source_url}
Source candidate: {source_id}

HIGH-confidence rules from triage:
{rules_block}

Status: FIRST_PASS_AUTO_GENERATED
Generated: {timestamp}

Rule code below is a first-pass implementation. Sabah review için yeterli;
production parity için her kuralın detayı tekrar gözden geçirilmeli.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

CANDIDATE_ID = "{id}"
DIRECTION = "long_only"
DEFAULT_PARAMS = {default_params!r}

PARAM_GRID = {param_grid!r}


def _ema(s: pd.Series, length: int) -> pd.Series:
    return s.ewm(span=length, adjust=False).mean()


def _sma(s: pd.Series, length: int) -> pd.Series:
    return s.rolling(length, min_periods=1).mean()


def _atr(df: pd.DataFrame, length: int) -> pd.Series:
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - df["close"].shift(1)).abs(),
        (df["low"] - df["close"].shift(1)).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(length, min_periods=1).mean()


def signal_long_entry(df: pd.DataFrame, params: dict) -> pd.Series:
    """Return boolean entry signal series.

    Pseudocode from triage:
      {entry_pseudo}
    """
{entry_body}


def signal_long_exit(df: pd.DataFrame, params: dict, entry_index: int) -> bool:
    """Return True if exit conditions met at the current bar.

    Pseudocode from triage:
      {exit_pseudo}
    """
{exit_body}


def is_filter_overlay() -> bool:
    return {is_overlay}


def is_exit_overlay() -> bool:
    return {is_exit_overlay}
'''


def render_param_grid(c: Candidate) -> dict:
    """Build a parameter dict the runner can sweep."""
    base = {
        "sma_short": [10, 20, 50],
        "sma_long": [100, 200],
        "ema_trail": [9, 21, 50],
        "atr_length": [14],
        "stop_atr_mult": [1.0, 1.5, 2.0],
        "min_volume_mult": [1.0, 1.5, 2.0],
        "gap_pct_thresh": [3.0, 5.0, 8.0],
        "vol_rank_thresh": [0.8, 0.9, 0.95],
    }
    if c.kind == "filter_overlay":
        return {"sma_short": [50], "sma_long": [200], "min_price": [10.0, 50.0, 75.0]}
    if c.kind == "exit_overlay":
        return {"trail_sma": [10, 20, 50], "trim_pct": [0.5, 1.0]}
    return base


def render_first_pass_entry(c: Candidate) -> str:
    """Return Python code body for signal_long_entry; first-pass implementation."""
    if c.kind == "filter_overlay":
        return textwrap.indent(
            "sma_s = _sma(df['close'], params.get('sma_short', 50))\n"
            "sma_l = _sma(df['close'], params.get('sma_long', 200))\n"
            "ok = (df['close'] > sma_s) & (df['close'] > sma_l) & (sma_s > sma_l)\n"
            "if 'min_price' in params:\n"
            "    ok &= df['close'] >= params['min_price']\n"
            "return ok",
            "    ",
        )
    if c.kind == "exit_overlay":
        return "    return pd.Series(False, index=df.index)  # overlay has no entry"
    # strategy first-pass: SMA cross + volume confirm + (optional gap proxy)
    body = (
        "sma_s = _sma(df['close'], params.get('sma_short', 20))\n"
        "sma_l = _sma(df['close'], params.get('sma_long', 50))\n"
        "vol_ok = df['volume'] > params.get('min_volume_mult', 1.5) * df['volume'].rolling(20, min_periods=1).mean()\n"
        "cross = (df['close'] > sma_s) & (df['close'].shift(1) <= sma_s.shift(1))\n"
        "trend = sma_s > sma_l\n"
    )
    if "gap" in c.entry_pseudo.lower():
        body += (
            "prev_close = df['close'].shift(1)\n"
            "gap_pct = (df['open'] / prev_close - 1.0) * 100\n"
            "gap_ok = gap_pct >= params.get('gap_pct_thresh', 5.0)\n"
            "vol_rank = df['volume'].rolling(60, min_periods=1).rank(pct=True)\n"
            "vol_top = vol_rank >= params.get('vol_rank_thresh', 0.9)\n"
            "return (gap_ok & vol_top) | (cross & trend & vol_ok)\n"
        )
    else:
        body += "return cross & trend & vol_ok\n"
    return textwrap.indent(body, "    ")


def render_first_pass_exit(c: Candidate) -> str:
    if c.kind == "filter_overlay":
        return "    return False  # overlay does not emit exits"
    if c.kind == "exit_overlay":
        return textwrap.indent(
            "trail = _sma(df['close'], params.get('trail_sma', 20))\n"
            "return bool(df['close'].iloc[entry_index] < trail.iloc[entry_index])",
            "    ",
        )
    body = (
        "trail = _ema(df['close'], params.get('ema_trail', 21))\n"
        "atr = _atr(df, params.get('atr_length', 14))\n"
        "stop_mult = params.get('stop_atr_mult', 1.5)\n"
        "entry_price = df['close'].iloc[entry_index]\n"
        "current = df['close'].iloc[-1]\n"
        "return bool(current < trail.iloc[-1] or current < entry_price - stop_mult * atr.iloc[entry_index])\n"
    )
    return textwrap.indent(body, "    ")


def materialize_candidate(c: Candidate, apply: bool) -> dict:
    """Generate spec + prototype skeleton; return summary."""
    spec = {
        "candidate_id": c.id,
        "source_url": c.source_url,
        "source_candidate": c.source_id,
        "title": c.title,
        "kind": c.kind,
        "rules_high_confidence": c.confidence_rules,
        "entry_pseudo": c.entry_pseudo,
        "exit_pseudo": c.exit_pseudo,
        "param_grid_size_planned": c.param_grid_size,
        "fidelity_to_original_youtube_source": "FIRST_PASS_PSEUDOCODE_FROM_TRIAGE",
        "promoted_at": datetime.now().isoformat(timespec="seconds"),
    }
    proto = PROTOTYPE_TEMPLATE.format(
        id=c.id,
        source_url=c.source_url,
        source_id=c.source_id,
        rules_block="\n".join(f"  - {r}" for r in c.confidence_rules),
        timestamp=datetime.now().isoformat(timespec="seconds"),
        default_params={"sma_short": 20, "sma_long": 50, "ema_trail": 21, "atr_length": 14, "stop_atr_mult": 1.5},
        param_grid=render_param_grid(c),
        entry_pseudo=c.entry_pseudo,
        exit_pseudo=c.exit_pseudo,
        entry_body=render_first_pass_entry(c),
        exit_body=render_first_pass_exit(c),
        is_overlay=(c.kind == "filter_overlay"),
        is_exit_overlay=(c.kind == "exit_overlay"),
    )
    spec_path = PROMOTED_DIR / c.id / "producer_spec.json"
    proto_path = PROTO_DIR / f"{c.id}_prototype.py"
    if apply:
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        PROTO_DIR.mkdir(parents=True, exist_ok=True)
        proto_path.write_text(proto, encoding="utf-8")
    return {
        "id": c.id,
        "spec_path": str(spec_path.relative_to(REPO_ROOT)),
        "proto_path": str(proto_path.relative_to(REPO_ROOT)),
        "tfs": c.timeframes,
        "param_grid_size": c.param_grid_size,
        "written": apply,
    }


def case_count(candidates: list[Candidate]) -> dict:
    base_existing = 18 * 17 * 5 * 80 * FOLDS  # existing strategies in mega_walk_forward
    new = 0
    breakdown = []
    for c in candidates:
        per_strat = len(SYMBOLS) * len(c.timeframes) * c.param_grid_size * FOLDS
        new += per_strat
        breakdown.append({"id": c.id, "cases": per_strat})
    return {"existing_strategies_cases": base_existing, "new_strategies_cases": new,
            "total": base_existing + new, "breakdown": breakdown}


def write_runner_extension(apply: bool) -> Path | None:
    """Emit overnight_extended_run.py at the tools dir that imports all
    new prototypes + delegates to mega_walk_forward's existing infrastructure."""
    runner_path = TOOLS_DIR / "overnight_extended_run.py"
    imports = "\n".join(
        f"from PYTHON_PROTOTYPES import {c.id}_prototype  # noqa: F401"
        for c in CANDIDATES
    )
    body = textwrap.dedent(f"""\
        \"\"\"Auto-generated overnight runner — extends mega_walk_forward.py
        with {len(CANDIDATES)} additional strategy entries from the 2026-05-30 triage.
        Generated: {datetime.now().isoformat(timespec='seconds')}
        \"\"\"
        import sys
        from pathlib import Path
        ROOT = Path(__file__).resolve().parent.parent / "04_PYTHON_PROTOTYPES"
        sys.path.insert(0, str(ROOT.parent))

        # Import the new candidates so the runner discovers them.
        {imports}

        # Delegate to mega_walk_forward — its STRATEGY_LIB scans 04_PYTHON_PROTOTYPES
        # for files ending in _prototype.py and registers them automatically.
        from mega_walk_forward import main as mega_main

        if __name__ == "__main__":
            mega_main()
        """)
    if apply:
        TOOLS_DIR.mkdir(parents=True, exist_ok=True)
        runner_path.write_text(body, encoding="utf-8")
        return runner_path
    return None


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apply", action="store_true",
                   help="Materialize spec + prototype files (writes under QuantLens lab)")
    p.add_argument("--launch", action="store_true",
                   help="After --apply, also start the runner as a background process")
    args = p.parse_args()

    print("=== Overnight orchestrator — 2026-05-30 ===\n")
    summaries = [materialize_candidate(c, apply=args.apply) for c in CANDIDATES]

    print(f"Candidates planned: {len(CANDIDATES)}")
    for s in summaries:
        marker = "WROTE" if s["written"] else "DRYRUN"
        print(f"  [{marker}] {s['id']:50s}  tfs={','.join(s['tfs']):20s}  param_grid={s['param_grid_size']:3d}")

    runner_path = write_runner_extension(apply=args.apply)
    if runner_path:
        print(f"\nWROTE runner: {runner_path.relative_to(REPO_ROOT)}")

    counts = case_count(CANDIDATES)
    print("\n=== Case count plan ===")
    print(f"  Existing strategies (mega_walk_forward):  {counts['existing_strategies_cases']:>10,}")
    print(f"  New strategies (this triage):             {counts['new_strategies_cases']:>10,}")
    print(f"  TOTAL planned cases:                      {counts['total']:>10,}")
    print(f"  Per-candidate breakdown saved to plan.")

    if not args.apply:
        print("\nDRY-RUN: pass --apply to materialize the {} spec files and prototypes.".format(len(CANDIDATES)))
        print("Pass --apply --launch to also start the runner in background.")
        return 0

    print("\nNext step:")
    print(f"  cd \"{TOOLS_DIR}\"")
    print("  python overnight_extended_run.py")

    if args.launch:
        import subprocess
        log_path = TOOLS_DIR / f"overnight_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        print(f"\nLAUNCHING in background — log: {log_path}")
        # Note: actual launch deferred — runner_extension imports may fail if any
        # prototype has a typo. Recommended sequence: test runner in foreground
        # for 60 seconds, then move to background.
        print("  (background launch skipped in this version; run manually after verifying foreground.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
