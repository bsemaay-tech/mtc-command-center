# Strategy Detail Page — Redesign Prototypes

Throwaway static mockups for **SP-005** (see
`03_QUANTLENS/_user_guide/11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md`).

**These files are NOT loaded by the live dashboard.** They are hand-filled HTML
for choosing a direction. Open them directly in a browser.

| File | Direction | Sample data |
|---|---|---|
| `proto_A_tabbed.html` | Professional tabbed dashboard (Overview / Rules / Scorecard / Evidence / Source / Technical). Full IA. | 8 EMA Pullback (scored, no backtest yet) |
| `proto_B_scroll.html` | Single-scroll, `<details>` progressive disclosure. Small-screen fallback. | VWAP Bounce Scalp (blocked, under-documented → "Not defined yet" / N/A paths) |
| `proto_C_compact.html` | Verdict-first compact "peek" card (decision + ladder + gate bars only). For a list/hover view. | three strategies at different readiness |

All three demonstrate: human name + thesis header, 10-second decision strip,
readiness ladder (no single-score headline), 4 gate bars with N/A states,
machine-term → human-label terminology, debug fields collapsed.

**Decision (2026-06-03): single-scroll B selected** as the primary full-page
layout. A (tabbed) dropped. C (compact) may later become a list-row "peek" view,
not the detail page. The plan was revised to **v2** on top of B — see
`11_STRATEGY_DETAIL_PAGE_REDESIGN_PLAN.md` (adds QuantLens Verdict, Strategy
Taxonomy, Salvageable Ideas, English-only UI, three-wave delivery).

## v2 visual-direction prototypes (2026-06-03)

Three alternative looks of the **same v2 single-scroll content** (same example:
"VWAP Bounce Scalp"), to choose an aesthetic before Wave A coding. All English-only,
all with sticky summary + QuantLens Verdict + Taxonomy + review journey + Salvageable
Ideas + collapsed Technical details.

| File | Aesthetic | Feel |
|---|---|---|
| `proto_B2_clinical.html` | Light, whitespace, hairline dividers, QuantLens as a bordered "audit stamp" | Calm clinical audit report |
| `proto_B2_terminal.html` | Dark, cyan/amber accents, mono data | Bloomberg-style quant terminal |
| `proto_B2_editorial.html` | Light, rounded cards with colored left accent, badge-heavy | Friendly-pro dashboard |

**Decision (2026-06-03): terminal selected.**

## v3 terminal stage set (2026-06-03)

Chosen **terminal** direction, revised for 5 structural changes: merged
Verdict & Decision block, **one scoring system** (Scorecard, QuantLens references it,
no double scoring), Scorecard directly under the verdict and **click-to-expand**,
**TradingView-tester-style** backtest cases (video-settings + optimized, each with
settings/symbol/timeframe on one standard window), and **one page per journey stage**.

> CSS is **inlined** in each HTML (so they render when opened directly / in the
> preview — an external stylesheet would not load over `file://`). `proto_terminal.css`
> is kept only as the readable single-source copy of that theme.

| File | Journey stage | Example |
|---|---|---|
| `proto_terminal.css` | — | shared theme + components for the set below |
| `proto_B2_terminal.html` | Source checked (blocked) | VWAP Bounce Scalp |
| `proto_stage_rules_extracted.html` | Rules extracted | 8 EMA Pullback |
| `proto_stage_testability.html` | Testability confirmed | RSI-2 Mean Reversion |
| `proto_stage_backtested.html` | Backtested (TV cases) | Donchian Breakout |
| `proto_stage_promotion.html` | Promotion review (TV cases) | Snapback 50 SMA |

The earlier `proto_B2_clinical/editorial` and v1 `proto_A/B/C` are superseded;
keep for reference or delete. The v3 terminal set is the sign-off target for Wave A.
