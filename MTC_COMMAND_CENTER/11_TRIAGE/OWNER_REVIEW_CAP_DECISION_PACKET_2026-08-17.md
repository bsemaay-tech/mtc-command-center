# Owner Decision Packet — Capped Documentation Reviews

**Date:** 2026-08-17
**Purpose:** let the owner decide whether four exact, corrected documentation
candidates may receive one exceptional fresh T2 review. This packet does not
accept any candidate, reset any repository-wide cap, authorize implementation,
or authorize host/trading activity.

## Plain-English issue

Each candidate below used its one permitted T2 review round but did not obtain
an accepting `PASS` or `PASS-WITH-NITS`. Two reviews returned required changes
that are now repaired. Two reviewer runs ended without a formal verdict. Under
the repository rule, none may silently receive another reviewer.

For each candidate, the narrow choice is:

- **AUTHORIZE ONE FRESH REVIEW:** one named exception for the current exact
  candidate only, using the normal T2 reviewer/model and verdict rules; or
- **PRESERVE UNACCEPTED:** keep the files as evidence/drafts, but do not commit,
  cite, transfer or use them as accepted authority.

Authorizing one review is not permission for more edits, implementation, host
contact, deployment, strategy compute or another round after that review.

## 1. AI-memory lossless rotation

**Current candidate paths**

- `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/NEXT_STEPS.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_2026-08-01_to_2026-08-10.md`
- `MTC_COMMAND_CENTER/_AI_MEMORY/archive/START_HERE_STALE_BANNER_2026-08-12.md`

**Tier:** T2 documentation/evidence; one reviewer, one round.

**Review history:** GLM could not run because its usage window was at quota.
The permitted DeepSeek reviewer reproduced all three reconstruction hashes,
the line endings, unique markers, neutral live pointer and the justified
`START_HERE` line-10 deviation. It then exhausted the 24-iteration harness
budget without calling `finish()`, so **no formal verdict exists**. The round is
treated as consumed.

**Reproduced required findings:** none. The line-10 deviation was reproduced
and justified: the archived banner actually ended there, and leaving that line
behind would have orphaned part of the stale banner.

**Repair status:** no substantive repair was required. Lead evidence says the
split is byte-for-byte reconstructable and `git diff --check` passes.

**What remains unaccepted:** all six rotation files. Mechanical proof is not a
substitute for the missing formal verdict. The separate memory-classification
report is not part of this six-file review scope and would not be accepted by a
waiver for this rotation.

**Risk of an extra round:** treating a timed-out reviewer as permission to keep
trying would weaken the one-round rule for later documentation packages. If
authorized, the exception must name only these six current files and must not
be described as a general cap reset.

**Narrow owner decision:** `AUTHORIZE ONE FRESH T2 REVIEW OF THE SIX-FILE
ROTATION` or `PRESERVE THE SIX-FILE ROTATION UNACCEPTED`.

## 2. Dashboard V2 architecture gap inventory

**Current candidate path**

- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_ARCHITECTURE_GAP_INVENTORY_2026-08-17.md`

**Tier:** T2 documentation/evidence. The report describes later T0/T1 work, but
the inventory itself is T2.

**Review history:** the durable checkpoint records that its only T2 review was
non-accepting and requested one host-risk classification repair plus two truth
clarifications. The reviewer identity and exact printed verdict token are not
recorded in the repo evidence inspected for this packet. The one-round cap is
recorded as consumed.

**Reproduced required findings:**

1. WP-D7 had to be classified **T0 by highest-risk-wins** because it includes
   KVM2 deployment/host-load measurement, backup/restore and owner controls;
   later KVM2 measurement also needs separate host-contact authorization.
2. The report had to describe `docs/30` as an **uncommitted working-copy diff**,
   not as an accepted or line-count-defined change.
3. The Help candidate truth had to preserve both known LLM defects: configuration
   can be read/served/displayed without activating an LLM gate, and a generic
   `LLM_SKIPPED` decision row is stored even though no directive or model-call
   record is persisted.

**Repair status:** all three corrections are present in the current candidate.
No new review accepted those repaired bytes.

**What remains unaccepted:** the entire gap inventory, its work-package
sequencing and its descriptions of proposed V2 work. The report itself grants
no host contact, no architecture selection and no acceptance of the separate
Help or `docs/30` candidates.

**Risk of an extra round:** a broad review could accidentally be read as
accepting embedded external ideas, Help wording or later T0 host/control work.
Any exception must cover only the current inventory document and only its T2
truth/consistency review.

**Narrow owner decision:** `AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT GAP
INVENTORY` or `PRESERVE THE GAP INVENTORY UNACCEPTED`.

## 3. Strategy research owner decision packet

**Current candidate path**

- `MTC_COMMAND_CENTER/11_TRIAGE/STRATEGY_RESEARCH_OWNER_DECISION_PACKET_2026-08-17.md`

**Tier:** T2 documentation/evidence. It proposes an owner choice; it authorizes
neither strategy implementation nor compute.

**Review history:** the durable checkpoint records that the sole T2 reviewer
found two source/rule overclaims and did not accept the packet. The reviewer
identity and exact printed verdict token are not recorded in the repo evidence
inspected for this packet. The single round is treated as consumed.

**Reproduced required findings:** the corrected text shows the two bounded
source/rule problems:

1. Transcript attribution overstated stock applicability, symmetric direction
   and not predicting direction in advance. These are now explicitly described
   as intake-derived or proposed research choices, not transcript mandates.
2. The claimed canonical minimum of at least eight symbols was unsupported and
   had to be removed. The seven-symbol discovery scope is now described only as
   a conservative proposal, not a canonical minimum or promotion rule.

**Repair status:** both exact attribution/scope repairs are present in the
current packet. No backtest or strategy implementation was launched.

**What remains unaccepted:** the whole owner-choice packet, including its
recommendation and proposed seven-symbol/4-hour discovery package. Choosing to
review the document is not choosing strategy option A, B or C.

**Risk of an extra round:** review acceptance could be misunderstood as strategy
approval or promotion evidence. The exception must be limited to documentation
truth and must preserve the separate owner decision and all research gates.

**Narrow owner decision:** `AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT
STRATEGY DECISION PACKET` or `PRESERVE THE STRATEGY PACKET UNACCEPTED`.

## 4. Dashboard V2 external pattern addendum

**Current candidate path**

- `MTC_COMMAND_CENTER/11_TRIAGE/DASHBOARD_V2_EXTERNAL_PATTERN_ADDENDUM_2026-08-17.md`

**Tier:** T2 supplemental documentation/research.

**Review history:** DeepSeek V4 Pro, through the sandboxed
`_deepseek_driver`, read the candidate, the gap inventory, `docs/30`, relevant
Bridge source and `AGENTS.md`. It exhausted 24 iterations without calling
`finish()` and returned **no formal verdict**. The T2 round is treated as
consumed.

**Reproduced required findings:** no substantive finding was returned. Lead
inspection found three Markdown trailing-space warnings.

**Repair status:** the three whitespace warnings were removed and the no-index
whitespace check was recorded clean apart from the normal line-ending notice.
No reviewer accepted the corrected candidate.

**What remains unaccepted:** the entire addendum. Its Hyperliquid, private-phone
access, monitoring, multi-wallet/multi-strategy and authentication patterns are
research options only; none is an architecture decision or implementation
authorization.

**Risk of an extra round:** a new verdict could be misread as selecting one of
the options rather than validating source attribution and repo truth. The
exception must cover the current addendum only and preserve every owner choice
as open.

**Narrow owner decision:** `AUTHORIZE ONE FRESH T2 REVIEW OF THE CURRENT
EXTERNAL PATTERN ADDENDUM` or `PRESERVE THE ADDENDUM UNACCEPTED`.

## Separate issue — Help/Wiki T1 quota blocker

This is **not** one of the four T2 cap decisions.

- Candidate: the six-file local Help/Wiki feature isolated in
  `C:\BRIDGE_HELP_IMPL`.
- Tier: T1 non-economic product UI/tests.
- T1 round 1: fresh Codex `gpt-5.6-sol`, effort `high`, returned
  `REQUEST_CHANGES` with two LLM source-truth findings.
- The required Claude `claude-opus-5`, effort `high`, counterpart reproduced
  both findings and also corrected the intended field location:
  `llm_directive_id` is a trade-row field, not a decision-row field.
- No repair bytes were applied. The first implementer run lacked edit
  permission; the fresh edit-enabled run stopped at the Claude weekly quota,
  reported to reset at 2026-08-19 23:00 Europe/Chisinau.
- The final permitted T1 review round has **not** been used. After the exact
  counterpart route is available, the already-bounded repair, D026 RED/GREEN
  demonstration and validation must occur before that final review.

Therefore the Help/Wiki needs no T2 waiver and no extra T1 review authorization.
Its blocker is counterpart availability before repair, not an exhausted T1
review cap.

## Owner reply form

Reply with one choice for each row. A single `AUTHORIZE ALL FOUR` may be used
only if it means exactly one fresh T2 review of each current candidate, with no
general cap reset and no other authorization.

| Candidate | Choice |
|---|---|
| AI-memory six-file rotation | `AUTHORIZE ONE FRESH REVIEW` / `PRESERVE UNACCEPTED` |
| Dashboard V2 gap inventory | `AUTHORIZE ONE FRESH REVIEW` / `PRESERVE UNACCEPTED` |
| Strategy owner decision packet | `AUTHORIZE ONE FRESH REVIEW` / `PRESERVE UNACCEPTED` |
| Dashboard external pattern addendum | `AUTHORIZE ONE FRESH REVIEW` / `PRESERVE UNACCEPTED` |

No choice in this table authorizes Hostinger/KVM2 contact, deployment, ARM or
orders, credentials, strategy code/backtests, Help implementation, or acceptance
of any separate working-copy file.
