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
| T0 | Economic, host, deploy, secret, broker/exchange, teardown, security | `claude-opus-5` + `gpt-5.6-sol` | xhigh / 3 |
| T1 | Non-economic product code/scripts | one alternating flagship; GLM-5.2 only after findings or diff >~300 lines | high / 2 |
| T2 | Docs/evidence | GLM-5.2 preferred, DeepSeek acceptable, otherwise one flagship | medium / 1 |
| T3 | Index/status/process artifacts | implementer self-verification only | — / 0 |

Highest overlap wins. T2 deployed-identity findings alone escalate to one T1 flagship check.
Invoked Claude is exact `claude-opus-5`; invoked Codex exact `gpt-5.6-sol`; no alias/fallback.
Unavailable exact model/effort is BLOCK unless the owner waives. Every audit round is fresh, with
only scope, plan, diff/files, evidence, and repo rules—never implementer-session continuation.
Verdicts: PASS; PASS-WITH-NITS (optional only); REQUEST_CHANGES; BLOCK.

An auditor unable to run the mandated suite returns BLOCK; a source-only view is supplemental.
In an explicitly owner-designated four-auditor review, both flagships must accept and no reproduced
required finding from DeepSeek V4 Flash or GLM-5.2 may remain. Secondary auditors gain no protected
implementation authority.

## Delegation and context discipline

- Send compact evidence pointers/excerpts, never whole sessions or evidence trees. Pre-extract
  large samples. Rules must describe the failure class, not one lane.
- Implementer sub-delegation is optional: Cline first, `_deepseek_driver` fallback; use the cheapest
  capable route. Never send Pine, parity, MTC, trading, Bridge-protected, or schema work to a cheap
  model without explicit approval. The Lead still audits real results.
- GLM routing: discovery/mechanics = 4.5-Air only if verified, else 4.7; ordinary code = 4.7;
  GLM-5.1 only if active entitlement confirms it; difficult/protected/exact request = 5.2. Record
  classification, protected reason, provider/model, why not cheaper, exact paths, context budget,
  fallback, and external-credit use. Re-verify time-sensitive entitlement/quota.
- Targeted `rg` first; line/symbol reads before full files over 400–500 lines; batch independent
  checks; stop broad exploration when evidence exists; start fresh if context is excessive.
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
- A real AI Boardroom run requires explicit owner approval because it spends external tokens and
  transmits redacted slices. Dry-run is allowed. It is read-only and never trading approval.
- Board provider failures are recorded and the remaining read-only run may continue; failure never
  upgrades coverage or authority.
- After an accepted safe work unit, continue only into the next already-authorized safe unit. At a
  hard gate, keep preparing safe evidence and record the exact authorization still required.
