# Deterministic Spec — Gon Low-Float Momentum Day Trading

> Source: YouTube `hzwBJxkVCTKPpcX` (Gon, low-float small-cap day trader).
> Re-triaged 2026-06-04 from `11_TRIAGE` cluster Stg115-120 (6 setups, shared
> transcript). 100% technical: **price + volume + 9EMA + 21EMA only.**

## Universe / scan
- Price **$0.50-$100**, volume **>= ~1M**, **low float**, top momentum / pre-market
  movers (live momentum scanner). Volume is mandatory — skip big % moves on low volume.

## Core entry logic
- **Buy point IS the stop**: if it doesn't go your way immediately, you're out.
- Look for **strong demand**, price goes **sideways at the top of the bars**, **volume
  subsides** (dry-up), then **reclaims** → entry on the reclaim.

## The 6 setups
1. **HALT_MOMENTUM_CONTINUATION** — after a halt-up, resume of the up-move → continue.
2. **NEXT_DAY_LOW_FLOAT_CONTINUATION** — day-after continuation on a low-float runner.
3. **OG_BULL_FLAG_HIGH_TIGHT** — high-tight bull flag → breakout.
4. **SHORT_SQUEEZE_REVERSAL_BALL_UNDER_WATER** — washed-out low-float squeezes back up
   ("ball held under water" pops) → reversal long.
5. **STRONG_DEMAND_LOW_VOLUME_EMA_TOUCH** — pullback to 9/21 EMA on **dry volume**, then
   reclaim → long (most mechanizable).
6. **STRONG_DEMAND_SLOW_FADER_RECLAIM** — slow fade into a demand level then reclaim → long.

## Risk / exit
- Tight: stop at the buy point; size so a quick failure is a small loss.
- Exit into spikes / loss of 9EMA; momentum scalp (intraday).

## Reusable components for MTC
- Halt detector, low-float/float filter, pre-market momentum scanner, 9/21-EMA
  pullback-reclaim entry, volume-dry-up confirmation, high-tight-flag detector,
  squeeze-reversal trigger, buy-point-as-stop money management.

## Lessons (keep)
- Volume is non-negotiable; ignore big moves without it.
- Make the buy point the stop — instant invalidation keeps losses tiny.
- Strip the chart to price + volume + two EMAs; less is more.
- Process/psychology (stop revenge-trading) mattered more than new setups.

## Risks for backtesting
- Low-float scalping has severe slippage, halts, and borrow constraints — a naive
  backtest will be wildly optimistic. Model frictions aggressively; treat as
  research-only.

## Disposition
CANDIDATE (low-float momentum, 6 setups). High overfit/friction risk. Research-only.
