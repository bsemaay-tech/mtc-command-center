# Corrected T2 Candidates — Fresh-Review Prompt Bundle

**Date:** 2026-08-17
**Artifact class:** T3 dispatch package; no review is launched by this file.

Use a prompt below only after Barış gives the exact candidate-specific exception
named in that prompt, or explicitly authorizes all four exceptions as defined in
`MTC_COMMAND_CENTER/11_TRIAGE/OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md`
(committed at `cb00967affd5952fa6191c85f417407ed9a91221`). An instruction to continue
ordinary work is not a review-cap exception.

Each authorized prompt consumes the one exceptional fresh T2 review it names.
It does not reset the permanent cap, authorize another repair/review round, or
accept any other candidate.

## Prompt 1 — AI-memory six-file lossless rotation

```text
OWNER EXCEPTION REQUIRED

Run this review only if the dispatcher supplies Barış's exact authorization:
"AUTHORIZE ONE FRESH T2 REVIEW OF THE SIX-FILE ROTATION" or the exact all-four
authorization defined in OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md.
Paste that authorization here: <OWNER_EXCEPTION_EVIDENCE>

If the evidence is absent, still a placeholder, or does not name this exception,
return BLOCK immediately. Do not infer permission.

ROLE AND TIER

You are the sole fresh T2 documentation/evidence reviewer for one exceptional
review of the current six-file AI-memory rotation. Normal T2 preference applies:
GLM-5.2 preferred; DeepSeek acceptable; one flagship at medium only if neither
is available. Use one reviewer only and one round only. A model/run failure is
BLOCK, not permission to dispatch another reviewer.

EXACT CANDIDATE PATHS

- MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md
- MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md
- MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md
- MTC_COMMAND_CENTER/_AI_MEMORY/archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md
- MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_2026-08-01_to_2026-08-10.md
- MTC_COMMAND_CENTER/_AI_MEMORY/archive/START_HERE_STALE_BANNER_2026-08-12.md

REQUIRED REPO EVIDENCE

- AGENTS.md
- MTC_COMMAND_CENTER/11_TRIAGE/AI_MEMORY_ROTATION_GATE1_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/AI_MEMORY_ROTATION_T2_STATUS_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md

ORIGINAL REVIEW HISTORY

GLM was unavailable at quota. The permitted DeepSeek reviewer independently
reproduced the reconstruction hashes, line endings, unique markers, neutral
pointer and justified START_HERE line-10 deviation, but exhausted 24 iterations
without finish() and returned no formal verdict. The ordinary T2 round was
therefore consumed without acceptance. No substantive required finding existed.

CLAIMS TO RE-CHECK

1. Reconstructing GLOBAL_HANDOFF from live plus archive reproduces 207,895 bytes
   and SHA-256 c6abba25c2e5e9c9832e52259437717326be58e0d176937cff2487d6fda6c08c.
2. Reconstructing NEXT_STEPS reproduces 198,155 bytes and SHA-256
   e1c085d82977c96f151f6f29d980fccdf1e8ffce029244b59b53c5e93e869015.
3. Reconstructing START_HERE with its preserved separating blank line reproduces
   7,263 bytes and SHA-256
   b3873547f7df4403cbfead91be599a63e7c5d3dbb3996ec42030788d78bc5368.
4. GLOBAL/NEXT live and archive files preserve LF; START_HERE live/archive
   preserve CRLF; archive markers are unique; no historical payload was
   summarized, reordered or used to close tasks.
5. Archiving START_HERE original lines 3-10, rather than Gate-1's stated 3-9,
   was necessary because the blockquote ended at line 10; the deviation is
   explicit and lossless.
6. The live pointers are neutral and do not replace volatile-state verification.
7. The separate AI-memory classification report is outside this review.

READ-ONLY METHOD AND STATUS PROOF

Before review, record `git status --short` for all six paths and SHA-256 for all
six current files. Review the exact working-copy bytes; do not substitute HEAD.
Perform the reconstruction and line-ending/marker checks independently. After
review, repeat the same scoped status and hashes and state whether the full repo
status changed during your run. The six before/after hashes must match. Do not
repair unrelated concurrent changes.

PROHIBITED

Do not edit, create, delete, move, stage, commit, checkout, reset or stash any
file. Do not rotate more memory, edit the classification report, contact hosts,
use credentials, deploy, run trading/strategy compute, change code, or touch the
Help/Wiki T1 candidate. This exception authorizes review only.

FORMAL OUTPUT

Report: owner-exception evidence; reviewer model/route; exact paths and pre/post
status/hash proof; each claim's reproduced result; required findings separately
from optional nits; and exactly one verdict:

- PASS — no required changes.
- PASS-WITH-NITS — accepting; optional nits only, zero required repair.
- REQUEST_CHANGES — at least one required repair. No repair/re-review is
  authorized by this prompt.
- BLOCK — review could not safely complete.
```

## Prompt 2 — Dashboard V2 architecture gap inventory

```text
OWNER EXCEPTION REQUIRED

Run this review only if the dispatcher supplies Barış's exact authorization:
"AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT GAP INVENTORY" or the exact
all-four authorization defined in OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md.
Paste that authorization here: <OWNER_EXCEPTION_EVIDENCE>

If the evidence is absent, still a placeholder, or does not name this exception,
return BLOCK immediately. Do not infer permission.

ROLE AND TIER

You are the sole fresh T2 documentation/evidence reviewer for one exceptional
review of the current Dashboard V2 inventory. GLM-5.2 is preferred; DeepSeek is
acceptable; one flagship at medium may be used only if neither is available.
Use one reviewer and one round. Although the report describes future T0/T1
packages, this review is only T2 prose/source-truth review.

EXACT CANDIDATE PATH

- MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_ARCHITECTURE_GAP_INVENTORY_2026-08-17.md

REQUIRED REPO EVIDENCE

- AGENTS.md
- MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_SEVEN_WORKSTREAM_CHECKPOINT_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_HELP_TRUTH_CYCLE2_T1_STATUS_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md
- The exact Bridge/dashboard/deployment/docs30 sources cited by the candidate.

ORIGINAL REVIEW HISTORY

The sole T2 review was non-accepting. Durable repo evidence records one required
host-risk classification repair and two truth clarifications, but not the
reviewer's identity or exact printed verdict token. The ordinary T2 round was
consumed. All three repairs are now present but unaccepted.

REPAIRED CLAIMS TO RE-CHECK

1. WP-D7 is T0 by highest-risk-wins because it includes KVM2 deployment and
   host-load measurement, backup/restore and owner controls. Any later KVM2
   measurement or host contact needs separate explicit authorization; this
   inventory grants none.
2. docs/30 is described only as an uncommitted working-copy diff, not an
   accepted or line-count-defined change.
3. The Help section preserves both unresolved LLM truth defects: reading,
   serving or displaying llm configuration is not LLM-gate activation; and a
   generic LLM_SKIPPED decision row is persisted even though no directive or
   model-call record is persisted.
4. Verify the wider inventory against current repository source: what V1 truly
   does, accepted owner directions, unaccepted draft ideas, dependencies,
   phone/private-access/control/AI boundaries, required evidence and explicit
   not-yet-build boundaries. Proposed work must not be stated as current truth.

READ-ONLY METHOD AND STATUS PROOF

Before review, record the candidate's `git status --short` and SHA-256, plus a
full-repo status snapshot. Review the exact working-copy bytes and targeted repo
evidence; do not substitute HEAD or accept prior reports blindly. After review,
repeat the candidate status/hash and full-repo status. The candidate hash must
match before and after; explain unrelated concurrent status drift without
altering it.

PROHIBITED

Do not edit, create, delete, move, stage, commit, checkout, reset or stash any
file. Do not select architecture, contact KVM2/any host, measure host load,
deploy, access credentials, ARM/order, change Bridge/dashboard code, accept or
repair docs/30, run strategy compute, or touch the Help/Wiki T1 candidate. This
review cannot accept embedded external ideas or future T0/T1 work.

FORMAL OUTPUT

Report: owner-exception evidence; reviewer model/route; exact candidate identity
and pre/post status/hash proof; source files inspected; each repaired claim's
result; wider truth/consistency findings; required findings versus optional
nits; and exactly one verdict:

- PASS — no required changes.
- PASS-WITH-NITS — accepting; optional nits only, zero required repair.
- REQUEST_CHANGES — at least one required repair; no repair/re-review authorized.
- BLOCK — review could not safely complete.
```

## Prompt 3 — Strategy research owner decision packet

```text
OWNER EXCEPTION REQUIRED

Run this review only if the dispatcher supplies Barış's exact authorization:
"AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT STRATEGY DECISION PACKET" or the
exact all-four authorization in OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md.
Paste that authorization here: <OWNER_EXCEPTION_EVIDENCE>

If the evidence is absent, still a placeholder, or does not name this exception,
return BLOCK immediately. Do not infer permission.

ROLE AND TIER

You are the sole fresh T2 documentation/evidence reviewer for one exceptional
review of the current strategy owner-choice packet. GLM-5.2 is preferred;
DeepSeek is acceptable; one flagship at medium may be used only if neither is
available. Use one reviewer and one round. This is document/provenance review,
not strategy approval, implementation, preregistration or compute.

EXACT CANDIDATE PATH

- MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_RESEARCH_OWNER_DECISION_PACKET_2026-08-17.md

REQUIRED REPO EVIDENCE

- AGENTS.md
- MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_SEVEN_WORKSTREAM_CHECKPOINT_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md
- MTC_COMMAND_CENTER/_AI_MEMORY/STRATEGY_RESEARCH_WORKFLOW.md
- The exact transcript/intake, registry, data-manifest and canonical research
  rules cited by the candidate.

ORIGINAL REVIEW HISTORY

The sole T2 review was non-accepting and found two required source/rule
overclaims. Durable repo evidence does not record the reviewer identity or exact
printed verdict token. The ordinary round was consumed. The current packet
contains the two repairs but has not been accepted.

REPAIRED CLAIMS TO RE-CHECK

1. Stock applicability, symmetric long/short direction and not predicting
   direction in advance are explicitly intake-derived or proposed research
   choices. They are not attributed as transcript mandates.
2. The unsupported canonical minimum of at least eight symbols is removed.
   Seven-symbol discovery is a conservative proposal only, not a canonical
   minimum, confirmation package or promotion rule.
3. Confirm that surrounding provenance remains bounded: direct transcript facts,
   intake facts and proposed preregistration choices are kept distinct; the
   packet does not claim profitability, robustness, promotion or live fitness.
4. Confirm the packet asks for an owner choice but authorizes no implementation,
   backtest, optimization, data acquisition or trading action.

READ-ONLY METHOD AND STATUS PROOF

Before review, record candidate `git status --short`, SHA-256 and a full-repo
status snapshot. Review the exact working-copy bytes and targeted cited repo
evidence. Do not execute the strategy or use results not already recorded in the
repo. After review, repeat candidate status/hash and full-repo status; the
candidate hash must be unchanged. Explain unrelated concurrent drift without
repairing it.

PROHIBITED

Do not edit, create, delete, move, stage, commit, checkout, reset or stash any
file. Do not write a preregistration, implement strategy/Pine/MTC/parity logic,
run tests as strategy compute, launch a backtest/optimization/smoke run, acquire
data, contact hosts/exchanges, deploy, use credentials, or touch Help/Wiki. A
PASS does not choose owner option A/B/C and is not promotion evidence.

FORMAL OUTPUT

Report: owner-exception evidence; reviewer model/route; exact candidate identity
and pre/post status/hash proof; repo sources inspected; each repaired claim's
result; required findings separately from optional nits; and exactly one verdict:

- PASS — no required changes.
- PASS-WITH-NITS — accepting; optional nits only, zero required repair.
- REQUEST_CHANGES — at least one required repair; no repair/re-review authorized.
- BLOCK — review could not safely complete.
```

## Prompt 4 — Dashboard V2 external pattern addendum

```text
OWNER EXCEPTION REQUIRED

Run this review only if the dispatcher supplies Barış's exact authorization:
"AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT EXTERNAL PATTERN ADDENDUM" or the
exact all-four authorization in OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md.
Paste that authorization here: <OWNER_EXCEPTION_EVIDENCE>

If the evidence is absent, still a placeholder, or does not name this exception,
return BLOCK immediately. Do not infer permission.

ROLE AND TIER

You are the sole fresh T2 reviewer for one exceptional review of the current
supplemental Dashboard V2 research addendum. GLM-5.2 is preferred; DeepSeek is
acceptable; one flagship at medium may be used only if neither is available.
Use one reviewer and one round. Source validation is not architecture selection.

EXACT CANDIDATE PATH

- MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_EXTERNAL_PATTERN_ADDENDUM_2026-08-17.md

REQUIRED REPO EVIDENCE

- AGENTS.md
- MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_EXTERNAL_PATTERN_ADDENDUM_T2_STATUS_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_ARCHITECTURE_GAP_INVENTORY_2026-08-17.md
- MTC_COMMAND_CENTER/11_TRIAGE/OWNER_REVIEW_CAP_DECISION_PACKET_2026-08-17.md
- docs/30 and the targeted Bridge sources cited by the addendum.

ORIGINAL REVIEW HISTORY

DeepSeek V4 Pro through the sandboxed _deepseek_driver read the candidate and
repo evidence but exhausted 24 iterations without finish() or a formal verdict.
No substantive required finding was returned. Lead inspection removed three
Markdown trailing-space warnings. The ordinary T2 round was consumed; the
corrected document remains unaccepted.

CLAIMS TO RE-CHECK

1. The candidate has no trailing-space defect and passes a no-index whitespace
   check apart from normal new-file/line-ending behavior.
2. Every material statement is clearly labelled as source fact, repo-verified
   gap, owner decision or optional proposal. External projects are inspiration,
   never authority.
3. Hyperliquid snapshot-versus-stream/order/fill subscription claims, Tailscale
   grant/device-posture claims and Prometheus symptom-alerting claims are
   faithfully attributed to their cited official sources.
4. Responsive multi-wallet/multi-strategy visibility, freshness badges,
   structured-log monitoring and authentication/unsafe-public-bind lessons are
   options, not selected architecture or current Bridge capability.
5. Tailscale versus Cloudflare/private-access topology and all compact
   accept/defer/reject questions remain open for later owner decision.

READ-ONLY METHOD AND STATUS PROOF

Before review, record candidate `git status --short`, SHA-256 and a full-repo
status snapshot. Review the exact working-copy bytes, targeted repo evidence and
the candidate's cited primary/official pages read-only where needed. Do not treat
README claims as authority. After review, repeat candidate status/hash and
full-repo status. The candidate hash must be unchanged; explain unrelated
concurrent drift without altering it.

PROHIBITED

Do not edit, create, delete, move, stage, commit, checkout, reset or stash any
file. Do not select or implement architecture, install/configure access or
monitoring, contact KVM2/Bridge/exchange hosts, use credentials, deploy, expose a
port, ARM/order, run strategy compute, accept the separate gap/docs30/Help
candidates, or touch the Help/Wiki T1 work. Official documentation browsing is
read-only source verification, not host authorization.

FORMAL OUTPUT

Report: owner-exception evidence; reviewer model/route; exact candidate identity
and pre/post status/hash proof; repo and official sources inspected; each claim's
result; required findings separately from optional nits; and exactly one verdict:

- PASS — no required changes.
- PASS-WITH-NITS — accepting; optional nits only, zero required repair.
- REQUEST_CHANGES — at least one required repair; no repair/re-review authorized.
- BLOCK — review could not safely complete.
```

## Separation reminder

These four prompts cover only four T2 documentation candidates. They do not
authorize or consume the Help/Wiki candidate's remaining T1 review round. That
candidate remains blocked on the exact Claude counterpart applying its already
bounded repair and producing validation evidence before the final permitted T1
review.
