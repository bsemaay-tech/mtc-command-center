# Worktree Retirement Audit — Batch 2

**Date:** 2026-08-17  
**Mode:** bounded read-only retirement audit; this report is the only write  
**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`  
**Result:** **HOLD ALL 10** — one worktree contains unpreserved mutation/test residue, and all ten lack full open-handle/current-directory proof.

## 1. Scope and exclusions

Batch 2 selected the next ten old, detached, tracked-clean Gate-A audit worktrees after Batch 1:

- two primary build-audit worktrees at `7be1c429...`
- eight duplicate WAL/SHM round-2 audit worktrees at `7aad0377...`

The selection excluded:

- all Batch-1 worktrees
- every tracked-dirty worktree
- active Help/System Map and Gemini worktrees
- KVM2 and current deployment/integration worktrees
- RP7, SEC102/Pathscope, Audit-2, and other currently locked paths
- ambiguous generic worktrees whose current role was not immediately clear

No worktree, branch, ref, file, process, lock, or Git configuration was changed. No worktree was removed. No host was accessed. No commit was created.

## 2. Proof checklist applied

Each candidate was checked for:

1. exact detached HEAD identity and commit date
2. Git tracked cleanliness
3. ordinary untracked inventory
4. ignored inventory, type, size, and read completeness
5. Git worktree `locked` and `prunable` markers
6. explicit running-process command-line/executable-path references
7. local open handles and process current-directory visibility
8. current `SESSION_LOCK.md` relevance
9. HEAD reachability from local branches, remote refs, or tags
10. commits unique to the detached HEAD
11. tracked evidence references to worktree names/paths and HEAD SHAs
12. apparent worktree size

Any uncertainty fails closed to `HOLD`.

## 3. Batch-wide results

- Candidates found: **10 of 10**
- Detached: **10 of 10**
- Git worktree `locked`: **0 of 10**
- Git worktree `prunable`: **0 of 10**
- Tracked changes: **0 in every candidate**
- Ordinary untracked files: **0 in every candidate**
- Exact candidate-name mentions in current `SESSION_LOCK.md`: **0**
- Explicit process command-line/executable-path references: **0**
- Unique commits outside local branches/remotes/tags: **0**
- Durable containing refs per HEAD: **8**
- Total apparent size: **10,066.89 MiB** (about **9.83 GiB**)

Nine candidates have only generated caches or no ignored files. One candidate, `C:\GAAUD_CODEX`, contains a substantial ignored `Temp/g5_r2_*` mutation/test corpus and permission-denied directories. That worktree fails the evidence and inventory-completeness checks independently of the process-proof gap.

## 4. Candidate results

| Worktree | HEAD | Commit date | Size MiB | Ignored inventory | Unique commits | Name refs / SHA refs | Verdict |
|---|---|---|---:|---|---:|---:|---|
| `C:\GAAUD_CODEX` | `7be1c429f70ed17c3f38a14d43e514495b2b64bd` | 2026-08-02 10:40 +03 | 1,030.89 | at least 453 / 28.73 MiB; mutation corpus + caches; incomplete read | 0 | 2 / 2 | HOLD — evidence + permissions + handles |
| `C:\GAAUD_CLAUDE` | `7be1c429f70ed17c3f38a14d43e514495b2b64bd` | 2026-08-02 10:40 +03 | 1,003.46 | 33 / 1.44 MiB; generated caches only | 0 | 1 / 2 | HOLD — handles |
| `C:\GAAUD_3BR2_CDX` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,007.41 | 71 / 5.37 MiB; generated caches only | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_3BR2_CLA` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,002.19 | 2 / 0.14 MiB; generated caches only | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_3BR2_DS` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,002.05 | none | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_3BR2_GLM` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,007.41 | 66 / 5.36 MiB; generated caches only | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_GA3BR2_CDX` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,002.05 | none | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_GA3BR2_CLA` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,007.33 | 65 / 5.28 MiB; generated caches only | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_GA3BR2_DSV4` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,002.05 | none | 0 | 0 / 15 | HOLD — handles |
| `C:\GAAUD_GA3BR2_GLM` | `7aad0377106c7bb1ebcf79990051806d2e6ce0d7` | 2026-08-02 22:20 +03 | 1,002.05 | none | 0 | 0 / 15 | HOLD — handles |

The nine cache-only/empty candidates total approximately **9,036.00 MiB** (about **8.82 GiB**). This is only a conditional review pool, not an authorized or proven reclaimable amount.

## 5. Ordinary untracked inventory

Every candidate returned zero paths from:

`git ls-files --others --exclude-standard`

This proves no ordinary untracked source, report, patch, manifest, or user file was visible through Git's standard untracked inventory at the audit snapshot.

It does not override the ignored-file findings below.

## 6. Ignored inventory

### Nine cache-only or empty candidates

- `GAAUD_CLAUDE`: 28 `__pycache__` files and 5 `.pytest_cache` files.
- `GAAUD_3BR2_CDX`: 61 `__pycache__` files and 10 `.pytest_cache` files.
- `GAAUD_3BR2_CLA`: 2 `__pycache__` files.
- `GAAUD_3BR2_DS`: no ignored files.
- `GAAUD_3BR2_GLM`: 61 `__pycache__` files and 5 `.pytest_cache` files.
- `GAAUD_GA3BR2_CDX`: no ignored files.
- `GAAUD_GA3BR2_CLA`: 60 `__pycache__` files and 5 `.pytest_cache` files.
- `GAAUD_GA3BR2_DSV4`: no ignored files.
- `GAAUD_GA3BR2_GLM`: no ignored files.

No accessible ignored path in these nine candidates fell outside generated Python/pytest cache categories. They pass the ignored-evidence screen, subject to a fresh recheck immediately before any future removal.

### `C:\GAAUD_CODEX` — independent hard hold

Git returned at least 453 ignored paths totaling 28.73 MiB:

- 60 ordinary `__pycache__` paths outside `Temp/`
- 393 paths beneath ignored `Temp/g5_r2_*` directories

The `Temp/` corpus includes:

- `g5_r2_mutations` — 319 returned paths
- locale/current/parent payload fixtures
- special-node and weird-path fixtures
- tar pinning fixtures
- size-mismatch and `mktemp` failure fixtures
- build/payload scripts and release checksum fixtures

These names align with build-determinism falsification and mutation evidence, so they must not be classified as disposable cache without a dedicated evidence-preservation audit.

Additionally, Git reported permission denied for:

- `.pytest_cache/`
- `Temp/g5_r2_pytest_common_parent/`
- `Temp/g5_r2_pytest_current/`
- `Temp/g5_r2_pytest_full/`
- `Temp/g5_r2_pytest_package_parent/`

Therefore:

1. the ignored inventory is incomplete;
2. the accessible ignored residue may contain unique D026/build evidence;
3. `C:\GAAUD_CODEX` is not a retirement candidate even if later process proof succeeds.

Do not alter permissions, take ownership, delete, or move this residue as part of general cleanup.

## 7. HEAD reachability and unique commits

### `7be1c429...`

Contained by eight durable refs:

- `refs/heads/codex/gate-a-build-determinism`
- `refs/heads/codex/gate-a-disarmed-start-mode`
- `refs/heads/codex/gate-a-integration`
- `refs/heads/integration/bridge-release-20260815`
- corresponding four `refs/remotes/origin/*` refs

Unique commits outside branches/remotes/tags: **0**.

### `7aad0377...`

Contained by eight durable refs:

- `refs/heads/codex/gate-a-3b-shm-validation`
- `refs/heads/codex/gate-a-disarmed-start-mode`
- `refs/heads/codex/gate-a-integration`
- `refs/heads/integration/bridge-release-20260815`
- corresponding four `refs/remotes/origin/*` refs

Unique commits outside branches/remotes/tags: **0**.

Both identities pass reachability and unique-commit proof at the snapshot. Ref state must be rechecked immediately before any future removal.

## 8. Evidence/path references

Tracked records preserve these workstreams and SHAs. Examples include:

- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_TAKEOVER_HANDOFF_2026-08-02.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/CODEX_GATE_A_INTEGRATION_AUDIT_PROMPT_EBADA020_2026-08-03.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_INTEGRATION_AUDIT_ROUND1_EBADA020_2026-08-03.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/GATE_A_INTEGRATION_FLAGSHIP_AUDITS_EBADA020_2026-08-08.md`

The `7aad0377` SHA is explicitly recorded as an accepted integration-chain ancestor. `GAAUD_CODEX` and `GAAUD_CLAUDE` are also named in the old takeover handoff.

For the nine cache-only/empty worktrees, tracked reports plus durable refs are sufficient evidence preservation if a later retirement record states that the historical path has been removed.

For `GAAUD_CODEX`, tracked prose does **not** prove that its ignored mutation/pytest corpus is duplicated elsewhere. Its evidence check fails pending a separate file-level comparison and preservation manifest.

## 9. Current lock relevance

Exact searches found zero candidate-name mentions in `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md`.

Current claimed rows cover RP7-WPI-RO, SEC102/Pathscope, Audit-2 readiness, shared `_AI_MEMORY`, and Bridge Help/System Map. These Batch-2 Gate-A audit paths are outside those named primary homes.

Lock relevance passes at the snapshot, but `SESSION_LOCK.md` must be reread immediately before any future worktree removal.

## 10. Process/open-handle proof — batch-wide blocker

A live `Win32_Process` snapshot found zero candidate-path strings in non-audit process command lines or executable paths.

Full proof remains unavailable:

- Sysinternals `handle.exe` is unavailable.
- `openfiles /query` says the local “maintain objects list” flag is disabled.
- remote-share open-file enumeration returned access denied.
- `Win32_Process` does not expose process current working directories.

Consequently, no candidate can be certified free of open handles or process current-directory use. This fails the mandatory process criterion for all ten candidates.

Do not install tools or enable the global `openfiles` flag as part of this audit; those are separate system changes.

## 11. Final disposition

### `C:\GAAUD_CODEX`

**HOLD — NOT A RETIREMENT CANDIDATE.** Blocking reasons:

1. unpreserved ignored mutation/test corpus;
2. permission-denied directories make inventory incomplete;
3. open-handle/current-directory proof unavailable.

### Remaining nine

**HOLD — CONDITIONALLY PROMISING ONLY.** They pass Git, untracked, ignored-evidence, lock, reachability, unique-commit, and tracked-reference checks, but fail the open-handle/current-directory proof.

### Required future action

At an owner-authorized cleanup window when agents are stopped:

1. recheck current locks and process state;
2. obtain approved open-handle/current-directory proof;
3. rerun tracked/untracked/ignored inventories;
4. rerun ref reachability and unique-commit checks;
5. exclude `GAAUD_CODEX` until its mutation corpus is separately preserved and inaccessible directories are inventoried without changing their content;
6. write an exact retirement record;
7. use `git worktree remove <exact-path>` only, never raw filesystem deletion.

No removal is authorized by this report.
