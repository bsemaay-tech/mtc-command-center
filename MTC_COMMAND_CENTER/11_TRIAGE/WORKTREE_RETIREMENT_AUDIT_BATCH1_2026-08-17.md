# Worktree Retirement Audit — Batch 1

**Date:** 2026-08-17 01:10 +03:00  
**Mode:** bounded read-only retirement audit; this report is the only write  
**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`  
**Result:** **HOLD ALL 10** — no worktree was removed or declared fully retirement-ready because open-handle/current-directory proof is unavailable on this Windows host.

## 1. Scope and exclusions

This batch selected ten old, detached, tracked-clean Gate-A audit worktrees. Selection deliberately excluded:

- every tracked-dirty worktree
- the active Help/System Map worktree
- Gemini worktrees
- KVM2 and current deployment/integration worktrees
- RP7, SEC102/Pathscope, Audit-2, and other currently locked workstreams
- ambiguous generic worktrees whose current purpose was not immediately clear

No worktree, ref, branch, file, process, lock, or Git configuration was changed. No server or host was accessed. No commit was created.

## 2. Proof standard applied

Each candidate was checked for:

1. exact detached HEAD identity
2. Git tracked cleanliness
3. ordinary untracked files and their sizes
4. ignored files and their types/sizes
5. Git worktree `locked` or `prunable` markers
6. explicit running-process command-line or executable-path references
7. ability to prove local open handles or process current directories
8. current `SESSION_LOCK.md` path/name relevance
9. HEAD reachability from permanent local, remote, or tag refs
10. commits unique to the detached HEAD
11. tracked evidence references to the worktree path/name and HEAD SHA
12. total apparent worktree size

The decision rule was fail-closed: any proof gap yields `HOLD`, not `READY TO REMOVE`.

## 3. Batch summary

All ten candidates share these results:

- detached: **yes**
- tracked changes: **0**
- ordinary untracked files: **0**
- Git worktree `locked`: **no**
- Git worktree `prunable`: **no**
- exact candidate-name mentions in current `SESSION_LOCK.md`: **0**
- current active lock rows directly covering these old Gate-A audit paths: **none found**
- explicit process command-line/executable-path references: **0**
- commits unique to the detached HEAD relative to local branches, remote refs, and tags: **0**
- HEAD reachable from multiple local and `origin/*` refs: **yes**
- full open-handle/current-directory proof: **failed / unavailable**
- final disposition: **HOLD**

Total apparent size of the ten worktrees: **10,061.73 MiB** (about **9.83 GiB**).

## 4. Candidate-by-candidate results

| Worktree | HEAD | Commit date | Size MiB | Ignored inventory | Containing refs | Unique commits | Path refs / SHA refs | Disposition |
|---|---|---|---:|---|---:|---:|---:|---|
| `C:\GAAUD_3B` | `df00634fc2e5fb19cddb34a6ad16d9764c4779a4` | 2026-08-02 10:38 +03 | 1,007.22 | 65 / 5.196 MiB | 10 | 0 | 4 / 24 | HOLD |
| `C:\GAAUD_3B_CDX` | `df00634fc2e5fb19cddb34a6ad16d9764c4779a4` | 2026-08-02 10:38 +03 | 1,007.24 | 65 / 5.219 MiB | 10 | 0 | 1 / 24 | HOLD |
| `C:\GAAUD_3B_CLA` | `df00634fc2e5fb19cddb34a6ad16d9764c4779a4` | 2026-08-02 10:38 +03 | 1,007.24 | 65 / 5.219 MiB | 10 | 0 | 2 / 24 | HOLD |
| `C:\GAAUD_C5` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,007.12 | 60 / 5.089 MiB | 8 | 0 | 6 / 16 | HOLD |
| `C:\GAAUD_C5_CDX` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,007.12 | 60 / 5.090 MiB | 8 | 0 | 2 / 16 | HOLD |
| `C:\GAAUD_C5_CLA` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,007.12 | 60 / 5.090 MiB | 8 | 0 | 1 / 16 | HOLD |
| `C:\GAAUD_BUILD_CODEX` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,002.03 | none | 8 | 0 | 0 / 16 | HOLD |
| `C:\GAAUD_BUILD_GLM` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,002.03 | none | 8 | 0 | 0 / 16 | HOLD |
| `C:\MORNAUD_C5` | `c5a4070a4836bbb9ee010dc63db69313066667c4` | 2026-08-02 12:51 +03 | 1,007.24 | 65 / 5.211 MiB | 8 | 0 | 0 / 16 | HOLD |
| `C:\GAAUD_4_GLM` | `5a9bb922d5255c6a9cb2e8d8b3e7bf9305438002` | 2026-08-02 14:16 +03 | 1,007.37 | 71 / 5.343 MiB | 8 | 0 | 0 / 15 | HOLD |

`Path refs / SHA refs` counts are tracked textual references found under `MTC_COMMAND_CENTER` and `IBKR_PAPER_BRIDGE`. They establish that the historical reports cite these audit paths/SHAs; they do not establish that the directories must stay on disk forever.

## 5. Untracked and ignored inventory

### Ordinary untracked files

Every candidate returned zero files from:

`git ls-files --others --exclude-standard`

This is a strong positive result: no ordinary untracked report, patch, evidence file, or user file was found in any candidate.

### Ignored files

The ignored inventories were completely classified:

- `GAAUD_3B`, `GAAUD_3B_CDX`, `GAAUD_3B_CLA`: 60 `__pycache__` files plus 5 `.pytest_cache` files each.
- `GAAUD_C5`, `GAAUD_C5_CDX`, `GAAUD_C5_CLA`: 60 `__pycache__` files each.
- `GAAUD_BUILD_CODEX`, `GAAUD_BUILD_GLM`: no ignored files.
- `MORNAUD_C5`: 60 `__pycache__` files plus 5 `.pytest_cache` files.
- `GAAUD_4_GLM`: 61 `__pycache__` files plus 10 `.pytest_cache` files.

No ignored file fell outside those two generated-cache categories. The largest examples were compiled Python test/store caches between about 364 KiB and 608 KiB. No ignored source, report, fixture, manifest, database, credential file, or D026 evidence artifact was found.

Therefore, ignored inventory passes the uniqueness/evidence screen for all ten candidates. The caches themselves need no archival ref, but no deletion is authorized in this audit.

## 6. HEAD reachability and unique commits

### `df00634f...` group

The HEAD is contained by ten durable refs, including:

- `refs/heads/codex/gate-a-3b-shm-validation`
- `refs/heads/codex/gate-a-disarmed-start-mode`
- `refs/heads/codex/gate-a-integration`
- `refs/heads/codex/wal-bundle-linux-sidecars`
- `refs/heads/integration/bridge-release-20260815`
- corresponding five `refs/remotes/origin/*` refs

Unique commits outside branches/remotes/tags: **0**.

### `c5a4070a...` group

The HEAD is contained by eight durable refs, including:

- `refs/heads/codex/gate-a-build-determinism`
- `refs/heads/codex/gate-a-disarmed-start-mode`
- `refs/heads/codex/gate-a-integration`
- `refs/heads/integration/bridge-release-20260815`
- corresponding four `refs/remotes/origin/*` refs

Unique commits outside branches/remotes/tags: **0**.

### `5a9bb922...` group

The HEAD is contained by eight durable refs, including:

- `refs/heads/codex/gate-a-credential-free-disarmed`
- `refs/heads/codex/gate-a-disarmed-start-mode`
- `refs/heads/codex/gate-a-integration`
- `refs/heads/integration/bridge-release-20260815`
- corresponding four `refs/remotes/origin/*` refs

Unique commits outside branches/remotes/tags: **0**.

All three identities pass reachability and unique-commit proof. Removing only a linked worktree would not make these commits unreachable under the observed ref state. Ref state must be rechecked immediately before any future removal.

## 7. Evidence and path-reference review

Tracked records preserve the purpose and outcome of the referenced worktrees/commits. Examples include:

- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_3B_RETROSPECTIVE_FLAGSHIP_ROUND_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_3B_AUDIT_ROUND1_2026-08-03.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_C5A4070A_FLAGSHIP_ROUND_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_C5A4070A_RETROSPECTIVE_AUDIT_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_CREDENTIAL_FREE_DISARMED_CANDIDATE_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_QUEUE_C_FLAGSHIP_AUDIT_2026-08-02.md`

Some records explicitly describe a worktree as detached and clean at audit close. The exact SHAs are also cited and remain reachable from multiple pushed refs. No ordinary untracked evidence exists inside the ten worktrees.

Evidence/path-reference proof therefore passes with one future-retirement condition: any actual removal record must state that the historical path no longer exists while the cited commit and report remain preserved.

## 8. Process and open-handle proof — blocking gap

A live `Win32_Process` snapshot found zero candidate-path strings in any non-audit process command line or executable path.

However, that is not full proof that no process has a candidate as its current working directory or holds an open file there:

- Sysinternals `handle.exe` is not installed/available.
- Windows `openfiles /query` reports that the local “maintain objects list” global flag is disabled.
- `openfiles` remote-share enumeration also returned access denied.
- `Win32_Process` does not expose process current working directories.

Therefore, the mandatory active-process/open-handle check is **not proven**. This single gap is sufficient to keep all ten candidates on `HOLD`, even though every Git/evidence check passed.

Do not enable the global `openfiles` flag or install tooling as part of this audit; both are external system changes requiring their own scope.

## 9. `SESSION_LOCK.md` relevance

Exact candidate-name searches returned zero mentions in `SESSION_LOCK.md`. The current claimed rows cover:

- RP7-WPI-RO
- SEC102/Pathscope
- Audit-2 readiness
- shared `_AI_MEMORY`
- Bridge Help/System Map

The selected old Gate-A audit worktrees are not named or covered by those current row paths. This criterion passes at the snapshot time. The lock table must still be re-read immediately before any future removal.

## 10. Final verdict

### What passed

- tracked cleanliness
- zero ordinary untracked files
- ignored-file classification
- no Git worktree lock/prunable marker
- no current `SESSION_LOCK.md` match
- no explicit running-process path reference
- multiple durable local and remote containing refs
- zero unique commits
- historical evidence/path documentation
- exact size measurement

### What failed

- full current-working-directory/open-file-handle proof is unavailable

### Disposition

**HOLD ALL 10. REMOVE NONE.**

If the owner later authorizes destructive cleanup, perform one fresh pre-removal check while no agents are running:

1. obtain open-handle/current-directory proof with an approved read-only tool or a controlled restart/session boundary
2. recheck `SESSION_LOCK.md`
3. recheck tracked and ordinary untracked status
4. recheck ignored inventory
5. recheck containing refs and zero unique commits
6. write the exact retirement record
7. use `git worktree remove <exact-path>` only; never raw filesystem deletion

Potential apparent disk recovery from this batch is about 9.83 GiB, but it is not authorized or presently proven safe to reclaim.
