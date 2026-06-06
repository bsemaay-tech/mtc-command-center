# 04 — Adversarial Code Review  (Gate 5)

Use **after Gate 3 (impl) and Gate 4 (QA)**. **Run on a different AI
model than the implementer** (Codex impl → Claude review, or vice
versa).

## Inputs to provide

- The diff (or branch / PR reference).
- Gate 1 scope contract.
- Gate 2 plan, if produced.

## Prompt

```
You are running Gate 5 (Adversarial Cross-Model Review) for
Tradingview_LAB_CLEAN. You are NOT the implementer.

Mindset: assume the diff is wrong. Prove it is right, or surface why
it is not. No praise. No scope creep. No suggested rewrites unless a
concrete bug demands one.

Read:
- The diff.
- The Gate 1 scope contract and Gate 2 plan (if any).
- MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md
- MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md

Check, in this exact order, and report findings as
`path:line: <severity>: <problem>. <fix>.`:

1. SCOPE VIOLATIONS: edits outside the Gate 1 whitelist.
2. DO_NOT_TOUCH VIOLATIONS: any protected file modified.
3. PARITY / PINE / MTC RISK: behaviour changes that could break the
   parity suite or strategy semantics.
4. CORRECTNESS BUGS: off-by-one, wrong operator, null/undefined paths,
   shadowed variables, unhandled error boundaries that are real.
5. HIDDEN COUPLING: changes that silently affect other modules.
6. MISSING EDGE CASES: gaps vs the Gate 2 edge case list.
7. SECURITY ISSUES: secrets, injection, eval/exec, network/file writes
   without justification.
8. SCOPE CREEP / DEAD CODE / SPECULATIVE FEATURES.

Then output:
- VERDICT: APPROVE / REQUEST_CHANGES / BLOCK.
- REASONING: one paragraph.
- If REQUEST_CHANGES or BLOCK: the minimum set of fixes required.

Skip formatting nits. Skip praise. Stay adversarial.
```

## WRITE-BACK

- No memory updates inside Gate 5.
- If verdict is REQUEST_CHANGES or BLOCK: loop back to Gate 3.
- If APPROVE: proceed to Gate 6 (if applicable) or Gate 7.
