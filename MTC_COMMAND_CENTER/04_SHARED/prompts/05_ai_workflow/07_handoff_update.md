# 07 - Handoff Update  (Gate 7)

**Mandatory before stopping**, regardless of sprint size.

This prompt does **not** create new handoff files. It updates the canonical
memory files for the route selected through `COMPONENT_ROUTER.md`; those files
may live in a component-local `_AI_MEMORY/` or the root `_AI_MEMORY/`.

## Prompt

```
You are running Gate 7 (Memory Write-Back) for Tradingview_LAB_CLEAN.

Actor: **Lead Orchestrator**, after Gate 5 (and Gate 6 if applicable) PASS is verified. Do not
execute this gate without a confirmed Gate 5 PASS (or PASS-WITH-NITS).
The implementer may supply factual inputs (commit hashes if authorized,
test results, exact file lists) to the lead; final write-back content and
authorized sequencing are Lead-owned. G7 must not require a future commit
hash - use the hash that exists at write-back time or omit the field.

Do NOT create new files at repo root. Update only the canonical memory files
for the applicable route (see COMPONENT_ROUTER.md Section 5).

## Route A: Component-scoped task

Update ONLY the affected component's _AI_MEMORY/. Do NOT touch root
GLOBAL_HANDOFF.md, NEXT_STEPS.md, ACTIVE_FILES.md, or SESSION_LOG.md.

1. <component>/_AI_MEMORY/CURRENT.md  (always update)
   - Current objective, phase, status, last session summary.

2. <component>/_AI_MEMORY/NEXT_STEPS.md  (always update)
   - Move completed items; add new items with [AI: ...] tags.

3. <component>/_AI_MEMORY/DECISIONS.md  (if a sticky decision was made)
   - Append D### entry with date + one-line rationale.

4. <component>/_AI_MEMORY/ACTIVE_FILES.md  (if working set changed)

5. SESSION_LOCK.md (root) - release if held.

## Route B: Cross-component task

Apply Route A for every affected component, then:

6. Root GLOBAL_HANDOFF.md - add ONE concise coordination entry only.
   Format: ## [MODEL_NAME] YYYY-MM-DD - Topic
   Root NEXT_STEPS.md - update only for cross-component next steps.

## Route C: Global/policy task

7. Root GLOBAL_HANDOFF.md  (always)
   Set fields:
   - Last updated, Updated by, Active project, Current objective,
     Current phase, Current blockers, Where to continue, Warnings.

8. Root NEXT_STEPS.md  (always)
9. Root DECISIONS.md  (if sticky decision)
10. Root ACTIVE_FILES.md  (if working set changed)
11. Root PROJECT_MEMORY.md  (if a stable repo fact changed)
12. SESSION_LOCK.md  (release if held)

Report:
- Route selected (A/B/C) and why.
- List of memory files updated, with the exact change made to each.
- Confirmation that no file outside the applicable _AI_MEMORY/ was
  modified inside this gate.
- Suggested next gate / next prompt for the following session.
```

## WRITE-BACK

This *is* the write-back. Nothing further required.
