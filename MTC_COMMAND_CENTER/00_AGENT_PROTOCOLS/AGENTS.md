# Governance and agent-operations stage

Owns workflow, audit, planning, triage, Git/handoff, migration, and supporting paths routed here.
Before writes/execution read `INPUTS.md` and `TESTS.md`; resume from relevant `HANDOFF.md`; read
`OUTPUTS.md` before delivery. For classification/audit/governance, read `REVIEW_POLICY.md`.

## Seven logical gates

One small task may use one brief for G1/G2/G4, not seven documents or meetings. Depth follows
consequence. Reuse settled decisions and existing task records; clarify only unresolved choices.

1. **G1 Scope — Lead:** user outcome, one smallest complete slice, exact allow/deny paths,
   authority, protected impact, dependencies, completion example, and review tier.
2. **G2 Plan — builder, Lead checks:** affected interfaces, meaningful failure cases, rollback,
   and verification. Add depth for consequential architecture; a trivial task needs no separate plan.
3. **G3 Implement — builder:** minimal scoped change, preserving existing architecture/work.
4. **G4 QA — builder:** actual commands with cwd/environment, expected and observed results,
   and a working path visible at the relevant boundary. Self-QA is not independent acceptance.
5. **G5 Review — Lead:** real diff and independent evidence reproduction under `REVIEW_POLICY.md`.
6. **G6 Security — independent when relevant:** apply the same policy and frozen packet;
   reuse valid evidence without redundant identical runs. No required auditor is waived.
7. **G7 Write-back:** record factual progress/blockers even before acceptance; only the Lead
   records ACCEPTED after its evidence/roster obligations. Keep stage `HANDOFF.md` <=4096 bytes.

Templates: `../04_SHARED/prompts/05_ai_workflow/00_index.md`. Completion includes the actual
owner outcome, limitations and exact next action. Tests and review must assess the agreed behavior,
not merely the implementation's chosen output. Consult `TESTS.md` for defect-closure evidence.

## Delegation and economical context

- Separate scope/acceptance from implementation. Ordinary low-risk builders need not be a pair
  of flagships; use the cheapest capable authorized route. Exact review slots and explicitly
  designated protected Lead/counterpart contracts remain binding.
- Bounded mechanical repo work routes to the approved cheap harness; read `_deepseek_driver/README.md`
  from root first. If routes fail, record actual errors and use only an authorized fallback.
  Never delegate Pine/parity/MTC/trading/Bridge-protected/schema work to cheap routes without
  explicit approval. Every lane has exact ownership, provider/model, budget, dependency and stop.
- For account/model/quota choices read `../_AI_MEMORY/AI_ACCOUNT_AND_MODEL_ROUTING.md` and only
  relevant dated records; verify current availability. Included subscriptions first; new PAYG
  needs owner authority. Supplemental routes never silently replace acceptance auditors.
- Claude Lead launches Codex through
  `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-CodexForClaude.ps1` (default secondary account),
  never bare Codex or the desktop home. Codex lanes must not spawn Claude children. Keep routing
  process-scoped; never globally switch active accounts or expose credentials.
- Offload long outputs per `../_AI_MEMORY/TOOL_OUTPUT_OFFLOAD_PROTOCOL.md`. Send compact contracts,
  exact refs/diffs and evidence pointers; no full sessions. Peer findings still need reproduction.
- Follow `AUTONOMY_AUTHORIZATION.md` for repair checkpoints, ordinary local commits, safe-lane
  continuation and material owner gates. Handoff of shared write paths must preserve ownership;
  no silent transfer of another writer's dirty files.
