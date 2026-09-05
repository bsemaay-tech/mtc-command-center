# Autonomy Authorization

Owner decisions OD-20260905-4 and OD-20260905-5, direct instructions 2026-09-05. Single source for
ask-vs-autonomous routing. Entries state existing permission or retained approval gate; no
entry creates new operation authority.

| Area | Existing permission | Retained approval gate |
|---|---|---|
| Local Git commits | **EXISTING PERMISSION:** Create ordinary forward local commits for authorized owned scope, including non-accepting candidates, fixes, and approved evidence/test-fixture alignment. | **RETAINED APPROVAL GATE:** These are checks the agent performs, not owner questions: exact paths, feature branch, hooks, staging, foreign-edit preservation, no amend/reset/force-push/destructive cleanup. Future explicit owner restriction wins. |
| Inspection and QA | **EXISTING PERMISSION:** Inspect dependencies, run scoped checks, reproduce defects, and update evidence/status. | **RETAINED APPROVAL GATE:** No execution outside task authority and no new behavior, path, economics, production facts, threshold, or schema. |
| Package repair and reseal | **EXISTING PERMISSION:** Within an already-approved package's behavior and path ceilings, perform necessary defect, test, and evidence repairs; reseal; and regenerate, archive, or restore the same-scope baseline. Prior numeric repair, reseal, and run limits are internal Lead checkpoints that the Lead may extend on concrete evidence without asking the owner. Future consolidated repair packets inside those bounds need no further approval. | **RETAINED APPROVAL GATE:** Record every actual round/run and its evidence. Change the hypothesis or evidence before retrying a failed attempt; never make an identical blind retry. New behavior, paths, economics, production facts, or package scope still require owner approval. |
| Safe lanes | **EXISTING PERMISSION:** Continue bounded independent lanes; delegate within included isolated subscriptions; use cheapest capable route. | **RETAINED APPROVAL GATE:** Exact model/audit requirements, mandatory tests, Lead acceptance, current-head protected CI, and provider policy remain binding. |
| Evidence and handoff | **EXISTING PERMISSION:** Record truthful status, evidence, blockers, `NEXT ACTION`, and `WAITING FOR OWNER`/`Nothing`. | **RETAINED APPROVAL GATE:** No acceptance, completion, promotion, or live-trading implication without required independent evidence. |
| P012 | **EXISTING PERMISSION:** Complete necessary same-scope repair, proof, reseal, and baseline work within its already-approved behavior and path ceilings. | **RETAINED APPROVAL GATE:** Item 4 `NONE_KEEP_REFUSED` stays refused; P012 cannot publish it. |
| Push, PR, merge | **EXISTING PERMISSION:** None added by this decision. | **RETAINED APPROVAL GATE:** Push/PR/merge only under prior standing permission and after package acceptance, required audits, up-to-date head, and protected CI green. |
| Ask owner | **EXISTING PERMISSION:** Resolve known facts independently; send one consolidated recommendations-first batch only for material gates below. | **RETAINED APPROVAL GATE:** Ask for new behavior/path scope, economics/strategy/production facts or thresholds; audit waiver/model substitution; host/deploy/credentials/authenticated exchange/TESTNET/mainnet/ARM/orders/wallet/transfers; external PAYG/new spend; irreversible deletion/history rewrite; or foreign-ownership conflicts. A future explicit owner restriction always wins. |

## Routing

- Claude Pro first; Claude Max only as exact-audit subscription fallback. Preserve exact model.
- Keep Gemini/current policy and economical subscription routing.
- No authorization for live trading, deployment, credentials, authenticated host/exchange contact,
  TESTNET/mainnet, ARM, orders, wallet/transfers, new spend, or history rewrite.
