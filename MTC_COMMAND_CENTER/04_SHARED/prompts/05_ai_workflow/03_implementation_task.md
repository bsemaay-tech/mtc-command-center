# 03 - Implementation Task  (Gate 3 - Implementer)

This gate is executed by the **IMPLEMENTER** (Claude Code CLI when Codex leads; Codex CLI when Claude leads). The lead's acceptance gate is Gate 5 - see `AGENTS.md` two-tier model.

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
  a gate violation - stop and report.
- Minimal diff. No unrelated edits. No speculative features. No
  premature abstractions.
- No new dependencies without explicit approval.
- Cross-check DO_NOT_TOUCH.md before each edit.
- Default to writing no comments. Only add a comment if the WHY is
  non-obvious.
- Errors only at real boundaries. No defensive try/except around code
  that cannot fail.
- Match existing code style. Look at neighbouring files first.
- You (the implementer) may sub-delegate bounded mechanical work (single/few-file edits, schema/JSON, script writing) to DeepSeek or Grok via Cline CLI or `_deepseek_driver` - audit sub-agent results yourself before handing off to the lead; do not pass sub-agent reports up as your own verification.
- Do **NOT** commit, push, merge, rebase, or run any destructive git operation (`reset --hard`, `restore`, `clean -fdx`, `stash drop`, branch deletion, `push --force`). Git sequencing is Lead-only, after the sequence: accepting G5, G6 if applicable, G7 handoff, and only where explicitly authorized by Barış.

Workflow:
1. Restate the scope and file whitelist in one line.
2. Make the edits.
3. Output a short diff summary: files touched, lines added/removed.
4. List anything you noticed but did NOT change (out-of-scope items).
   Do not silently fix them.
5. Hand off to Gate 4 (QA).

Refuse to claim "done" inside this gate. Done lives after an accepting
Gate 5, optional Gate 6, and Gate 7 handoff sequence.
```

## WRITE-BACK

- No memory updates inside Gate 3 itself.
- Out-of-scope items noticed:
  - **Component-scoped:** go into `<component>/_AI_MEMORY/NEXT_STEPS.md` during Gate 7.
  - **Cross-component:** go into each affected component's `_AI_MEMORY/NEXT_STEPS.md` where relevant; root coordination entry in root `NEXT_STEPS.md` only when needed. Log to the most relevant component first; never route component findings directly to root.
  - **Global/policy:** go into root `NEXT_STEPS.md` during Gate 7.
