# 04 - Adversarial Code Review  (Gate 5)

Use **after Gate 3 (impl) and Gate 4 (QA)**. **Run by the LEAD ORCHESTRATOR** - the model that is not the implementer (Codex impl -> Claude lead reviews; Claude impl -> Codex lead reviews). The lead independently inspects the actual diff/files; it does not merely accept the implementer's report. See `AGENTS.md` two-tier model.

## Mandatory audit model/effort (AGENTS.md CANONICAL AUDIT ROSTER)

**Claude auditor:** exact model `claude-opus-4-8`, effort `xhigh`. No Sonnet, no alias, no silent fallback.
Example fresh-session CLI: `claude -p --model claude-opus-4-8 --effort xhigh --no-session-persistence`

**Codex auditor:** exact model `gpt-5.6-sol`. Effort `high` for ordinary Gate 5. Effort `xhigh` for: Gate 6 security review; Pine/parity/MTC/trading/protected surface; architecture/cross-cutting change; re-audit after REQUEST_CHANGES or BLOCK.
Example fresh-session CLI (ordinary G5): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c 'model_reasoning_effort="high"' "<audit prompt>"`
Example fresh-session CLI (protected/re-audit): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c 'model_reasoning_effort="xhigh"' "<audit prompt>"`

**If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives.**

**Fresh independent session required every round** - never `--resume` or `--continue` the implementer session. Provide only: scope contract, plan (if any), actual diff/files, test evidence, repo rules.

Audits are diff-first: unified diff by default; full files only for necessary context with stated reason.

## Inputs to provide

- The diff (or branch / PR reference).
- Gate 1 scope contract.
- Gate 2 plan, if produced.

## Prompt

```
You are the Lead Orchestrator running Gate 5 (Adversarial Cross-Model
Review) for Tradingview_LAB_CLEAN. You are NOT the implementer. You
independently inspect the actual diff/files - do not accept the
implementer's self-report as evidence.

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
- VERDICT: PASS / PASS-WITH-NITS / REQUEST_CHANGES / BLOCK.
  PASS-WITH-NITS: accepting - optional nits only; no required repair.
  REQUEST_CHANGES: non-accepting - includes required repair(s).
  BLOCK: workflow cannot safely continue.
- REASONING: one paragraph.
- If REQUEST_CHANGES or BLOCK: the minimum set of required fixes.

Skip formatting nits. Skip praise. Stay adversarial.
```

## WRITE-BACK

- No memory updates inside Gate 5.
- If PASS or PASS-WITH-NITS: lead proceeds to Gate 6 (if applicable) or Gate 7. Only after Gate 7 may the lead perform repository hygiene and - where authorized - commit/push.
- If REQUEST_CHANGES or BLOCK: lead sends a focused repair prompt to the same counterpart implementer (loop back to Gate 3). **Maximum 3 repair/re-audit rounds total.** After the third non-accepting verdict, stop and report the blocker to Barış.
