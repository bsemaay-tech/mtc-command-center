# Deterministic Spec — David Ryan Price-Volume-Stage

> Source: YouTube `eWtY7uoJL_0` (Market Wizard David Ryan, 3x US Investing
> Champion). Re-triaged 2026-06-04 from `11_TRIAGE` Stg104. CANSLIM school. The
> highest-value, most reusable piece is the **price-volume accumulation filter**.

## Core idea: price + volume tell the story
"Eliminate everything else — just price and volume."

- **Accumulation (uptrend) signature:** advances on **higher** volume, pullbacks on
  **lower** volume; up moves expand volume, sideways/declines contract it.
- **Distribution (topping) signature:** the opposite — weak rallies on light volume,
  declines on big volume; rising-then-falling average daily volume; climax volume.
- **Volume spikes** are key tells (breakouts and climaxes).
- **Base pattern:** volume **dries up** during consolidation, then a **huge volume
  spike** launches the breakout; series of bases → measured moves.
- **Stage filter:** MAs in uptrend and price above MA before buying (Weinstein-style).

## Reusable components for MTC (primary value)
- **Price-volume accumulation/distribution confirmation filter** (up-volume vs
  down-volume balance) — usable as a confirmation across breakout strategies.
- Base/consolidation + volume-dry-up detector; volume-spike breakout trigger.
- Climax/distribution exit guard.

## Entry / exit skeleton
- Buy base breakout confirmed by a volume spike, in a stage-2 uptrend (price above
  rising MAs) with prior accumulation signature.
- Sell into climax/distribution (volume up on down days) or breakdown of base.

## Lessons (keep)
- Most signal is in price + volume; indicators are secondary.
- Volume dry-up before a breakout = supply exhausted; the spike confirms demand.
- The same characteristics repeat in the greatest winners (CANSLIM precedent).
- "The battle is with yourself" — process and discipline over prediction.

## Risks for backtesting
- Define "higher/lower volume" objectively (e.g. vs 50-day average) to avoid
  hindsight. Compute on closed bars only.

## Disposition
CANDIDATE (confirmation methodology + base breakout). Not prototyped, research-only.
