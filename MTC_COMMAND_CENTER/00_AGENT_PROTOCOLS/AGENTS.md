# Governance and agent-operations stage rules

This stage owns workflow, audit, planning, triage, Git/handoff, repository migration, shared
governance, and supporting paths not assigned to a product stage by root `CONTEXT_MAP.md`.

## Seven gates and actors

1. **G1 Scope — Lead:** value, smallest safe change, allow/deny paths, protected surfaces,
   success criteria, and recorded T0/T1/T2/T3. If the counterpart flagship is unavailable, BLOCK.
2. **G2 Plan — Implementer:** flow, modules, edge cases, rollback, Pine/parity/MTC impact. The Lead
   accepts it before implementation; skip only trivial docs/typos/single-line work.
3. **G3 Implement — Implementer:** minimal scoped diff; no unrelated or speculative change.
4. **G4 QA — Implementer:** real tests/lint/typecheck and explicit parity/UI risk; provide evidence,
   never a self-issued acceptance verdict.
5. **G5 Audit — Lead:** inspect real files/diff and reproduce evidence independently. Use the tier
   contract below. Required reproduced findings bind; unreproduced findings remain recorded.
6. **G6 Security — independent:** security/auth/secret/network/host/deploy defaults T0. Pure docs,
   Pine plotting, and cosmetic changes skip only when no security surface exists.
7. **G7 Write-back — Lead after acceptance:** update the selected stage `HANDOFF.md`, root
   `DECISIONS.md` for a sticky owner decision, and durable tracker/claim state as applicable.

Prompt templates live in `MTC_COMMAND_CENTER/04_SHARED/prompts/05_ai_workflow/`.

## Audit contract

| Tier | Surface | Required review | Effort / cap |
|---|---|---|---|
| T0 | Economic, host, deploy, secret, broker/exchange, teardown, security | `claude-opus-5` + `gpt-5.6-sol`, plus mandatory Gemini parallel corroboration | xhigh / 3 |
| T1 | Non-economic product code/scripts | one alternating flagship; GLM-5.2 only after findings or diff >~300 lines; plus mandatory Gemini parallel corroboration | high / 2 |
| T2 | Docs/evidence | GLM-5.2 preferred, DeepSeek acceptable, otherwise one flagship; plus mandatory Gemini parallel corroboration | medium / 1 |
| T3 | Index/status/process artifacts | implementer self-verification only | — / 0 |

Highest overlap wins. T2 deployed-identity findings alone escalate to one T1 flagship check.
Invoked Claude is exact `claude-opus-5`; invoked Codex exact `gpt-5.6-sol`; no alias/fallback.
Unavailable exact model/effort is BLOCK unless owner-waived. Each audit is fresh, receives only
scope, plan, diff/files, evidence, and repo rules, and is never resumed/continued. Codex audits are
ephemeral and read-only.

**OD-20260829-1 — mandatory Gemini parallel corroboration.** Every T0, T1, or T2 Gate 5/Gate 6
audit that dispatches one or more model auditors must also dispatch a fresh
`gemini-3.7-flash-high` review through
`C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`. Gemini receives the same
scope, allowed/forbidden paths, actual diff/files, test evidence, and repository rules as every
other auditor. The Lead records a comparison: common findings, Gemini-only findings,
contradictions, and the independently reproduced disposition of every required finding. Gemini is
a required parallel dispatch; an unavailable Gemini route blocks audit completion unless Barış
waives it. It does not replace an exact flagship slot, Lead/counterpart role, acceptance authority,
protected implementation boundary, or the existing tier/repair-cap rules. Gemini's isolated
read-only route cannot execute the mandated suite; label that report `SUPPLEMENTAL_UNEXECUTED`.
That non-execution alone is not a BLOCK, but no Gemini finding binds until the Lead reproduces it.
The launcher reads only the canonical checkout: when the audited SHA is in another worktree, give
Gemini the exact SHA plus literal, safety-redacted diff and relevant file slices in its review
package; never let it substitute canonical-checkout contents for the audited source.
T3 remains self-verification-only unless a later owner task explicitly requests a model audit.
Verdicts: PASS; PASS-WITH-NITS (optional only); REQUEST_CHANGES; BLOCK.
After a non-accepting verdict, Lead sends the same implementer a focused repair within the tier cap.

An acceptance auditor unable to run the mandated suite returns BLOCK; a source-only view is
supplemental. The owner-mandated Gemini parallel route is the explicit exception: it is dispatched
and compared on every T0–T2 model audit, but its known suite non-execution is
`SUPPLEMENTAL_UNEXECUTED`, not a standalone BLOCK.
In an explicitly owner-designated four-auditor review, both flagships must accept and no reproduced
required finding from DeepSeek V4 Flash or GLM-5.2 may remain. Secondary auditors gain no protected
implementation authority.
D025 secondary identities are `cline-pass/deepseek-v4-flash` via ClinePass and GLM-5.2 via Z.AI
Coding Plan. Both audit in a dedicated worktree at the frozen SHA; afterwards require empty
`git status --porcelain` as proof they edited nothing.

## Delegation and context discipline

- Send compact evidence pointers/excerpts, never whole sessions or evidence trees. Pre-extract
  large samples. Rules must describe the failure class, not one lane.
- Implementer sub-delegation is optional: Cline first, `_deepseek_driver` fallback; use the cheapest
  capable route. Never send Pine, parity, MTC, trading, Bridge-protected, or schema work to a cheap
  model without explicit approval. The Lead still audits real results.
- Prefer subscription routes over external-credit routes while preserving exact-model, cost, and
  independence requirements.
- GLM routing: discovery/mechanics = 4.5-Air only if verified, else 4.7; ordinary code = 4.7;
  GLM-5.1 only if active entitlement confirms it; difficult/protected/exact request = 5.2. Record
  classification, protected reason, provider/model, why not cheaper, exact paths, context budget,
  fallback, and external-credit use. Re-verify time-sensitive entitlement/quota.
  These repository tiers override provider-default model mappings.
- Targeted `rg` first; line/symbol reads before full files over 400–500 lines; batch independent
  checks; stop broad exploration when evidence exists; start fresh if context is excessive. Resume
  or continue only with explicit owner authorization. Record measured token/context consumption
  after unexpectedly large runs.
- Probe a changed CLI/model route cheaply before spending a dispatch. Codex lanes must not spawn
  Claude children; verify the guard. Commit completed agent work before another agent receives the
  same files; if commit is not authorized, pause instead of handing off dirty shared files.
- GLM execution-sensitive reviews run unattended without approval loops and remain source-level
  until the Lead executes the real harness. Security-flavoured Codex audits use narrow bands,
  symbolic fixtures, and file-offloaded verbose output so transport filtering cannot erase verdicts.
- When Claude is Lead, launch Codex only through
  `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1` (default `-Account secondary`);
  never run bare `codex` or route to the desktop `.codex` home. Read the account-routing file only
  when choosing/checking an account, quota, or credential source.
- Propose AI Boardroom only for a high-stakes ambiguous decision. A real run needs owner approval
  because it spends external tokens and transmits redacted slices. Dry-run is allowed; the tool is
  read-only and never trading approval.
- Board provider failures are recorded and the remaining read-only run may continue; failure never
  upgrades coverage or authority.
- After an accepted safe work unit, continue only into the next already-authorized safe unit. At a
  hard gate, keep preparing safe evidence and record the exact authorization still required.
