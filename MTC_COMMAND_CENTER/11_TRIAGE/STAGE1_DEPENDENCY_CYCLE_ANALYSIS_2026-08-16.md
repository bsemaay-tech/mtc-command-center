# Step 8 / Step 10 dependency-cycle analysis

Status: **ANALYSIS ONLY — NO OPTION SELECTED.** This document creates no acceptance, authorization, host permission, or implementation decision.

Audit classification: **T2 documentation/evidence analysis.** The task contract expressly prohibited delegation and external model processes, so this lane used self-verification only and does not claim a model-audit verdict.

## Evidence basis

The detached worktree at `C:\RO` does not contain the three task-named source paths at its current `HEAD`. They were therefore read as pinned Git objects, without checkout or worktree mutation:

| Source | Commit read | Blob read |
|---|---|---|
| `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md` | `e730dc584755571e506becca013a7d86962f0b01` | `26309967bb141ff45730ee55fb0b293d48a690ef` |
| `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md` | `cd735760d32158d4ef97e3bc4b9524c95f35f77b` | `99d07ba23083c9caa478f0332cc42419b4381d65` |
| `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md` | `a4833939b02a60815cfb321287d089cc6fdf8332` | `592764f370958efb292ed54bbf4db1d0069a8acf` |
| `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_REVIEW_2026-08-15.md` | `8b1eeac56386897499f080d885e8d29af8ea3b45` | `85f04ff271128d353c5a2405c4a34793e5f770d5` |

All `file:line` citations below refer to those pinned bytes for the absent sources and to the detached worktree bytes for sources present there. No equality between an absent source's pinned Git object and any worktree path is inferred.

## 1. The real dependency

### 1.1 What Steps 8–11 actually require

The current transition graph says:

```text
Step 8 fresh A-0..A-9
    -> final-checkpoint label plus live process fields
    -> STAGE1_CANDIDATE_BINDING.tsv
    -> Step 10 creates and verifies Commit 1
    -> COMMIT_1_OBJECT_VERIFIED
    -> Step 8 precondition
```

That is a directed cycle. Step 8 requires `COMMIT_1_OBJECT_VERIFIED`; Step 10 requires all three TSVs and says no host command may have run; each step is explicitly marked unreachable because of the other. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:267-274,284-290`

Step 9 is serialized after Step 8 in the runbook, but its product is a local allocation row. Its fields are identifiers, derived paths, a collision result, and a reservation disposition; none is a Gate-A observation. The source contract defines those fields at `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:89-110`, while the runbook adds Step 8 PASS as a sequencing precondition at `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:276-282`. Therefore Step 9's dependency on Step 8 is procedural, not intrinsic to the allocation data.

Step 11 is downstream of Step 10. It binds the owner's D2 grant to the exact Commit-1 object and performs no host contact. It does not feed Step 8 and is not a member of the cycle. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:292-298`

### 1.2 Exactly which TSV and field create the Step-8 dependency

Commit 1 may consume only three exact committed TSV sources. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:83-87`

| TSV | Relationship to Step 8 |
|---|---|
| `STAGE1_ALLOCATION_RECORD.tsv` | Local allocation data; no field intrinsically requires A-0..A-9. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:89-110` |
| `STAGE1_ROOT_CHANNEL_BINDING.tsv` | Root-channel, launcher, process-chain, mutation-denial, and crossover facts; independently blocked, but not derived from Gate-A A-0..A-9. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:139-170` |
| `STAGE1_CANDIDATE_BINDING.tsv` | The only TSV that names and carries the Gate-A checkpoint. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:112-137` |

The field that directly names Step 8 is:

> `CHECKPOINT_ID` | literal `STAGE1_EXACT_CANDIDATE_A0_A9_FINAL`

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:119-123`

That one field is the explicit **A-0..A-9 dependency**. It is narrower than “Step 10 needs Step 8.” Step 10 needs this one TSV; within it, `CHECKPOINT_ID` says the record is the final A-0..A-9 checkpoint.

There is also a narrower **live-host-observation payload** in that same row: `WPI_MAINPID`, `WPI_MAINPID_STARTTIME_TICKS`, `WPI_MAINPID_EXE_PATH`, `WPI_MAINPID_EXE_SHA256`, and `WPI_MAINPID_NET_NS`; the row also fixes active state, restart count, candidate-specific cwd, and command-line digest. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:121-135` The producer embeds the PID and start time in its exact argv and later requires the live snapshot to equal the committed checkpoint fields. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:214-220,231-242`

So the precise dependency is:

- the direct Step-8 label is **one field of one TSV**: `STAGE1_CANDIDATE_BINDING.tsv.CHECKPOINT_ID`;
- several other fields in that same one-row TSV require a live candidate process and make the checkpoint substantive rather than a label; and
- neither of the other two TSVs is Step-8-derived.

This distinction matters: moving the allocation step cannot by itself break the cycle, while changing the candidate-binding contract can.

## 2. Is the cycle real or an artifact?

### 2.1 Possibility: Step 8's Commit-1 precondition is stronger than necessary

Evidence that this may be a contract artifact:

1. The owner-approved D2 sentence names only the exact committed read-only grant-#6 capture and WP-I operations; all other host actions are outside **that grant**. The explanation says Commit 1 must precede spending D2, not that every separately authorized staging action in the programme must follow Commit 1. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-52`
2. The runbook itself gives Step 8 and grant #6 distinct authority labels and says there is no edge from D2 to H-A. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:164-190`
3. The integration design independently sequences fresh A-0..A-9 after local/T0 acceptance and says it runs only under separate host authority; it does not name Commit 1 as a prerequisite. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:209-230`
4. `GATEA-STAGING` is explicitly disposable and not KVM2. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:54-60` The Gate-A host contract says the rehearsal host must be expendable and expressly forbids using the active KVM2 destination. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:29-44`

Evidence against treating the guard as casually removable:

1. Step 8 is mutating: A-2 installs, A-4 starts the service, and A-5 performs SIGKILL followed by explicit start. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:239-250`
2. The prior review explicitly required that no numbered host action be reachable before a mechanically verified Commit-1 object. It also said that a separate ad hoc Step-8 authority sentence would not satisfy that structural rule. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_RUNBOOK_REVIEW_2026-08-15.md:7-15`
3. V2 adopted that review rule in H-A's incoming edge and cannot self-amend it. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:167-173,267-274`

Finding: the **current rule is real**, but its universal scope is review-derived rather than established by the quoted D2 owner sentence. Whether Barış intended “no host action before Commit 1” to bind the separately authorized disposable Gate-A programme is **UNKNOWN**. An owner-approved replacement ordering could therefore remove an over-broad edge, but an operator cannot infer that replacement from the disposable-host distinction.

### 2.2 Possibility: Step 10 can get its input from another source

Under the current schema, no established alternate source exists:

- Candidate SHA, unit name, expected cwd, and expected command-line bytes can be derived from frozen candidate/package inputs.
- A live PID, its start time, current executable path/digest, network namespace, active state, and restart count cannot be derived from Git or an artifact manifest. They require observation of a live subject. The current row then insists that the subject is the final A-0..A-9 checkpoint. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:119-137`
- Historical Gate-A evidence cannot fill the row for new bytes: the integration contract states that no A-0..A-9 PASS transfers and every relevant host/runtime check must be fresh on the integrated candidate. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:232-255`

There is historical evidence that a **different contract** is possible. The predecessor two-commit design said Commit 1 contained the exact capture procedure plus non-consumable placeholders, that the capture needed no value it was about to observe, and that Commit 2 consumed the observation. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_SUCCESSOR_PREREG_DRAFT_R3_2026-08-11.md:495-528,771-779` That is design evidence, not satisfaction of V2's current TSV.

Safety cost of using that route: if volatile MainPID/starttime/netns values are first learned during the later capture, the capture can prove its process was stable and bound to independently committed candidate expectations, but it no longer proves that the process is the same process that survived the final Gate-A checkpoint. A manual restart between Gate-A and capture would become invisible unless a separate independent binding catches it. The earlier analysis calls `NRestarts` and `MainPID` perishable and says a restart destroys those exact observations. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/ROWS_1_9_OPTIONS_CODEX_2026-08-10.md:580-593`

Finding: “another source satisfies the existing TSV” is **UNKNOWN and presently unsupported**. “Redesign the TSV so stable expectations are precommitted and volatile facts are later observations” is a real option, but it changes the safety claim and must not be presented as merely sourcing the same fields elsewhere.

### 2.3 Possibility: the cycle is genuine

Under the currently pinned V2 documents, the cycle is genuine:

- H-A requires Commit 1. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:167-173`
- Commit 1 requires a committed final-A-0..A-9 checkpoint row and says no host command has run. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:1452-1466`
- V2 records `STAGE1_PREHOST_ORDERING_CYCLE_STOP` and requires an owner-approved replacement contract before revision. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:22-38`

This is a **contract cycle**, not proof that the safety floor itself is impossible. It can be broken only by changing an edge, changing what Commit 1 contains, or adding a separately bound object.

Breaking this cycle also does not make Step 10 reachable by itself. The root-channel TSV still contains fields that the preregistration says are all `UNKNOWN`, and the readiness register carries other independent blockers. `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/WPI_STAGE1_COMMIT1_PREREG_DRAFT_V2_2026-08-15.md:139-170,1468-1478`

## 3. Options — no selection

Exact hour estimates are **UNKNOWN** because no cited source estimates these redesigns. Relative work is stated qualitatively.

### Option A — split Commit 1 into a pre-stage commit and a final preregistration commit

**Change.** Create a mechanically verified pre-stage commit that freezes the candidate identity, capture/recorder design, schemas, and the fact that it grants no D2 capture authority. Run fresh A-0..A-9 afterward under separate Gate-A authority. Use its final checkpoint to populate the candidate TSV, then create a second, final preregistration commit. Step 11 binds D2 only to that final commit.

**Safety property cost.** The broad property “no host action before the final exact Commit 1” is replaced by the narrower property “no D2/grant-#6 capture before the final exact preregistration commit.” A mutating disposable-host run occurs between the two commits.

**Preserves.** The owner's read-only capture is still bound to exact final committed bytes; the Gate-A record is fresh for the candidate; production KVM2 remains outside the route; and no historical PASS transfers.

**Required anti-self-confirmation.** The final commit must fail preflight if it is not a descendant of the pre-stage commit, if the fresh Gate-A record names different candidate/host bytes, if any non-allowlisted field changes, or if grant #6 is bound to the first rather than final object. The expected candidate identity must come from the frozen candidate/T0 package, not from the TSV producer.

**Relative work.** **High.** Commit semantics, Step 8–11 ordering, Packet-9/P9-02 identity, read-back checks, recorder inputs, D026 evidence, and host-touching audit contracts all change.

### Option B — remove the Commit-1 predicate only from disposable Gate-A H-A

**Change.** Delete `COMMIT_1_OBJECT_VERIFIED` only from H-A's incoming edge. Retain `RUNBOOK_ACCEPTED_AND_PINNED`, exact candidate T0 acceptance, cycle-resolution record, a separate exact Gate-A authority, exact `GATEA-STAGING` identity, and the accepted safe-close contract. Step 8 then produces the candidate TSV; Step 10 creates Commit 1; Step 11 binds D2; grant #6 remains later.

**Safety property cost.** This explicitly abandons the review's universal no-numbered-host-action-before-Commit-1 rule. It relies on the distinction between a separately authorized, disposable staging mutation and the owner's exact committed read-only capture.

**Preserves.** The final read-only capture remains impossible before Commit 1; Gate-A remains staging-only; new candidate bytes receive fresh A-0..A-9; KVM2 is excluded; and D2 is never reused as Gate-A authority.

**Required anti-self-confirmation.** A wrong host, wrong candidate, absent/over-broad authority, missing close contract, or non-accepting T0 identity must STOP before socket open. A prose statement is insufficient: V2 itself admits that its current edges are not a mechanical host interlock. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:190-192` The revised package must show the real dispatch guard going RED for each mismatch.

**Relative work.** **Medium in design, high in assurance.** The graph change is small, but it changes a host-touching safety edge and therefore requires a revised accepted contract plus proportionate T0 host/run-kit scrutiny.

### Option C — keep no pre-Commit-1 host contact and derive only stable candidate expectations

**Change.** Redefine `STAGE1_CANDIDATE_BINDING.tsv` as a pre-Commit-1 expectations record derived from the frozen candidate/T0 package: candidate SHA, unit name, expected candidate-specific cwd, command-line bytes/digest, and executable artifact identity. Remove volatile PID/starttime/netns/active/restart observations from that pre-Commit-1 row. The later Commit-1-bound capture obtains a fresh manager MainPID, opens a pidfd, proves before/after stability, compares all stable candidate expectations, and commits volatile observations only in Commit 2.

**Safety property cost.** Gate-A-to-capture process continuity is narrowed. Without a separately committed final Gate-A process token, this route cannot detect a same-candidate manual restart between Gate-A and capture. It proves “the capture observed a stable process bound to these candidate bytes,” not “the exact process that passed A-0..A-9 remained continuous.”

**Preserves.** No host contact before Commit 1; the capture procedure is exact committed code before observation; stable expected values come from an independent frozen candidate source; the observed values are not retroactively called preregistered; and production KVM2 remains separate.

**Required anti-self-confirmation.** The process that supplies the PID cannot also supply the stable expected candidate values. Wrong candidate cwd/cmdline/executable must be RED; process exit/reuse/drift must STOP; a deliberate same-candidate restart between Gate-A and capture must demonstrate the exact limitation rather than falsely PASS a continuity claim. This follows the rule that an expectation produced by the same process as the artifact is not a check. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`

**Relative work.** **High.** It changes the TSV schema, producer semantics, exact argv, readiness gate, result claim, Commit-2 consumer, and the D026 matrix.

### Option D — Commit 1 first, Stage 8 second, then add a distinct binding commit

**Change.** Create an immutable procedure-only Commit 1 before staging. Its code is designed to consume a later, separately committed candidate-binding object but cannot edit its own procedure bytes. Run fresh A-0..A-9 after Commit 1. Commit the exact final checkpoint as a distinct descendant binding object. Step 11 then binds D2 to the exact pair, or to the descendant whose manifest proves both object identities, before grant #6.

**Safety property cost.** The single-object Commit-1 identity becomes a two-object authority subject. Every consumer must understand which properties belong to the procedure object and which belong to the later binding object; a missed consumer can silently bind only half the subject.

**Preserves.** A mechanically verified procedure commit exists before any staging action; the procedure bytes do not change after staging; the live checkpoint remains a committed independent input before grant #6; fresh A-0..A-9 remains mandatory; and KVM2 stays outside the route.

**Required anti-self-confirmation.** The binding commit must fail if its parent is not exact Commit 1, if it changes any procedure/package blob, if its Gate-A record names another candidate/host, or if the recorder checks only one of the two objects. The declared, bound, and executed object universe must reconcile one-to-one; otherwise this repeats the “declared instrument is not the executed instrument” defect. `MTC_COMMAND_CENTER/11_TRIAGE/DESIGN_DEFECT_PATTERNS_2026-08-10.md:860-895,933-967`

**Relative work.** **Very high.** This adds a new identity type, ancestry/allowed-delta proof, two-object manifest and recorder logic, authority wording, packet mappings, D026 mutations, and downstream consumer conservation checks.

## 4. Safety floor for every option

No option is eligible unless all of the following remain true:

1. **Owner capture bound to exact committed bytes.** Before any grant-#6 socket opens, the recorder must derive the governing object identity or exact object pair from a clean current state, read the objects back, prove byte equality and manifest completeness, and write that identity first in the immutable record. Any procedure/input change requires a new binding and a new capture; Step 11 cannot infer rebinding. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:284-298`
2. **No Gate-A PASS transfer.** Every new integrated candidate must run fresh A-0..A-9 and produce a new candidate/artifact/manifest-bound final record; historical evidence is supplemental only. `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:232-255`
3. **Disposable staging is not production.** Every host edge must name `GATEA-STAGING` as the expendable rehearsal host and explicitly exclude the production KVM2 destination. The staging verdict grants staging acceptance only. `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_PREREGISTRATION_AND_STAGING_RUNBOOK_2026-08-01.md:29-44`; `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md:252-255`
4. **Authorities remain separate.** Gate-A H-A needs its own exact authority and safe-close contract. D2 may bind only the committed read-only grant-#6 capture and later WP-I operations; it cannot be reused to authorize install, service start, SIGKILL, or restart. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:164-190`; `MTC_COMMAND_CENTER/11_TRIAGE/WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:30-58`
5. **Checks must be falsifiable and enforced.** For each revised guard, the package must name the independent expected-value source, the complete subject universe, the mechanism that rejects mismatch, and a real RED case. A property that is merely asserted or whose expectation comes from the checked producer does not count. `MTC_COMMAND_CENTER/11_TRIAGE/SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:45-63`
6. **`UNKNOWN` remains STOP.** No missing source, unobservable live fact, unavailable identity, or partial object pair may be converted into FAIL or PASS. The transition model already requires inability to evaluate to terminate. `MTC_COMMAND_CENTER/11_TRIAGE/STAGE1_TO_AUDIT2_EXECUTION_RUNBOOK_V2_2026-08-15.md:152-162`

## 5. Exact one-line owner decision sentences

These sentences select a design route only. Each deliberately says it does **not** authorize host contact.

**Option A**

> I select Option A: replace the current single Commit-1 contract with a reviewed two-commit chain consisting of a mechanically verified pre-stage procedure commit and a final exact preregistration commit whose candidate binding comes only from the fresh candidate-bound A-0..A-9 record and whose other required inputs remain independently verified; bind grant #6 only to the final commit, and treat this as design-and-review authority only, not host-contact authority.

**Option B**

> I select Option B: revise the accepted ordering contract so `COMMIT_1_OBJECT_VERIFIED` is removed only from the separately authorized disposable-`GATEA-STAGING` A-0..A-9 edge while exact candidate T0 acceptance, separate Gate-A authority, the safe-close contract, and every Commit-1-before-grant-#6 rule remain mandatory; this selects a design and authorizes no host contact.

**Option C**

> I select Option C: keep the no-pre-Commit-1-host rule and redesign Commit 1 so only independently derived stable candidate expectations are committed, while volatile MainPID, start-time, executable, and network-namespace values are first observed by the later Commit-1-bound capture and consumed only in Commit 2; this selects a design and authorizes no host contact.

**Option D**

> I select Option D: create and verify an immutable procedure-only Commit 1 before staging, run fresh A-0..A-9 afterward under separate authority, commit a distinct candidate-binding descendant that cannot alter the procedure bytes, and bind grant #6 to the exact Commit-1-plus-binding pair; this selects a design and authorizes no host contact.

No option is selected by this analysis.
