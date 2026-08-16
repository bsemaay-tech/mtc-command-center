# Repository Memory and Worktree Hygiene Inventory

**Date:** 2026-08-17 01:04 +03:00  
**Mode:** read-only inventory followed by this documentation-only report  
**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`  
**Authority boundary:** no memory-file edit, move, delete, worktree removal, branch change, reset, stash, host access, or protected-surface change was performed.

## 1. Executive findings

- `_AI_MEMORY` contains 59 files totaling 1,284,114 bytes (about 1.225 MiB).
- Its two live journals alone total 396.5 KiB:
  - `GLOBAL_HANDOFF.md`: 203.0 KiB and 2,828 physical lines.
  - `NEXT_STEPS.md`: 193.5 KiB and 2,729 physical lines.
- A lossless date rotation can reduce both live journals by about 92%, removing about 366 KiB from routine live reads. At a rough four bytes per token, this is approximately 90,000 tokens avoided when both complete files would otherwise be loaded.
- Git registers 155 worktrees: 66 branch-attached and 89 detached.
- The registered worktrees have a combined apparent size of 160.15 GiB; the median is 1,003.2 MiB per worktree.
- Of those worktrees, 137 have no tracked changes and 18 have tracked changes. Eighty-eight are both tracked-clean and detached, but they are **not yet proven safe to remove**.
- The main worktree contains 183 untracked files totaling 114.54 MiB. Of these, 130 `.log` files account for 112.50 MiB.
- `.git/worktrees` metadata alone contains 983 files totaling about 181.5 MiB.
- `git worktree prune --dry-run --verbose` found no automatically prunable entry: all 155 registered paths currently exist.

These are two different problems:

1. The live memory journals are the dominant repeated-context and token-cost problem.
2. The worktree population is the dominant disk-cost problem.

## 2. Immediately safe, non-destructive compaction and rotation plan

“Safe” here means preserve content verbatim, maintain an index, validate reconstruction, and obtain the normal documentation review. It does **not** mean edits should race the current `_AI_MEMORY` owner.

### P0 — Rotate `GLOBAL_HANDOFF.md` verbatim

Measured split:

| Portion | Lines | Size |
|---|---:|---:|
| Current live head, lines 1–245 | 245 | 15.8 KiB |
| Historical tail, lines 246–2,828 | 2,583 | 187.2 KiB |
| Total | 2,828 | 203.0 KiB |

The first historical heading begins at line 246 (`2026-08-15`). The current live head covers the 2026-08-16/17 state.

Proposed archive path:

`MTC_COMMAND_CENTER/_AI_MEMORY/archive/GLOBAL_HANDOFF_2026-08-01_to_2026-08-15.md`

Required safeguards:

1. Copy the historical tail verbatim; do not summarize it.
2. Add only an archive header outside the preserved payload.
3. Add a live-file pointer to the archive.
4. Verify that the preserved live payload plus archived payload reconstructs the old file byte-for-byte after normalizing only the deliberate archive header boundary.
5. Update `START_HERE.md` rotation note.

Expected live-file reduction: 92.2%.

### P0 — Rotate `NEXT_STEPS.md` verbatim

Measured split:

| Portion | Lines | Size |
|---|---:|---:|
| Current live head, lines 1–230 | 230 | 14.7 KiB |
| Historical tail, lines 231–2,729 | 2,499 | 178.8 KiB |
| Total | 2,729 | 193.5 KiB |

Line 231 begins the older 2026-08-10 continuation history. The live head covers the current owner roadmap and 2026-08-16/17 work.

Proposed archive path:

`MTC_COMMAND_CENTER/_AI_MEMORY/archive/NEXT_STEPS_2026-08-01_to_2026-08-10.md`

This rotation also removes misleading superseded duplicates from the active view. For example, the newest Help/Wiki section is `BLOCKED` at line 73 while an older section still says `READY` at line 117. Newest-first ordering makes this technically interpretable, but it is unnecessarily expensive and error-prone for an incoming agent.

Expected live-file reduction: 92.4%.

### P0 — Correct stale `START_HERE.md` banner

`MTC_COMMAND_CENTER/_AI_MEMORY/START_HERE.md` lines 3–9 still announce the 2026-08-12/13 WP-I run as live, refer to an expired 23:00 provider-window milestone, and describe time-specific quota conditions.

Keep `START_HERE.md` canonical. Replace only the stale banner with a neutral current-state pointer to the newest `GLOBAL_HANDOFF.md` and `NEXT_STEPS.md`. Preserve the old banner in the dated archive rather than discarding it.

### P1 — Retire stale `ACTIVE_FILES.md` as a live source

`MTC_COMMAND_CENTER/_AI_MEMORY/ACTIVE_FILES.md` is 65.2 KiB and contains more than 70 dated “active” sections reaching from June through 2026-08-01. It has not been updated since 2026-08-01 and is now a historical journal, not a dependable live-file inventory.

Proposed no-loss action:

1. Archive the full file verbatim as `_AI_MEMORY/archive/ACTIVE_FILES_through_2026-08-01.md`.
2. Replace it with a small generated/current index or a retirement pointer.
3. Never use its old host, branch, worktree, or blocker state as current truth without live verification.

### P1 — Rotate `SESSION_LOCK.md` history only after current agents stop

Measured split:

| Portion | Lines | Size |
|---|---:|---:|
| Rules and current lock table, lines 1–46 | 46 | 3.5 KiB |
| Historical claim/release log, lines 47–228 | 182 | 11.9 KiB |
| Total | 228 | 15.4 KiB |

Archive the historical claim/release tail verbatim and retain the compact rules/current table. This must be an atomic, serialized change after the current memory owner finishes.

### P2 — Historical cohort, lower token priority

Tracked `_AI_MEMORY` categories:

| Category | Files | Size |
|---|---:|---:|
| Already archived | 3 | 470.6 KiB |
| Live journals | 2 | 396.5 KiB |
| Historical candidates | 14 | 150.6 KiB |
| Canonical/standing | 16 | 145.0 KiB |
| June parallel prompts/reports | 14 | 78.6 KiB |
| June result notes | 9 | 13.2 KiB |

Lower-priority historical candidates include:

- `MCC_COMPLETION_MASTER_PLAN.md` — 23.0 KiB
- `CODEX_PICKUP_2026-06-08.md` — 9.2 KiB; `START_HERE.md` already calls it historical
- `MCC_READINESS_REPORT.md` — 8.2 KiB
- `N5_CODABILITY_AUDIT.md` — 7.9 KiB
- `HANDOFF_PROMPT_SP004_PHASE3.md` — 7.7 KiB
- `A3_GAP_MATRIX.md` — 7.0 KiB
- `PIPELINE_STATE.md` — 4.0 KiB
- `NIGHT_BATCHES.md` — 4.0 KiB
- June `PARALLEL_AGENT_PROMPTS/`, `PARALLEL_AGENT_REPORTS/`, and `RESULT_*` notes

Do not move this cohort blindly. Several names are referenced by older handoffs and by `WPL_P2_STAGING.../CANDIDATE_RELEASE_SHA256SUMS`. Before any move, create an archive index containing old path, new path, SHA-256, references, and preservation reason. Any deployed-artifact identity or manifest impact requires the policy-defined focused identity verification.

## 3. Canonical memory that must not be summarized away

Keep these canonical or immutable:

- `DECISIONS.md` — 28.4 KiB but only 35 very long decision records. It may later be split by decision range with an index, but decision IDs and exact wording must remain intact.
- `AI_RULES.md`
- `DO_NOT_TOUCH.md`
- `LIVE_TRADING_GATE.md`
- `PROJECT_MEMORY.md`
- `LESSONS.md`
- `AI_ACCOUNT_AND_MODEL_ROUTING.md`
- `START_HERE.md` itself
- `REPO_MAP.md`
- `TOOL_OUTPUT_OFFLOAD_PROTOCOL.md`
- strategy workflow, library, and checklist files
- the existing `_AI_MEMORY/archive/` content
- the small retired `SESSION_LOG.md` pointer

## 4. Current `SESSION_LOCK.md` ownership affecting memory

At the inventory snapshot, the live shared-memory surface was explicitly owned:

- Shared memory layer (`_AI_MEMORY` handoffs, rules, routing): **Codex Lead `01a00921`**, owner-authorized overnight program and handoff.
- Bridge Help/System Map: **Codex Lead `01a00921`**.
- RP7-WPI-RO block: **Codex Lead `019fe77c`**.
- §10.2 prover / SEC102: **Codex Lead `019fe77c`**.
- Audit-2 readiness package: **Codex Lead `019fe77c`**.

Therefore, the journal/lock rotations above are non-destructive plans, but they must be performed by or handed off from the current shared-memory owner. No other agent should edit `_AI_MEMORY` concurrently.

## 5. Untracked/generated backlog

Main-worktree snapshot:

- 183 untracked files
- 114.54 MiB total
- 130 `.log` files totaling 112.50 MiB
- file dates range from 2026-08-09 through 2026-08-13
- 6 zero-byte files
- 41 files smaller than 1 KiB
- 93 files smaller than 10 KiB

Logical groups:

| Group | Files | Size | Classification |
|---|---:|---:|---|
| `11_TRIAGE` top-level run logs | 56 | 69.65 MiB | Raw model/tool run transcripts; likely generated, but may contain cited audit evidence |
| `WPI_PREREG_DRAFT_ROUND1` run outputs | 32 | 26.58 MiB | Audit/prereg run transcripts; evidence review required |
| `WPI_BLOCKS_DRAFT` run outputs | 44 | 16.28 MiB | Build/audit run transcripts; evidence review required |
| `WPI_BLOCKS_DRAFT/.r16scratch` | 36 | 1.83 MiB | Scratch plus mutation/RED-GREEN candidates; do not discard by name alone |
| `WPI_BLOCKS_DRAFT/.r13scratch` | 11 | 0.13 MiB | Scratch plus possible closure evidence |
| root `tmprepo_map_inventory.md` | 1 | 0.06 MiB | Obvious generated inventory candidate; verify references first |
| WPL staging evidence logs | 3 | 0.01 MiB | Contract/host evidence; strongest do-not-touch classification |

Largest examples:

- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/SEC102_R2_CODEX_RUN_2026-08-11.log` — 14.07 MiB
- `MTC_COMMAND_CENTER/11_TRIAGE/RP6_R18_REPAIR_CODEX_RUN_2026-08-12.log` — 7.33 MiB
- `MTC_COMMAND_CENTER/11_TRIAGE/RULE2_SWEEP_CODEX_RUN_2026-08-12.log` — 5.16 MiB
- `MTC_COMMAND_CENTER/11_TRIAGE/RP7_ROWS_1_9_BUILD_CODEXFREE_RUN_2026-08-13.log` — 5.15 MiB
- `MTC_COMMAND_CENTER/11_TRIAGE/GITATTR_DURABILITY_CODEX_RUN_2026-08-12.log` — 4.07 MiB

No-loss disposition plan:

1. Determine which raw logs are cited as acceptance evidence, D026 RED/GREEN evidence, or host evidence.
2. Preserve cited evidence with a SHA-256 manifest and a pointer from its canonical verdict/report.
3. Compress or externally archive uncited raw model transcripts outside the active repository surface.
4. Keep concise verdict and evidence records in Git; do not commit 112.5 MiB of raw logs by default.
5. Add narrowly scoped ignore rules for future `*_RUN_*.log` files and designated run/scratch directories. Do not blanket-ignore `*.log`, because some logs are contractual evidence.
6. Keep all three WPL staging evidence logs until a contract/evidence review explicitly releases them.
7. Treat `.r13scratch` and `.r16scratch` as potentially valuable mutation evidence. Preserve any referenced `.sh`, `.out`, `.err`, `.rc`, or prose fixture.

## 6. Worktree and Git storage inventory

### Counts and sizes

- Registered worktrees: 155
- Branch-attached: 66
- Detached: 89
- Tracked-clean: 137
- Tracked-dirty: 18
- Tracked-clean and detached: 88
- Existing paths: 155 of 155
- Dry-run prune candidates: 0
- Combined apparent worktree size: 160.15 GiB
- Median apparent size: 1,003.2 MiB
- Local branches: 103
- Branches reported merged into the then-current HEAD: 46
- Git loose objects: 18,815 objects, 218.76 MiB
- Packed objects: 20,997 objects in two packs, 121.30 MiB
- Git garbage: 0 bytes
- `.git/worktrees` metadata: 983 files, about 181.5 MiB

Largest measured worktrees:

| Apparent size | Files | Path |
|---:|---:|---|
| 8.66 GiB | 87,198 | `C:/LAB/Tradingview_LAB_CLEAN` |
| 1.08 GiB | 9,297 | `C:/LAB/MTC_AIONUI_PILOT` |
| 1.03 GiB | 7,208 | `C:/TSP1004A2` |
| 1.01 GiB | 7,695 | `C:/GAAUD_CODEX` |
| 1.00 GiB | 8,074 | `C:/BRIDGE_RELEASE_INTEGRATION_20260815` |
| 1.00 GiB | 8,068 | `C:/AUD62A` |
| 1.00 GiB | 8,068 | `C:/AUD62B` |
| 1.00 GiB | 8,063 | `C:/P10FIX` |
| 1.00 GiB | 8,151 | `C:/R7FINAL` |
| 1.00 GiB | 8,060 | `C:/BRIDGE_HELP_IMPL` |

The 88 tracked-clean detached worktrees are the first review pool. At the measured median they represent roughly 86 GiB, but **this is not a reclaimable-space claim** until the proof checklist below succeeds for each path.

## 7. Mandatory proof checklist before retiring any worktree

Worktree removal is destructive cleanup and is separate from the safe memory rotations above. For every candidate, record all of the following:

1. **Exact identity:** path, full HEAD SHA, detached/branch state, branch name, upstream, and candidate purpose.
2. **Tracked cleanliness:** `git status --porcelain --untracked-files=no` is empty.
3. **Untracked inventory:** enumerate all untracked and ignored-but-local files; prove there is no unique report, patch, test evidence, key-free configuration, or user file.
4. **Active process check:** prove no shell, editor, test process, server, auditor, Claude/Codex/Gemini process, or watcher has that path as working directory or open target.
5. **Lock check:** map the path and workstream against the current `SESSION_LOCK.md`; owner must release the row before retirement.
6. **Ref reachability:** prove HEAD is reachable from a permanent branch, tag, accepted integration commit, or explicit archive ref.
7. **Unique-commit check:** enumerate commits reachable from the worktree HEAD but not from the accepted integration/master refs. Preserve them before removal.
8. **Dirty patch check:** even when tracked status is clean, verify no submodule, nested repository, alternate index, or linked worktree metadata carries unique state.
9. **Evidence-reference check:** search handoffs, decisions, manifests, acceptance records, and audit reports for the worktree path and HEAD SHA.
10. **Artifact identity check:** verify removal does not destroy the only local copy of a candidate release, manifest, test corpus, D026 RED/GREEN fixture, or host evidence.
11. **Preservation step:** before removing a detached worktree, create a durable archival ref/tag or Git bundle and record its hash/location. A bare SHA in prose is insufficient if the commit may become unreachable.
12. **Removal method:** use `git worktree remove <exact-path>` from the owning repository. Never delete the directory with `Remove-Item`, Explorer, `rm`, or another shell.
13. **Branch cleanup separation:** branch deletion is a later, separate reviewed action. Do not combine it silently with worktree removal.
14. **Post-removal verification:** rerun `git worktree list`, `git fsck`, branch/ref reachability, active lock checks, and disk measurement.

Only a candidate satisfying every item is eligible for retirement.

## 8. Tracked-dirty worktrees — do not touch

The inventory found tracked changes in these 18 worktrees:

- `C:/KVM2P03` — 52 tracked status rows
- `C:/TSP1004` — 13
- `C:/TSP1004A2` — 13
- `C:/TSP1004A4` — 11
- `C:/TSP1003A5` — 9
- `C:/TSP1003A3` — 8
- `C:/TSP1003A4` — 7
- `C:/TSP1003A1` — 7
- `C:/BRIDGE_HELP_IMPL` — 4
- `C:/tmp/postgate_runkit_design_claude` — 4
- `C:/TSP1003A2` — 3
- `C:/TSP1002A3` — 3
- `C:/TSP1002A2` — 3
- `C:/TSP1002A4` — 3
- `C:/TSP1002` — 1
- `C:/KVM2GLM` — 1
- `C:/CDXFAILOVER` — 1
- `C:/LAB/Tradingview_LAB_CLEAN` — 1

The current main-worktree modification is:

`IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`

It is foreign, active work and must not be overwritten, staged, reset, moved, or included in hygiene commits.

## 9. Explicit do-not-touch list

Until separately reviewed and released:

- all 18 tracked-dirty worktrees above
- every worktree associated with the active RP7, SEC102/Pathscope, Audit-2, shared-memory, or Help locks
- `C:/BRIDGE_HELP_IMPL`
- `IBKR_PAPER_BRIDGE/docs/30_V2_BACKEND_AND_DASHBOARD_DESIGN_DECISIONS.md`
- WPL staging evidence logs
- D026 RED/GREEN and mutation fixtures, even under a directory named `scratch`
- current `DECISIONS.md`, `AI_RULES.md`, `DO_NOT_TOUCH.md`, `LIVE_TRADING_GATE.md`, and existing archives
- any Pine, `MTC_V2`, parity, schema, deployment, credential, broker/exchange, ARM, TESTNET, mainnet, or host evidence surface
- any worktree directory through raw filesystem deletion

## 10. Recommended execution sequence

1. Current shared-memory owner performs the verbatim `GLOBAL_HANDOFF.md` and `NEXT_STEPS.md` rotation.
2. Correct the stale `START_HERE.md` banner and verify archive navigation.
3. Archive/replace stale `ACTIVE_FILES.md`.
4. Rotate `SESSION_LOCK.md` history only after concurrent owners have stopped.
5. Build a SHA/reference manifest for the 114.54 MiB untracked backlog; compress/archive only evidence-cleared logs.
6. Add narrow future-output ignore patterns in a separate reviewed hygiene change.
7. Build the per-worktree proof manifest for all 155 worktrees.
8. Review the 88 tracked-clean detached candidates first, but remove none until every proof item passes.
9. Perform worktree removal and branch cleanup as separately logged destructive operations.

This sequence preserves all knowledge while attacking the largest recurring token cost first and the largest disk cost second.
