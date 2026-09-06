# Owner decisions — 2026-09-06 ~12:40 +03:00 (reply to OWNER_DECISION_SHEET_20260906.md)

Verbatim intent, recorded by the Lead. These supersede the sheet's open lines. The sheet is a draft reconciled here, not a form.

Lead-assigned ids for the DECISIONS.md fold (next free id after OD-20260906-1):
OD-20260906-2 = SYNTHETIC_ONLY milestone approved; OD-20260906-3 = Gemini 3.8 required Section-16 reviewer until P012 closes;
OD-20260906-4 = public-capture packet PREPARE_NOW (one final authorization request for the frozen scope);
OD-20260906-5 = Item-4 unsourced-fact dispositions (table below); OD-20260906-6 = P0-21 engineering-first process (no raw owner numbers);
OD-20260906-7 = autonomy rule (pending owner choices block only the exact operation). Already answered 2026-09-05 and unchanged:
`RESEAL23 = YES`, `INSTRUMENT_SCHEMA = RULE_PRICE_AND_NULL_MIN_QTY`, `ITEM4_EXISTING_OFFLINE_SOURCES = NONE_KEEP_REFUSED`.

| Key | Decision | Lead reading / consequence |
|---|---|---|
| `SECTION16_REVIEW_DISPATCH` | **YES_GEMINI_3_8_UNTIL_P012_CLOSED** | Gemini 3.8 Flash High is the required campaign reviewer for P0-12 until the package closes. No substitution to 3.7, no re-ask on clock windows. |
| `P0-12 SYNTHETIC_ONLY_MILESTONE` | **APPROVED** | Accept corrected-engine mechanics as a synthetic-only milestone via an explicit dependency/design amendment; unblocks downstream design/mechanical work. Production economics stay fail-closed. Not full production acceptance; grants no live-trading, deployment, credential, host, account, order, wallet, transfer, mainnet or PAYG authority. |
| `PUBLIC_CAPTURE_PACKET` | **PREPARE_NOW** | Prepare the exact read-only public-capture packet from official public sources only; no credentials, PAYG, host changes, deployment or trading. Internal QA first. One final authorization request only if governance genuinely requires approval of the exact frozen capture scope. Other work continues meanwhile. |
| `FEE_FIXED_COMPONENT_ZERO` | KEEP_REFUSED | |
| `FEE_MINIMUM_FEE_ZERO` | KEEP_REFUSED | |
| `FEE_ROUNDING_RULE` | KEEP_REFUSED | |
| `LIQUIDATION_FEE_CLASS` | KEEP_REFUSED_UNTIL_OFFICIAL_SOURCE | |
| `COST_EFFECTIVE_INTERVAL` | CAPTURE_FORWARD_AFTER_AUTHORIZED_CAPTURE | interval starts at the authorized capture moment; no history claim |
| `FUNDING_EFFECTIVE_INTERVAL` | CAPTURE_FORWARD_AFTER_AUTHORIZED_CAPTURE | same |
| `HUMAN_REVIEWER_FIELDS` | LEAVE_EMPTY_UNTIL_REAL_RECORDS_EXIST_AND_A_REAL_REVIEW_OCCURS | |
| Standing rule | Never ask the owner to assume production facts that should come from authoritative evidence. | |

## P0-21 (no raw numbers from the owner)

- Preserve decided initial rule `single_trade_loss_risk_unit_multiple_max = 1`.
- Preserve `day_trade_count_min = 30` as provisional policy v1.
- Preserve the instruction to measure divergence and gap behaviour before selecting limits.
- Do NOT equate the recorded 1% risk-per-trade / no-leverage rule with `stop_loss_ceiling`: identify the exact unit and field, explain the difference plainly, offer three risk-policy choices with consequences and one recommendation.
- Engineering defines: strategy-type taxonomy, normal-market-condition taxonomy, divergence metric, alignment method, gap formula, policy-version contracts.
- Measure actual strategy trade cadence; derive recommended swing/position counts and forward durations.
- Present fast / balanced / conservative evidence-policy profiles with one recommendation; ask the owner only for a genuine risk-appetite or waiting-time trade-off.
- Do not ask for values that can be calculated, measured, researched or chosen by engineering judgment. Reconcile every question against existing owner decisions first; never re-ask an answered decision.

## Autonomy

Continue every safe, authorized, dependency-independent lane in parallel. A pending owner choice blocks only the exact
operation needing it. Ask only for: a genuine risk/economic policy choice after recommendations; an exact bounded
external-operation authorization; production facts or human attestation only the owner can give. Every question carries:
plain explanation, consequence per option, one recommendation, exactly what is blocked. Always end with NEXT ACTION /
WAITING FOR OWNER (write "Nothing" when nothing genuinely requires the owner).
