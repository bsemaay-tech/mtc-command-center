# 07 - Handoff Update  (Gate 7)

**Mandatory before stopping**, regardless of sprint size.

This prompt does **not** create new handoff files. It updates the
canonical ones inside `MTC_COMMAND_CENTER/_AI_MEMORY/`.

## Prompt

```
You are running Gate 7 (Memory Write-Back) for Tradingview_LAB_CLEAN.

Actor: **Lead Orchestrator**, after Gate 5 (and Gate 6 if applicable) PASS is verified. Do not
execute this gate without a confirmed Gate 5 PASS (or PASS-WITH-NITS).
The implementer may supply factual inputs (commit hashes if authorized,
test results, exact file lists) to the lead; final write-back content and
authorized sequencing are Lead-owned. G7 must not require a future commit
hash - use the hash that exists at write-back time or omit the field.

Do NOT create new files. Update only the existing ones inside
MTC_COMMAND_CENTER/_AI_MEMORY/.

Steps:

1. GLOBAL_HANDOFF.md  (always update)
   Set fields:
   - Last updated:       <ISO date>
   - Updated by:         <model name + session label>
   - Active project:     <subproject name>
   - Current objective:  <one sentence>
   - Current phase:      <gate or milestone>
   - Current blockers:   <one line, or "none">
   - Where to continue:  <file path or gate to run next>
   - Warnings:           <parity / DO_NOT_TOUCH / approval-needed flags>

2. NEXT_STEPS.md  (always update)
   - Move completed items from "Immediate" to "Recently Closed" with
     date + short note + commit hash if any.
   - Add new "Immediate" items uncovered during this sprint
     (including out-of-scope items Gate 3 noticed but did not fix).

3. DECISIONS.md  (update IF a sticky decision was made)
   - Append a new D### entry with phase + one-line rationale.

4. ACTIVE_FILES.md  (update IF working set changed)
   - Add files now in active rotation.
   - Remove files no longer relevant.

5. PROJECT_MEMORY.md  (update IF a stable repo fact changed)
   - Layout change, new module, new contract, new policy doc, etc.
   - Do not log per-session noise here.

6. SESSION_LOCK.md
   - If you held a write lock, release it (set Status: unlocked).

Report:
- List of memory files updated, with the exact change made to each.
- Confirmation that no file outside _AI_MEMORY/ was modified inside
  this gate.
- Suggested next gate / next prompt for the following session.
```

## WRITE-BACK

This *is* the write-back. Nothing further required.
