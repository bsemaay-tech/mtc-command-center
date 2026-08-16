# Worktree Retirement Audit — Batch 3

**Date:** 2026-08-17

**Mode:** bounded read-only retirement inventory; this report is the only write

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Result:** **18 conditional RETIRE-CANDIDATE; 2 HOLD; remove none**

## 1. Meaning of the verdicts

- **RETIRE-CANDIDATE** means the worktree passed every non-handle check in this snapshot. It is a review queue classification only. It does **not** authorize or prove safe removal.
- **HOLD** means an independent blocker exists even before the Windows handle/current-directory gap is resolved.
- **No Batch-3 worktree may be removed now.** `handle.exe` is unavailable, local `openfiles` tracking is disabled, and `Win32_Process` does not expose process current directories. Therefore open-handle/current-directory proof is unavailable for all twenty.

No worktree, branch, ref, file, process, lock, permission, or Git configuration was changed. No worktree was removed. No host was accessed. No commit was created.

## 2. Selection method

Batch 3 selected the next twenty detached, tracked-clean worktrees not already covered by Batch 1 or Batch 2. Git does not preserve a canonical worktree-creation timestamp, so “oldest” was ranked by detached HEAD commit date, then by path.

For each registered worktree, the audit required:

1. path exists and Git reports detached HEAD;
2. `git status --porcelain --untracked-files=no` is empty;
3. exact HEAD commit date is recorded;
4. the path is not one of the twenty Batch-1/2 paths.

The selected range is `008e065e...` dated 2026-07-19 through `61d88f12...` dated 2026-08-09.

## 3. Proof checklist

Each selected worktree was checked for:

1. tracked cleanliness;
2. ordinary untracked files;
3. ignored/generated files, accessible size, and inventory-read errors;
4. Git worktree `locked` and `prunable` markers;
5. exact path/name references in current `SESSION_LOCK.md`;
6. explicit candidate-path strings in live process command lines or executable paths;
7. durable containing local branches, remote refs, and tags;
8. commits reachable from the detached HEAD but from no branch, remote, or tag;
9. tracked repository references to the candidate name and exact HEAD SHA;
10. recursive apparent file size and scan completeness;
11. availability of Windows open-handle and process-current-directory proof.

All measurements are a 2026-08-17 snapshot and must be repeated immediately before any later retirement action.

## 4. Batch summary

- Candidates audited: **20**
- Detached and tracked-clean: **20 of 20**
- Git `locked` markers: **0**
- Git `prunable` markers: **0**
- Ordinary untracked paths: **0 across all twenty**
- Exact candidate path/name hits in current `SESSION_LOCK.md`: **0 across all twenty**
- Unique commits outside branches/remotes/tags: **0 across all twenty**
- Explicit live process path hits: **1**, for `C:\P2RT`
- Incomplete filesystem/ignored inventory: **1**, for `C:\WPSAUD5`
- Total apparent size: **20,122.93 MiB** (about **19.65 GiB**)
- Conditional 18-tree retirement pool: **18,094.37 MiB** (about **17.67 GiB**)
- Accessible ignored content: approximately **86.678 MiB**; the `WPSAUD5` value is a lower bound because one directory is unreadable

The apparent-size figures are logical file-length sums, not guaranteed physical disk savings. Shared blocks, filesystem allocation, inaccessible files, and Git common-dir storage can make actual reclaimed space differ.

## 5. Candidate results

| Worktree | HEAD | Commit date | Size MiB | Ignored inventory | Durable refs | Unique commits | Name / SHA refs | Process hit | Verdict |
|---|---|---|---:|---|---:|---:|---:|---|---|
| `C:\P2RT` | `008e065e8e0ffa68f46134da6698d58f91ef2dcb` | 2026-07-19 21:48 +03 | 1,022.43 | 128 / 23.724 MiB; caches plus live DB/WAL/log evidence | 113 | 0 | 73 / 8 | **Yes** | **HOLD — active process + operational data** |
| `C:\KVM2F61_PROBE` | `f61ed91919110e8856b2bc309c2c807365bb5fea` | 2026-07-26 22:25 +03 | 1,000.32 | none | 84 | 0 | 0 / 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\WPSAUD5` | `732b37c39612082958d2863681e75d17aabae088` | 2026-08-01 09:30 +03 | at least 1,006.13 | at least 61 / 5.126 MiB; cache inventory incomplete | 43 | 0 | 2 / 0 | No | **HOLD — permission-denied inventory + handles** |
| `C:\GA4RED` | `637307e83951ffe23e768ed8e50ddaf8712b0660` | 2026-08-01 20:30 +03 | 1,007.21 | 70 / 5.192 MiB; generated caches only | 41 | 0 | 0 / 14 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_5A_CDX` | `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` | 2026-08-02 14:16 +03 | 1,007.10 | 61 / 5.078 MiB; generated caches only | 8 | 0 | 1 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_5A_CLA` | `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` | 2026-08-02 14:16 +03 | 1,007.10 | 61 / 5.078 MiB; generated caches only | 8 | 0 | 1 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_5A_CLD` | `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` | 2026-08-02 14:16 +03 | 1,007.10 | 61 / 5.078 MiB; generated caches only | 8 | 0 | 1 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\MORNAUD_5A` | `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` | 2026-08-02 14:16 +03 | 1,007.22 | 66 / 5.199 MiB; generated caches only | 8 | 0 | 0 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_BUILD_R2_CDX` | `82e92c98fdc24cfc1632960460d3ac7e4131db25` | 2026-08-03 01:36 +03 | 1,002.03 | none | 8 | 0 | 0 / 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_BUILD_R2_GLM` | `82e92c98fdc24cfc1632960460d3ac7e4131db25` | 2026-08-03 01:36 +03 | 1,007.27 | 65 / 5.235 MiB; generated caches only | 8 | 0 | 0 / 0 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_INT_GLM` | `ebada020a59edf539f60acfbb3a6bf870c8679e9` | 2026-08-03 04:54 +03 | 1,007.43 | 65 / 5.359 MiB; generated caches only | 6 | 0 | 6 / 12 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM` | `ed3d053432fb496123ac43bcb7d40cfb64edbb8b` | 2026-08-08 15:55 +03 | 1,002.07 | none | 4 | 0 | 3 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM_CLA` | `ed3d053432fb496123ac43bcb7d40cfb64edbb8b` | 2026-08-08 15:55 +03 | 1,007.48 | 66 / 5.406 MiB; generated caches only | 4 | 0 | 3 / 4 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM_CDX_R2` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | 2026-08-08 18:28 +03 | 1,007.44 | 65 / 5.365 MiB; generated caches only | 4 | 0 | 1 / 117 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM_CLA_R2` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | 2026-08-08 18:28 +03 | 1,007.49 | 66 / 5.413 MiB; generated caches only | 4 | 0 | 1 / 117 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM_DS_R2` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | 2026-08-08 18:28 +03 | 1,002.08 | none | 4 | 0 | 1 / 117 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAAUD_DISARM_GLM_R2` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | 2026-08-08 18:28 +03 | 1,007.44 | 65 / 5.365 MiB; generated caches only | 4 | 0 | 1 / 117 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2CAND` | `2ce41e34bceb599d80af24c5c33d835820ec321b` | 2026-08-08 18:28 +03 | 1,002.14 | 1 / 0.060 MiB; generated Python cache | 4 | 0 | 1 / 117 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAEAC` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.72 | none | 30 | 0 | 1 / 5 | No | RETIRE-CANDIDATE — handles unresolved |
| `C:\GAEAD` | `61d88f12054cdc81896ca7596c699aff1a7b9a71` | 2026-08-09 02:00 +03 | 1,002.72 | none | 30 | 0 | 1 / 5 | No | RETIRE-CANDIDATE — handles unresolved |

“Name / SHA refs” counts tracked files returned by exact `git grep` searches in the current repository. They are evidence-preservation signals, not blockers by themselves.

## 6. Ordinary untracked inventory

Every candidate returned zero paths from:

`git ls-files --others --exclude-standard`

This proves no ordinary untracked source, report, patch, manifest, or user file was visible through Git's standard inventory at the snapshot. It does not override ignored content, inaccessible paths, process use, or handle uncertainty.

## 7. Ignored/generated content

### Cache-only or empty candidates

The eighteen conditional candidates contain either no ignored paths or only generated Python/pytest caches:

- Empty: `KVM2F61_PROBE`, `GAAUD_BUILD_R2_CDX`, `GAAUD_DISARM`, `GAAUD_DISARM_DS_R2`, `GAEAC`, `GAEAD`.
- Python cache only: `GAAUD_5A_CDX`, `GAAUD_5A_CLA`, `GAAUD_5A_CLD`, `WP2CAND`.
- Python plus pytest caches: `GA4RED`, `MORNAUD_5A`, `GAAUD_BUILD_R2_GLM`, `GAAUD_INT_GLM`, `GAAUD_DISARM_CLA`, `GAAUD_DISARM_CDX_R2`, `GAAUD_DISARM_CLA_R2`, `GAAUD_DISARM_GLM_R2`.

No accessible ignored path in those eighteen fell outside generated cache categories. A future pre-removal check must reproduce that result.

### `C:\P2RT` — operational state, not disposable cache

The 128 ignored paths include:

- 97 `__pycache__` paths;
- 9 `.pytest_cache` paths;
- `IBKR_PAPER_BRIDGE/data/bridge.db`;
- `bridge.db-shm` and `bridge.db-wal`;
- 18 dated Bridge logs from 2026-07-13 through 2026-08-15;
- `reports/parity_report.json`.

The SQLite database, WAL/SHM sidecars, logs, and parity report are operational/evidence content. They must not be deleted, moved, copied as a supposedly stable backup, or treated as cache by repository cleanup.

### `C:\WPSAUD5` — inventory incomplete

Git reported:

`warning: could not open directory 'IBKR_PAPER_BRIDGE/.pytest_cache/': Permission denied`

The recursive size scan independently reported access denied for the same directory. Therefore the visible 61 ignored files / 5.126 MiB and the 1,006.13 MiB total are lower bounds. Do not change permissions, take ownership, delete, or move the directory as part of cleanup.

## 8. Live process and lock checks

### Active `P2RT` process

The live `Win32_Process` snapshot found one exact worktree-path reference:

- PID 48064, `powershell.exe`
- command launches `C:\P2RT\IBKR_PAPER_BRIDGE\tools\run_bridge_p2.ps1`

This is direct evidence that `C:\P2RT` is active. It is a hard **HOLD**, independent of the handle-tool limitation. This audit did not inspect or alter the process, its database, or its logs.

No explicit command-line or executable-path reference was found for the other nineteen candidates. This is weaker than open-handle/current-directory proof.

### Current session lock

Exact searches of current `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md` found zero candidate names or paths. No current Git worktree entry carried a `locked` or `prunable` marker.

The lock result is a volatile snapshot. It must be re-read immediately before any future retirement attempt.

## 9. Reachability and unique commits

Every candidate HEAD is reachable from at least four durable local/remote refs; most older commits are ancestors of many current refs. Representative exact groups:

| HEAD | Worktrees | Durable refs | Representative containing local branches |
|---|---|---:|---|
| `008e065e...` | `P2RT` | 113 | 77 local branches, including current chore, Bridge, and integration descendants |
| `f61ed919...` | `KVM2F61_PROBE` | 84 | 53 local branches, including current chore, Bridge, and integration descendants |
| `732b37c3...` | `WPSAUD5` | 43 | 21 local branches, including Gate-A descendants |
| `637307e8...` | `GA4RED` | 41 | 20 local branches, including `master` and Gate-A descendants |
| `5a9bb922...` | four Queue-C/5A trees | 8 | `codex/gate-a-credential-free-disarmed`, `codex/gate-a-disarmed-start-mode`, `codex/gate-a-integration`, `integration/bridge-release-20260815` |
| `82e92c98...` | two build round-2 trees | 8 | `codex/gate-a-build-determinism`, `codex/gate-a-disarmed-start-mode`, `codex/gate-a-integration`, integration release |
| `ebada020...` | `GAAUD_INT_GLM` | 6 | disarmed-start, Gate-A integration, integration release |
| `ed3d0534...` | two DISARM round-1 trees | 4 | disarmed-start and integration release |
| `2ce41e34...` | five DISARM round-2 trees | 4 | disarmed-start and integration release |
| `61d88f12...` | `GAEAC`, `GAEAD` | 30 | 21 local Gate-A/readiness and later descendant branches |

For every HEAD:

`git rev-list <HEAD> --not --branches --remotes --tags --count`

returned **0**. No commit unique to a detached Batch-3 HEAD was found. Refs can move, so this must be rerun immediately before removal.

## 10. Tracked evidence references

Tracked records preserve the named audit work and/or exact candidate SHAs. Examples include:

- `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-01.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_QUEUE_C_FLAGSHIP_AUDIT_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_QUEUE_C_FLAGSHIP_ROUND_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE_A_INTEGRATION_AUDIT_PROMPT_EBADA020_2026-08-03.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_INTEGRATION_RECORD_EBADA020_2026-08-03.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND1_ED3D0534_2026-08-08.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_DISARM_FIX_AUDIT_ROUND2_2CE41E34_2026-08-08.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_A5_E_CANONICAL_ACCEPTANCE_2026-08-09.md`

`KVM2F61_PROBE` and its exact HEAD SHA produced no tracked text hit, but the commit is still reachable from 84 durable refs and has zero unique commits. Tracked evidence references are not a substitute for preserving untracked/ignored files; that is why `P2RT` and `WPSAUD5` remain held.

## 11. Windows open-handle/current-directory blocker

Full process-use proof is unavailable:

- Sysinternals `handle.exe` is not installed or discoverable.
- `openfiles /query` reports that the system-wide “maintain objects list” flag is disabled for local handles.
- `Win32_Process` exposes executable paths and command lines but not each process's current working directory.

Therefore none of the eighteen conditional candidates is removal-ready. Do not install tools, enable global tracking, restart the machine, stop processes, or alter permissions as part of this audit.

## 12. Final disposition and future proof gate

### HOLD

1. `C:\P2RT` — active Bridge runner plus operational database/WAL/log evidence.
2. `C:\WPSAUD5` — unreadable ignored directory makes inventory and size incomplete.

These remain held even if open-handle proof becomes available.

### Conditional RETIRE-CANDIDATE

The remaining eighteen pass tracked/untracked, accessible ignored-content, lock-name, explicit process-path, reachability, unique-commit, and tracked-evidence checks at this snapshot. They remain **not removal-authorized** because open-handle/current-directory proof is missing.

Before any future removal, at an owner-authorized cleanup window when agents are stopped:

1. reread `SESSION_LOCK.md` and the live worktree registry;
2. reproduce tracked cleanliness and ordinary untracked inventory;
3. reproduce ignored inventory with zero read errors;
4. reproduce containing refs and zero unique commits;
5. obtain approved open-handle and process-current-directory proof;
6. exclude `P2RT` and `WPSAUD5` unless separately resolved under a dedicated preservation plan;
7. write the exact retirement record and exact path list;
8. use `git worktree remove <exact-path>` only—never raw recursive filesystem deletion.

No removal is authorized by this report.
