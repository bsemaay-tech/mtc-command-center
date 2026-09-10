# 04 — Adversarial Code Review  (Gate 5)

Use **after Gate 3 (impl) and Gate 4 (QA)**. **Run by the LEAD ORCHESTRATOR** — the model that is not the implementer (Codex impl → Claude lead reviews; Claude impl → Codex lead reviews). The lead independently inspects the actual diff/files; it does not merely accept the implementer's report. See `AGENTS.md` two-tier model.

## Mandatory tier classification + audit matrix (AGENTS.md §AUDIT TIER POLICY — PERMANENT DEFAULT)

Gate 5 is driven by the **audit tier** recorded in the Gate 1 scope contract. The tier decides auditor count, effort, and round cap. The canonical roster (`AGENTS.md` §CANONICAL AUDIT ROSTER) controls the exact model identity/quality for the slots actually invoked; fresh independence remains mandatory for every invoked slot.

| Tier | Auditors | Effort | Max rounds |
|------|----------|--------|------------|
| **T0** | Two flagships: `claude-opus-5` + `gpt-5.6-sol` | xhigh | 3 |
| **T1** | One alternating flagship (Claude/Codex per round) `high`; **plus GLM-5.2 second opinion ONLY if the flagship raises findings or the diff exceeds ~300 lines** | high | 2 |
| **T2** | Single reviewer, single round. GLM-5.2 preferred; DeepSeek acceptable; flagship at medium effort only if neither is available | medium | 1 |
| **T3** | **No model audit.** Implementer self-verification only | — | 0 |

**Claude auditor (T0/T1 flagship slot):** exact model `claude-opus-5`, effort `xhigh` (T0) / `high` (T1). No Sonnet, no alias, no silent fallback.
Example fresh-session CLI: `claude -p --model claude-opus-5 --effort xhigh --no-session-persistence`

**Codex auditor (T0/T1 flagship slot):** exact model `gpt-5.6-sol`. Effort `xhigh` for T0; `high` for T1. If Gate 6, Pine/parity/MTC/trading/protected, host-touching, architecture, or cross-cutting scope is discovered inside a T1 contract, stop and correct the Gate-1 classification to T0; do not silently raise effort while leaving the wrong tier recorded.
Example fresh-session CLI (ordinary): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=high" <audit_prompt_file>`
Example fresh-session CLI (T0/protected): `codex exec --ephemeral --sandbox read-only -m gpt-5.6-sol -c "model_reasoning_effort=xhigh" <audit_prompt_file>`

**If exact model/effort unavailable: stop as BLOCK unless Barış explicitly waives.**

**Fresh independent session required every round** — never `--resume` or `--continue` the implementer session. Provide only: scope contract, plan (if any), actual diff/files, test evidence, repo rules.

## Inputs to provide

- The diff (or branch / PR reference).
- Gate 1 scope contract (must include the **AUDIT TIER** classification).
- Gate 2 plan, if produced.

## Prompt

```
You are the Lead Orchestrator running Gate 5 (Adversarial Cross-Model
Review) for Tradingview_LAB_CLEAN. You are NOT the implementer. You
independently inspect the actual diff/files — do not accept the
implementer's self-report as evidence.

Mindset: assume the diff is wrong. Prove it is right, or surface why
it is not. No praise. No scope creep. No suggested rewrites unless a
concrete bug demands one.

Read:
- The diff.
- The Gate 1 scope contract (including its AUDIT TIER) and Gate 2 plan (if any).
- MTC_COMMAND_CENTER/_AI_MEMORY/DO_NOT_TOUCH.md
- MTC_COMMAND_CENTER/_AI_MEMORY/AI_RULES.md

Tier gate: read the AUDIT TIER from the Gate 1 scope contract.
- If the tier is **T3**, do NOT run a model audit. Record that the
  implementer's self-verification replaces this Gate 5 model audit and
  stop — do not invoke any auditor slot.
- Otherwise, before reporting any findings, state the applied auditor
  contract: `TIER: <T0/T1/T2>` and `APPLIED AUDITOR CONTRACT:
  <auditor(s) + effort + max rounds>` per the matrix above.

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
  PASS-WITH-NITS: accepting — optional nits only; no required repair.
  REQUEST_CHANGES: non-accepting — includes required repair(s).
  BLOCK: workflow cannot safely continue.
- REASONING: one paragraph.
- If REQUEST_CHANGES or BLOCK: the minimum set of required fixes.

Skip formatting nits. Skip praise. Stay adversarial.
```

## WRITE-BACK

- No memory updates inside Gate 5.
- If PASS or PASS-WITH-NITS: lead proceeds to Gate 6 (if applicable) or Gate 7. Only after Gate 7 may the lead perform repository hygiene and — where authorized — commit/push.
- If REQUEST_CHANGES or BLOCK: lead sends a focused repair prompt to the same counterpart implementer (loop back to Gate 3). **Repair/re-audit rounds are capped per audit tier: T0=3, T1=2, T2=1, T3=0.** After the cap is exhausted with no accepting verdict, stop and report the blocker to Barış.
