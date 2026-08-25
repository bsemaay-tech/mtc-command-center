# 07 — Handoff Update  (Gate 7)

**Mandatory before stopping**, regardless of sprint size.

This prompt updates the selected stage's existing `HANDOFF.md` plus only the
durable records triggered by the completed work.

## Prompt

```
You are running Gate 7 (Memory Write-Back) for Tradingview_LAB_CLEAN.

Actor: **Lead Orchestrator**, after the required audit tier acceptance
is verified. Do not execute this gate without the required tier
acceptance: for T0/T1/T2, a confirmed Gate 5 PASS (or PASS-WITH-NITS)
per the tier's auditor contract; for T3, the recorded implementer
self-verification replaces the model Gate 5. The implementer may supply
factual inputs (commit hashes, test results, exact file lists) to the
lead; final write-back content and authorized sequencing are
Lead-owned.

Do not create a new handoff or session journal.

Steps:

1. The selected stage's `HANDOFF.md` (always update)
   - Use `## [MODEL_NAME] YYYY-MM-DD — Topic`.
   - Record only current state: practical next actions, exact paths/commands,
     unresolved authorization, test evidence, and commit SHA.
   - Keep the file at or below 4 KiB; rotate stale detail to grep-on-demand
     history instead of growing another journal.

2. Root `DECISIONS.md` (update only if a sticky owner decision was made)
   - Add one dated linked summary; keep detailed wording in its source record.

3. Durable tracker/shared GitHub claim and `_AI_MEMORY/SESSION_LOCK.md` mirror
   (update only when applicable)
   - Before releasing the claim, reconcile current `master`, the work branch,
     and durable tracker state. `UNKNOWN` ownership or liveness is a stop.

Historical homes:
- `_AI_MEMORY/history/GLOBAL_HANDOFF.md` and
  `_AI_MEMORY/history/NEXT_STEPS.md` are read-only, search-on-demand archives.
- `_AI_MEMORY/SESSION_LOG.md` is retired; do not recreate or append it.

Report:
- List every handoff, decision, tracker, or claim file updated, with the exact
  change made to each.
- Suggested next gate / next prompt for the following session.
```

## WRITE-BACK

This *is* the write-back. Nothing further required.
