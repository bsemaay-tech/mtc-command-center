# Deterministic Spec — Oliver Kell Price Cycle

> Source: YouTube `fYxSQvuwOQc` (Oliver Kell, US Investing Champion). Re-triaged
> 2026-06-04 from `11_TRIAGE` cluster Stg121-124. Companion wedge-pop/crossback
> already exists as **STG023**; this captures the full cycle + basin break + exit.

## Regime (objective)
- Indicators: **10 EMA (red)** + **20 EMA (blue)** only.
- **Green light (long)**: price above the EMAs. **Red light (short/flat)**: below.
- Scale exposure/aggressiveness by where you are in the cycle.

## The price cycle (state machine)
1. **Reversal extension** — price stretches far *below* the MAs (capitulation).
2. **Snapback** — rallies back to the MAs, often pulls back again (higher low).
3. **WEDGE_POP** — pushes up *through* the 10/20 EMA zone building a higher low →
   long entry (see STG023).
4. **EMA_CROSSBACK** — reclaim/cross back above EMAs (re-entry/confirm; STG023).
5. **BASIN_BREAK** — breakout from a rounded basin/base after the snapback.
6. **WEDGE_DROP** — exhaustion wedge rolling over → **exit / short** signal.

## Entry / risk / exit
- **Entry:** wedge pop / basin break in a green-light (above-EMA) regime.
- **Stop:** below the higher low / below the EMA zone reclaimed.
- **Exit:** wedge drop, or loss of the 10/20 EMA regime (flip to red light).

## Reusable components for MTC
- 10/20-EMA regime gate (green/red light), price-cycle state machine, wedge-pop
  entry, basin-break entry, wedge-drop exit, reversal-extension snapback entry.

## Lessons (keep)
- Trade with an objective regime overlay (above/below EMAs) — don't fight the light.
- Price moves in a repeatable cycle; name the stage you're in and act accordingly.
- Hold winners back to the moving averages; let the cycle, not emotion, time exits.

## Risks for backtesting
- Stage labeling needs objective triggers (e.g. "wedge pop = close > 10EMA after a
  higher low within N bars of touching it"). Compute on closed bars.

## Disposition
CANDIDATE (Kell cycle, 4 setups). Overlaps STG023. Research-only.
