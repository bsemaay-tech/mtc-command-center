# Deterministic Spec — Fishhook (EP Day-1 Retake) + Slingshot context

> Source: YouTube `c7ZSb2wNcOc` ("The Slingshot Pullback Pattern"). Re-triaged
> 2026-06-04 from `11_TRIAGE` Stg114. The companion **slingshot** setup (Stg159)
> already exists as **STG025**; this folder captures the distinct **fishhook**.

## Companion: Slingshot (already STG025)
- **4-EMA of HIGHS** crossover, used as an objective, scannable pullback trigger
  (chosen specifically so it can be scanned). Buy the pullback that crosses back.
- Rationale: buying raw breakouts gets faded / slipped / stopped; the slingshot
  enters the pullback instead.

## Fishhook (this candidate)
- Context: an **episodic pivot** — a stock **gaps up and runs** (often a low-float
  new-high name that gaps the day after).
- **Day-1 retake**: after the EP day, price pulls in and then **retakes** the prior
  high / day-1 high → entry (the "hook").
- Price/auction logic over MAs: support is at **congestion points** (where buyers/
  sellers transacted), not merely at a 50DMA ("moving averages are overrated").

## Entry / risk / exit skeleton
- **Entry:** EP gap+run identified → wait for the pull-in → buy the reclaim of the
  day-1 high (the hook), avoiding the breakout-chase fill.
- **Stop:** below the hook low / below the retake level; cap absolute risk on big
  gappers (don't accept $10 of risk on a $10 gap).
- **Exit:** trail with the move; exit on failure of the retake.

## Reusable components for MTC
- EP (gap+run) detector; day-after retake trigger; 4-EMA-of-highs pullback (slingshot,
  see STG025); congestion/auction support levels; absolute-risk cap on gappers.

## Lessons (keep)
- Define setups with **objective, scannable** criteria (why the 4-EMA-of-highs).
- Entering the *retake* beats chasing the *breakout* (less slippage/fade).
- Think in auction terms: who controls price at congestion, not just MA lines.

## Risks for backtesting
- EP/gapper volatility + slippage must be modeled realistically.
- "Retake" and "congestion" need objective definitions to avoid hindsight.

## Disposition
CANDIDATE (fishhook EP). Slingshot companion = STG025. Research-only.
