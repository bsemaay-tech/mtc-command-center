# Worktree Retirement Audit — Batch 6 Final

**Date:** 2026-08-17

**Mode:** bounded read-only retirement inventory; this report is the only write

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Result:** **8 remaining worktrees exhausted; 4 conditional RETIRE-CANDIDATE; 4 HOLD; remove none**

## 1. Verdict meanings and hard boundary

- **RETIRE-CANDIDATE** means the worktree passed every non-handle check in this snapshot. It is a review-queue classification only, not removal authorization.
- **HOLD** means unique evidence or current-lock ambiguity independently blocks retirement.
- **No Batch-6 worktree may be removed now.** Windows open-handle/current-directory proof remains unavailable for every candidate.

No worktree, branch, ref, file, process, lock, permission, or Git configuration was changed. No file was copied or moved. No worktree was removed. No host was accessed. No commit was created.

## 2. Selection and remainder exhaustion

Batch 6 selected all remaining detached, tracked-clean worktrees not listed in Batches 1–5.

The live selection returned exactly **8**, matching the expected remainder:

1. `C:\PLANREC`
2. `C:\WBS`
3. `C:\PSCAUD`
4. `C:\RO`
5. `C:\AUD62A`
6. `C:\AUD62B`
7. `C:\AUD62C`
8. `C:\AUD62D`

Git has no canonical worktree-creation timestamp, so the remainder was ordered by detached HEAD commit date, then by path. The range begins at `4f367ce1...` dated 2026-08-15 21:31 +03 and ends at `acdf4e37...` dated 2026-08-16 16:33 +03.

Selection required an existing registered path, detached HEAD, empty `git status --porcelain --untracked-files=no` output, and no path match in the earlier five reports.

## 3. Proof checklist

Each remaining worktree was checked for:

1. tracked cleanliness;
2. ordinary untracked files, sizes, hashes, and current-checkout duplication;
3. ignored/generated content and inventory-read errors;
4. operational database, WAL/SHM, log, and evidence residue;
5. Git worktree `locked` and `prunable` markers;
6. exact path/name relevance in current `SESSION_LOCK.md`;
7. explicit candidate-path strings in live process command lines or executable paths;
8. durable containing local branches, remote refs, and tags;
9. commits reachable from the detached HEAD but from no branch, remote, or tag;
10. tracked repository references to the candidate path/name and exact HEAD SHA;
11. recursive apparent file size and permission/scan errors;
12. availability of Windows open-handle and process-current-directory proof.

All findings are a 2026-08-17 snapshot and must be repeated before any later retirement action.

## 4. Batch summary

- Remaining candidates audited: **8 exactly**
- Detached and tracked-clean: **8 of 8**
- Git `locked` markers: **0**
- Git `prunable` markers: **0**
- Ordinary untracked paths: **3 across 3 worktrees**
- Unique untracked evidence: **3 files totaling 87,317 bytes**
- Ignored paths: **124**, all generated Python bytecode
- Accessible ignored size: **11,432,453 bytes** (approximately 10.903 MiB)
- Operational DB/WAL/SHM/log paths: **0 visible**
- Permission or recursive-scan errors: **0**
- Explicit live process-path hits: **0**
- Exact lock ambiguity: **1**, for `C:\RO`
- Unique commits outside branches/remotes/tags: **0**
- Total apparent size: **8,147.342 MiB** (about **7.956 GiB**)
- Conditional four-tree retirement pool: **4,078.492 MiB** (about **3.983 GiB**)
- Four-tree HOLD pool: **4,068.850 MiB** (about **3.973 GiB**)

The apparent-size figures are logical file-length sums, not guaranteed physical disk savings. Git common-dir storage, allocation, and shared filesystem blocks can make actual reclaimed space differ.

## 5. Candidate results

| Worktree | HEAD | Commit date | Size MiB | Untracked | Ignored | Durable refs | Unique commits | Process hit | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---|---|
| `C:\PLANREC` | `4f367ce13c834d3c73ddf757de35f2b7281d9274` | 2026-08-15 21:31 +03 | 1,016.584 | **1 unique** | 0 | 6 | 0 | No | **HOLD — unique authority evidence** |
| `C:\WBS` | `4f367ce13c834d3c73ddf757de35f2b7281d9274` | 2026-08-15 21:31 +03 | 1,016.580 | **1 unique** | 0 | 6 | 0 | No | **HOLD — unique deployment plan** |
| `C:\PSCAUD` | `ec98cbd4d629d7e035f99da70d5e73fb7f610da1` | 2026-08-16 00:55 +03 | 1,017.225 | **1 unique** | 2 cache | 2 | 0 | No | **HOLD — unique flagship audit evidence** |
| `C:\RO` | `c84497c885e16e1111fc3005d7cb9a82a34fb907` | 2026-08-16 07:57 +03 | 1,018.461 | 0 | 0 | 2 | 0 | No | **HOLD — current lock-name ambiguity** |
| `C:\AUD62A` | `62bf661b065dec5b5d9895d83575581fe369252d` | 2026-08-16 11:50 +03 | 1,022.218 | 0 | 61 cache | 2 | 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\AUD62B` | `be68953787c299bdaf30f83f301aa66a8ec0ea1f` | 2026-08-16 13:56 +03 | 1,022.260 | 0 | 61 cache | 2 | 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\AUD62C` | `a7460784c1563c140ee7c75197aeab2b0170da8a` | 2026-08-16 15:05 +03 | 1,017.000 | 0 | 0 | 2 | 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\AUD62D` | `acdf4e379fb60ee319854acae19fd3eaf7db71a2` | 2026-08-16 16:33 +03 | 1,017.013 | 0 | 0 | 2 | 0 | No | RETIRE-CANDIDATE — handles unresolved |

## 6. Unique untracked evidence

The following ordinary untracked files are absent from both the current working tree and current tracked index:

| Worktree | Untracked path | Bytes | SHA-256 |
|---|---|---:|---|
| `PLANREC` | `MTC_COMMAND_CENTER/11_TRIAGE/PLAN_AUTHORITY_RECONCILIATION_2026-08-15.md` | 27,721 | `3C5486E2D8918B3CBFF562DC0294CE70B11D1B27E7D709C3006EA2DE0459B505` |
| `WBS` | `MTC_COMMAND_CENTER/11_TRIAGE/DEPLOY_WORK_BREAKDOWN_2026-08-15.md` | 23,475 | `6F150CD701A15700D2D946FCFDA968282AA99F38E062408EF2C7B8E5901DA213` |
| `PSCAUD` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_OPTION_C_FLAGSHIP_AUDIT_2026-08-16.md` | 36,121 | `B08C4AC78C35FCF64339CE240B9A2839B681A617545BBD26B9C042546921C66A` |

These are authority reconciliation, deployment work-breakdown, and flagship Pathscope audit records. They are evidence, not generated cache. This audit did not copy, move, edit, stage, or commit them.

All three worktrees remain **HOLD** until a separate owner-authorized preservation review decides whether and where to retain the files.

## 7. Ignored and operational residue

- `PSCAUD`: 2 ignored `.pyc` files totaling 416,129 bytes.
- `AUD62A`: 61 ignored `.pyc` files totaling 5,493,098 bytes.
- `AUD62B`: 61 ignored `.pyc` files totaling 5,523,226 bytes.
- The other five worktrees: no ignored paths.

Every ignored path is under a `__pycache__` directory. No accessible ignored path is a database, WAL/SHM sidecar, log, report, virtual environment, temporary mutation corpus, or operational evidence file.

All ignored queries and recursive scans completed without permission errors.

## 8. Current lock relevance

Exact path searches found no `C:\RO` or `C:/RO` entry in current `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md`.

However, the current lock table contains a claimed row named **`RP7-WPI-RO block`**, owned by Codex Lead `019fe77c`, and its history says an uncommitted `RP7-WPI-RO.sh` partial repair is preserved and must not be reset, stashed, overwritten, or exposed to a second writer.

The lock does not explicitly identify `C:\RO`, and this worktree is tracked-clean with no ordinary untracked or ignored files. Nevertheless, its bare basename exactly overlaps the claimed workstream token `RO`, and this read-only audit did not prove that the worktree is unrelated. It therefore fails closed to **HOLD — lock-name ambiguity**.

The other seven candidate names and paths produced no current lock relevance.

## 9. Live process and permission checks

A `Win32_Process` snapshot found zero explicit Batch-6 path strings in process command lines or executable paths.

No selected Git worktree entry carried a `locked` or `prunable` marker. Every recursive filesystem scan and ignored-file query completed without permission errors.

These checks are weaker than open-handle/current-directory proof and must be repeated before any later action.

## 10. Reachability and unique commits

Every Batch-6 HEAD is reachable from durable local and remote refs:

| HEAD | Worktrees | Durable refs | Exact containing-ref summary |
|---|---|---:|---|
| `4f367ce1...` | `PLANREC`, `WBS` | 6 | P9, Pathscope, RP7 local branches and corresponding remotes |
| `ec98cbd4...` | `PSCAUD` | 2 | local and remote `codex/pathscope-accounting-redesign-20260815` |
| `c84497c8...` | `RO` | 2 | local and remote `codex/rp7-r1-r4-repair-20260815` |
| `62bf661b...` | `AUD62A` | 2 | local and remote `integration/bridge-release-20260815` |
| `be689537...` | `AUD62B` | 2 | local and remote `integration/bridge-release-20260815` |
| `a7460784...` | `AUD62C` | 2 | local and remote `integration/bridge-release-20260815` |
| `acdf4e37...` | `AUD62D` | 2 | local and remote `integration/bridge-release-20260815` |

For every HEAD:

`git rev-list <HEAD> --not --branches --remotes --tags --count`

returned **0**. No commit unique to a detached Batch-6 HEAD was found. Ref and unique-commit checks must be repeated immediately before removal because refs can move.

## 11. Windows handle/current-directory blocker

Full process-use proof remains unavailable:

- Sysinternals `handle.exe` is not installed or discoverable.
- `openfiles /query` reports that the global “maintain objects list” flag is disabled for local handles.
- `Win32_Process` exposes executable paths and command lines but not each process's current working directory.

Therefore none of the four conditional candidates is removal-ready. Do not install tools, enable global tracking, restart the machine, stop processes, or alter permissions as part of this audit.

## 12. Batches 1–6 coverage reconciliation

At this snapshot:

- registered worktrees: **155**;
- detached, tracked-clean review pool: **88**;
- unique paths recorded in Batches 1–5: **80**;
- previously uncovered eligible paths found for Batch 6: **8**;
- eligible clean-detached paths remaining after Batch 6 selection: **0**.

| Batch | Paths audited | Conditional RETIRE-CANDIDATE | HOLD |
|---|---:|---:|---:|
| Batch 1 | 10 | 0 | 10 |
| Batch 2 | 10 | 0 | 10 |
| Batch 3 | 20 | 18 | 2 |
| Batch 4 | 20 | 19 | 1 |
| Batch 5 | 20 | 10 | 10 |
| Batch 6 | 8 | 4 | 4 |
| **Total** | **88** | **51** | **37** |

**Coverage conclusion:** Batches 1–6 cover the full live detached, tracked-clean review pool of 88 worktrees as measured on 2026-08-17. This does not cover branch-attached, tracked-dirty, unavailable, or future worktrees. Registry and status changes can invalidate the snapshot.

## 13. Final disposition and future proof gate

### HOLD

- `PLANREC`, `WBS`, and `PSCAUD`: unique untracked evidence absent from the current checkout.
- `RO`: current claimed `RP7-WPI-RO` lock-name ambiguity.

### Conditional RETIRE-CANDIDATE

`AUD62A`, `AUD62B`, `AUD62C`, and `AUD62D` pass tracked state, untracked/ignored-content preservation, operational-residue, permissions, lock-name, explicit process-path, reachability, and unique-commit checks at this snapshot. They remain **not removal-authorized** because open-handle/current-directory proof is missing.

Before any future removal, at an owner-authorized cleanup window when agents are stopped:

1. reread `SESSION_LOCK.md` and the live worktree registry;
2. reproduce tracked cleanliness and ordinary untracked inventory;
3. reproduce ignored and operational-residue inventories with zero read errors;
4. reproduce containing refs and zero unique commits;
5. obtain approved open-handle and process-current-directory proof;
6. exclude all HOLD paths until their evidence or lock ambiguity receives a separate decision;
7. write the exact retirement record and exact path list;
8. use `git worktree remove <exact-path>` only—never raw recursive filesystem deletion.

No removal is authorized by this report.
