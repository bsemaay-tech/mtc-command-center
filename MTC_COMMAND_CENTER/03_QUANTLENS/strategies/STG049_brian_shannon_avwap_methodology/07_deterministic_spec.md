# Deterministic Spec — Brian Shannon AVWAP Methodology

> Source: YouTube `UmLa9FAlMgw` (Brian Shannon, CMT — author of the AVWAP book).
> Re-triaged 2026-06-04 from `11_TRIAGE` cluster Stg096-101 (6 AVWAP setups, shared
> transcript). Overlaps existing avwap_brian set (STG004-007) — these 6 setups are
> distinct/more complete; cross-check before prototyping to avoid duplication.

## Core concept
- **AVWAP** (Anchored VWAP) = VWAP anchored to a significant event bar (earnings,
  gap day, YTD/Jan 1, COVID low, swing high/low). It is time+volume+price → a
  reference superior to SMA/EMA for "who is in control".
- **Above AVWAP = buyers in control; below = sellers; oscillating = balance.**
- **Confluence ("breadcrumbs")**: stack AVWAP with 5DMA, 20/50/200 DMA, and 2/3
  retracement / Fib. More aligned references = higher-quality level.
- **5DMA = primary intermediate trend gate**: do NOT buy if the 5-day MA is declining.
- **MA stack**: prefer 20>50>200 alignment; 200DMA rising for trust (institutional
  "can only buy above rising 200" tendency).

## The 6 setups
1. **5DMA_AVWAP_MOMENTUM_ENTRY** — 5DMA rising AND price reclaims/holds above a key
   AVWAP → long; stop below the reclaim low.
2. **AVWAP_GAP_PULLBACK_STRENGTH** — stock gaps up; don't chase. Let it settle; when
   it pulls back and **reclaims the daily VWAP** while not too extended → buy, stop
   below low of day.
3. **AVWAP_HANDOFF_TREND_CONTINUATION** — in an uptrend, support "hands off" from an
   older AVWAP anchor to a newer one (e.g. last earnings AVWAP); buy the hold of the
   newer anchor.
4. **AVWAP_PINCH_BREAKOUT** — two meaningful AVWAPs **converge/pinch**; a break out of
   the pinch (with volume) → entry in breakout direction.
5. **BREAKAWAY_GAP_AVWAP_CONTINUATION** — a breakaway gap that **holds above the AVWAP
   anchored to the gap day** → continuation long; invalidation = close back below it.
6. **FAILED_AVWAP_TRAP** — price attempts to reclaim a key AVWAP and **fails** (rejects
   back below) → avoid longs / short candidate (bull trap).

## Entry / risk / exit skeleton
- **Entry:** setup trigger above the chosen AVWAP with confluence + rising 5DMA.
- **Stop:** below the low of day / below the reclaimed AVWAP (clear invalidation).
- **Exit/trail:** trail under rising AVWAP / 5DMA; exit on loss of the anchor or
  failed reclaim.

## Reusable components for MTC
- Multi-anchor AVWAP component (earnings/gap/YTD/swing), AVWAP-pinch (convergence)
  detector, AVWAP-reclaim entry, failed-reclaim guard, 5DMA trend gate, MA-stack
  regime filter, low-of-day stop.

## Lessons (keep regardless of mechanization)
- AVWAP answers "who is in control since the event that matters" — pick the anchor
  that the market cares about (earnings, the gap, the year's open).
- Don't chase gaps; let price come back to a reference and prove itself.
- Confluence of independent references beats any single line.
- A *failed* reclaim is information (trap) — as tradable as a successful one.

## Risks for backtesting
- **Anchor selection** is discretionary → fix an objective anchor rule per backtest
  (e.g. "AVWAP from the most recent earnings").
- **Repaint/lookahead**: compute AVWAP only up to the closed bar; never use future
  volume; intraday AVWAP must exclude the forming bar at decision time.

## Disposition
CANDIDATE (methodology, 6 setups). Not prototyped, not promoted, research-only.
