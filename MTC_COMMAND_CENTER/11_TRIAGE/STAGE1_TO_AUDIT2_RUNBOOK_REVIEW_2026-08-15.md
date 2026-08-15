NEEDS-REWORK

Audit tier: T2 documentation/evidence review, one round. Review basis: the specified files were absent from the detached worktree, so I reviewed pinned Git objects rather than guessing path contents. Subject runbook blob: `1bfd7ea2f4b377729605446c129ab1a5f066e204`; preregistration-v2 blob: `99d07ba23083c9caa478f0332cc42419b4381d65`; self-confirming-pattern blob: `592764f370958efb292ed54bbf4db1d0069a8acf`; freeze-reconciliation blob: `665ca079e6bd7f950ca1b002a7af99fcb4b4d7b4`. Commit `cd735760d32158d4ef97e3bc4b9524c95f35f77b` contains all four blobs. This is a pinned-object review; no worktree-byte identity is inferred.

## Required findings

### F1 — The host ordering guard is false: Step 8 reaches a mutating host before Commit 1

The document claims a two-token Stage-1 host barrier, but it applies that barrier only to the grant-#6 capture in Step 12. The ordered path reaches Step 8, `AUTHORIZED HOST ACTION — fresh candidate-bound A-0 through A-9`, after Step 7 and before Step 10 creates Commit 1. Step 8 requires only separate host authority; it does not require `COMMIT_1_GATE=PASS` or even the existence of Commit 1. An operator following the runbook in good faith can therefore contact and mutate a host early. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:24-42,120-145`

This is not a harmless staging observation. A-2 installs the candidate, A-4 starts the service, and A-5 performs a SIGKILL/explicit-start sequence. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:239-250`

The owner record says the existing Stage-1/WP-I grant is unspendable until Commit 1 exists and that any earlier host contact is outside that grant. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-52` Step 8 tries to avoid that conflict by requiring a different, currently `UNKNOWN`, authorization, but a second warning/authority check is not the required structural barrier.

Required repair: no numbered host action may be reachable before a mechanically verified Commit-1 object exists. There is also a design cycle to resolve: preregistration v2 requires a fresh candidate/checkpoint source, including live MainPID identities, before Commit 1, while the host barrier forbids obtaining it through a pre-Commit-1 host action. The safe resolution is `UNKNOWN`. What would settle it is an explicit redesign that either derives the pre-Commit-1 candidate binding without host contact or changes the binding/order under a new owner-approved contract; a separate ad hoc Step-8 authorization does not satisfy the stated structural requirement.

### F2 — Step 10 does not reflect preregistration-v2's Commit-1 blockers and can fail only after it starts

Step 10's precondition is merely that Step 9 allocations are complete/collision-free and no attestation-derived value has been inserted. It then attempts to create Commit 1 and discovers missing fields as an in-step stop. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:138-145`

Version 2 says something materially stronger. It carries as Commit blockers the exact root principal/shell/forced-command or wrapper/process chain, pre-environment, initial cwd, descriptor mapping, full outer argv, enforced category-1 mutation denial on success and failure paths, and proof that native logging cannot cross into rotation/out-of-store actions or side-effecting hooks. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:9-19,33-49,139-170`

It also requires three exact committed TSV sources. Step 9 does not specify all fields of `STAGE1_ALLOCATION_RECORD.tsv`; Step 8 does not produce the exact `STAGE1_CANDIDATE_BINDING.tsv`; and no runbook step produces `STAGE1_ROOT_CHANNEL_BINDING.tsv`. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:83-115,139-170`; `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:120-145`

Finally, the v2 readiness gate requires D026 evidence for the exact filled producer/recorder bytes and a fresh accepting T2 review before Commit 1. Neither is a Step-10 precondition or an earlier exact-package step. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:1452-1466`

Required repair: add explicit, checkable pre-Commit-1 production and acceptance steps for all three exact TSV sources, the root-channel/mutation-boundary proofs, exact filled package D026 RED/GREEN, and the final T2 review. Step 10 must be unreachable while any v2 readiness item is `UNKNOWN`; "stop if a field is missing" after entering Step 10 is not a precondition.

### F3 — Both plan readings are represented honestly, but a prerequisite common to both is missing from the executable sequence

The runbook correctly states that plan authority is contested, records the choice as `UNKNOWN`, requires an owner selection, and does not silently label A or B as adopted. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:44-64`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:129-131`

However, both readings require the applicable KVM2 Phase-2 close before the shared release candidate. `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md:85-103,112-124` Runbook Step 4 names that close as a precondition, calls its current state `UNKNOWN`, and supplies no preceding step that can produce or verify it. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:84-91` Thus the document is honest about the contested fork but incomplete under either reading.

Required repair: either make a pinned accepting Phase-2 close an explicit runbook-entry precondition, with the exact evidence and identity that proves it, or include the dependency-ordered steps that produce it. What currently satisfies the close is `UNKNOWN`; an exact accepted close record plus pinned blob/dual-form identity would settle it.

### F4 — The allocation collision and append-only checks repeat the named self-confirming defect

Step 9 asks for collision results and append-only dispositions, but it defines neither an independently derived complete collision universe nor a mechanism that rejects ledger overwrite. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:129-136` These are the two exact recurring defects already recorded: a collision check can pass by not looking, and append-only can be asserted without enforcement. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:16-23`

What would make the current checks fail? A collision inside whatever unspecified set the operator happened to scan, or a missing disposition. A collision outside that set, or an overwrite not detected by a mechanical predecessor/link check, can still pass. The expected value and the observed result are produced by the same allocation process.

Required repair: pin a complete collision universe derived independently of the new allocation, record one terminal disposition per member, and execute a falsification with a collision in every source class. Enforce append-only mechanically with a predecessor identity/hash-chain or equivalent write-once control and demonstrate that an overwrite is RED.

### F5 — Identity discipline is stated, not closed over an independent universe

The dual-form rule itself is clear, but the final proof only asks whether every identity *table* contains both forms. An operator can omit an artifact from all tables and still tick that box. The manifest is also produced by the same bundle-building process whose completeness it is meant to prove. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:13-22,237-243,255-269`

The independent packet scope already supplies a useful required universe: 17 Packet-9 components, 15 Packet-10 components, and 10 Packet-11 components. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:132-138` The runbook never requires a one-to-one reconciliation from that universe to manifest members and dual-form rows. This violates the conservation rule that every admitted member needs exactly one terminal disposition. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:933-967`

The runbook also cites governing sources only as mutable path/line references and repeatedly relies on the ephemeral `C:\tmp\lane_kick\Y5.md` without a byte identity. It does not pin its own blob or the governing-source blobs, despite making identity discipline load-bearing. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:1-22,255-269`

Required repair: define the identity universe independently from the produced tables, reconcile every required packet component and every retained file to exactly one manifest/identity row, reject missing/duplicate/unresolved members, and pin every governing source by blob OID or record both on-disk and Git-object forms. Which source revisions an operator should use is currently `UNKNOWN`; a frozen authority/source manifest would settle it.

### F6 — Several preconditions are checked too late

1. Step 5 can discover a merge conflict, blob-fence mismatch, hook failure, or identity mismatch only after beginning the integration. Its stop clause gives no pre-start conflict proof and no defined incomplete-candidate disposition. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:93-100`
2. Step 15 permits the WP-I host run while saying only that the missing P9-15 producer/command/evidence contract must be defined before *closure*. Step 16 then admits that P9-15 still has no producing contract. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:183-199` The canonical packet scope identifies this as a known gap. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:39-45` A known evidence-contract gap should be closed before the expensive one-use host run, not discovered after retrieval.
3. Step 22 treats exact-model availability and ability to execute as stop conditions, not an all-slots preflight. If one auditor is dispatched and the second process cannot start, the step is already half complete. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:246-252`

Required repair: move every checkable condition before the irreversible or expensive part of its step. Preflight merge applicability in a disposable exact tree; define/validate P9-15 before Step 15; and preflight both exact auditor routes, worktrees, auth/quota, commands, and executable suite access before either dispatch begins.

### F7 — Stop conditions do not always produce a safe, named terminal state

Step 5 says stop on merge/conflict/fence failures but does not say whether to abort, preserve, quarantine, or identify the in-progress merge. Step 8 can stop after an install, service start, or restart-safety action but provides no mandatory rollback/mask/stop/quarantine/evidence-close sequence and no safe host-state predicate. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:93-100,120-127`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:239-250`

Step 16 says an undefined P9-15 or missing record makes Packet 9 incomplete, but it does not require a P9-17 `STOP` closure that inventories the partial run and first divergence. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:192-199` The packet contract supports PASS/FAIL/STOP and a first-divergence record, so leaving no closure record is avoidable. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKETS_9_10_11_SCOPE_2026-08-12.md:40-45`

Step 22 likewise has no terminal classification for a one-of-two partial dispatch. Required repair: every step needs an explicit failure-state artifact and a safe-state action. Host steps need predeclared `always` cleanup/close behavior; partial Packet 9 must still receive an immutable STOP closure; a partial Audit-2 dispatch must be labelled invalid, its output quarantined as supplemental/non-accepting, and no later gate may consume it.

### F8 — The frozen-suite check proves self-consistency, not necessarily the mandated suite or runtime

Step 18 allows "one authoritative source" to define the command, expected counts/signatures, and baseline, then checks execution against those values. It does not establish who independently chooses that source, how the command is proved to be the complete Bridge suite, or how the expected values are prevented from being copied from the same run. It records a generic environment but no exact interpreter, dependency-lock/install, OS/tool, or fixture identities. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_2026-08-15.md:210-217`; `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_AUDITOR_SESSION_INPUTS.md:82-104`

This is the named environment-reproducibility failure: materially different runtimes can satisfy a broad runtime description. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:21-23` As written, the check fails only when the produced run disagrees with the author-supplied expectations. A narrowed command and expectations derived from that same narrowed run can pass while the claimed full-suite property is false.

Required repair: derive the suite node universe and mandated command from an independently pinned test inventory/authority source; freeze exact interpreter and dependency/tool/environment identities; record every collected test ID with a terminal disposition; and show a falsification in which a missing test, altered runtime, or unauthorized anomaly makes the contract RED.

## Completeness cross-check

The seven high-level rows in freeze-reconciliation section 3 are visibly represented: Pathscope decision/disposition in Steps 2-3, allocation in Step 9, Commit 1 in Step 10, capture in Step 12, fills in Step 13, and order proof/Commit 2 in Step 14. `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md:58-70`

That apparent coverage is not sufficient. The newer preregistration-v2 contract subdivides Commit 1 into additional mandatory inputs and acceptance gates which have no producing steps, as F2 describes. The common KVM2 Phase-2 predecessor is also absent, as F3 describes. P9-15 is deferred until after the host run rather than made a pre-host executable contract, as F6 describes. These omissions mean an operator cannot complete the stated sequence from its documented starting state without improvising.

## Bottom line

The plan-authority discussion is candid, the exact-diff requirement is stronger than an unchanged-bits assertion, and the Step-12/Step-14 order checks are directionally sound. Those strengths do not rescue the runbook. A good-faith operator can reach a mutating host step before Commit 1, Step 10 lacks prerequisites that v2 expressly calls Commit blockers, common-plan work is missing, and multiple checks or stop paths can succeed or halt without proving or preserving the claimed state. The document is not safe to operate under time pressure until F1-F8 are repaired.
