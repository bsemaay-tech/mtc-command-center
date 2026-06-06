# 03 — Implementation Task  (Gate 3)

Use **only after Gate 1 (and Gate 2 if non-trivial) have passed**.

## Inputs to provide

- Gate 1 scope contract.
- Gate 2 plan, if produced.
- Whitelist of files allowed.

## Prompt

```
You are running Gate 3 (Implementation) for Tradingview_LAB_CLEAN.

Constraints:
- Stay inside the Gate 1 file whitelist. Editing anything outside it is
  a gate violation — stop and report.
- Minimal diff. No unrelated edits. No speculative features. No
  premature abstractions.
- No new dependencies without explicit approval.
- Cross-check DO_NOT_TOUCH.md before each edit.
- Default to writing no comments. Only add a comment if the WHY is
  non-obvious.
- Errors only at real boundaries. No defensive try/except around code
  that cannot fail.
- Match existing code style. Look at neighbouring files first.

Workflow:
1. Restate the scope and file whitelist in one line.
2. Make the edits.
3. Output a short diff summary: files touched, lines added/removed.
4. List anything you noticed but did NOT change (out-of-scope items).
   Do not silently fix them.
5. Hand off to Gate 4 (QA).

Refuse to claim "done" inside this gate. Done lives after Gate 5 (or
Gate 7 for trivial scopes).
```

## WRITE-BACK

- No memory updates inside Gate 3 itself.
- Out-of-scope items noticed go into `NEXT_STEPS.md` during Gate 7.
