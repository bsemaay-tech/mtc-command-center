# Autonomy Authorization

Owner decision OD-20260905-4, direct instruction 2026-09-05 ~21:33. Single source for
ask-vs-autonomous routing. Entries state existing permission or retained approval gate; no
entry creates new operation authority.

| Area | Existing permission | Retained approval gate |
|---|---|---|
| Local Git commits | **EXISTING PERMISSION:** Create ordinary forward local commits for authorized owned scope, including non-accepting candidates, fixes, and approved evidence/test-fixture alignment. | **RETAINED APPROVAL GATE:** These are checks the agent performs, not owner questions: exact paths, feature branch, hooks, staging, foreign-edit preservation, no amend/reset/force-push/destructive cleanup. Future explicit owner restriction wins. |
| Inspection and QA | **EXISTING PERMISSION:** Inspect dependencies, run scoped checks, reproduce defects, and update evidence/status. | **RETAINED APPROVAL GATE:** No execution outside task authority; no scope, behavior, threshold, schema, or repair-cap expansion. |
| Safe lanes | **EXISTING PERMISSION:** Continue bounded independent lanes; delegate within included isolated subscriptions; use cheapest capable route. | **RETAINED APPROVAL GATE:** Exact model/audit requirements, Lead acceptance, repair limits, and provider policy remain binding. |
| Evidence and handoff | **EXISTING PERMISSION:** Record truthful status, evidence, blockers, `NEXT ACTION`, and `WAITING FOR OWNER`/`Nothing`. | **RETAINED APPROVAL GATE:** No acceptance, completion, promotion, or live-trading implication without required independent evidence. |
| P012 | **EXISTING PERMISSION:** Correct approved fixture/metadata alignment and make authorized local forward commits within approved repair scope and repair cap, not a numeric commit cap. | **RETAINED APPROVAL GATE:** Item 4 `NONE_KEEP_REFUSED` stays refused; P012 cannot publish it. |
| Push, PR, merge | **EXISTING PERMISSION:** None added by this decision. | **RETAINED APPROVAL GATE:** Push/PR/merge only under prior standing permission and after package acceptance, required audits, up-to-date head, and protected CI green. |
| Ask owner | **EXISTING PERMISSION:** Resolve known facts independently; send one consolidated recommendations-first batch for material unknowns. | **RETAINED APPROVAL GATE:** Ask for new economics/strategy/production facts or thresholds; protected behavior/path expansion; explicit baseline/reseal/run-limit changes; audit waiver/model substitution/repair-cap extension; host/deploy/credentials/authenticated exchange/TESTNET/mainnet/ARM/orders/wallet/transfers; external PAYG/new spend; irreversible deletion/history rewrite; foreign-ownership conflicts. |

## Routing

- Claude Pro first; Claude Max only as exact-audit subscription fallback. Preserve exact model.
- Keep Gemini/current policy and economical subscription routing.
- No authorization for live trading, deployment, credentials, authenticated host/exchange contact,
  TESTNET/mainnet, ARM, orders, wallet/transfers, new spend, or history rewrite.
