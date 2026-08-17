# Dispatch prompt — worktree inventory package T2 review

## Status and authorization boundary

This is a dispatch-only review prompt. It may be used only after the Lead
separately authorizes the review. Creating or reading this prompt does not launch
a reviewer, accept the reports, authorize cleanup, or authorize any worktree or
branch mutation.

## Audit classification and reviewer route

**T2 — documentation/evidence review, one reviewer, one round, medium effort.**

Use one fresh independent reviewer session. Follow the current `AGENTS.md` T2
route: GLM-5.2 preferred, DeepSeek acceptable, or a flagship at medium effort
only if neither is available. Record the exact model, provider, effort, and
fresh-session evidence. Do not silently substitute a route after dispatch. A
reviewer unable to execute the required read-only reconciliation must return
`BLOCK`, not an accepting opinion.

The review is limited to factual consistency, coverage, terminology, and
non-authorization boundaries in the named documentation package. It grants no
worktree-retirement, preservation, or Git authority.

## Repository and reports in scope

Repository:

```text
C:\LAB\Tradingview_LAB_CLEAN
```

Read these eight reports completely:

```text
MTC_COMMAND_CENTER/11_TRIAGE/REPO_MEMORY_AND_WORKTREE_HYGIENE_INVENTORY_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH1_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH2_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH3_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH4_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH5_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_RETIREMENT_AUDIT_BATCH6_FINAL_2026-08-17.md
MTC_COMMAND_CENTER/11_TRIAGE/WORKTREE_NONRETIREMENT_CLASSIFICATION_2026-08-17.md
```

Authority files:

```text
AGENTS.md
MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md
MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md
```

Read only the current lock table and the minimum directly relevant lock history;
do not read unrelated large history or logs.

## Required package reconciliation

Do not trust the report summaries or each other's copied totals. Independently
extract every worktree path from the six retirement-batch result tables and the
non-retirement classification tables, normalize Windows path separators/case
for set comparison without rewriting the displayed path, and reproduce or
refute all of the following:

### Full registry partition

```text
155 registered paths
  = 88 detached tracked-clean review-pool paths
  + 47 branch-attached fully clean paths
  + 18 branch-attached dirty paths
  +  1 detached tracked-dirty path
  +  1 main/current checkout
```

Required sub-classification:

- the 18 branch-attached dirty paths are exactly 16 tracked-dirty plus 2 with
  no tracked changes but ordinary untracked content;
- the two ordinary-untracked-only branch-attached paths are `GEMINI` and
  `MTC_AIONUI_PILOT`;
- the sole detached tracked-dirty path is the one reported by the
  non-retirement classification;
- paths missing from the combined classification: 0;
- duplicate classified paths after normalization: 0;
- missing/unavailable registered paths at the dated snapshot: 0.

Reproduce the six-batch partition independently:

| Batch | Paths | Conditional RETIRE-CANDIDATE | HOLD |
|---|---:|---:|---:|
| 1 | 10 | 0 | 10 |
| 2 | 10 | 0 | 10 |
| 3 | 20 | 18 | 2 |
| 4 | 20 | 19 | 1 |
| 5 | 20 | 10 | 10 |
| 6 | 8 | 4 | 4 |
| **Total** | **88** | **51** | **37** |

Prove that every one of the 88 retirement-pool paths appears exactly once in
Batches 1–6 and that no non-retirement path appears in a retirement batch.

## Mandatory terminology audit: clean versus tracked-clean

This distinction is a required review target, not an optional nit.

Apply these definitions exactly:

- **tracked-clean**: `git status --porcelain --untracked-files=no` has no
  tracked modifications; ordinary untracked and ignored content may still
  exist;
- **fully clean** in the non-retirement report: no tracked modifications and no
  ordinary untracked paths; ignored content may still exist and was not
  exhaustively expanded for all 47 branch-attached fully clean trees;
- ignored files do not make a Git worktree dirty, but may contain operational or
  unique evidence and therefore still matter to retirement safety.

Specifically verify:

1. the 88 detached pool is described as **detached tracked-clean**, never as 88
   universally clean/empty/removal-ready trees;
2. within that pool, 72 had no ordinary untracked paths and 16 had ordinary
   untracked content;
3. `RETIRE-CANDIDATE` means only conditional review-queue status with unresolved
   handle/current-directory proof, not `READY`, `safe to remove`, or authorized;
4. the 47 branch-attached fully clean category receives no retirement verdict;
5. statements such as “137 have no tracked changes” are not paraphrased as “137
   clean worktrees” without the tracked-only qualifier;
6. the 2 ordinary-untracked-only branch-attached paths remain in the 18-path
   dirty operational category even though they are tracked-clean.

Any report language that materially collapses these terms, inflates removal
readiness, or makes the category arithmetic ambiguous is a required finding.

## Required independent evidence sampling

Use targeted read-only checks and sample enough distinct cases to reproduce the
reports' methods and catch copied or fabricated conclusions. Do not attempt to
rerun every expensive recursive scan. For every sample, cite the report path and
line plus the read-only evidence/method used.

### A. Unique and duplicate evidence

Sample at least:

- one Batch-2 hard HOLD with ignored mutation/test residue and incomplete
  permission inventory (`GAAUD_CODEX`);
- one Batch-4 unique ordinary-untracked design/evidence HOLD (`PGRK`);
- two different Batch-5 unique evidence HOLD classes, including at least one T0
  audit/economic-deployment-related record;
- one Batch-5 proven duplicate/newline-only-equivalent residue classified
  conditional rather than unique;
- one Batch-6 unique evidence HOLD (`PLANREC`, `WBS`, or `PSCAUD`).

For small text evidence, metadata, exact path, size, and SHA-256 comparison are
allowed. Do not read secret-like files, databases, WAL/SHM files, or large log
contents. A filename or hash is not proof of semantic duplication unless the
reports' stated comparison method is independently reproduced.

### B. Process and operational-use evidence

Sample the reported process/operational HOLD for `P2RT` and the active-use
classification for `MTC_AIONUI_PILOT`. Use only current process metadata and
safe file metadata/path classes. Do not open databases, WAL/SHM sidecars, lock
contents, logs, credentials, or application data. Distinguish dated report
evidence from current live state; a process may have changed since the snapshot.

### C. Permission/incomplete-inventory evidence

Sample at least two reported permission-limited inventories from different
reports, such as `GAAUD_CODEX`, `WPSAUD5`, `TSP1003A5`, or `TSP1004A2`. Do not
take ownership, change ACLs/permissions, elevate, or force access. Confirm that
visible counts are treated as lower bounds and that permission uncertainty
causes HOLD or non-retirement caution rather than a clean conclusion.

### D. Lock relevance

Sample:

- one report path with a direct current lock/active-workstream relationship;
- the Batch-6 `RO` lock-name ambiguity;
- one path with no exact lock hit.

Verify that absence of a Git worktree `locked` marker or exact
`SESSION_LOCK.md` path hit is not treated as permission to remove. Current lock
state is volatile; record the time of the read-only snapshot and separate it
from the dated classification.

### E. Ref reachability and unique commits

Across at least three batches, independently select representative detached
HEADs covering:

- a multi-ref accepted/integration group;
- a single or fragile remote rescue-ref group;
- a recent two-ref group from Batch 6.

Use read-only Git plumbing to reproduce containing refs and zero commits outside
the relevant durable ref universe. Confirm that reachability is snapshot-bound,
refs can move, a prose SHA is not preservation by itself, and branch deletion is
not part of these reports.

## Live registry cross-check and snapshot semantics

Take a fresh read-only `git worktree list --porcelain` snapshot and compare it
with the dated 155-path universe. Also use read-only status commands narrowly
where needed to validate category semantics.

- If the live registry has drifted since 2026-08-17, report the delta explicitly
  and audit whether the reports clearly label their counts as dated snapshots.
- Do not rewrite a historically correct dated inventory merely because current
  state changed.
- Do not accept a report that presents a dated count as permanently live truth.
- Do not run `git worktree prune`, even with mutation intent hidden behind a
  review command. A plain read-only list is sufficient.

## Mandatory handle/current-directory blocker verification

Reproduce or refute the package-wide conclusion that **none of the 51
conditional RETIRE-CANDIDATE paths is removal-ready because full Windows
open-handle and process-current-directory proof remains absent**.

Check read-only availability/state only:

- whether Sysinternals `handle.exe` is installed/discoverable;
- whether local `openfiles` tracking can currently provide the needed proof;
- whether the available `Win32_Process` fields expose executable/command-line
  paths but not every process current working directory.

Do not install a tool, enable global object tracking, restart Windows, stop a
process, alter a service, change configuration, or infer handle absence from no
command-line path hit. If complete proof remains unavailable, every conditional
candidate remains blocked from removal.

## Non-authorization review

Verify every report, especially its result and conclusion, preserves all of
these boundaries:

- no report authorizes worktree removal or raw directory deletion;
- no report authorizes copying/moving unique evidence as a presumed-stable
  backup;
- no report authorizes permission/ACL/ownership changes;
- no report authorizes ref, branch, process, lock, Git configuration, or shared
  AI-memory changes;
- conditional candidates require a fresh live registry/status/ref/lock/process,
  permissions, evidence-preservation, handle, and CWD proof before a separately
  authorized cleanup window;
- future removal, if ever authorized, uses `git worktree remove <exact-path>`,
  not raw recursive filesystem deletion;
- branch cleanup remains a separate later action.

An apparent-space total is a logical inventory, not guaranteed reclaimed disk
space because Git common storage, allocation, inaccessible files, and shared
blocks may differ.

## Prohibited actions

- Do not remove, copy, move, rename, edit, create, delete, stage, commit, reset,
  checkout, clean, stash, or prune any worktree, report, branch, ref, or file.
- Do not change permissions, ownership, ACLs, Git configuration, process state,
  service state, lock state, openfiles configuration, or tool installation.
- Do not contact a host, VPS, exchange, network service, or credential store.
- Do not read secret values, `.env` contents, keys, wallets, databases,
  WAL/SHM contents, application lock contents, or large log contents.
- Do not run tests, application code, backtests, packaging, deployment, or
  cleanup scripts.
- Do not touch `docs/30` or any AI-memory file.

Allowed actions are limited to targeted report reads, read-only Git/worktree
plumbing, safe filesystem metadata, small safe-text hashes/comparisons, current
process metadata, and narrowly scoped read-only calculations needed for this
review.

## Required output and verdict

Capture `git status --porcelain --untracked-files=all` before and after review.
Existing dirt is allowed; prove that the review added no mutation.

Return exactly one formal verdict:

- `PASS` — all required facts, terminology, coverage, and boundaries reproduced;
- `PASS-WITH-NITS` — accepting; optional nits only, zero required repairs;
- `REQUEST_CHANGES` — at least one required factual, set-reconciliation,
  terminology, evidence, or authorization defect;
- `BLOCK` — required evidence cannot be inspected safely or the reviewer route
  cannot satisfy the T2 contract.

Then provide:

1. exact model/provider/effort, fresh-session evidence, and T2 classification;
2. pre/post repository status comparison;
3. a reconciliation table for all 155 paths and all six retirement batches;
4. explicit uniqueness, missing-path, and duplicate-path results;
5. a dedicated clean-versus-tracked-clean terminology verdict;
6. sampled evidence results for unique/duplicate content, process/operational
   use, permission gaps, locks, refs, and unique commits;
7. handle/CWD proof status and its consequence for all 51 conditional paths;
8. current-live-registry drift versus dated-snapshot distinction;
9. required findings with severity, exact report path/line, reproduced evidence,
   consequence, and exact repair;
10. optional nits separately;
11. explicit UNKNOWN items where the allowed read-only scope cannot prove a
    claim;
12. explicit statement that the verdict is documentation review only and grants
    no cleanup or mutation authority.

Do not return an accepting verdict if the 155-path conservation, 88-path batch
uniqueness, 51/37 disposition totals, clean/tracked-clean semantics,
non-authorization boundary, or handle/CWD blocker is unproved.
