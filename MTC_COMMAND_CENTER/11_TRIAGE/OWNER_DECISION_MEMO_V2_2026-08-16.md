# Five owner decisions that unblock the programme

This page asks for decisions only. It creates no acceptance or operational authority.

## 1. Settle the privileged staging channel

Commit 1 needs eight channel facts; all are `UNKNOWN`. Three are choices—exact account, direct login versus an escalation/forced-command route, and the control enforcing read-only—while five describe the selected live channel: account shell, forced command or `NONE`, environment before cleanup, starting directory, and inherited file connections. (`WPI_PREREG_DRAFT_ROUND1/ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:10-12`, `:172-185`)

Option A, an existing direct privileged login, has fewer components but still needs independent account, key, and enforcement records. Option B, an ordinary account plus an exact escalation or forced-command chain, adds mappings to verify but may constrain privilege more narrowly; which route exists and its cost are `UNKNOWN`.

The five properties would normally require observing the running machine, but observation is blocked until Commit 1 exists. The way out is one administrator conversation: choose the three design facts, then obtain the five properties from authoritative configuration records, with nothing run; the records must be independent and read-only must be enforced, not asserted. (`ROOT_CHANNEL_RECORD_GAP_2026-08-15.md:174-185`; `SELF_CONFIRMING_CHECK_PATTERN_2026-08-15.md:47-63`)

**Recommendation:** use whichever already-configured route the administrator can document completely. The strongest reason is that this removes the blocker without guessing and without touching the machine.

**Reply verbatim:** “Convene one host-administrator configuration review: choose the exact privileged account, choose direct login or the exact escalation/forced-command route, choose the independently enforced read-only control, and provide the other five channel facts from authoritative configuration records; this is a documentation decision only and authorizes no machine contact or change.”

## 2. Break the ordering cycle

The current rules say a machine-touching staging step must wait for Commit 1, while Commit 1 needs live process facts produced by that staging step. Rewording cannot manufacture a running process's ID, start time, executable identity, network isolation identity, state, or restart count; those facts genuinely require observing something running. (`STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:24-35`, `:88-100`)

- **Option A — two commits.** High work; preserves a fresh staging record and a final exact preregistration. Exact reply appears below. (`STAGE1_DEPENDENCY_CYCLE_ANALYSIS_2026-08-16.md:118-128`, `:181-183`)
- **Option B — remove one staging prerequisite.** Medium design but high assurance work; smallest graph change, but abandons the universal no-machine-action-before-Commit-1 rule. Exact sentence: “I select Option B: revise the accepted ordering contract so `COMMIT_1_OBJECT_VERIFIED` is removed only from the separately authorized disposable-`GATEA-STAGING` A-0..A-9 edge while exact candidate T0 acceptance, separate Gate-A authority, the safe-close contract, and every Commit-1-before-grant-#6 rule remain mandatory; this selects a design and authorizes no host contact.” (`:130-140`, `:185-187`)
- **Option C — commit only stable expectations first.** High work; keeps the no-contact rule but loses proof that the process surviving staging is later observed. Exact sentence: “I select Option C: keep the no-pre-Commit-1-host rule and redesign Commit 1 so only independently derived stable candidate expectations are committed, while volatile MainPID, start-time, executable, and network-namespace values are first observed by the later Commit-1-bound capture and consumed only in Commit 2; this selects a design and authorizes no host contact.” (`:142-152`, `:189-191`)
- **Option D — bind a procedure object and later evidence object.** Very high work; every consumer must understand a new two-object identity. Exact sentence: “I select Option D: create and verify an immutable procedure-only Commit 1 before staging, run fresh A-0..A-9 afterward under separate authority, commit a distinct candidate-binding descendant that cannot alter the procedure bytes, and bind grant #6 to the exact Commit-1-plus-binding pair; this selects a design and authorizes no host contact.” (`:154-164`, `:193-195`)

**Recommendation:** Option A. Its strongest advantage is that it preserves both the fresh live staging facts and one final exact object governing the later read-only capture, without Option D's two-object identity risk.

**Reply verbatim:** “I select Option A: replace the current single Commit-1 contract with a reviewed two-commit chain consisting of a mechanically verified pre-stage procedure commit and a final exact preregistration commit whose candidate binding comes only from the fresh candidate-bound A-0..A-9 record and whose other required inputs remain independently verified; bind grant #6 only to the final commit, and treat this as design-and-review authority only, not host-contact authority.”

## 3. Decide which plan governs

The later 50-hour plan and the older KVM2 plan describe the same deployment, but no recorded owner sentence says one replaces the other. Option A applies both: it costs more records, sign-offs, and possibly duplicate reviews, but drops no protection; Option B applies KVM2 alone: it is not proven cheaper and loses the 50-hour plan's named review, freeze, and final owner checkpoints. (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:9-11`, `:132-156`)

**Recommendation:** Option A. The strongest reason is that no safety checkpoint from either plan can disappear silently; shared evidence counts only when it expressly satisfies both. (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:158-166`)

**Reply verbatim:** “I ratify the cumulative reading: the 50-hour §23a sequence and KVM2 Phases 0–4 plus all ten Bridge VPS Deploy Task List items are jointly mandatory, and one artifact, test, audit, or owner sentence may close gates in both only when its record explicitly names and satisfies both contracts.”

## 4. Keep or enlarge the audit budget

The single six-hour pool must cover four deep first-pass reviews plus any repeat review; that is 1.5 hours per first pass with nothing left over. Option A keeps the hard cap and costs a possible mandatory stop (`BLOCK`) mid-review; Option B enlarges the pool, but the correct amount is `UNKNOWN`, and choosing one now would be a guess. (`AUDIT2_READINESS_PACKAGE/AUDIT2_AUDIT3_DISPATCH_PLAN_2026-08-15.md:150-162`)

**Recommendation:** keep the cap for now and measure both Audit 2 sessions. The strongest reason is that an exhausted cap fails visibly and can be revisited, while an invented estimate only hides uncertainty.

**Reply verbatim:** “The six-hour pool stays a hard cap and I accept BLOCK if it is exhausted; meter both Audit 2 sessions and bring me the measured actuals before Audit 3/Gate 6 so I can set that reserve on evidence, not a guess.”

## 5. Archive the paper-period record

A clean start intentionally carries no old history, so the retiring PC would otherwise hold the only paper-period copy. Option A makes one verified, encrypted off-machine copy and adds storage/key custody; Option B costs nothing now and does not block pre-cutover work, but the decommission date is `UNKNOWN` and loss of the only copy would be irreversible. (`CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:443-481`)

**Recommendation:** archive it. The strongest reason is the asymmetry: an extra copy can later be deleted, but an only copy cannot be recovered after the old machine fails or goes. (`CUTOVER_TABLETOP_AND_CLEAN_START_PROOF_2026-08-15.md:488-498`)

**Reply verbatim:** “Archive the pre-cutover risk-state bundle and raw cutover captures off-host, encrypted, before the fresh start; the recorded bundle and invariants hashes live in the cutover record.”

## What is not waiting on you

You are not being asked to invent an `UNKNOWN`, inspect a machine, design proof commands, reproduce findings, choose an audit verdict, or close a checkpoint. Those are Lead or auditor duties; silence does not mean they await you. Nor does this memo ask you to authorize contact, execution, configuration changes, deployment, credentials, or economic action.
