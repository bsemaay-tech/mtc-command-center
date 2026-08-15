# Stage-1-to-Audit-2 execution runbook

Status: **ordered operator reference only — not executed, not an acceptance, not an authorization, and not a dispatch.** This document itself permits no host, network, SSH, deployment, service, credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC, trading, merge-to-`master`, push, product-code, or economic action. (`C:\tmp\lane_kick\Y5.md:52-56`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:3-5,88`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:1-9`)

The endpoint is **Audit 2 dispatch**, not an Audit 2 verdict, repair, acceptance, WP-A action, or later deployment step. Audit 2 must review an already frozen pre-WP-A checkpoint, and WP-A may not begin before an accepting Audit 2 close record. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:5-7,20-31`; `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:617-620`)

## Non-negotiable controls

### Classification

Every numbered step is marked `LOCAL`, `OWNER DECISION`, or `AUTHORIZED HOST ACTION`, as required by the task contract. A label describes the kind of future step; it does not supply authority to perform it. (`C:\tmp\lane_kick\Y5.md:47-49`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:19-25`)

### Dual-form identity rule

For **every identity-bearing repository file, artifact, manifest, record, or bundle member**, record both forms in the same evidence row:

1. worktree/on-disk byte count and SHA-256; and
2. Git-object byte count and SHA-256 plus blob OID.

Record the derivation mode/command for each form. If the forms happen to be identical, record both and state equality; do not collapse them into one identity. If an evidence object has not yet been admitted to Git, record its source-byte identity immediately, but it cannot satisfy a commit, freeze, or dispatch gate until the corresponding worktree and Git-object forms are both recorded. Missing either form is `IDENTITY_STOP`. (`C:\tmp\lane_kick\Y5.md:38-45`; `.gitattributes:1-2`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:6-27,46-64`)

This is load-bearing: a prior table mixed LF Git-object and CRLF Windows-worktree identities and was impossible to reproduce; the corrected contract used worktree bytes/SHA-256, Git-blob bytes/SHA-256, and blob OID. The same ambiguity later appeared as a third instance in two days. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:8-27,48-57`; `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:24-29`)

### Stage-1 host barrier — two gates, both mandatory

The grant-#6 capture in Step 12 is unreachable until **both** of these tokens exist:

- `COMMIT_1_GATE=PASS`: Step 10 produced the exact committed attestation-only preregistration and recorded its exact Commit-1 object ID and dual-form identities; and
- `AUTHORITY_GATE=PASS`: Step 11 bound Barış's narrow sentence to those exact committed bytes and to no broader action.

The grant is real but was explicitly recorded as unspendable until the exact preregistration is committed. Any host contact before Commit 1 is outside the grant. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-52`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:488-528`)

```text
Step 10 COMMIT_1_GATE=PASS
          AND
Step 11 AUTHORITY_GATE=PASS
          |
          v
Step 12 may become reachable
```

No operator may bypass, parallelize across, or infer either gate. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:497-526,528-533`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:25-28,106-113`)

## Contested plan authority

The governing plan reading remains an owner question; the catalogue says an ordering is not authorization and the owner must settle which reading governs. The later owner-decision record still lists the plan-authority choice as outstanding, so the selected reading is **UNKNOWN** until an owner record establishes it. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:19-25`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:129-131`)

| Reading | Order relevant to this runbook | Different part outside this runbook |
|---|---|---|
| **A — cumulative authority** | Pathscope and KVM2 preparation feed one shared candidate; after the shared candidate, `R09 -> R10`, with `R11` parallel but `R12` waiting for both, then `R13 -> R14 -> R15 -> R16 -> (R17 + preparable R18) -> R19 -> R20 -> R21`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:85-102`) | KVM2 Phase 4 waits for both the active-plan chain through R26 and the KVM2 Phase-3 close. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:103-110`) |
| **B — KVM2 as its own programme** | The active-plan branch is still `R09/R10` (with `R11` parallel), then `R12 -> R13 -> R14 -> R15 -> R16 -> (R17 + R18) -> R19 -> R20 -> R21`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:112-124`) | KVM2 Phase 4 may fork after the shared candidate only if the owner ratifies this reading and separately opens every KVM2 owner gate. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:126-133`) |

**Unaffected steps:** whichever reading is selected, Steps 1-22 below retain the same dependency order through Audit 2 dispatch; only the out-of-scope KVM2 Phase-4 relationship differs. Both readings also place the same shared release candidate before Stage 1. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:90-101,117-124`)

## Ordered execution steps

### 1. `OWNER DECISION` — record the governing plan reading

- **What:** Obtain an owner record selecting Ordering A or Ordering B; do not infer the choice.
- **Exact precondition:** None established beyond the existence of the contested readings; current selection is `UNKNOWN`.
- **Governing document/section:** `DEPLOY_WORK_BREAKDOWN_2026-08-15.md`, “Scope, frozen subject, and reading rule” and “Ordering A/B.” (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:19-25,85-133`)
- **Evidence:** Owner-authored selection, exact source path/date, limits, and dual-form identity record.
- **Stop:** No selected reading, or language that is not an explicit choice, means stop before treating either ordering as authority.
- **Estimate:** `OWNER`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:19-25`)

### 2. `OWNER DECISION` — verify the recorded Pathscope Option C decision

- **What:** Bind the already recorded choice: one accounting-layer redesign, followed by one fresh flagship execution audit; the parser stays and the reporting layer is replaced.
- **Exact precondition:** The exact D1 owner record must be present; no different option or broader repair cycle may be inferred.
- **Governing document/section:** `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md`, D1; `PATHSCOPE_DECISION_OPTIONS_2026-08-15.md`, “Option C.” (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:8-28`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:74-87,108-124`)
- **Evidence:** Exact owner sentence and source identity, recorded in both forms.
- **Stop:** Any attempt to substitute A/B/D, add open-ended repair rounds, or redesign by merely recognizing three more shapes returns to the owner boundary.
- **Estimate:** `OWNER`. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:21-28`)

### 3. `LOCAL` — execute only Option C and close its one audit

- **What:** Produce the accounting invariant, implementation, full-fixture execution evidence, and the one fresh flagship execution audit required by D1.
- **Exact precondition:** Step 2's exact Option C authority is bound; the work remains limited to the accounting/reporting layer and its existing harness.
- **Governing document/section:** `PATHSCOPE_DECISION_OPTIONS_2026-08-15.md`, “Why it keeps happening” and “Option C”; D1 scope limits in the owner record. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:26-45,74-87`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:13-28`)
- **Evidence:** Design note; exact changed-byte identities in both forms; full fixture/harness command and real output; fresh audit session identity, execution proof, and accepting verdict with zero required repair.
- **Stop:** A required audit finding stops the lane at the owner boundary; D1 supplies no repair round. Stage-1 remains blocked until Pathscope closes. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:19-28`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:123-124`)
- **Estimate:** `6-10 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_DECISION_OPTIONS_2026-08-15.md:74-87`)

### 4. `OWNER DECISION` — authorize the branch-local Gate-A-forward integration

- **What:** Obtain the separate release-integration authority; it is not merge-to-`master` authority.
- **Exact precondition:** Step 3 accepted; the applicable KVM2 Phase-2 close required by both readings exists. The current completion state of that close is `UNKNOWN` in the permitted sources.
- **Governing document/section:** Work-catalogue R03 and both ordering sections. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:42-42,90-96,117-120`)
- **Evidence:** Exact owner authority record naming the branch-local integration and its limits, in both identity forms.
- **Stop:** Missing integration authority or missing Phase-2 close means no integration work.
- **Estimate:** `OWNER`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:42-42`)

### 5. `LOCAL` — create the exact integrated candidate

- **What:** Perform the Gate-A-forward integration, exact README/WAL synthesis, 33-path blob fence, and runtime observation of the new candidate identities; use the conditional repair lane only for a merge-induced fixture/count issue.
- **Exact precondition:** Step 4 authority exists; the repaired WP-I input, Gate-A input, merge base, and anomaly-repair/D026 evidence match the frozen runbook inputs.
- **Governing document/section:** `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md`, “Recommended future sequence”; `BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md`, §§1, 7, 8. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:209-225`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:29-37,767-783,785-833`)
- **Evidence:** Exact two-parent local candidate SHA/tree OID observed at runtime; 33-path fence; expected first-parent scope; clean final state; dual-form identities for every frozen input/output.
- **Stop:** Any frozen identity, ancestry, merge shape, conflict path, fence member, suite result, hook, scope, or runtime identity differing from the runbook stops without improvisation; a product/deploy defect requires re-estimation, not the conditional row. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md:785-822`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:43-44`)
- **Estimate:** `3-5 h`, plus `0-3 h` only if the merge-induced conditional row is actually triggered. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:43-44`)

### 6. `LOCAL` — run the candidate's local acceptance matrix

- **What:** Run scope/blob fences, syntax/import checks, focused and full locked-runtime suites, D026 RED/GREEN, package reproducibility/falsification, credential-free, and WAL matrices.
- **Exact precondition:** Step 5 produced one frozen exact candidate and immutable identity package; no untracked build input exists.
- **Governing document/section:** `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md`, §6 “Local matrix before host rerun.” (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:257-281`)
- **Evidence:** Commands, environments, stdout/stderr/rc, exact node IDs, RED and GREEN arms for each claimed regression closure, reproducible package inventories/hashes, and all identities in both forms.
- **Stop:** Any unexplained failure, absent executed RED, reproducibility mismatch, or identity mismatch means no candidate acceptance audit.
- **Estimate:** `5-8 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:45-45`)

### 7. `LOCAL` — obtain the candidate's own T0 acceptance

- **What:** Two fresh xhigh flagship auditors independently execute the mandatory matrix on the exact candidate; this is not Audit 2.
- **Exact precondition:** Step 6 is complete and frozen; both auditors receive the same exact candidate/evidence and no implementer-session context.
- **Governing document/section:** `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md`, §§6-7; work-catalogue R07. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:283-305`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:46-46`)
- **Evidence:** Two independent session records, executed matrix output, exact candidate dual identities, and accepting verdicts with zero required repair.
- **Stop:** Non-execution is BLOCK; a required product/deploy finding enters only an authorized bounded repair/re-audit and stops when the T0 cap is exhausted.
- **Estimate:** `8-16 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:283-305`)

### 8. `AUTHORIZED HOST ACTION` — fresh candidate-bound A-0 through A-9

- **What:** Re-run staging A-0..A-9 on the exact integrated candidate and issue a new candidate-bound staging verdict.
- **Exact precondition:** Step 7 accepted and a separate exact host authorization for this A-0..A-9 run exists. That separate authorization is `UNKNOWN` in the permitted sources; the D2 grant in Step 11 is limited to grant-#6 capture and WP-I operations and must not be broadened. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:226-230`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`)
- **Governing document/section:** `BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md`, §5 “Re-acceptance”; work-catalogue R08. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:232-255`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:47-47`)
- **Evidence:** Fresh A-0..A-9 logs/hashes, exact candidate/artifact/manifest identities in both forms, and a new staging-only verdict.
- **Stop:** No separate host authority means stop. No historical A-0..A-9 PASS transfers to the new bytes; any failed gate or identity mismatch stops the sequence. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:234-255`)
- **Estimate:** `5-9 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:47-47`)

### 9. `LOCAL` — produce the Stage-1 allocation record

- **What:** Allocate the concrete `BASE`, P0/RO RUNIDs, stage IDs, `REMOTE_BASE`, confirmation token, operator root, collision/grammar results, and append-only dispositions.
- **Exact precondition:** Steps 3-8 are closed on one exact candidate; no downstream lane treats any allocation as already existing.
- **Governing document/section:** Freeze-blocker reconciliation §3 order 3; Packet 9 P9-01. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-67`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:23-25,106-110`)
- **Evidence:** Literal generator command, shell version, stdout/stderr/rc, all allocated values, grammar/equality/collision results, burn-ledger entries, and dual-form identity record.
- **Stop:** Any invalid grammar, equality/collision failure, missing append-only disposition, or pre-existing allocation means stop; do not guess a value.
- **Estimate:** `1-2 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:66-66`)

### 10. `LOCAL` — create Commit 1 and set `COMMIT_1_GATE`

- **What:** Commit the exact attestation-only, non-WP-I-dispatchable preregistration with producer, argv, clean environment, cwd, output grammar, capture universe, placeholders, package manifest, and clean-HEAD binding rule.
- **Exact precondition:** Step 9's allocations are complete and collision-free; no attestation-derived value has been observed or inserted.
- **Governing document/section:** Successor preregistration §5.2, “Commit 1”; Packet 9 P9-02. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:488-528`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:26-26,110-110`)
- **Evidence:** Exact Commit-1 object ID; proof the procedure and manifest are contained in clean current `HEAD`; proof no derived value or unfilled command/path/grammar/authority/producer field exists; full dual-form identity table. Only then record `COMMIT_1_GATE=PASS`.
- **Stop:** Any missing field, observed value in Commit 1, dirty checkout, object/content mismatch, or absent dual identity keeps `COMMIT_1_GATE` unset and makes Step 12 unreachable.
- **Estimate:** `1-2 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:67-67`)

### 11. `OWNER DECISION` — bind the narrow host/credential sentence and set `AUTHORITY_GATE`

- **What:** Verify that Barış's recorded D2 sentence applies to the **exact preregistered and committed** Step-10 bytes and only to the grant-#6 capture and WP-I operations on `GATEA-STAGING`, with the pinned SSH identity used solely for those actions.
- **Exact precondition:** `COMMIT_1_GATE=PASS` and the exact Commit-1 identity exists. The owner sentence alone, evaluated before Commit 1, is not spendable.
- **Governing document/section:** Owner decisions D2; authority consolidation §3 host-and-credential sentence. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-60`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md:87-97`)
- **Evidence:** Exact owner sentence/source, exact Commit-1 object ID it attaches to, host/action/credential limit, and dual-form source identity. Only then record `AUTHORITY_GATE=PASS`.
- **Stop:** Any mismatch in bytes, host, action, credential, or scope; any attempt to use KVM2 or another credential; or absent Commit 1 keeps `AUTHORITY_GATE` unset.
- **Estimate:** `OWNER`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:50-50`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:40-58`)

### 12. `AUTHORIZED HOST ACTION` — execute the Commit-1-bound grant-#6 capture

- **What:** Run only the exact committed read-only capture and close/hash the operator-side record.
- **Exact precondition:** `COMMIT_1_GATE=PASS AND AUTHORITY_GATE=PASS`; clean current `HEAD` equals Commit 1; the recorder proves the committed procedure/manifest before opening a socket or starting the root command.
- **Governing document/section:** Successor preregistration §5.2, “Only after Commit 1”; Packet 9 P9-03. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:519-548`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:27-27,111-111`)
- **Evidence:** First field `attestation_prereg_commit=<COMMIT_1>`; byte-preserved mountinfo; namespace, root-mount, covering-mount, and projection-v2 outputs; producer/status; stdout/stderr/rc; record path/bytes/SHA-256; then dual-form identity binding when admitted to the evidence freeze.
- **Stop:** Either gate absent, dirty/different `HEAD`, malformed/incomplete/unequal capture, status/grammar failure, or any write/broader action means immediate stop; no WP-I op runs in this interval. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:484-484,528-548`)
- **Estimate:** `0.5-1.5 h once access and inputs exist`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:68-68`)

### 13. `LOCAL` — consume captured values into every allowed consumer

- **What:** Derive each captured value once, perform allowlisted targeted fills, populate all duplicated consumers, reconcile accepted identities/disclosures, finalize the deterministic successor/runkit, and execute the composite conservation proof.
- **Exact precondition:** Step 12's capture record is closed, hashed, complete, and bound to Commit 1.
- **Governing document/section:** Successor preregistration §5.2, “Commit 2”; reconciliation §3 order 6. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:550-579`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-69`)
- **Evidence:** Every placeholder replaced consistently; final allocations/pins, block/support/archive/tool identities, capture identity/status, accepted composite proof, zero unresolved dispatch tokens, and dual-form identity table.
- **Stop:** Any read/parse/projection/status/completeness/digest error, inconsistent duplicate consumer, unresolved token, or change to the Commit-1 observation procedure means no Commit 2. A changed procedure requires a new Commit 1 and a new authorized capture. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:554-573`)
- **Estimate:** `2-4 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:69-69`)

### 14. `LOCAL` — prove order/identity and create Commit 2, the Stage-1 freeze

- **What:** Prove strict Commit-1 ancestry, allowed Commit-1-to-Commit-2 delta, evidence digest binding, clean-current-HEAD ordering, final exact identities, and exact-byte review; then create Commit 2.
- **Exact precondition:** Step 13 is complete; Commit 1 is unchanged; every final identity has both forms; no transport op exists or predates Commit 2.
- **Governing document/section:** Successor preregistration §5.2, “Mechanical order-violation check”; Packet 9 P9-04/P9-06. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:581-607`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:28-30,112-113`)
- **Evidence:** Commit-2 object ID; Commit-1 ID; strict ancestry; exact allowed delta; capture path/bytes/SHA/producer/status; clean-HEAD proof; emitted `wpi_prereg_commit=<COMMIT_2>`; no unresolved token; full dual-form freeze table.
- **Stop:** Any predicate failure emits the fixed order-stop disposition, burns the attestation values and RUNIDs for dispatch, and stops before host contact; timestamps alone are not order evidence. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:583-607`)
- **Estimate:** `1.5-3 h`. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:70-70`)

### 15. `AUTHORIZED HOST ACTION` — execute the frozen WP-I transport/stages

- **What:** Using Commit 2 only, execute ops 01-10 in their frozen order: topology/upload/verify, P0, RO, row-24 probe, always-close records, and retrieval. This consumes but does not recreate Stage-1 evidence.
- **Exact precondition:** Step 14 Stage-1 freeze and mechanical preflight pass; `AUTHORITY_GATE=PASS` still matches the exact scope; transport current `HEAD` is clean Commit 2; the missing P9-15 producer/command/evidence contract is defined before WP-I closure.
- **Governing document/section:** Packet 9 “Combined production order” steps 7-10 and P9-05 through P9-14. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:29-41,106-118`)
- **Evidence:** Complete op records; immutable P0/RO logs and rows 1-24 results; close digests; retrieved trees; RUNID/path/bytes/SHA bindings; dual-form identities at evidence admission.
- **Stop:** Sequence mismatch skips non-`always` work as specified; close established trees through the declared `always` operations. Any authority, scope, identity, no-clobber, upload/extract, stage, close, or retrieval failure stops further ordinary operations and preserves the first divergence. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:31-38,114-117`)
- **Estimate:** `NO SOURCED ESTIMATE`. The catalogue explicitly supplies none for the combined WP-I staging/closure/Packet-9 unit. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54-54`)

### 16. `LOCAL` — bind evidence and close immutable Packet 9

- **What:** Run local ops 11/12 binding, produce the static security/secret/egress inventory under a newly defined exact contract, then issue the current-state index, final evidence index, and WP-I closure/ledger.
- **Exact precondition:** Step 15 retrieval is complete; remote close records are stable; every Packet-9 component has a producing contract. P9-15 currently has no defined producing step in the source scope, so that gap must be closed explicitly before this step can pass.
- **Governing document/section:** Packet 9 P9-11, P9-14 through P9-17, “Packet-9 gap result,” and combined-order step 11. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:35-45,117-118`)
- **Evidence:** All 17 mandatory Packet-9 components; per-file remote/local equality; P9-15 exact command/universe/output contract; indexed retained files with paths/bytes/SHA/provenance; closure PASS/FAIL/STOP and first divergence; prospective hour booking; dual-form identities.
- **Stop:** Undefined P9-15, any missing/unindexed file, binding mismatch, unresolved result, or absent closure record means Packet 9 is incomplete and Step 17 is forbidden.
- **Estimate:** `NO SOURCED ESTIMATE`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:54-54`)

### 17. `LOCAL` — freeze the full pre-WP-A checkpoint

- **What:** After immutable Packet-9 closure, freeze the full SHA and begin Packet 10 with the exact base/diff, file list, identities, closure evidence, scope/rules, and bundle inputs.
- **Exact precondition:** Step 16 proves Packet 9 complete and immutable; Audit 2 has not dispatched and WP-A has not begun.
- **Governing document/section:** Packet 10 P10-01 through P10-09 and combined-order step 12; freeze prerequisites gates 4-5. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-61,119-119`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:16-17`)
- **Evidence:** Full frozen SHA; base SHA and exact base-to-freeze diff; frozen file list; candidate/artifact/manifest bundle; actual frozen payload; WP-L and Packet-9 identities; exact-current acceptance/freeze sources; scope contract; all identities in both forms.
- **Stop:** Packet 9 not immutable, any placeholder, missing exact diff/file, single-form identity, or attempted inference of unchanged bits means no checkpoint and no Audit 2 bundle.
- **Estimate:** `NO SOURCED ESTIMATE`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:55-55`)

### 18. `LOCAL` — define, run, and adjudicate the frozen-SHA mandated suite

- **What:** Define the authoritative suite contract, execute it at the frozen SHA in the locked environment, and adjudicate the exact anomaly set, closing P10-10/P10-11/P10-12.
- **Exact precondition:** Step 17 exact frozen SHA exists; one authoritative source can fill every baseline field before execution. Old failure examples and counts are not a baseline.
- **Governing document/section:** `AUDIT2_AUDITOR_SESSION_INPUTS.md`, §5; Packet 10 P10-10 through P10-12. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-71,120-120`)
- **Evidence:** `MANDATED_COMMAND`, expected rc/counts/test IDs/signatures/skip-xfail counts, baseline source; exact cwd/environment/stdout/stderr/rc; output bytes/SHA; frozen-SHA proof; observed and authorized anomaly register; dual-form identities.
- **Stop:** No authoritative command/baseline, substitute command, inferred anomaly, unadjudicated output, or identity mismatch means Packet 10 remains non-authoritative.
- **Estimate:** `NO SOURCED ESTIMATE`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:56-56`)

### 19. `LOCAL` — complete Packet 11 technical authority/ledger work

- **What:** Re-bind the authority-content source by final path/bytes/SHA, calculate the post-WP-I freeze-time ledger, prove order/compliance, and finalize the go/no-go matrix. The preparable portion may overlap Step 18, but both must finish before Step 20.
- **Exact precondition:** Step 16 Packet-9 closure and Step 17 freeze identities exist; all prospective WP-I time is booked; this step does not invent an owner YES.
- **Governing document/section:** Packet 11 P11-01 through P11-10; catalogue Ordering A/B pre-WP-A wave. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:73-92`; `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:100-101,122-123`)
- **Evidence:** Final authority-source manifest; grant/exclusion/roster/budget sources; P11-07 calculation; P11-09 go/no-go matrix; P11-10 Commit-1/capture/Commit-2/WP-I/freeze order proof; every final source identity in both forms.
- **Stop:** Any missing authority source, obsolete estimate, unbooked work, sequence breach, broadened grant, or inferred YES stops Packet-11 closure.
- **Estimate:** `NO SOURCED ESTIMATE`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:57-57`)

### 20. `OWNER DECISION` — ratify the refreshed freeze-time ledger

- **What:** Present Step 19's actual freeze-time calculation to Barış and obtain the exact P11-08 ratification.
- **Exact precondition:** P11-07 final calculation exists and includes every remaining WP-I booking. D3 ratified approximately 63.75 hours only as of 2026-08-15 and requires re-presentation if the real freeze checkpoint differs.
- **Governing document/section:** Owner decisions D3; Packet 11 P11-07/P11-08. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:62-78`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:85-92`)
- **Evidence:** Owner-authored ratification naming the refreshed used/remaining balance, timestamp/source, and explicit acceptance of P11-07; dual-form identity of the final record.
- **Stop:** No fresh signature, stale 63.75 carry-forward, or any mismatch between the ratified sentence and P11-07 means P11-08 remains open.
- **Estimate:** `OWNER`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:58-58`)

### 21. `LOCAL` — finalize the one authoritative Packet-10 dispatch bundle

- **What:** Bind the Step-18 baseline and final Step-19/20 Packet-11 identity into one Packet-10 manifest delivered identically to both auditors.
- **Exact precondition:** Packets 9 and 11 are complete; P10-01 through P10-14 are resolved; no placeholder or blocker remains.
- **Governing document/section:** Packet 10 P10-13 through P10-15 and combined-order steps 12-15. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65-67,119-122`)
- **Evidence:** Bundle root, full frozen SHA, exact manifest of every input path/role/worktree bytes+SHA/Git-object bytes+SHA/blob OID, common scope/rules, and proof that both intended dispatches reference byte-identical bundle/manifest identities.
- **Stop:** Different auditor bundles, any placeholder, missing Packet-11 ratification, incomplete mandated-suite fields, or single-form identity means no dispatch.
- **Estimate:** `NO SOURCED ESTIMATE`. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:59-59`)

### 22. `LOCAL` — dispatch Audit 2 and stop this runbook

- **What:** Dispatch the same frozen bundle to exactly two fresh independent sessions: `claude-opus-5` xhigh and `gpt-5.6-sol` xhigh. This step ends at dispatch evidence.
- **Exact precondition:** Step 21 passes; every freeze prerequisite and honest-start condition is closed; both isolated audit worktrees are at the exact full frozen SHA with empty pre-review status; neither session receives implementer context or the other auditor's output.
- **Governing document/section:** `AUDIT2_AUDITOR_SESSION_INPUTS.md`, §§1, 3-5; Packet combined-order step 15. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:3-22,44-104`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:122-122`)
- **Evidence:** Two fresh-session dispatch records; exact model/effort; common bundle/manifest identity in both forms; resolved audit worktree paths; exact-HEAD equality; empty pre-review status; no-resume/no-cross-talk contract; mandated-suite execution requirement.
- **Stop:** Any missing prerequisite, different bundle, wrong/unavailable exact model or effort, resumed/continued session, non-empty/different-SHA worktree, substitute suite, or inability to execute means **do not dispatch / BLOCK**. After successful dispatch, stop this runbook before verdict interpretation, acceptance, repair, WP-A, or any later action. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:11-22,65-104`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:30-31`)
- **Estimate:** `NO SOURCED ESTIMATE`. The sources define the roster and state, while the only cited audit reserve is shared across later audits/re-audits and is not a disjoint Audit-2 price. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60-60`; `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md:211-215`)

## Final dispatch checklist

Every box must be evidenced; an unchecked or inferred box is STOP. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:3-7`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:119-122`)

- [ ] Governing plan reading is owner-selected; the active chain used here is unchanged under that selection. (`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:85-133`)
- [ ] Option C has its one accepting execution audit and zero required repairs. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:13-28`)
- [ ] Shared exact candidate is integrated, locally accepted, T0 accepted, and freshly A-0..A-9 staging-bound under separate authority. (`MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:209-230,232-255`)
- [ ] Commit 1 predates and exactly binds the authorized grant-#6 capture; Commit 2 consumes it before op 01. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:488-533,550-607`)
- [ ] `COMMIT_1_GATE=PASS` and `AUTHORITY_GATE=PASS` are both preserved in the capture evidence. (`MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:35-52`)
- [ ] Packet 9 has all 17 components, including a defined/executed P9-15 contract, and is immutable. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:19-45`)
- [ ] Pre-WP-A full SHA, exact base diff, file list, and candidate/artifact/manifest/evidence identities are frozen. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:47-61`)
- [ ] P10-10/11/12 contain an authoritative mandated-suite definition, real frozen-SHA execution, and adjudicated anomaly set. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:62-71`)
- [ ] Packet 11 carries the final authority/order proof and a refreshed owner-ratified P11-08 balance. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:73-92`)
- [ ] Every identity table contains both worktree/on-disk and Git-object forms; no bare single-form identity remains. (`C:\tmp\lane_kick\Y5.md:44-45`; `.gitattributes:1-2`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_IDENTITY_TABLE_LEAD_FINDING_2026-08-15.md:48-64`)
- [ ] One authoritative P10-15 manifest is byte-identical for both fresh required flagships; every placeholder is resolved. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:65-67`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:44-63`)
- [ ] The operator stops at dispatch; Audit 2 acceptance and WP-A remain outside this runbook. (`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_PREREQUISITES.md:24-31`; `MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:617-620`)
