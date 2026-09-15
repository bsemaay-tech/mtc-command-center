# 03 — Implementation Task  (Gate 3 — Implementer)

This gate is executed by the **IMPLEMENTER** (Claude Code CLI when Codex leads; Codex CLI when Claude leads). The lead's acceptance gate is Gate 5 — see `AGENTS.md` two-tier model.

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
- You (the implementer) may sub-delegate bounded mechanical work (single/few-file edits, schema/JSON, script writing) to DeepSeek or Grok via Cline CLI or `_deepseek_driver`, or to GLM via Z.AI Coding Plan — audit sub-agent results yourself before handing off to the lead; do not pass sub-agent reports up as your own verification. **GLM sub-delegation requires a routing record before dispatch** (classification · protected flag · model+provider · cheaper-model rationale · exact paths · budget · fallback · external API credits); use the decision tree in `AGENTS.md` §GLM SUPPLEMENTAL ROUTING to select the cheapest capable tier.
- Do **NOT** commit, push, merge, rebase, or run any destructive git operation (`reset --hard`, `clean -fdx`, `restore`, `stash drop`, branch deletion). Git sequencing is Lead-only, after an accepting Gate 5 audit, and only where explicitly authorized by Barış.

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
- Out-of-scope items noticed are factual inputs for the selected stage's `HANDOFF.md` during Gate 7.
