# WP-P0-21 — the two decisions that are yours (2026-09-06 16:00, Lead: Claude Fable 5.1)

Plain language. Nothing here asks you for a raw number; engineering already fixed every unit, field, formula and count
(per your 12:40 decision). Source: `C:\tmp\P021_DESIGN_V21_AUDIT_20260906_1545` (design v2.1; Opus T0 review
**PASS-WITH-NITS** — all round-1 defects repaired, no measured number moved; Gemini corroboration runs after the Section-16
wave). Nothing here accepts WP-P0-21; `implementation_authorized` stays `false` either way.

Your two earlier rules are preserved exactly: `single_trade_loss_risk_unit_multiple_max = 1` and `day_trade_count_min = 30`
(provisional v1). The "1 % of the account, no leverage" rule is NOT the same thing as `stop_loss_ceiling` — the explainer
(`RISK_POLICY_EXPLAINER.md` §1–2) shows the difference with a worked example: 1 % caps how much money a strategy is *given*;
your rule B caps a trade to losing no more than it *said* it would risk; `stop_loss_ceiling` caps how much a trade may *say*
it risks. That third number is blank, so today rule B can reject nothing and live-gate precondition 10 reads
`BLOCKED — the lower loss-at-stop cap is undefined`.

## Decision 1 — how much of the account may ONE stop-out cost you? (risk appetite)

| Choice | What it allows / forbids | Consequence |
|---|---|---|
| **A. 0.50 % of equity per stop-out — RECOMMENDED** | Four consecutive stop-outs fit inside your 2 % daily limit; your existing 3-loss guard fires first, as designed | Equals the value already configured and deployed (`risk_pct_per_trade = 0.005`). Mints no new number. |
| B. 0.25 % | Eight consecutive stop-outs fit in the daily limit | Wide-stop strategies size down to ~1 % of equity and start hitting the minimum order size (more refusals, not more safety). |
| C. a formula: `max_daily_loss_pct ÷ max_consecutive_losses` (today 2 % ÷ 3 = 0.667 %) | Re-derives itself if you change either guard | Your per-trade ceiling silently moves when you change an unrelated setting — found after a loss, not before. |

- Unit/field: fraction of total account equity at the stop price, enforced as `stop_loss_ceiling_equity_fraction` (catalogue key), the
  upper half of `P021.BASIC_FAILURE_FLOOR`. Coherent range is bounded above at 0.667 % by two guards you already have.
- **What your answer unblocks:** the `stop_loss_ceiling` half of the basic-failure floor and the open half of live-gate precondition 10.
- **What it does NOT unblock:** the swing/position minimum-trade counts (Decision 2) and thirteen other live-gate preconditions.
- **If you answer nothing:** A is recorded as policy **v1, provisional** (reversible, versioned, visible) exactly like `day_trade_count_min = 30`.

## Decision 2 — how long are you willing to WAIT per candidate strategy? (waiting-time appetite)

Measured, not assumed: 253 trade series from 42 files; 62 day-class series trade 0.0426–29.8 trades/day (a 700-fold spread), so
"30 forward trades" means 1 day for the fastest and 704 days for the slowest. The profiles differ mainly in one median wait per class.

| Profile | Median wait: day → swing → position (†position = extrapolated, no measured series) | Characteristic failure |
|---|---|---|
| fast | 2 wk → 13 wk → 39 wk † | **false pass** — twelve forward trades inside one market mood can look like proof |
| **balanced — RECOMMENDED** | 4 wk → 17 wk → 52 wk † | five of fourteen measured swing strategies still wait longer than the period |
| conservative | 6 wk → 25 wk → 78 wk † | **false fail** — 31.5 % of swing series excluded; position strategies effectively unevaluable |

- **What your answer unblocks:** the swing and position halves of the basic-failure floor and all seven forward-evidence numbers
  (the whole `forward_evidence_refusal` block). The divergence and gap groups stay measure-first and wait on measurement, not on you.
- **If you answer nothing:** balanced is recorded as policy **v1, provisional**; the checker then refuses only on the two measure-first
  groups instead of on all fourteen numbers.

## How to answer (one line each, or nothing)

`P021_DECISION_1 = A | B | C` (recommended A)
`P021_DECISION_2 = fast | balanced | conservative` (recommended balanced)

Both are reversible: a change is a new hashed `strategy_type_policy_set` version plus fresh evidence — the rule decisions 129/130
already require. No live trading, deployment, credential, host, order or account action follows from either answer.
