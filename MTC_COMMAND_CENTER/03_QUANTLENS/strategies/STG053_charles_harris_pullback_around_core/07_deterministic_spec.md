# Deterministic Spec — Charles Harris Pullback / Swing-Around-Core

> Source: YouTube `NNGCxRmyNZYqNrJ` (Charles Harris, PM at O'Neil Capital).
> Re-triaged 2026-06-04 from `11_TRIAGE` cluster Stg107-113 (7 setups, shared
> transcript). Pullback family — overlaps STG024/025/029/041/042; distinct in the
> core-management layer.

## Overlay rules (must hold for ALL setups)
- **General market in an uptrend** (don't buy weakness in a topping/down market).
- **Stock in an uptrend**: higher highs / higher lows, supported by a **rising 50DMA**.
- Buy weakness only *in the context of a rising trend*; require conviction + liquidity.

## The 7 setups
1. **FIRST_PULLBACK_50DMA** — first pullback to the rising 50DMA after a breakout → buy.
2. **21EMA_PULLBACK_ADDON** — pullback to the 21EMA → add to an existing position.
3. **PRIOR_BASE_TOP_SUPPORT_PULLBACK** — pullback to a prior base top (now support) → buy.
4. **REVERSE_PYRAMID_PULLBACK_SCALEIN** — scale in (largest first / as confirmed) on
   pullbacks to support.
5. **SWING_AROUND_CORE** — hold a **core** in a big winner; **sell into strength** when
   extended, **buy back / add into weakness** at support. Recover shares sold higher.
6. **UPSIDE_REVERSAL_PULLBACK** — buy the upside-reversal bar off a support level.
7. **WEEKLY_SHAKEOUT_CONFIRMATION_GUARD** — use the weekly chart shakeout/reclaim as a
   confirmation guard before adding.

## Entry / risk / exit skeleton
- **Entry:** price pulls back to a defined support (50DMA / 21EMA / prior base top /
  pivot) within an uptrend and shows a reversal → buy/add.
- **Pyramid:** add at successive supports while trend intact (reverse pyramid sizing).
- **Stop:** below the pullback low / below the support being defended.
- **Exit/trim:** sell into strength when extended; exit core on technical sell signals
  (loss of 50DMA / trend break).

## Reusable components for MTC
- Multi-support pullback detector (50DMA/21EMA/base-top/pivot), rising-50DMA trend
  gate, core-position manager (trim strength / add weakness), reverse-pyramid sizing,
  weekly shakeout confirmation guard.

## Lessons (keep)
- All big winners pull back to the 50DMA multiple times — use those, don't fear them.
- Buying weakness needs an uptrend context; the same overlay rules apply to buying
  strength.
- Swing around a core: let the core ride the multi-year move, harvest the wiggles.

## Risks for backtesting
- "Extended" / trim timing is discretionary → define objectively (e.g. % above 21EMA).
- Core-management adds path dependence; model fills/sizing carefully.

## Disposition
CANDIDATE (pullback methodology, 7 setups). Research-only, not prototyped.
