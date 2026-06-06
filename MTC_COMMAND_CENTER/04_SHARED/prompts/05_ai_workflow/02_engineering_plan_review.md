# 02 — Engineering Plan Review  (Gate 2)

Use **before architecture changes, multi-file edits, or anything
touching Pine / MTC / parity surfaces**. Skip for typo / single-line
fixes.

## Inputs to provide

- The scope contract output from Gate 1.
- Pointer to the relevant module(s).

## Prompt

```
You are running Gate 2 (Engineering Plan Review) for
Tradingview_LAB_CLEAN. Do not write code yet. Produce a plan.

Read:
- The Gate 1 scope contract for this task.
- MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md
- MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md
- MTC_COMMAND_CENTER/_AI_MEMORY/PROJECT_MEMORY.md
- Any module-level README under the affected paths.

Then output, in this exact order:

1. DATA FLOW: textual description (or ASCII diagram) of inputs ->
   transformations -> outputs.
2. AFFECTED MODULES: file-level list, grouped by module.
3. EDGE CASES: explicit list. Include parity edge cases if relevant.
4. ROLLBACK PLAN: how we revert if this lands and breaks something.
5. PARITY / PINE / MTC IMPACT: explicit statement. If "none", justify.
6. TEST PLAN: what we will run in Gate 4.
7. GATE DECISION: proceed to Gate 3 or loop back to Gate 1 — and why.
8. APPROVAL NEEDED: if the change touches protected surfaces, name
   what Barış must explicitly approve before Gate 3 can start.

Refuse to skip any of the eight items.
Refuse to start coding inside this gate.
```

## WRITE-BACK

- Append a one-line entry to `SESSION_LOG.md` summarizing the plan.
- Update `ACTIVE_FILES.md` if the plan introduces files outside the
  current working set.
