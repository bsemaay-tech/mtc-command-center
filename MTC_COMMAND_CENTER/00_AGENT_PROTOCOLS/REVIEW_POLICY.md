# Canonical review policy

Read for task classification, G5/G6 dispatch, or governance edits; not routine startup.
Owner-authorized workflow revision, 2026-09-09. This branch is a governance candidate: editing
this policy is itself T0 and supplies no self-acceptance, audit waiver or completed verdict.
Activation: OD-20260909-1 is prospective. These revised defaults take effect only after this
candidate satisfies the pre-change T0 contract and authorized protected integration. Until then,
the previously operative obligations continue; this candidate cannot use its own lighter tiers
to accept itself. Root `DECISIONS.md` and `../11_TRIAGE/WORKFLOW_MEMORY_RECONCILIATION_2026-09-09.md`
record the revision authority. For pre-activation classification and acceptance only, read the
preserved [pre-change Audit contract](../_AI_MEMORY/history/workflow-20260909/policy__MTC_COMMAND_CENTER__00_AGENT_PROTOCOLS__AGENTS.md#audit-contract).
This pointer delegates only that section's pre-change review obligations, subject to current
explicit owner task authority; it does not reactivate expired overrides, old routing, or other
archived instructions. After activation, older generic tier tables are historical.

## Classify by highest consequence

| Tier | Actual consequence | Required review |
|---|---|---|
| T0 | Sizing, orders, recovery, parity, economics, security, credentials, live host/deploy; binding safety, acceptance or evidence logic, including policy changes | Fresh exact `claude-opus-5` **and** `gpt-5.6-sol`, both `xhigh`, plus fresh mandatory `gemini-3.7-flash-high` corroboration on the same packet; independent Lead reproduction |
| T1 | Ordinary non-economic functionality or scripts with no T0 consequence | One fresh independent exact flagship (`claude-opus-5` or `gpt-5.6-sol`) at `high`; independent Lead reproduction |
| T2 | Presentation-only cosmetic changes or nonbinding prose | Appropriate self-check; no automatic model auditor |
| T3 | Generated status/index updates with no binding safety/acceptance consequence | Self-check, including generation consistency where relevant |

Highest applicable consequence wins. Extension, line count, a "docs" label, or small diff cannot
downgrade safety, acceptance, economic meaning, executable evidence, or a changed refusal gate.
T0 review precedes acceptance of the affected safety surface; ordinary T1 review is at a useful
package boundary. Findings or >300 changed lines do not automatically add auditors or rounds.
T2/T3 outcomes may be recorded complete after the appropriate checks; never imply a model audit.

Preserve explicitly designated existing multi-auditor/package contracts. In an owner-designated
four-auditor review both flagships must accept, and no independently reproduced required finding
from DeepSeek V4 Flash or GLM-5.2 may remain. D025 secondary identities stay
`cline-pass/deepseek-v4-flash` via ClinePass and GLM-5.2 via Z.AI Coding Plan. Their frozen-SHA
dedicated worktrees must finish with empty `git status --porcelain`; no protected write authority.
This default does not silently relax existing P012, Bridge, or other specifically frozen contracts.

## Freshness, evidence, and verdicts

- Each required auditor is fresh and independent of the builder: never resume/continue the
  implementation session. Supply scope/authority, relevant rules and acceptance criteria,
  exact base/head and actual diff/files, plan if needed, and the same frozen evidence packet.
  Codex acceptance reviews are ephemeral and read-only. No silent model, effort or route fallback;
  an unavailable required slot blocks acceptance unless the owner explicitly waives/substitutes it.
- The Lead inspects actual files/diff, runs the applicable repeatable checks independently, and
  records required findings' reproduced disposition. A peer report, test count, or source-only
  review is not executed acceptance evidence. An acceptance auditor unable to run the mandated
  suite returns BLOCK. See `TESTS.md` for exact commands, RED/GREEN and independent expectations.
- For T0 and any retained contract requiring Gemini, dispatch fresh `gemini-3.7-flash-high` via
  `C:\Users\BarışSemaay\AI_CLI_HELPERS\Invoke-GeminiProReadOnly.ps1`. Its known read-only
  non-execution is `SUPPLEMENTAL_UNEXECUTED`, not by itself BLOCK; missing required dispatch is
  blocking absent owner waiver. It never replaces a flagship slot, execution or Lead acceptance.
  Compare common findings, Gemini-only findings, contradictions and each required disposition.
  When the launcher sees only the canonical checkout, give exact audited SHA and literal redacted
  diff/file slices; do not substitute another checkout's state. Dated campaign overrides apply
  only during their recorded windows; consult relevant decisions, never infer current entitlement.
- PASS and PASS-WITH-NITS accept only their reviewed scope; nits must be optional. REQUEST_CHANGES
  and BLOCK do not accept. A local candidate commit, progress handoff or passing subset is not
  package acceptance. Live release, owner permission, protected CI and merge gates remain separate.

## Repairs and specialist review

Default repair checkpoints T0=3, T1=2, T2=1, T3=0 are internal Lead checkpoints under
`AUTONOMY_AUTHORIZATION.md`, not automatic stop-and-ask limits. Record actual rounds; repair only
the reproduced issue; change the hypothesis/evidence before retrying. Recheck affected behavior
and required fences. Do not blindly rerun identical failed commands or commission duplicate audits.

G6 may share G5's exact frozen packet and valid suite evidence. Reuse is tied to source identity,
environment, scope and provenance; materially changed code/environment or an unresolved concern
needs the relevant new check. This avoids identical reruns, never waives actual canonical auditors'
execution or other obligations. Record why security review is applicable or unnecessary.

Add a bounded specialist review for the first kernel, first live release, major security change,
or serious unresolved disagreement; name the question and stop condition. An experienced engineer
reviews before the first money-exposed release, not every package. These checks do not confer
live-trading authority or replace exact protected acceptance contracts.
