# Autonomy Authorization

Owner decisions OD-20260905-4, OD-20260905-5, and OD-20260906-1. Single source for
ask-vs-autonomous routing. Entries state existing permission or retained approval gate; none
creates operation or acceptance authority.

| Area | Existing permission | Retained approval gate |
|---|---|---|
| Local Git commits | **EXISTING PERMISSION:** Create ordinary forward local commits for authorized owned scope, including non-accepting candidates, fixes, and approved evidence/test-fixture alignment. | **RETAINED APPROVAL GATE:** These are checks the agent performs, not owner questions: exact paths, feature branch, hooks, staging, foreign-edit preservation, no amend/reset/force-push/destructive cleanup. Future explicit owner restriction wins. |
| Inspection and QA | **EXISTING PERMISSION:** Inspect dependencies, run scoped checks, reproduce defects, and update evidence/status. | **RETAINED APPROVAL GATE:** No execution outside task authority and no new behavior, economics, production facts, threshold, schema, or path except a Package repair corrective path. |
| Package repair and reseal | **EXISTING PERMISSION:** Within an already-approved package behavior, perform necessary defect, test, and evidence repairs; reseal; and regenerate, archive, or restore its same-scope baseline. For a reproduced defect, the Lead may add the necessary local corrective paths, tests, verifier changes, and identity-only references without an owner re-ask. Prior numeric repair, reseal, and run limits remain internal Lead checkpoints extendable on concrete evidence. | **RETAINED APPROVAL GATE:** Before dispatch, record exact paths/ownership, original approved behavior, reproduced defect, invariants, and D026 RED/GREEN plan. Expected identity bytes come from an independent contract/counterfactual, never implementation output alone. Preserve actual round/run evidence and change the hypothesis before retrying. New features/packages, original behavior or numeric/economic/strategy values, and production facts still require owner approval. |
| Safe lanes | **EXISTING PERMISSION:** Continue bounded independent lanes; delegate within included isolated subscriptions; use cheapest capable route. | **RETAINED APPROVAL GATE:** Exact model/audit requirements, mandatory tests, Lead acceptance, current-head protected CI, and provider policy remain binding. |
| Evidence and handoff | **EXISTING PERMISSION:** Record truthful status, evidence, blockers, `NEXT ACTION`, and `WAITING FOR OWNER`/`Nothing`. | **RETAINED APPROVAL GATE:** No acceptance, completion, promotion, or live-trading implication without required independent evidence. |
| P012 | **EXISTING PERMISSION:** All three rows in `C:/tmp/P012_ITEM2_VERIFIER_SCOPE_DECISION_20260906_0056.md` are owner-approved: Item-2 verifier reachability/module binding, exit-sequence propagation, and the eight independently derived identity-only oracle refreshes. The Package repair rule governs necessary follow-on corrective scope. | **RETAINED APPROVAL GATE:** Preserve monetary/order/refusal invariants, archived old bytes, exact audits and Gemini, dependency gates, current-head protected CI, and independent Lead acceptance. Item 4 `NONE_KEEP_REFUSED` stays refused and cannot publish. |
| Push, PR, merge | **EXISTING PERMISSION:** None added by this decision. | **RETAINED APPROVAL GATE:** Push/PR/merge only under prior standing permission and after package acceptance, required audits, up-to-date head, and protected CI green. |
| Ask owner | **EXISTING PERMISSION:** Resolve known facts independently; the Lead decides evidenced same-package corrective paths under Package repair. Send one consolidated recommendations-first batch only for retained material gates. | **RETAINED APPROVAL GATE:** Ask for a new feature/package, behavior beyond the original approval, original numeric/economic/strategy values, production facts or thresholds; audit waiver/model substitution; host/deploy/credentials/authenticated exchange/TESTNET/mainnet/ARM/orders/wallet/transfers; external PAYG/new spend; irreversible deletion/history rewrite; or foreign-ownership conflicts. A future explicit owner restriction always wins. |

## Routing

- Claude Pro first; Claude Max only as exact-audit subscription fallback. Preserve exact model.
- Keep Gemini/current policy and economical subscription routing.
- No authorization for live trading, deployment, credentials, authenticated host/exchange contact,
  TESTNET/mainnet, ARM, orders, wallet/transfers, new spend, or history rewrite.

## Maximum useful throughput

- Target 4–6 actually `RUNNING` independent workers; Lead, CI, queued/completed work, and failed
  subscriptions do not count. Refill on completion or quiet-window end without owner prompting.
  Use 8–10 only when distinct authorized tasks and resources exist.
- Every lane records its output, exact read/write paths, dependency, provider/model, deadline, and
  stop condition. Use the cheapest capable included route and prioritize the critical path.
- During Gemini quiet windows, pause watched-repository/Git writers; use already-frozen read-only
  packets elsewhere. Preserve path isolation.
- Throughput never creates duplicate audits, busywork, path collisions, or waivers of tests,
  evidence, acceptance, permissions, safety, or audit requirements.
- Report shortfalls/provider idleness precisely: dependency, overlap, missing frozen packet,
  provider failure, runtime capacity, or no useful work. The current native worker limit of three is
  session capacity, not permanent repository policy.
