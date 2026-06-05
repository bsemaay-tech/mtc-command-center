# MTC_V2 Indicator Inventory (read-only extraction)

RESEARCH-003 deliverable. Extracted **2026-06-05 (Claude)** from
`01_MTC_PROJECT/01_PINE/MTC_V2.pine` (2079 lines) WITHOUT modifying the `.pine`
(HARD denylist) and WITHOUT ingesting the full file — derived from its `ta.*`
primitive calls and its plot/variable titles (`group=` families + named feature
flags).

> **Not the registry.** `05_REGISTRY/INDICATOR_REGISTRY.json` is *generated* by
> `03_QUANTLENS/tools/build_strategy_research_registry.py` (AGENTS.md: do not
> hand-edit generated registries). This file is a reference inventory; feed it
> into the generator's curated indicator seed if/when the registry should carry
> the full MTC_V2 set. Today the registry holds 27 indicators seeded from
> strategy references; the items below marked **(new)** are present in MTC_V2 but
> may not yet be in that seed.

## Computational indicators (from `ta.*` primitives + feature flags)

| Indicator | MTC_V2 evidence (primitive / feature flag) | Role in MTC_V2 | Category |
|---|---|---|---|
| Supertrend | `supertrend_line`, plot "ST Line" (custom-coded, not `ta.supertrend`) | primary **signal producer** | trend / signal |
| MACD | `ta.macd` ×3; `macd_line/signal/hist`, `macd_cross_*`, `macd_regime_*`, `macd_zero_dist_ok`, `macd_htf_line`, `prev_macd_hist` | momentum **entry gate** + HTF confirmation | momentum |
| ADX / DMI | `ta.dmi` ×2 → `adx`, `adx_ok` | trend-strength **entry gate** | trend strength |
| ATR | `ta.atr`; `sl_atr`, `tp_atr`, `sl_swing_atr`, `atr_floor_ok`, `atr_vol_floor_fast`, `atr_vol_floor_baseline` | volatility sizing → stops / targets / vol floor | volatility |
| MA filter | `ma_filter_line`, `ma_filter_long_ok`, `ma_filter_short_ok` (configurable MA over `ta.sma/ema/wma`) | trend **filter gate** | trend |
| MA slope | `ma_slope_line`, `ma_slope_ratio`, `ma_slope_long_ok`, `ma_slope_short_ok` | trend-slope **entry gate** | trend |
| McGinley Dynamic | `mcginley_line`, `mcginley_long_ok`, `mcginley_short_ok` | adaptive-MA **gate** | trend (adaptive) **(new)** |
| Choppiness / chop | `chop`, `chop_ok` | range/chop **guard** | regime / guard **(new)** |
| Donchian / Highest-Lowest | `ta.highest` ×4, `ta.lowest` ×3 | breakout / swing levels (stops, channels) | breakout |
| EMA / SMA / WMA / RMA | `ta.ema` ×2, `ta.sma` ×4, `ta.wma` ×3, `ta.rma` ×8 | moving-average building blocks (filters, smoothing, RSI/ATR internals) | moving average |
| HTF trend / HTF MACD | `htf_trend_line`, `macd_htf_line` | higher-timeframe **confirmation** | multi-timeframe |
| `ta.barssince` | ×2 | timing helper (re-entry / cooldown logic) | timing helper |

## Functional families (from `group=` input groups, not indicators)

`01 Global` · `02 Signal Producer` · `03 Entry Gates` (59 inputs) · `04 Position
Sizing` · `05 Exit Skeleton` · `06 Signal/Filter Exits` · `07 Time Exits` ·
`08 Guards` · `09 Signal Transform` · `10 Integrations` · `11 Visualization/
Performance`. These are the MTC pipeline roles each indicator plugs into, not
indicators themselves.

## Scope / honesty note

This is a **primitive- and flag-level** extraction: every row is grounded in a
real `ta.*` call or a named plot/variable in `MTC_V2.pine`. A line-by-line
semantic map of how each gate composes its primitives (exact lengths, sources,
boolean conditions) was deliberately NOT produced here to respect the
token-efficiency constraint and the `.pine` read-only rule. Items tagged
**(new)** — McGinley Dynamic, Choppiness — are the inventory gaps most likely
missing from the current 27-entry seed.
