NEEDS-REWORK

# Runbook V2 guard review

Audit tier: T2 documentation/evidence review, one round. The specified files are absent from the detached worktree. I reviewed the pinned objects in commit `e730dc584755571e506becca013a7d86962f0b01`; the V2 runbook blob is `26309967bb141ff45730ee55fb0b293d48a690ef`. Worktree-byte identity is `UNKNOWN`, and nothing here accepts or authorizes the runbook.

## Bottom line

V2's current ordered body does block all three named host nodes. The Step 8/Step 10 cycle is real under the cited preregistration, and `GATE_A_STAGE_AUTHORITY` is not conflated with `GRANT6_CAPTURE_AUTHORITY` in the body. Those improvements are not enough for `SOUND`:

1. the apparently exhaustive final checklist omits the Step-15 `WPI_OPS_AUTHORITY` and safe-close gates, while no numbered pre-host step binds that authority to Commit 2;
2. the state machine is a documentary convention, not an enforced interlock, which V2 itself concedes;
3. two mandatory Commit-1 TSVs and several executable check contracts have no producing step—the runbook merely requires them to exist; and
4. post-mutation failure and host-quarantine transitions are not consistently represented by the named terminal states.

These are required repairs because the task requires every route, including summaries and name-based references, to preserve the guard.

## 1. Every host path walked

| Host node | All compliant routes found | Predicate walk | Result |
|---|---|---|---|
| Step 8 / H-A, fresh A-0..A-9 | Sequentially, Step 7 to Step 8. The final checklist also refers to H-A by name. No other host edge was found. | The body requires accepted/pinned V2, accepted candidate T0, resolved ordering cycle, verified Commit 1, separately bound `GATE_A_STAGE_AUTHORITY`, and an accepted Gate-A safe-close contract. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:164-174,267-274` | Currently blocked. The predicates are stated before socket-opening work and several are `UNKNOWN`. D2 has no edge to H-A. |
| Step 12 / H-6, grant-#6 capture | Sequentially, Step 10 PASS to Step 11 authority binding to Step 12. The final checklist refers to H-6 separately. | Verified Commit 1, D2 bound by C5 to the exact bytes, verified root channel/mutation boundary, and accepted create-once close contract. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:175-181,292-306` | Currently blocked. This is the strongest host guard: Step 11 is an explicit no-host binding step and Step 13 requires a closed PASS. |
| Step 15 / H-WPI, WP-I ops 01–12 | Sequentially, Step 14 to Step 15. No other host edge was found. | Verified Commit 2, `WPI_OPS_AUTHORITY_BOUND`, accepted/preflighted P9-15, and accepted WP-I always-close contract. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:182-188,315-328` | The body blocks entry, but the guard leaks outside the body: there is no Step-11 equivalent that actually applies C5 to bind the WP-I clause to Commit 2, and the final checklist omits both `WPI_OPS_AUTHORITY_BOUND` and `WP_I_ALWAYS_CLOSE_CONTRACT_ACCEPTED`. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:403-420` |

The local/model steps are not hidden host routes. Step 7 expressly requires the five observation facts without host contact or a revised owner-approved contract; if the resolution changes ordering or permits pre-Commit-1 contact, V2 requires revision, review, acceptance, and pinning before continuation. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:258-265`

### Required repair R1 — close the Step-15 authority leak

Add an explicit local, no-host authority-binding/preflight transition after Commit 2 and before H-WPI. It must apply C5/C11 to the exact Commit-2 runkit, produce `WPI_OPS_AUTHORITY_BOUND=PASS` and `WP_I_ALWAYS_CLOSE_CONTRACT_ACCEPTED=PASS`, and be required in the final checklist. As written, the body uses a predicate that no numbered step produces, and the short checklist can appear exhaustive while omitting it. This is the same defect class as an authority omitted from a short dispatch gate. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:703-711`

## 2. Authority separation

The two requested authorities remain distinct in the closure table, authority section, structural edges, ordered-path proof, and final checklist:

- Gate-A is `GATE_A_STAGE_AUTHORITY=UNKNOWN`; D2 does not cover it. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:83-105,267-274`
- Grant #6 is `GRANT6_CAPTURE_AUTHORITY`, quoted from D2 and spendable only after exact Commit-1 binding. It cannot set Gate-A authority. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:94-105,292-306`
- V2 expressly removes generic `AUTHORITY_GATE`. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:164-190`

No direct Gate-A/grant-#6 conflation was found. The remaining authority defect is the third host authority: `WPI_OPS_AUTHORITY` is correctly named in the body but disappears from the final checklist, as R1 describes. The H-A checklist row also lists C5/C11 before the separate C8 Commit-1 row; because this is an evidence checklist rather than an execution sequence, that ordering does not itself open H-A, but it should state the H-A Commit-1 dependency explicitly to prevent a name-based reading from recreating V1's order.

## 3. The declared cycles

### Step 8 / Step 10 cycle: real

Commit 1 requires `STAGE1_CANDIDATE_BINDING.tsv` with a live service state, `MainPID`, start-time ticks, cwd, command-line digest, executable identity, and network namespace from the named A-0..A-9-final checkpoint. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:112-137` The same readiness gate requires that no socket or host command have run before Commit 1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:1452-1466` V2 then requires verified Commit 1 before H-A. Therefore:

```text
H-A PASS -> live candidate-binding facts -> Commit 1
Commit 1 -> H-A eligibility
```

This is not invented by V2's prose; it follows from the cited preregistration plus the V1 review's required no-pre-Commit-1 host rule. V2 correctly declares Steps 8 and 10 unreachable. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:267-290`

### Root-channel cycle: also real

Three facts first need an owner/admin design choice; five are properties of the selected runtime channel. The source states that none is established and that the five require authoritative configuration evidence or later authorized observation. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:172-191` Yet all must be concrete before Commit 1, while the readiness gate bans pre-Commit-1 host commands. The safe resolution is `UNKNOWN`.

### No route around either cycle

Step 9 explicitly requires Step 8 PASS under a revised accepted topology; Step 10 requires the exact three TSVs and all blockers concrete; Step 11 requires Step 10 PASS; Steps 12–15 then retain their own joins. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:276-303` Section 7 declares terminal STOP/FAIL nodes and forbids bypassing joins. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:152-162` No compliant bypass was found.

The cycle is nevertheless a design blocker, not a safety accomplishment. A permanently unreachable host node cannot falsely run, but it also does not prove the eventual repaired ordering safe. Any resolution that changes Step 8/9/10 must be reviewed as new bytes, exactly as V2 says. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:258-265`

## 4. Predicates: checkable versus asserted

C5 and C11 describe independent expectations and concrete RED cases, and the host edges name their required PASS records. That is stronger than V1. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:131-150,164-188`

But V2 supplies no executable dispatcher/interlock and explicitly limits its proof to an operator who follows the transitions. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:190-192` Thus the structural guard is procedurally asserted, not mechanically enforced. Current safety comes from `UNKNOWN` predicates making the document inoperable. That is a valid STOP state, but the closure table overstates it as a repaired guard.

### Required repair R2 — make the scope of the claim truthful

Either provide an accepted executable pre-host verifier/dispatcher that consumes the independently sourced records and refuses socket opening unless every node-specific predicate passes, with real RED/GREEN evidence, or narrow every closure claim to “documentary transition contract for a compliant operator.” Do not call the prose state machine a mechanical host interlock; V2 itself says none exists.

## 5. Failure paths and terminality

`HOST_STATE_UNKNOWN_QUARANTINE` is reachable through C11 and explicitly from failed H-A or H-6 close/safe-state proof. It is declared terminal, H-A says “No later step,” and Step 13 requires Step 12 closed PASS. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:147-148,162,267-273,300-310` Thus no ordinary continuation from H-A/H-6 quarantine was found.

Two gaps remain:

1. H-WPI failure says proceed to Step 16 STOP closure, while the universal rule calls `HOST_STATE_UNKNOWN_QUARANTINE` terminal. Step 16 accepts Step-15 PASS, FAIL, or STOP. The document needs an explicit closure-only edge: quarantine may produce P9-17 STOP but can never take Step 16's PASS branch or reach Step 17. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:194-207,322-343`
2. Step 10 creates Commit 1 and only then reads it back. Any read-back/object/identity failure is labelled `COMMIT1_NOT_STARTED_STOP`, although the mutation may already have occurred. “No half-commit is represented” is an assertion, not a defined post-creation state. Step 14 has the analogous create-then-read-back shape. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:284-289,315-320`

### Required repair R3 — define post-mutation states

Separate pre-create failure from post-create verification failure. Name and preserve/quarantine the actual object/current-reference state without destructive recovery. Also make the Step-15-quarantine-to-P9-17 edge an explicit closure-only exception whose only terminal result is Packet-9 STOP.

## 6. V1 finding status after V2

| V1 finding | Status after this walk |
|---|---|
| F1 false host ordering | **Partly repaired.** No compliant V2 body walk reaches H-A before Commit 1, and the two authorities are separate. Still open as an enforcement/summary discipline issue under R1–R2. |
| F2 Commit-1 blockers discovered inside commit step | **OPEN.** Step 9 produces only the allocation TSV. Step 7 does not produce `STAGE1_ROOT_CHANNEL_BINDING.tsv`, and Step 8 does not require production/review of exact `STAGE1_CANDIDATE_BINDING.tsv`; Step 10 simply assumes all three exist. Compare `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:258-290` with `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:83-170`. Post-create failure is also mislabelled. |
| F3 missing common KVM2 predecessor | **Structurally repaired, factually unresolved.** Step 3 is explicit and STOPs because the satisfying record is `UNKNOWN`. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:227-233` |
| F4 self-confirming collision/append-only checks | **OPEN operationally.** C6/C7 now have sounder specifications and RED cases, but their accepted executable implementations, completeness authority, and evidence are `UNKNOWN`; Step 9 assumes those contracts already exist rather than producing them. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:8,142-143,276-282` |
| F5 identity universe | **Partly repaired.** Independent packet/tree universes and conservation are now stated, but the accepted governing-source universe and revisions remain `UNKNOWN`; Step 1 cannot currently pass. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:40-66,211-217` |
| F6 late preconditions | **Partly repaired.** Integration, P9-15, and two-auditor preflights moved earlier, but Step-15 authority/close binding is omitted from the final checklist and has no explicit producing transition. |
| F7 undefined half-states | **OPEN.** Host quarantine is mostly terminal, but H-WPI closure needs an explicit terminal-only edge and Commit-1/2 post-creation verification failures lack truthful named states. |
| F8 self-consistent suite | **Open as a prerequisite, safe as a STOP.** C10 now requires independent inventory/runtime/anomaly inputs and mutation arms, but exact command/runtime/baseline remain `UNKNOWN`, so Steps 18–19 are not executable. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:146,345-358` |

V2 is safer than V1 because its unresolved inputs stop the path rather than silently authorizing host work. It is still not a sound execution runbook: the current guard is documentary, a host-authority gate disappears from the final checklist, mandatory inputs appear without producing transitions, and some failure states do not truthfully describe mutations that may already have happened.
