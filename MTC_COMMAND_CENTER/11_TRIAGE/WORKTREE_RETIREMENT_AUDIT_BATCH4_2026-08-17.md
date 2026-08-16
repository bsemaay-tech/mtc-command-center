# Worktree Retirement Audit — Batch 4

**Date:** 2026-08-17

**Mode:** bounded read-only retirement inventory; this report is the only write

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Result:** **19 conditional RETIRE-CANDIDATE; 1 HOLD; remove none**

## 1. Verdict meanings and hard boundary

- **RETIRE-CANDIDATE** means the worktree passed every non-handle check in this snapshot. It is a review-queue classification only, not removal authorization.
- **HOLD** means an independent preservation blocker exists before the Windows handle/current-directory gap is resolved.
- **No Batch-4 worktree may be removed now.** `handle.exe` is unavailable, local `openfiles` tracking is disabled, and `Win32_Process` does not expose process current directories.

No worktree, branch, ref, file, process, lock, permission, or Git configuration was changed. No worktree was removed. No host was accessed. No commit was created.

## 2. Selection method

Batch 4 selected the next twenty detached, tracked-clean worktrees not covered by Batches 1–3. Git has no canonical worktree-creation timestamp, so age was ranked by detached HEAD commit date, then by path.

The selected range begins at `61d88f12...` dated 2026-08-09 02:00 +03 and ends at `4599b466...` dated 2026-08-09 08:00 +03.

For each registered worktree, selection required:

1. an existing path;
2. a detached HEAD;
3. empty `git status --porcelain --untracked-files=no` output;
4. no path match in the Batch-1, Batch-2, or Batch-3 result tables.

## 3. Proof checklist

Each candidate was checked for:

1. tracked cleanliness;
2. ordinary untracked files;
3. ignored/generated content and inventory-read errors;
4. operational database, WAL/SHM, log, and evidence residue;
5. Git worktree `locked` and `prunable` markers;
6. exact path/name references in current `SESSION_LOCK.md`;
7. explicit candidate-path strings in live process command lines or executable paths;
8. durable containing local branches, remote refs, and tags;
9. commits reachable from the detached HEAD but from no branch, remote, or tag;
10. tracked repository references to the candidate name and exact HEAD SHA;
11. recursive apparent file size and permission/scan errors;
12. availability of Windows open-handle and process-current-directory proof.

All findings are a 2026-08-17 snapshot and must be repeated before any later retirement action.

## 4. Batch summary

- Candidates audited: **20**
- Detached and tracked-clean: **20 of 20**
- Git `locked` markers: **0**
- Git `prunable` markers: **0**
- Ordinary untracked paths: **1**, in `C:\PGRK`
- Ignored paths: **0 across all twenty**
- Operational DB/WAL/SHM/log paths: **0 visible across all twenty**
- Permission or recursive-scan errors: **0 across all twenty**
- Exact candidate path/name hits in current `SESSION_LOCK.md`: **0 across all twenty**
- Explicit live process-path hits: **0 across all twenty**
- Unique commits outside branches/remotes/tags: **0 across all twenty**
- Total apparent size: **20,059.371 MiB** (about **19.589 GiB**)
- Conditional 19-tree retirement pool: **19,055.997 MiB** (about **18.609 GiB**)

The apparent-size figures are logical file-length sums, not guaranteed physical disk savings. Git common-dir storage, allocation, and shared filesystem blocks can make actual reclaimed space differ.

## 5. Candidate results

| Worktree | HEAD | Commit date | Size MiB | Ordinary untracked | Ignored | Durable refs | Unique commits | Name / SHA refs | Process hit | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `C:\GAEAG` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.715 | 0 | 0 | 30 | 0 | 1 / 5 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAEAX` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.715 | 0 | 0 | 30 | 0 | 2 / 5 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAEAX2` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.715 | 0 | 0 | 30 | 0 | 2 / 5 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAEAX3` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.715 | 0 | 0 | 30 | 0 | 1 / 5 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAE3C` | `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1` | 2026-08-09 03:03 +03 | 1,002.779 | 0 | 0 | 30 | 0 | 0 / 3 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAE3D` | `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1` | 2026-08-09 03:03 +03 | 1,002.779 | 0 | 0 | 30 | 0 | 0 / 3 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAE3G` | `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1` | 2026-08-09 03:03 +03 | 1,002.779 | 0 | 0 | 30 | 0 | 0 / 3 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAE3X` | `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1` | 2026-08-09 03:03 +03 | 1,002.779 | 0 | 0 | 30 | 0 | 0 / 3 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAE3X2` | `b2c369f73abd3d90b17000e601c6f9cdc21c4cf1` | 2026-08-09 03:03 +03 | 1,002.779 | 0 | 0 | 30 | 0 | 0 / 3 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\tmp\gatea_postgate_prereg_glm` | `7c4cac2bf4ec28f66416490e40e5a66503c81ca7` | 2026-08-09 05:54 +03 | 1,003.029 | 0 | 0 | 1 | 0 | 0 / 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGAA` | `f8a6bc0f1a7fa00fcd1637297e05424732386da7` | 2026-08-09 06:47 +03 | 1,003.085 | 0 | 0 | 2 | 0 | 0 / 2 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGAC` | `f8a6bc0f1a7fa00fcd1637297e05424732386da7` | 2026-08-09 06:47 +03 | 1,003.085 | 0 | 0 | 2 | 0 | 0 / 2 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGAD` | `f8a6bc0f1a7fa00fcd1637297e05424732386da7` | 2026-08-09 06:47 +03 | 1,003.085 | 0 | 0 | 2 | 0 | 0 / 2 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGAG` | `f8a6bc0f1a7fa00fcd1637297e05424732386da7` | 2026-08-09 06:47 +03 | 1,003.085 | 0 | 0 | 2 | 0 | 0 / 2 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PG2A` | `2fa120b928045704405c0a5156d73b3b930d1837` | 2026-08-09 07:44 +03 | 1,003.174 | 0 | 0 | 1 | 0 | 0 / 1 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PG2C` | `2fa120b928045704405c0a5156d73b3b930d1837` | 2026-08-09 07:44 +03 | 1,003.174 | 0 | 0 | 1 | 0 | 0 / 1 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PG2D` | `2fa120b928045704405c0a5156d73b3b930d1837` | 2026-08-09 07:44 +03 | 1,003.174 | 0 | 0 | 1 | 0 | 0 / 1 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PG2G` | `2fa120b928045704405c0a5156d73b3b930d1837` | 2026-08-09 07:44 +03 | 1,003.174 | 0 | 0 | 1 | 0 | 0 / 1 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGR` | `2fa120b928045704405c0a5156d73b3b930d1837` | 2026-08-09 07:44 +03 | 1,003.173 | 0 | 0 | 1 | 0 | 18 / 1 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\PGRK` | `4599b466def320cd4afeeb238e0e192303bd85c4` | 2026-08-09 08:00 +03 | 1,003.374 | **1** | 0 | 15 | 0 | 13 / 1 | No | **HOLD — unique untracked evidence + handles** |

“Name / SHA refs” counts tracked files returned by exact `git grep` searches in the current repository. Name matches such as `PGR` can include textual substring matches and are evidence-location hints, not sole disposition evidence.

## 6. Ordinary untracked and ignored inventory

Nineteen candidates returned zero paths from both:

`git ls-files --others --exclude-standard`

`git ls-files --others --ignored --exclude-standard`

No accessible database, WAL/SHM sidecar, log, evidence directory, Python cache, pytest cache, virtual environment, temporary corpus, or other ignored path was visible in any Batch-4 worktree. Recursive scans produced zero permission errors.

This is a snapshot only. A future pre-removal audit must reproduce the result.

## 7. `C:\PGRK` preservation hold

`C:\PGRK` contains one ordinary untracked file:

`MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_2026-08-09.md`

Measured identity:

- size: **194,207 bytes** (approximately 189.655 KiB);
- SHA-256: `D12E25FB06273B006C47342FAC093D4AFC99E32BDA815FB5E428B8A3DA584107`;
- absent from the current main checkout;
- absent from the `PGRK` HEAD index;
- not returned by `git ls-files` in the current repository.

The document identifies itself as a Gate-A post-gate local run-kit design contract covering read-only Stage B, stop, reboot, WAL bundle, rollback, safety gates, provenance, and proposed command shapes. It explicitly says it was not executed and grants no host authority. Its content is unique untracked design/evidence material, not disposable generated output.

`PGRK` is therefore **HOLD** until a separate owner-authorized preservation review proves whether and where the document should be retained. This audit did not copy, edit, move, stage, or commit it.

## 8. Live process, lock, and permission checks

A `Win32_Process` snapshot found zero explicit Batch-4 path strings in process command lines or executable paths.

Exact searches of current `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md` found zero candidate names or paths. No selected Git worktree entry carried a `locked` or `prunable` marker.

Every recursive filesystem scan and ignored-file query completed without permission errors.

These checks do not prove absence of open handles or process current-directory use. They are volatile and must be repeated before any later action.

## 9. Reachability and unique commits

Every Batch-4 HEAD is reachable from at least one durable ref:

| HEAD | Worktrees | Durable refs | Containing-ref summary |
|---|---|---:|---|
| `61d88f12...` | four `GAEA*` trees | 30 | 21 local later Gate-A/readiness/Bridge branches plus remotes |
| `b2c369f7...` | five `GAE3*` trees | 30 | 21 local later Gate-A/readiness/Bridge branches plus remotes |
| `7c4cac2b...` | `gatea_postgate_prereg_glm` | 1 | `refs/remotes/origin/rescue/local-only-7c4cac2b` |
| `f8a6bc0f...` | four `PGA*` trees | 2 | remote rescue refs `local-only-f8a6bc0f` and descendant `local-only-2fa120b9` |
| `2fa120b9...` | five `PG2*`/`PGR` trees | 1 | `refs/remotes/origin/rescue/local-only-2fa120b9` |
| `4599b466...` | `PGRK` | 15 | current local Bridge/integration descendants and corresponding remotes |

For every HEAD:

`git rev-list <HEAD> --not --branches --remotes --tags --count`

returned **0**. No commit unique to a detached Batch-4 HEAD was found.

The `7c4cac2b...` and `2fa120b9...` groups depend on a single remote-tracking rescue ref, so their reachability is more fragile than the multi-ref groups. The exact ref and unique-commit checks must be repeated immediately before any removal.

## 10. Tracked evidence references

Tracked records preserve the audit work and/or exact SHAs. Examples include:

- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_E_CANONICAL_ACCEPTANCE_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_E_CANONICAL_AUDIT_ROUND1_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_E_PACKAGE_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PREREGISTRATION_GAP_MATRIX_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_PROVENANCE_REPAIR_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_POST_GATE_LOCAL_RUN_KIT_DESIGN_BLOCKER_2026-08-09.md`

The exact `7c4cac2b...` identity and its worktree name produced no current tracked text hit, but its commit remains reachable from the explicit rescue remote ref with zero unique commits.

Tracked records do not preserve the untracked `PGRK` design contract itself. That distinction is the reason for the hold.

## 11. Windows handle/current-directory blocker

Full process-use proof remains unavailable:

- Sysinternals `handle.exe` is not installed or discoverable.
- `openfiles /query` reports that the global “maintain objects list” flag is disabled for local handles.
- `Win32_Process` exposes executable paths and command lines but not each process's current working directory.

Therefore none of the nineteen conditional candidates is removal-ready. Do not install tools, enable global tracking, restart the machine, stop processes, or alter permissions as part of this audit.

## 12. Final disposition and future proof gate

### HOLD

`C:\PGRK` — unique, ordinary untracked Gate-A run-kit design/evidence document, plus unresolved handle/CWD proof.

### Conditional RETIRE-CANDIDATE

The other nineteen pass tracked/untracked, ignored-content, operational-residue, permissions, lock-name, explicit process-path, reachability, unique-commit, and tracked-reference checks at this snapshot. They remain **not removal-authorized** because open-handle/current-directory proof is missing.

Before any future removal, at an owner-authorized cleanup window when agents are stopped:

1. reread `SESSION_LOCK.md` and the live worktree registry;
2. reproduce tracked cleanliness and ordinary untracked inventory;
3. reproduce ignored and operational-residue inventories with zero read errors;
4. reproduce containing refs and zero unique commits;
5. obtain approved open-handle and process-current-directory proof;
6. exclude `PGRK` until its unique document receives a separate preservation decision;
7. write the exact retirement record and exact path list;
8. use `git worktree remove <exact-path>` only—never raw recursive filesystem deletion.

No removal is authorized by this report.
