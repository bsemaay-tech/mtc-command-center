# Lane L11 — Reconcile the stale KVM2 Phase 3 status

> **Correction, 2026-08-16 morning:** the ordering caveat "whether the
> cumulative or KVM2-own-programme reading governs" is settled — owner decision
> §3 (`OWNER_DECISIONS_2026-08-16_MORNING.md`) ratified the cumulative reading.

- Status: **EVIDENCE RECORD FOR THE LEAD AND OWNER — DECIDES NOTHING, AUTHORIZES NOTHING, CLOSES NO GATE.**
- Date: 2026-08-15 (night). Lane input: `C:\tmp\lane_kick\L11.md`.
- Checkout under examination: `C:\RO`, detached at `25564449`, clean worktree (lane
  input; session git snapshot lists `25564449` "docs: dashboard after the owner's
  five decisions" as the newest commit). `C:\RO` is a linked worktree of
  `C:\LAB\Tradingview_LAB_CLEAN` (`C:\RO\.git` → `gitdir:
  C:/LAB/Tradingview_LAB_CLEAN/.git/worktrees/RO`).
- Nothing was written inside `C:\RO`. No host, network, SSH, deployment, service,
  credential, broker/exchange, ARM, order, TESTNET/mainnet, Pine, parity, MTC,
  trading, merge-to-master, push, or economic action was taken or requested.
  Handoff files inside the repo were **not** updated: this lane's contract permits
  exactly one output file, this one.

## 0. Method, and one honest limitation

This lane's sandbox denied every Git invocation ("requires approval"), including
the read-only `rev-parse`/`ls-tree`/`log`/`branch` calls the lane endorses, and
denied reads of the main repo's `.git` metadata under `C:\LAB` (outside the
granted directories). Per the standing rule — never present a guessed number as
derived — the settlement below uses only:

1. **Direct reads tonight** of the three files in the clean detached worktree at
   `25564449` (worktree bytes = HEAD bytes for a clean checkout).
2. **Recorded command transcripts and verification records already committed in
   the repository**, cited `file:line`, including two object-level checks dated
   2026-07-26 and 2026-08-15.

What could not be re-executed tonight is marked `UNKNOWN` with the exact command
that would settle it (§2.3, §2.4, §2.5). No blob OID, SHA, or hour figure below
is invented.

## 1. The three contract files, named exactly

As named by both sides of the conflict:

- `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md`
- `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md`
- `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md`

- Master plan's list: `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:552-558`
  (each annotated "currently referenced from the PR #25 candidate and absent
  from this checkout") and the Phase-3 BLOCK paragraph at `:256-261`.
- Deploy list's list: `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:36-41`.
- Execution companion's list (inside P3-02's stop block):
  `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:214-219`.

## 2. Presence in `origin/master` and in current HEAD

### 2.1 Current HEAD (`25564449`) — PRESENT (verified tonight)

All three files exist in the worktree of the clean detached checkout, and were
opened directly tonight:

- `IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md:1` — begins
  `# Runtime Baseline Contract (TS-P0-001)`; owner-approved hash scope D018
  2026-07-20 (`:10-11`).
- `IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md:1-4` — begins
  `# Release Evidence Contract (TS-P0-002)`; "APPROVED — Barış, 2026-07-20
  (D018)".
- `IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md:1-3` — begins
  `# 21 — Honest Monitoring-Window State (TS-P0-003)`; module
  `bridge/engine/window.py`.

A clean worktree is the checkout of HEAD, so presence in the worktree is
presence in HEAD. This substitutes a direct content read for the blocked
`git ls-tree HEAD -- <paths>`; it yields no blob OID (§2.3).

### 2.2 `origin/master` — PRESENT (established by four committed records, two of them object-level)

1. **2026-07-26, object-level, by the builder session:**
   `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/audits/READINESS_STATUS.md:25` —
   "PR #25 contracts in merged master | **CONFIRMED at base
   `423897b76b32f68cdabcae16b39c078fdd1f67cb`**". Same record, `:36-40`, already
   flagged the master plan and companion as carrying a stale "absent" statement
   (the builder was outside its write whitelist).
2. **2026-07-26, provenance record:**
   `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/rebuild/manifests/TRUSTED_INPUTS.md:4-5`
   — "Base source commit: `423897b76b32f68cdabcae16b39c078fdd1f67cb`; Base
   provenance: `origin/master`, **merge of PR #25**".
3. **2026-07-26, the deploy list itself:**
   `BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:31-41` — "Current repository facts
   were verified locally on 2026-07-26 … `origin/master` … exact commit
   `423897b76b32f68cdabcae16b39c078fdd1f67cb` … PR #25 is merged … these three
   canonical contracts are present in merged master … The old 'PR #25 contracts
   absent' Phase-3 blocker is closed."
4. **2026-08-15, object-level, by the plan-authority reconciliation:**
   `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:74`
   — "At frozen SHA `4f367ce1`, all three files also exist in the local
   `refs/remotes/origin/master` object."

The deploy list's claim is therefore correct, and corroborated independently.
One nuance kept honest: P3-02's original stop wording required the files
"present … and independently verified" (`KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:212-213`).
The 2026-07-26 confirmation is builder self-QA (`READINESS_STATUS.md:4-6` —
"Independent audit verdict: NONE / OPEN"); the 2026-08-15 reconciliation is a
Lead-level read-only record, not a formal audit verdict. Presence itself is
object-confirmed twice; no gate ever demanded a formal audit of that presence,
and nothing downstream turns on the distinction.

### 2.3 Blob OIDs — UNKNOWN (not guessable here)

No document read in this lane records the git blob OID of any of the three files
at `origin/master` or at HEAD. (The WPL-P2 prereg records SHA-256 file digests at
the old candidate — e.g.
`MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_STAGING_WPLP2-20260809T125940Z-8dc78f08/02_PREREG/CANDIDATE_RELEASE_SHA256SUMS:73,84-85`
— which are content digests, not blob OIDs, and not at either ref asked for.)
Per the lane rule, this is reported as **UNKNOWN**. Settled by one approved
read-only run:

```text
git -C C:/RO rev-parse HEAD origin/master
git -C C:/RO ls-tree origin/master -- IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md
git -C C:/RO ls-tree HEAD      -- IBKR_PAPER_BRIDGE/docs/RUNTIME_BASELINE_CONTRACT.md IBKR_PAPER_BRIDGE/docs/RELEASE_EVIDENCE_CONTRACT.md IBKR_PAPER_BRIDGE/docs/21_WINDOW_STATE_CONTRACT.md
```

### 2.4 When PR #25 actually landed — merged by 2026-07-26; exact merge commit UNKNOWN here

- PR #25 was opened from `cfb08b819aa9890725344e8315571299718cd554` on branch
  `feature/ts-p0-baseline`, 2026-07-20, OPEN/unmerged at that time
  (`MTC_COMMAND_CENTER/_AI_MEMORY/GLOBAL_HANDOFF.md:2873-2880`, dated section).
- The master plan's own §4 dated facts record the same pre-merge world —
  "`origin/master` … at `008e065e8e0ffa68f46134da6698d58f91ef2dcb` … PR #25 was
  open and unmerged" (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:111-118`).
  That section is explicitly labelled historical ("re-verify before every
  action", `:102-104`); it is not the defect.
- By 2026-07-26 the merge is confirmed in `origin/master` at base `423897b7…`
  (§2.2 items 1–3). The exact merge commit and its date: **UNKNOWN** from the
  documents read. Settled by:
  `git -C C:/RO log --diff-filter=A --format='%h %ad %s' --date=iso origin/master -- <the three paths>`.
- Reconstruction, offered as sequence only (both document dates are 2026-07-26;
  `PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:65-67` dates the master/companion
  bytes to `01269f56` and the deploy-list bytes to `6fe0130f`, both 2026-07-26):
  the master plan's BLOCK text was written against the pre-merge `008e065e`
  view; the deploy list's same-day update saw the post-merge `423897b7`. The
  master plan and companion were simply never refreshed after the merge.

### 2.5 Gate-A candidate `2ce41e34` — NOT in `origin/master` (recorded command output)

Full OID `2ce41e34bceb599d80af24c5c33d835820ec321b`
(`MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_EVIDENCE_CHECKLIST_DRAFT_2026-08-09.md:31`).
Recorded read-only Git output, 2026-08-15
(`MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_PATH_SYNTHESIS_2026-08-15.md:85-91`; the
doc's hour synthesis was withdrawn, but this measured Git transcript is outside
the withdrawn ranges and is the direct evidence):

```text
git merge-base --is-ancestor 2ce41e34 origin/master  -> rc=1  (NOT an ancestor)
git merge-base --is-ancestor 2ce41e34 master         -> rc=1  (NOT an ancestor)
git branch -a --contains 2ce41e34
  codex/gate-a-disarmed-start-mode
  remotes/origin/codex/gate-a-disarmed-start-mode
```

Corroborated at `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:44-49`
(`git merge-base --is-ancestor 2ce41e34 <checkout> → rc=1`, "not an ancestor of
this checkout") and `:82-84` ("there is still no accepted release candidate for
the current product tree … `2ce41e34` is not in its ancestry"). Its A-0..A-9
pass is staging-only and carried **no merge authority**
(`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:37-42`,
`DEPLOY_PATH_SYNTHESIS_2026-08-15.md:97-108`). Tonight's independent re-run was
permission-blocked; settle with
`git -C C:/RO merge-base --is-ancestor 2ce41e34bceb599d80af24c5c33d835820ec321b origin/master`
(expected rc=1) and `git -C C:/RO branch -a --contains 2ce41e34…`.

## 3. Which document is stale, and its corrected text

**Verdict: the master plan
(`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md`) is stale, in four places;
the execution companion
(`KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md`) carries the same stale
claim in two places. The lower-level deploy list is correct on this point.**
The KVM2 program's own 2026-07-26 readiness record already said so
(`KVM2_PROGRAM/audits/READINESS_STATUS.md:36-40`), and the 2026-08-15
reconciliation repeated it (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:74`).

Important: settling this does **not** make Phase 3 ready. It swaps a dead
blocker for the live ones (§5). The stale text claimed a *different* blocking
reason than reality.

### 3.1 Proposed corrected text — master plan

**Location 1 — `:246`, Phase-summary row 3, Purpose cell.** Current:
"Bridge release readiness — **BLOCKED** pending PR #25 merge or equivalent".
Proposed: *"Bridge release readiness — **OPEN** (PR #25 merged; the three
contract files are present in `origin/master`; remaining predecessors: Phase 2
close, P3-01 spec acceptance, and an immutable merged release candidate)."*
The row's Hard-Predecessor cell ("three PR #25 contract files present in
`origin/master`") is a requirement that now **holds** and may stand unchanged.

**Location 2 — `:256-261`, the "Phase 3 BLOCK" paragraph.** Proposed
replacement:

> **Phase 3 status (corrected 2026-08-15):** The three canonical bridge
> contract files are **present** in `origin/master` (merged with PR #25;
> confirmed at merged base `423897b76b32f68cdabcae16b39c078fdd1f67cb` on
> 2026-07-26, and re-confirmed in the `4f367ce1` checkout's local
> `refs/remotes/origin/master` object on 2026-08-15) and in the current HEAD.
> The old "PR #25 contracts absent" blocker is **CLOSED**. Phase 3 remains
> OPEN on its live predecessors instead: Phase 2 close (P2-12, including the
> P2-09 rehearsal verdict), P3-01's remaining owner approval of the fail-closed
> staging-test specification (risk-state policy selected 2026-08-15:
> conservative fresh-database reset,
> `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md` §D5), and an immutable merged
> release candidate — the Gate-A staging-accepted candidate `2ce41e34…` is
> **not** in `origin/master` (`git merge-base --is-ancestor 2ce41e34
> origin/master` → rc=1, recorded 2026-08-15), so its A-0..A-9 pass does not
> transfer to any current candidate.

**Location 3 — `:552-558`, canonical references.** Delete "(currently
referenced from the PR #25 candidate and absent from this checkout)" from each
of the three entries; replace with "(merged to `origin/master` via PR #25;
confirmed at `423897b7`, 2026-07-26)".

**Location 4 — `:560-566`, second "Phase 3 BLOCK" paragraph.** Proposed
replacement:

> **Phase 3 status:** the PR #25 file dependency above is closed (files present
> in `origin/master`; see §7). Phase 3 is gated on Phase 2 close, P3-01
> staging-spec acceptance, and a clean merged immutable release SHA. Candidate
> text on unmerged branches — including the Gate-A candidate `2ce41e34…`, which
> is not in `origin/master` — is not merged authority.

### 3.2 Proposed corrected text — execution companion

**Location 5 — `:199-200`, Phase-3 header.** Current: "Phase 3 is BLOCKED
pending P3-02's PR #25/equivalent files; Phases 0–2 may proceed." Proposed:
*"The PR #25 contract-file dependency is CLOSED (files merged to
`origin/master`; confirmed at `423897b7`, 2026-07-26; re-confirmed 2026-08-15).
Phase 3 remains OPEN pending Phase 2 close, P3-01 staging-spec acceptance, and
an immutable merged candidate. Phases 0–2 may proceed."*

**Location 6 — `:214-219`, P3-02's "Phase 3 BLOCK" sub-block.** Replace the
"three PR #25 contract files absent from `origin/master`" bullet with: *"PR #25
contract files are PRESENT in `origin/master` (confirmed at `423897b7`,
2026-07-26). P3-02 remains gated on P3-01 spec acceptance, Phase-2 close, and a
clean merged immutable SHA; the Gate-A candidate `2ce41e34…` is branch-only
(`codex/gate-a-disarmed-start-mode`) and is not a release identity."* The stop
line at `:212-213` then needs no "absent files" clause; its other stops
(branch-only identity, dirty worktree, moving dependency) all stand.

### 3.3 Write authority

None of §3 was applied: the master plan grants no standing update authority —
"Every later creation/update needs task-specific explicit owner write
authorization" (`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:470`), and
this lane is read-only in the repo. The text above is proposed material for the
Lead/owner. `GLOBAL_HANDOFF.md:2800` ("PR #25 open/unmerged at `cfb08b81`")
needs no correction — it sits in a dated historical section.

## 4. P3-01 → P3-05: does each stated precondition currently hold?

Trace and task text: `KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:197-246`.
Phase 3's Hard Predecessor per the master plan is **Phase 2**
(`KVM2_AI_LAB_AND_BRIDGE_MASTER_PLAN_2026-07-25.md:246`).

| Task | Stated precondition(s) | Holds now? | Evidence |
|---|---|---|---|
| Phase-3 header / Phase 2 close (P2-12) | Phase 2 accepted as preparation only, with the P2-09 verdict disclosed | **NO — not evidenced closed** | The 2026-08-15 catalogue still carries the Phase-2 rows open: R31 designs `NO SOURCED ESTIMATE`, R32 rehearsal `NO SOURCED ESTIMATE`, R33 acceptance `OWNER` (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:70-72`); 2026-07-26 record: "P2-09 Ubuntu rebuild rehearsal: BLOCKED / UNVERIFIED" (`KVM2_PROGRAM/audits/READINESS_STATUS.md:30`). No P2-12 acceptance record was found in this lane's reads. |
| **P3-01** (`:202-207`) | (a) owner selects risk-state policy; (b) written owner approval of the pre-cutover staging-test spec (cases, failure criteria, pass/fail) that P3-03 executes | **PARTIAL** — (a) **DONE**; (b) **OPEN** | (a) Decided 2026-08-15 night: conservative fresh-database reset, "start clean" — `WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:89-96`, recorded at `BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:115-128`. (b) No record of owner acceptance of the fail-closed staging-test spec; the 2026-08-15 refresh still listed item 5 `NEEDS-OWNER` with a *recommended* (WAL) sentence, not an approval (`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:175-193`); D5 itself requires the spec to "preserve or block on" the four evidence classes and leaves the off-host-archive sub-question open (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:100-116`). |
| **P3-02** (`:208-219`) | P3-01 accepted before P3-02; evidence: clean source, exact SHA, locked deps+hashes, tested Ubuntu install, unit hashes, rollback artifact, matrices, zero protected-scope drift. Stops: branch-only identity; dirty worktree; moving dependency; three contract files absent from `origin/master` | **NO — but the file-absence stop is now dead** | Files present: §2.2 (stop clause can no longer trigger). Live stops: the only staging-accepted candidate `2ce41e34` is **branch-only** (§2.5), and "there is still no accepted release candidate for the current product tree" (`BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:82-84`); the current unit lacks `credential_free_disarmed` entirely (`:60-68`). The Gate-A-forward integration that would create the candidate is **not yet owner-authorized** (R03 is an `OWNER` row, `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:42`; the runbook was never executed, `:8-12`). P3-01(b) also still gates P3-02 (`EXECUTION_TASKS:206-207`). |
| **P3-03** (`:220-230`) | Exact P3-02 SHA tested per the P3-01 spec, locally plus one named expendable Ubuntu 24.04 environment from the P2-09 classes; P2-09-class environment available | **NO** | No P3-02 SHA exists (row above). A disposable non-KVM2 staging host does exist and proved the environment class (`GATEA-STAGING`; `WPI_OWNER_DECISIONS_2026-08-15.md:60`, real Ubuntu 24.04 install for the historical candidate at `BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md:123-126`), but that evidence binds to `2ce41e34`'s bytes only and "no PASS transfers" (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:10-12`); a fresh candidate-bound run is its own row, R08 (`:47`). The P2-09 *rebuild-kit* verdict is separately absent (R32 open). |
| **P3-04** (`:231-236`) | Named independent reviewer recorded before verification; confirms P3-02 candidate SHA, artifacts, and P3-03 evidence | **NO** | Depends on P3-02/P3-03 outputs that do not exist. 2026-07-26 record: "Independent review: OPEN" (`KVM2_PROGRAM/audits/READINESS_STATUS.md:33`); no later record found closing it. |
| **P3-05** (`:237-246`) | Fresh Gate 5/Gate 6 on the exact candidate diff/tests, exact `claude-opus-5`/`xhigh`, no fallback/resume, unless a later owner decision amends it; crosswalk items 1, 2, 3, 5 close; P2-09/P3-03 `VERIFIED` carried | **NO** | Nothing to audit yet (no accepted candidate). Mapped in the catalogue to R07 (candidate T0 acceptance, 8–16 h) plus R35 (`OWNER` phase close) — `DEPLOY_WORK_BREAKDOWN_2026-08-15.md:46,74`; the catalogue binds R04–R08 as P3-02/P3-03/P3-04 production exactly once (`:93-96,206`). |

Also relevant, one level up: Phase 1 (KVM2-P1-01..03) remains OPEN/BLOCKED
pending a separately authorized read-only host baseline
(`BRIDGE_VPS_DEPLOY_TASK_LIST_2026-07-25.md:25-27`); tonight's D2 host grant is
approved but **not yet spendable** — Commit 1 and the Stage-1 allocation record
do not exist — and it names `GATEA-STAGING` only, explicitly excluding the
Hostinger KVM2 production server (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:41-60`).

## 5. Corrected Phase 3 status

> **Phase 3 (Bridge release readiness) is OPEN, not blocked on PR #25.** The
> "three contract files absent from `origin/master`" blocker is CLOSED and its
> text in the master plan and companion is stale (present-tense claims last
> true before the 2026-07-26 merge at `423897b7`). What actually blocks P3-02
> onward now: (1) Phase 2 is not closed (P2-12 acceptance, including the P2-09
> rehearsal verdict); (2) P3-01 is half-done — policy decided 2026-08-15
> (fresh reset, D5), staging-test spec approval still missing; (3) there is no
> immutable merged release candidate — the Gate-A candidate `2ce41e34…` passed
> A-0..A-9 on a disposable staging host but is not in `origin/master`
> (recorded `rc=1`), so that pass transfers to nothing; the Gate-A-forward
> integration that would produce a candidate is not yet owner-authorized; and
> (4) the dependent chain P3-03 → P3-04 → P3-05 therefore has nothing to run
> on, verify, or audit. No KVM2 execution authority exists at any point
> (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:158-160` — the narrowest safe
> interim rule).

## 6. What Phase 3 actually still requires — estimate

Row IDs are the 2026-08-15 work catalogue (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md`),
which binds R04–R08 as the P3-02/P3-03/P3-04 production units exactly once
(`:93-96`, `:206`, coverage index `:155`). Hours are quoted from the catalogue's
own sourced rows; no figure below is invented.

| Unit | Catalogue row | Type | Sourced estimate |
|---|---|---|---|
| Owner authorizes the branch-local Gate-A-forward release integration (authority, not merge-to-`master`) | R03 (`:42`) | **OWNER** | — |
| Perform the integration, README/WAL synthesis, 33-path blob fence, record candidate identities | R04 (`:43`) | labour | **3–5 h** |
| Conditional: repair a merge-induced test/fixture issue with D026 evidence (may close at zero) | R05 (`:44`) | labour | **0–3 h** |
| Candidate's local acceptance matrix (fences, suites, reproducibility, credential-free, WAL, D026) | R06 (`:45`) | labour | **5–8 h** |
| Candidate's own T0 acceptance — two fresh xhigh flagships (P3-05's audit substance) | R07 (`:46`) | labour | **8–16 h** |
| Fresh candidate-bound staging A-0..A-9 on the disposable host (P3-03's staging substance) | R08 (`:47`) | labour | **5–9 h** |
| P3-01 remainder: owner accepts the fail-closed pre-cutover staging-test spec (policy already decided, D5) | R34 remainder (`:73`) | **OWNER** | — |
| Close Phase 3 / P3-05 after the above | R35 (`:74`) | **OWNER** | — |
| **Sourced technical subtotal (R04–R08)** | | | **21–41 h** |

Phase-2 predecessor (required before Phase 3 can close, not part of the 21–41 h):

| Unit | Row | Type | Estimate |
|---|---|---|---|
| Phase-2 rebuild-kit designs P2-01..P2-08, P2-10/P2-11 | R31 (`:70`) | labour | **NO SOURCED ESTIMATE** — "estimate each artifact after its write/validation contract is frozen" |
| P2-09 reproducibility rehearsal verdict on a named expendable environment | R32 (`:71`) | labour | **NO SOURCED ESTIMATE** |
| P2-12 owner acceptance of the rebuild kit | R33 (`:72`) | **OWNER** | — |

Discipline notes:

- The 21–41 h is the sum of the catalogue's own five sourced rows (3+0+5+8+5 =
  21 min; 5+3+8+16+9 = 41 max); it is arithmetic over sourced figures, not a new
  estimate.
- **NO SOURCED ESTIMATE** for any P3-03 test delta beyond the A-0..A-9 staging
  matrix: the KVM2 P3-01 spec adds WAL/`integrity_check`/risk-state-invariant,
  loss, foreign-order/position, and corruption-blocking cases
  (`KVM2_AI_LAB_AND_BRIDGE_EXECUTION_TASKS_2026-07-25.md:220-230`), which the
  50-hour staging rows do not price; D5's fresh-reset choice re-scopes that spec
  and it does not exist yet, so it cannot be priced
  (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:105` marks this overlap
  "Compatible", not identical).
- The active plan's shared 6 h audit reserve (Audit 2 + Audit 3/Gate 6 +
  re-audits) is **excluded** — it is not Phase 3 work and no source
  disaggregates it (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:60,179`).
- Ordering caveat that the owner has not settled: whether the cumulative or
  KVM2-own-programme reading governs (`PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md:116-166`).
  Under either reading the rows above are the same Phase-3 units; only their
  position relative to the WP-I/Audit-2/WP-A chain changes
  (`DEPLOY_WORK_BREAKDOWN_2026-08-15.md:85-133`). This lane takes no position.
- Still open from tonight and affecting the chain: D4 leaves the TESTNET wallet
  deferred, which blocks the *first start* (Phase 4), not Phase 3
  (`WPI_OWNER_DECISIONS_2026-08-15_NIGHT.md:82-87`).

## 7. Boundaries observed

Read-only throughout the repo; one output file written (this one). No gate,
acceptance, or authorization is expressed or implied; §3's corrected text is
proposed material only. No other AI CLI or agent was invoked, spawned, or
probed; no repo handoff file was updated because the lane contract forbids
writes inside `C:\RO`.
