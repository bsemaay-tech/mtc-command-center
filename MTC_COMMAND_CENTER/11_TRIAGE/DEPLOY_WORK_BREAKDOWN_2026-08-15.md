Status: WORK BREAKDOWN — PLANNING ONLY, NO AUTHORITY, NO GATE OPENED

> **Superseded by `DEPLOY_WORK_BREAKDOWN_V2_2026-08-16.md` (2026-08-16).** Also:
> the "plan authority remains contested" reading rule is resolved — owner
> decision §3 (`OWNER_DECISIONS_2026-08-16_MORNING.md`) ratified the cumulative
> reading.

# Dependency-ordered deploy work breakdown — 2026-08-15

## Scope, frozen subject, and reading rule

This is a planning record over detached, initially clean worktree `C:\WBS` at
`4f367ce13c834d3c73ddf757de35f2b7281d9274`. It performs no work below and
grants no authority. The Gate-A integration runbook exists but was not executed
(`BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:824-833`); the old Gate-A candidate
passed A-0..A-9 only on its old bytes, and no PASS transfers to an integrated
candidate (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:232-255`). Stage-1
allocation, Commit 1, grant-#6 capture, targeted fills, and Commit 2 do not exist
(`AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-72`). Packet 9 lacks its
host run and closure, Packet 10 lacks its frozen checkpoint/baseline, and Packet
11 lacks final bound authority and a fresh freeze-time ratification
(`AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:3-10`; `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:110-122`).

The plan authority remains contested. The later active plan orders WP-I, Audit
2, WP-A, final freeze, Audit 3/Gate 6, Gate B, and WP-V
(`GLOBAL_HANDOFF.md:617-620`), while the unsuperseded KVM2 programme has its own
Phase 0→1→2→3→4 chain (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:239-248`).
Accordingly, the row catalogue below is used unchanged in two orderings. An
ordering is not authorization; the owner must first settle which reading
governs.

Audit tier for this document: **T2 documentation/evidence**. The kickoff's hard
no-sub-delegation rule prevented a reviewer dispatch; the checks at the end are
self-verification only.

## One row catalogue

`OWNER` means an owner decision/action rather than estimable implementer labour.
`NO SOURCED ESTIMATE` means the permitted evidence defines the work but gives no
disjoint row price. A conditional row remains one row and is performed only when
its stated condition occurs.

| Row | One and only one work unit | Hours and exact source |
|---|---|---|
| **R01** | **Choose exactly one Pathscope disposition (A/B/C/D).** This is the missing owner choice; do not infer it. | **OWNER.** Options and exact owner sentences: `PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:47-96,108-124`. |
| **R02** | Execute only R01's chosen disposition and obtain its specified closure/audit. This row includes the Option-B disclosure if B is selected; that disclosure is not another job. | **A 3–5 h; B 1–2 h; C 6–10 h; D 2–3 h**, sourced at `PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:49-96`. |
| **R03** | Authorize the branch-local **Gate-A-forward** release integration. This is separate integration/merge authority, not merge-to-`master` authority. | **OWNER.** The accepted Gate-A result carried no merge authority: `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:225-230`; the runbook boundary is `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:780-783`. |
| **R04** | Perform the Gate-A-forward merge from repaired WP-I, apply the exact README/WAL synthesis, enforce the 33-path blob fence, and record the candidate identities. | **3–5 h**, `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:293-295`; exact route/sequence: `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:209-225`. |
| **R05** | **Conditional only:** repair a merge-induced test/fixture/count issue, with D026 evidence. A product/deploy defect requires re-estimation rather than silently entering this row. The known repaired WP-I input already exists, so this row may close at zero. | **0–3 h**, `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:289-299`; current repaired input identity: `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:29-37`. |
| **R06** | Run the exact candidate's local acceptance matrix: scope/blob fences, focused and full Bridge suites, package reproducibility/falsification, credential-free and WAL matrices, and D026 checks. | **5–8 h**, `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:257-281,293-299`. |
| **R07** | Obtain the candidate's own T0 acceptance from the two fresh xhigh flagships. This is the pre-host candidate audit, not Audit 2 or Audit 3/Gate 6. | **8–16 h**, `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:283-285,293-299`. |
| **R08** | Execute fresh candidate-bound staging **A-0 through A-9** and issue a new exact-candidate staging verdict. Historical `2ce41e34…` results are inputs/templates only. | **5–9 h**, `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:229-230,239-255,300-301`. |
| **R09** | Produce the Stage-1 allocation record: `BASE`, P0/RO RUNIDs, stage IDs, `REMOTE_BASE`, token, root, grammar/collision results, and append-only dispositions. | **1–2 h**, `AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:62-70`. |
| **R10** | Create **Commit 1**, the exact read-only attestation-only preregistration, before any grant-#6 contact. | **1–2 h**, `AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66-68`. |
| **R11** | Resolve the narrow Stage-1/WP-I host-and-credential authority conflict, including whether the pinned SSH identity may be used. | **OWNER.** Exact missing confirmation and blocked work: `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:93-97,108-109`. |
| **R12** | Capture the grant-#6 read-only attestation and preserve mountinfo, namespace, mount, projection, producer, stdout/stderr/rc, path, bytes, and digests. | **0.5–1.5 h once access/inputs exist**, `AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:68-68`. |
| **R13** | Consume the capture into every allowed consumer; fill allocations/pins; reconcile identities/disclosures; build the final successor/runkit and composite proof. | **2–4 h**, `AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-69`. |
| **R14** | Prove Commit-1 ancestry, allowed delta, token/clean-HEAD/order/identity conditions; run exact-byte review; create **Commit 2** as the Stage-1 freeze. | **1.5–3 h**, `AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:70-70`. |
| **R15** | **Execute WP-I staging and close WP-I, thereby completing Packet 9.** This single row merges those three genuinely identical production units: it consumes rather than recreates R09–R14, executes ops 01–12/P0/RO/row 24, defines and produces the missing P9-15 inventory, binds/retrieves/indexes the evidence, and issues P9-17 closure. | **NO SOURCED ESTIMATE.** Packet 9's 17 components and producer gap: `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:19-45`; ordered production: `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:106-118`. A bounded Packet-9/WP-I price is not supplied; define P9-15's producer/command/evidence contract and estimate the frozen op plan. |
| **R16** | Freeze the full **pre-WP-A checkpoint** after immutable Packet-9 closure: full SHA, base/diff, file list, identities, unchanged-bits conclusion, and initial Packet-10 bundle inputs. | **NO SOURCED ESTIMATE.** `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-61,119-119`. Produce an exact freeze procedure and timed dry run. |
| **R17** | Define and execute Packet 10's **full Bridge suite at the frozen SHA in the locked environment**, recording command, environment, outputs, counts/node IDs/signatures, and adjudicated anomaly set (P10-10/11/12). | **NO SOURCED ESTIMATE.** The suite choice is already made but the exact freeze command/baseline is absent: `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:51-52`; gaps and required production are `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-71,120-120`. Freeze the command/evidence contract and time one isolated execution. |
| **R18** | Complete Packet 11's technical work: re-bind the existing authority-content source by final path/bytes/SHA, calculate the post-WP-I ledger, prove order/compliance, and finalize the go/no-go matrix. | **NO SOURCED ESTIMATE.** Required components: `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:73-92`; the existing consolidation is content, not the final bound Packet 11: `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:110-122`. Time the final binding/ledger procedure after R15. |
| **R19** | Ratify Packet 11's refreshed freeze-time balance after R18. The old ~55 h and current ~63.75 h snapshots do not pre-ratify the final number. | **OWNER.** `WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:93-97,110-111`; `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:85-92`. |
| **R20** | Finalize Packet 10's one authoritative dispatch manifest/bundle, binding the R17 baseline and final R18–R19 Packet-11 identity, identically for both auditors. | **NO SOURCED ESTIMATE.** `AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65-67,119-122`. Estimate after the bundle schema and exact member list exist. |
| **R21** | Run **Audit 2** on R16/R20 with the exact T0 roster and close any authorized repair/re-audit within its cap. | **NO SOURCED ESTIMATE.** The sources define roster/state, not a disjoint hour price; the active plan has only a shared 6 h reserve for Audit 2 + Audit 3 + Gate 6 + all re-audits: `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:211-215`. Obtain timed auditor executions; do not allocate the shared reserve twice. |
| **R22** | Execute **WP-A** on the retained host and preserve its evidence. | **3 h exactly**, the canonical WP-A budget confirmed at `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:214-214`; sequence: `GLOBAL_HANDOFF.md:617-619`. |
| **R23** | After WP-A evidence, freeze the **final exact SHA/artifact** that later acceptance and deployment will name. This is distinct from R16's pre-WP-A checkpoint. | **NO SOURCED ESTIMATE.** Required order: `GLOBAL_HANDOFF.md:618-620`; absence of a row price: `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:215-216`. Time a frozen identity/build procedure. |
| **R24** | Run **Audit 3 with Gate 6** on R23 and close only under the required verdict rules. | **NO SOURCED ESTIMATE.** It shares, but is not assigned, the same 6 h aggregate audit reserve described at `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:213-215`; order: `GLOBAL_HANDOFF.md:619-620`. Record timed executions rather than inventing a split. |
| **R25** | Close **Gate B** after R24. This row is the Gate-B decision only; it contains no WP-V approval or deployment work. | **OWNER.** Canonical position: `GLOBAL_HANDOFF.md:619-620`; omission from the refuted table: `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:225-231`. |
| **R26** | Give the separate **WP-V deployment approval** after Gate B. This is not R25, KVM2 install authority, cutover authority, secret authority, or first-start authority. | **OWNER.** `GLOBAL_HANDOFF.md:619-620`; separate authorization requirement: `NIGHT_CLAIM_VERIFICATION_2026-08-15.md:225-231`. |
| **R27** | Complete KVM2 Phase-0 technical governance: P0-01, P0-03, P0-04, P0-04A, and P0-05 (static facts, roster reconciliation, artifact/evidence layout, index/ledger, source-scenario reconciliation). | **NO SOURCED ESTIMATE.** Exact jobs: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:20-27,38-74`. Estimate each artifact after its write/validation contract is frozen. |
| **R28** | Complete KVM2 P0-01B live-state verification and P0-02 lifecycle decision. These are owner-controlled Phase-0 close inputs. | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:28-37`; phase close: `KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:241-244`. |
| **R29** | Complete KVM2 Phase-1 P1-01/P1-02: reproduce the hardened-host baseline and issue its redacted manifest. | **NO SOURCED ESTIMATE.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:76-87`. The readiness record's 2–4 h is inseparably bundled with later install/verification, so it is deliberately assigned to neither R29 nor R37; obtain a timed read-only baseline run. |
| **R30** | Accept or reject the Phase-1 baseline (P1-03). | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:88-90`. |
| **R31** | Complete the Phase-2 rebuild-kit designs P2-01 through P2-08 plus P2-10/P2-11: profiles, trusted inputs, identity/filesystem/network/service/secret/state/recovery/teardown/maintenance/incident contracts. No install. | **NO SOURCED ESTIMATE.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:92-157,168-187`. Scope and estimate the ten artifacts after inventorying which already exist and their acceptance state. |
| **R32** | Execute Phase-2 reproducibility rehearsal P2-09 on a named expendable clean environment and record VERIFIED or BLOCKED/UNVERIFIED. | **NO SOURCED ESTIMATE.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:158-167`. Produce a frozen rehearsal command/environment contract and time it. |
| **R33** | Accept the Phase-2 rebuild kit as preparation only (P2-12), including R32's honest verdict. | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:188-192`. |
| **R34** | Select the KVM2 risk-state continuity policy and approve its adversarial staging specification (P3-01). | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:197-207`; current recommended sentence: `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:175-193`. |
| **R35** | Close KVM2 Phase 3 / P3-05 after R04–R08 supply P3-02/P3-03/P3-04's exact candidate, staging, independent verification, and audits. This is a phase close, not a second candidate build, staging run, or audit. | **OWNER.** Phase-3 trace and close evidence: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:197-246`; crosswalk proving the modern work is consumed once: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:248-263`. |
| **R36** | Authorize exactly one KVM2 installation/configuration attempt for the accepted SHA, masked/unstarted, with no secret/cutover/start authority (P4-01). | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:265-277`. |
| **R37** | Perform the bounded KVM2 install/configuration and exact-SHA verification (P4-02): immutable hashes, Python/lock install, paths/unit/UFW/closed-port proof, service masked and unstarted. | **NO SOURCED ESTIMATE.** Exact P4-02 work: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:278-284`. The only 2–4 h source bundles R29 baseline with this row (`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:332-338`), so a disjoint install estimate requires a timed rehearsal. |
| **R38** | Make the backup/retention/monitoring-provider choices and separately provision the KVM2-specific TESTNET secret under P4-03. No value may enter evidence. | **OWNER.** Secret action: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:285-293`; owner choices: `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:158-173,230-260,332-338`. |
| **R39** | Finalize and tabletop the cutover-abort/PC-off/zero-dual-writer procedure (P4-04), with no live mutation. | **NO SOURCED ESTIMATE.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:294-303`. Time the frozen tabletop script and evidence write-up. |
| **R40** | Authorize exactly one Windows-writer quiesce with raw flat proof and no VPS start (P4-04A). | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:304-312`. |
| **R41** | Execute the required backups/rollback/isolated restore/logrotate/monitoring evidence package once. Ordering A places it before cutover under the newer readiness path; Ordering B places it after first start under the KVM2 Phase-4/5 sequence. It is never performed twice. | **3–6 h host labour**, `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:230-260,332-340`. KVM2 rollback evidence requirements: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:357-366`. |
| **R42** | Execute the ordered **single-writer cutover** and accepted WAL-consistent migration/reset proof (P4-05), after R40. | **1.5–3 h host labour**, `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:332-340`; exact ordered proof: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:313-330`. |
| **R43** | Authorize exactly one first DISARMED, TESTNET-only, loopback-only start of the named SHA (P4-06), no retry and no ARM. | **OWNER.** `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:331-336`; required sentence shape: `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:290-316`. |
| **R44** | Perform the **first DISARMED start** once (P4-07); verify exact artifact/state, health, reconcile, zero restarts, one loopback listener, no public 8790, TESTNET-only, no `HL_LIVE_ACK`, and preserve evidence. | **1–2 h host labour**, `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:332-340`; exact P4-07 contract: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:337-348`. |

## Ordering A — cumulative authority

This reading requires both complete gate systems. The valid dependency waves
are:

1. **Parallel preparation:** `R01 → R02` may run in parallel with KVM2
   `R27 + R28 → R29 → R30 → R31 → R32 → R33 → R34`. Within a `+` wave,
   different operators may work concurrently; host actions remain serialized.
2. **Shared release candidate:** after R02 and the Phase-2 close, obtain `R03`,
   then `R04 → R05(if triggered) → R06 → R07 → R08`. `R35` closes only after
   R33, R34, R07, and R08. R04–R08 are also P3-02/P3-03/P3-04 production; they
   are not repeated for R35.
3. **Stage-1 and WP-I:** `R09 → R10`; R11 may be obtained in parallel with
   R09–R10, but `R12` waits for both R10 and R11. Then
   `R12 → R13 → R14 → R15`.
4. **Pre-WP-A package:** `R16`; after it, R17 and the preparable portion of R18
   may run in parallel. Finish `R17 + R18 → R19 → R20 → R21`.
5. **Later active-plan gates:** `R22 → R23 → R24 → R25 → R26`.
6. **KVM2 Phase 4, only after both plans' joins:** R36 waits for **R26 and R35**.
   Then `R36 → R37 → R38 → R39 → R40 → R41 → R42 → R43 → R44`.

Important parallelism consequence: KVM2 Phase-0/1/2 preparation can overlap
Pathscope/candidate preparation, but no KVM2 install can overlap the
WP-I/Audit-2/WP-A/Audit-3 chain. R41 is before cutover here because the newer
readiness critical path explicitly orders rollback/backup/monitoring before the
single-writer cutover (`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:327-341`).

## Ordering B — KVM2 as its own programme

This reading preserves the same 44 rows but removes the active-plan chain as a
predecessor of KVM2 Phase 4:

1. **Two parallel programmes begin:** active-plan Pathscope `R01 → R02`, and
   KVM2 `R27 + R28 → R29 → R30 → R31 → R32 → R33 → R34`.
2. **Shared release input occurs once:** after the KVM2 Phase-2 close, obtain
   `R03`, then `R04 → R05(if triggered) → R06 → R07 → R08 → R35`.
3. **Fork after the shared candidate:**
   - active-plan branch: R09/R10 (with R11 in parallel) then
     `R12 → R13 → R14 → R15 → R16 → (R17 + R18) → R19 → R20 → R21 → R22 → R23 → R24 → R25 → R26`;
   - KVM2 branch: `R36 → R37 → R38 → R39 → R40 → R42 → R43 → R44 → R41`.

Thus KVM2 install/cutover/first-start may run in parallel with Stage-1, WP-I,
Audit 2, WP-A, Audit 3/Gate 6, Gate B, and WP-V **only if the owner ratifies this
authority reading and separately opens every KVM2 owner gate**. R41 moves after
R44 because the standalone KVM2 programme places P4-08 rollback after P4-07 and
then monitoring in Phase 5 (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:247-248`;
`KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:337-379`). This differs
from Ordering A's newer readiness ordering and is one reason the authority choice
cannot be inferred.

## Required-coverage index

| Required named item | Exactly-once row |
|---|---|
| Pathscope disposition | R01–R02 (decision and its chosen execution are distinct) |
| Stage-1 allocation and both commits | R09, R10, R14 |
| Grant-#6 read-only attestation capture | R12 |
| WP-I staging execution; WP-I closure; Packet 9 | **R15**, explicitly merged as one production/closure row |
| Packet 10 frozen-SHA locked-environment suite baseline | R17 |
| Packet 11 completion | R18–R19 (technical completion then owner ratification) |
| Pre-WP-A checkpoint freeze | R16 |
| Audit 2 | R21 |
| WP-A | R22 |
| Final exact-SHA/artifact freeze | R23 |
| Audit 3 with Gate 6 | R24 |
| Gate B | R25 |
| WP-V deployment approval | R26 |
| Gate-A-forward release integration | R03–R04 (authority then execution) |
| Candidate's own T0 acceptance | R07 |
| Fresh candidate-bound A-0..A-9 staging | R08 |
| KVM2 Phase-0/1/2/3 close gates | R27–R35; P3 technical work is R04–R08, not duplicated |
| KVM2 install and verification | R36–R37 |
| Backups, rollback, and monitoring | R38 decisions plus R41 execution |
| Single-writer cutover | R40 authority plus R42 execution |
| First DISARMED start | R43 authority plus R44 execution |

## Hours discipline, overlap removal, and honest subtotal

The withdrawn synthesis table and its 55–105 total are not used
(`DEPLOY_PATH_SYNTHESIS_2026-08-15.md:3-45,123-152`). Overlaps are resolved as
follows:

1. The integration design's **16–32 h candidate subtotal** is not counted as a
   row. It is decomposed exactly once into R04 3–5, R05 0–3, R06 5–8, and R07
   8–16 (`BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:293-300`).
2. R08's 5–9 h A-0..A-9 run is separate candidate-bound Gate-A staging. R15 is
   WP-I ops/closure/Packet 9; neither contains the other.
3. The reconciliation's 7–14.5 h Option-B scenario total is not counted. R02
   contains the chosen Pathscope disposition once, and R09–R14 use only their
   direct step estimates (`AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-86`).
4. R07's T0 audit labour is the candidate's pre-host acceptance. Audit 2 (R21)
   and Audit 3/Gate 6 (R24) are later, genuinely distinct checkpoints. The
   active plan's **single 6 h shared reserve** for R21 + R24 + all re-audits is
   assigned to neither row and excluded from the subtotal because no source
   disaggregates it (`NIGHT_CLAIM_VERIFICATION_2026-08-15.md:211-223`).
5. The readiness record's 2–4 h KVM2 baseline/install bundle spans R29 and R37;
   it is assigned to neither, preventing reuse. Its 3–6 h operations package is
   R41 once, its 1.5–3 h cutover is R42 once, and its 1–2 h first start is R44
   once (`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:332-341`).

Across the **15 sourced rows**, the disjoint subtotal excluding R02 is
**35.5–67.5 labour hours**. With exactly one Pathscope scenario, the sourced
subtotal is:

| Pathscope choice | Sourced subtotal only |
|---|---:|
| A | **38.5–72.5 h** |
| B | **36.5–69.5 h** |
| C | **41.5–77.5 h** |
| D | **37.5–70.5 h** |

There are **14 `NO SOURCED ESTIMATE` rows** and **15 `OWNER` rows**. A grand
total is therefore not honest: essential Packet 9/10/11, freeze, audit, KVM2
phase, baseline/install, and tabletop work still has no disjoint sourced price.

## Self-verification and boundary

- Catalogue count: **44 unique row IDs**; 15 sourced + 14 unsourced + 15 owner
  rows = 44.
- The required-coverage index maps every kickoff item to one production row or
  to a decision/execution pair; no item is absent.
- R04–R08 are reused as KVM2 P3-02/P3-03/P3-04 evidence, not performed again.
- R09–R14 are consumed by Packet 9, not reproduced inside R15.
- Byte-changing release integration is before WP-I, the pre-WP-A freeze, Audit
  2, final freeze, and Audit 3 in both orderings.
- No host, network, deployment, service, credential, broker/exchange, ARM,
  order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-master, push, or
  economic action is authorized or performed by this document.
