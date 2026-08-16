# NEXT_STEPS

> **Pathscope disclosure (owner decision 2026-08-16, section 6):** Pathscope is a supplemental aid only: its output may inform review, but it may never be cited as proof, a gate, or an acceptance input anywhere in WP-I or downstream, and no Pathscope PASS may close any gate.
> Governing record: MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_SUPPLEMENTAL_DISCLOSURE_V2_2026-08-16.md. Identity split: the prover in this repository is the older 137520-byte R5 code; the audited 185272-byte Option C prover is UNMERGED on codex/pathscope-accounting-redesign-20260815. Prerequisite gate 2 is UNKNOWN until the Lead re-derives it at freeze-prerequisite review.


> **Correction, 2026-08-16 morning:** the owner questions this draft lists are
> answered in `OWNER_DECISIONS_2026-08-16_MORNING.md` — §3 plan authority
> (cumulative, sentence adopted verbatim), §4 audit reserve (hard cap, metered),
> §5 archive (adopted verbatim), and §6 Pathscope (Option C cycle consumed in a
> non-accepting audit; disposition is supplemental-with-disclosure — the
> WPI-PATHSCOPE-C section's closure condition is void). Fold these in before
> promoting this draft to `_AI_MEMORY/NEXT_STEPS.md`.

> Current through 2026-08-15 night. This is a planning/status document, not
> acceptance or authority. No host, deployment, credential, trading, merge-to-
> master, or other operational gate is opened here.

## Immediate order

1. Finish the owner-authorized Pathscope Option C redesign and its one fresh
   flagship execution audit.
2. Resolve the three immediate owner decisions below; plan authority controls
   which prerequisite ordering governs.
3. Prepare the Gate-A-forward Bridge integration route, but do not execute its
   unapproved runbook or carry old Gate-A acceptance onto new bytes.
4. Complete the Stage-1 allocation and root-channel facts, then create Commit 1.
   Only after Commit 1 may its exact read-only capture run.
5. Continue through Commit 2, WP-I/Packet 9, Packet 10/11, Audit 2, WP-A, final
   freeze, Audit 3/Gate 6, Gate B, and separately approved WP-V in the ordering
   selected by the owner.

## Open work

### WPI-PATHSCOPE-C | IN PROGRESS 2026-08-15 [AI: Claude]

- Barış authorized Option C: replace the accounting layer so every admitted
  member receives exactly one terminal disposition; do not add another set of
  shape patches. One fresh flagship execution audit is authorized after the
  redesign. A required finding returns the lane to the owner boundary.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-28`)
- Closure condition: implemented accounting invariant, full existing harness and
  fixtures with discriminating RED/GREEN evidence, Lead execution, and an
  accepting fresh audit. Until then Pathscope and Audit-2 gate 2 remain open.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:118-124`)

### BRIDGE-RELEASE-INTEGRATION | PLANNED, NOT EXECUTED [AI: Claude]

- The selected design route is Gate-A-forward into the repaired WP-I line. Keep
  Gate-A blobs where specified, synthesize the Linux README, replay the accepted
  WAL-test repair, and enforce the 33-path blob fence. Reimplementation and a
  Gate-A-first partial forward-port are rejected/fallback routes.
  (`11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:1-9,193-225`)
- The runbook is explicitly not executed and not authorized to execute. Any
  integrated candidate needs its own local matrix, two-flagship T0 acceptance,
  and fresh candidate-bound A-0 through A-9; no old runtime PASS transfers.
  (`11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:1-23`;
  `11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:227-250,257-285`)
- The two suite repairs are valid inputs, not a release: replay them semantically
  during integration and reprove them on the exact frozen candidate.
  (`11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:66-78`)

### WPI-STAGE-1 | BLOCKED ON COMMIT 1 [AI: Claude]

- The owner approved the narrow read-only `GATEA-STAGING` grant, but its own
  precondition is unmet: the exact preregistration and allocation record do not
  exist. No host contact is inside the grant before Commit 1.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-60`)
- Commit 1 is blocked until the root-channel/capture facts are complete: exact
  candidate and staging identity, grant and read-only limit, capture surface,
  producer identity, argv, clean environment, cwd, output grammar, capture route,
  package manifest, and clean-HEAD binding. The Packet-9 skeleton still marks the
  authority and producer fields `PENDING-STAGE-1`.
  (`11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET9_SKELETON_2026-08-12.md:35-47`;
  `11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-526`)
- What settles it: independently source those facts, allocate the one-use IDs,
  and commit an attestation-only document with no unfilled command, path,
  authority, grammar, or producer field. Observed attestation values remain
  explicit non-consumable placeholders until the later committed capture.

## Owner decisions needed now

### OWNER-PLAN-AUTHORITY | OPEN [AI: Barış]

- Decide whether the 50-hour sequence and KVM2 Phases 0-4 are cumulative, or the
  KVM2 programme governs on its own. No existing sentence establishes precedence.
  Until decided, only already-authorized local/read-only preparation that crosses
  neither plan's gates is safe.
  (`11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:5-13,158-166`)

### OWNER-AUDIT-RESERVE | OPEN — UNKNOWN ALLOCATION [AI: Barış]

- The active plan has one shared 6-hour WP-R reserve for Audit 2, Audit 3, Gate 6,
  and all re-audits; no source allocates it among those distinct checkpoints or
  supports the larger per-row estimates. What settles it: an explicit owner record
  retaining that shared cap or approving a revised reserve/allocation after timed
  executions. Do not count the same six hours twice.
  (`11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:211-215`;
  `11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:175-179`)

### OWNER-PAPER-ARCHIVE | OPEN [AI: Barış]

- Decide whether the pre-cutover paper-period risk state must be archived off-host
  before the fresh start or may remain on the old machine. The Lead recommends an
  archive; no decision is recorded. The decision is not a blocker for work before
  cutover.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:112-116`)

## Current planning register

### DEPLOY-WORK-REGISTER | ACTIVE PLANNING REFERENCE [AI: Any]

- Use `11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md` as the dependency catalogue,
  with the later owner decisions in this document applied as deltas. It contains
  44 unique work units and two orderings because plan authority is unresolved.
  (`11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:19-36,85-133,200-209`)
- For authorized Option C, its sourced-row subtotal is 41.5-77.5 labour hours.
  This is not a grand total: 14 rows have `NO SOURCED ESTIMATE`, and owner actions
  are not implementer labour. The current full total is **UNKNOWN**. It becomes
  estimable only after the unsourced work contracts are frozen and timed and the
  register is rebased against the night decisions.
  (`11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:161-198`)

## Closed decisions and accepted work

### WPI-RP7-R1-R4 | CLOSED — T0 ACCEPTED 2026-08-15 [AI: Any]

- RP7 rows 1-9 are accepted only on candidate `80cbed461d0b0371e6eabbfff0e732e5001affaf`:
  Codex PASS and Claude PASS-WITH-NITS, zero required repairs. This does not accept
  Pathscope or authorize Stage 1. Changing the accepted bytes reopens T0.
  (`11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_FINAL_ACCEPTANCE_2026-08-15.md:3-12,22-27,65-82`)

### BRIDGE-SUITE-A1-A2 | CLOSED AT T1, UNMERGED 2026-08-15 [AI: Any]

- The LF ledger-identity repair and dynamic schema-version test repair are T1
  accepted: 1021 tests passed twice; the fresh Claude audit returned
  PASS-WITH-NITS with zero required changes. They are not merged, not a release,
  and do not satisfy the exact-release-SHA deploy gate.
  (`11_TRIAGE/BRIDGE_SUITE_ANOMALY_LEAD_ADJUDICATION_2026-08-15.md:3-17,19-49,66-72`)

### OWNER-D2/D3 | DECIDED WITH CARRIED PRECONDITIONS [AI: Any]

- D2 approved the narrow read-only staging grant, but it remains unspendable until
  Commit 1 and its allocation exist. D3 signed the approximately 63.75-hour
  Packet-11 snapshot as of 2026-08-15; the value must be re-presented if it changes
  at the real freeze checkpoint.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-78`)

### OWNER-D4 | DECIDED — WALLET DEFERRED [AI: Barış]

- The KVM2-specific TESTNET wallet is deferred. No wallet is provisioned or
  inferred; first start remains blocked when the sequence reaches that requirement.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:80-87,118-127`)

### OWNER-D5 | DECIDED — START CLEAN [AI: Claude]

- Use a fresh-database reset, not WAL migration. The deploy proof must still
  preserve or block on lost risk/history evidence and retain the single-writer
  empty-orders/positions proof. The separate archive decision remains open above.
  (`11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-116`)
