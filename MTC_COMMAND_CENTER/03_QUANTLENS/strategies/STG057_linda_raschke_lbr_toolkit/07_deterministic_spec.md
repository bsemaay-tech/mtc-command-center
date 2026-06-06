# Deterministic Spec — Linda Raschke (LBR) Mechanical Toolkit

> Source: YouTube `kTqKRi-j9kM` (Linda Bradford Raschke). Re-triaged 2026-06-04 from
> `11_TRIAGE` cluster Stg125-132 (8 setups/modules, shared transcript). Among the
> most mechanical / low-discretion material in the whole re-triage — high priority.

## Entry setups
- **THREE_BAR_BREAKOUT** — 3 bars with price **overlap** at the bottom (or top) of a
  swing = market coming into balance → breakout play in the resolved direction.
- **COIL_BREAKOUT_RANGE_EXPANSION** — contraction/coil precedes a **range-expansion**
  day; enter the expansion breakout (Crabel-adjacent; see STG026).
- **ROC2_REVERSAL** — 2-period Rate-of-Change reversal (momentum snap) for timing
  reversals at extremes.
- **BOX_MIDPOINT_RECLAIM** — market-profile **box** (2 points resistance, 2 support);
  reclaim of the **box midpoint** is constructive → entry.
- **PREV_DAY_HIGH_LOW_TAYLOR_RHYTHM** — Taylor trading technique: buy-day/sell-day
  rhythm referencing **previous day high/low**.

## Risk / exit modules (reusable across strategies)
- **ATR_VOLATILITY_EXIT_OVERLAY** — ATR-based trailing/exit on range-expansion days.
- **ADTR_POSITION_SIZING** — size positions by Average Daily True Range (volatility
  normalization).
- **EQUITY_CURVE_RISK_THROTTLE** — manage risk **off the equity curve**: when it rolls
  over, cut size; scale up when smooth. (Raschke managed risk primarily this way.)

## Entry / risk / exit skeleton
- **Entry:** 3-bar breakout / coil expansion / ROC reversal / box-midpoint reclaim.
- **Stop:** structural (swing/box) ; prefer not resting large stops — manage actively.
- **Exit:** ATR trail on expansion days; take profits into momentum exhaustion.
- **Sizing:** ADTR-normalized; throttle by equity-curve state.

## Reusable components for MTC (high value)
- 3-bar reversal/breakout pattern, coil→range-expansion detector, 2-period ROC
  reversal, box midpoint, Taylor prev-day H/L, ATR exit overlay, ADTR sizing,
  equity-curve risk throttle (money management).

## Lessons (keep)
- Manage risk by the **equity curve** and **volatility-normalized sizing**, not just
  per-trade stops.
- Markets come into **balance** (overlap/coil) before expansion — trade the resolution.
- Mechanical, repeatable patterns + strict sizing beat prediction.

## Risks for backtesting
- Some setups need intraday / market-profile data; ensure objective definitions.
- Originally futures-oriented; validate on the target universe.

## Disposition
CANDIDATE (LBR toolkit, 8 setups/modules). High reuse value. Research-only.
