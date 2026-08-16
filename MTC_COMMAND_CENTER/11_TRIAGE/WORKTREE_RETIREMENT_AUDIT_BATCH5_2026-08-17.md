# Worktree Retirement Audit — Batch 5

**Date:** 2026-08-17

**Mode:** bounded read-only retirement inventory; this report is the only write

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Result:** **10 conditional RETIRE-CANDIDATE; 10 HOLD; remove none**

## 1. Verdict meanings and hard boundary

- **RETIRE-CANDIDATE** means the worktree passed every non-handle check in this snapshot, including preservation review of any untracked residue. It is not removal authorization.
- **HOLD** means unique untracked evidence is not preserved in the current checkout.
- **No Batch-5 worktree may be removed now.** Windows open-handle/current-directory proof remains unavailable for every candidate.

No worktree, branch, ref, file, process, lock, permission, or Git configuration was changed. No file was copied or moved. No worktree was removed. No host was accessed. No commit was created.

## 2. Selection method

Batch 5 selected exactly the next twenty detached, tracked-clean worktrees not covered by Batches 1–4. The audit stopped after those twenty even though later eligible worktrees remain.

Git has no canonical worktree-creation timestamp, so age was ranked by detached HEAD commit date, then by path. The selected range begins at `779bd038...` dated 2026-08-09 08:10 +03 and ends at `93479b0e...` dated 2026-08-15 21:07 +03.

Selection required:

1. an existing registered worktree path;
2. a detached HEAD;
3. empty `git status --porcelain --untracked-files=no` output;
4. no path match in the Batch-1 through Batch-4 result tables.

## 3. Proof checklist

Each selected worktree was checked for:

1. tracked cleanliness;
2. ordinary untracked files, sizes, hashes, and current-checkout duplication;
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

- Candidates audited: **20 exactly**
- Detached and tracked-clean: **20 of 20**
- Git `locked` markers: **0**
- Git `prunable` markers: **0**
- Ordinary untracked paths: **12 across 12 worktrees**
- Proven duplicate untracked paths: **2** in `R7AC` and `R7AX`
- Unique untracked evidence paths: **10**, totaling **230,068 bytes**
- Ignored paths: **59**, all generated Python bytecode in `P10BASE`
- Operational DB/WAL/SHM/log paths: **0 visible across all twenty**
- Permission or recursive-scan errors: **0 across all twenty**
- Exact candidate path/name hits in current `SESSION_LOCK.md`: **0 across all twenty**
- Explicit live process-path hits: **0 across all twenty**
- Unique commits outside branches/remotes/tags: **0 across all twenty**
- Total apparent size: **20,234.135 MiB** (about **19.760 GiB**)
- Conditional 10-tree retirement pool: **10,073.470 MiB** (about **9.837 GiB**)
- Ten-tree HOLD pool: **10,160.665 MiB** (about **9.923 GiB**)

The apparent-size figures are logical file-length sums, not guaranteed physical disk savings. Git common-dir storage, allocation, and shared filesystem blocks can make actual reclaimed space differ.

## 5. Candidate results

| Worktree | HEAD | Commit date | Size MiB | Untracked | Ignored | Durable refs | Unique commits | Lock / process hits | Verdict |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `C:\WP2AC` | `779bd038957a192db47ff7ad68eb51304a2fba46` | 2026-08-09 08:10 +03 | 1,003.230 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2AD` | `779bd038957a192db47ff7ad68eb51304a2fba46` | 2026-08-09 08:10 +03 | 1,003.230 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2AG` | `779bd038957a192db47ff7ad68eb51304a2fba46` | 2026-08-09 08:10 +03 | 1,003.230 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2AUD` | `779bd038957a192db47ff7ad68eb51304a2fba46` | 2026-08-09 08:10 +03 | 1,003.230 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2CL` | `313bc187ed78d6183391629b87c620977a3cedef` | 2026-08-09 10:20 +03 | 1,003.301 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2PKG2` | `2bd4ae8d4a381f328b8a4c4eca09acf3760d7107` | 2026-08-09 11:00 +03 | 1,003.331 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\WP2PKG3` | `3fa33555354e5ab71e17376986520247ac84eb02` | 2026-08-09 11:11 +03 | 1,003.337 | 0 | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — handles unresolved |
| `C:\PSRETRY` | `40091b2b795be3339dc0df7014df6bfc091e4eca` | 2026-08-14 14:39 +03 | 1,015.048 | **1 unique** | 0 | 15 | 0 | 0 / 0 | **HOLD — unique audit evidence** |
| `C:\R7AC` | `d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f` | 2026-08-15 00:39 +03 | 1,015.165 | 1 duplicate | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — duplicate proven, handles unresolved |
| `C:\R7AX` | `d4e90cb05bfbe227d17ce6264f0d3c19d3b5337f` | 2026-08-15 00:39 +03 | 1,015.143 | 1 content duplicate | 0 | 15 | 0 | 0 / 0 | RETIRE-CANDIDATE — newline-only difference, handles unresolved |
| `C:\R7T0CDX` | `4d28debbc69f35d21c022fd314309aa052e3a4aa` | 2026-08-15 10:38 +03 | 1,015.312 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique T0 audit evidence** |
| `C:\R7T0CLA` | `4d28debbc69f35d21c022fd314309aa052e3a4aa` | 2026-08-15 10:38 +03 | 1,015.339 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique T0 audit evidence** |
| `C:\BRDG` | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` | 2026-08-15 20:05 +03 | 1,016.346 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique deployment-readiness evidence** |
| `C:\FRZMAP` | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` | 2026-08-15 20:05 +03 | 1,016.337 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique freeze evidence** |
| `C:\P10BASE` | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` | 2026-08-15 20:05 +03 | 1,020.275 | 0 | 59 cache | 10 | 0 | 0 / 0 | RETIRE-CANDIDATE — caches only, handles unresolved |
| `C:\P11LED` | `ddc8a9c802cc45f66f449b02f18a07448afc5f70` | 2026-08-15 20:05 +03 | 1,016.332 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique ledger evidence** |
| `C:\AUTHCON` | `678d4be22ddde2201948de0d60343c1edfa85a06` | 2026-08-15 20:29 +03 | 1,016.450 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique authority evidence** |
| `C:\RELDES` | `678d4be22ddde2201948de0d60343c1edfa85a06` | 2026-08-15 20:29 +03 | 1,016.449 | **1 unique** | 0 | 10 | 0 | 0 / 0 | **HOLD — unique release-design evidence** |
| `C:\CLAIMCHK` | `93479b0e5923b8288ba47dd0dcc5cf8ebf0e096f` | 2026-08-15 21:07 +03 | 1,016.519 | **1 unique** | 0 | 6 | 0 | 0 / 0 | **HOLD — unique claim-verification evidence** |
| `C:\MRGRUN` | `93479b0e5923b8288ba47dd0dcc5cf8ebf0e096f` | 2026-08-15 21:07 +03 | 1,016.534 | **1 unique** | 0 | 6 | 0 | 0 / 0 | **HOLD — unique merge-runbook evidence** |

## 6. Ordinary untracked evidence

### Unique HOLD files

The following ordinary untracked files are absent from both the current working tree and current tracked index:

| Worktree | Untracked path | Bytes | SHA-256 |
|---|---|---:|---|
| `PSRETRY` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/PATHSCOPE_FINAL_OVERRIDE_RETRY_CODEX_T1_AUDIT_2026-08-15.md` | 16,973 | `74E96E6A154B3103780B61951BBDA00F9B8B17C0C61BBF05FC1C51F99C72910F` |
| `R7T0CDX` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CODEX_T0_AUDIT_2026-08-15.md` | 9,727 | `3A70ECDA92DB20EB7EA4B317D4D06B24554BA3AAD99CA2D96B7DC2D53AB8D1B4` |
| `R7T0CLA` | `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_R1_R4_CLAUDE_T0_AUDIT_2026-08-15.md` | 38,057 | `E480C5DD097FEF883783722FCA0CED60389A35242889058B44C3AC1D6CCE367E` |
| `BRDG` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_VPS_DEPLOY_READINESS_REFRESH_2026-08-15.md` | 22,139 | `1C070782237EA60ADBCDCF4C6DE1CF855F0252E728ADEDFB654E96A83C36EB8C` |
| `FRZMAP` | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_FREEZE_BLOCKER_RECONCILIATION_2026-08-15.md` | 11,829 | `C1BEE0EC41398E776BE3FE054DF33E0BDE0570B7D4A6FB1FFFF2EA33AED10C95` |
| `P11LED` | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/AUDIT2_PACKET11_LEDGER_MEASUREMENT_2026-08-15.md` | 7,024 | `7F4F38F5E6692AB1473E29C6636051A1865840453E8AE1A0DC7CB5B17C971254` |
| `AUTHCON` | `MTC_COMMAND_CENTER/11_TRIAGE/AUDIT2_READINESS_PACKAGE/WPI_FINAL_AUTHORITY_CONSOLIDATION_2026-08-15.md` | 34,465 | `71B06CF1903939DE5071CCB964E22E045E16E13570883080AE585F1D47791451` |
| `RELDES` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_INTEGRATION_DESIGN_2026-08-15.md` | 33,138 | `21C23B4CC539260B474FFD65F4590AB68000AB38D7EB56EE0B96C1B6283F2EC3` |
| `CLAIMCHK` | `MTC_COMMAND_CENTER/11_TRIAGE/NIGHT_CLAIM_VERIFICATION_2026-08-15.md` | 20,214 | `43780F1AB385D6C010D677B719D5861986E6297BBE1587C34A1409CC3C5A0E49` |
| `MRGRUN` | `MTC_COMMAND_CENTER/11_TRIAGE/BRIDGE_RELEASE_MERGE_RUNBOOK_2026-08-15.md` | 36,502 | `7BD33CB21A190E656053AD827672D9CB477A132FEEC82AF7FC783F7C32E7CE13` |

These files are audit, deployment-readiness, freeze reconciliation, ledger, authority, release-design, claim-verification, and merge-runbook records. They are evidence, not generated cache. This audit did not copy, move, edit, stage, or commit them.

### Proven duplicates

`R7AC` contains:

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_CLAUDE_T0_AUDIT_2026-08-13.md`

Its 30,179-byte content and SHA-256 `BA1A16E0661423AC5314A2E2561C86D65DC01D7391602B3A8335E8EE5E24F77F` exactly match the current tracked file at the same path.

`R7AX` contains:

`MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_CODEX_T0_AUDIT_2026-08-13.md`

The worktree copy is 7,041 bytes. The current tracked copy is 7,042 bytes. After normalizing line endings and removing only the final newline, textual content is identical. The sole difference is terminal newline representation.

Those two residue files are therefore preserved in the current tracked checkout. Their worktrees remain non-removable only because handle/CWD proof is missing.

## 7. Ignored and operational residue

Nineteen worktrees returned zero ignored paths.

`P10BASE` contains 59 ignored `.pyc` files totaling 4,141,248 bytes (approximately 3.949 MiB). Every path is under a `__pycache__` directory. One cache resides under `MTC_COMMAND_CENTER/11_TRIAGE/KVM2_PROGRAM/evidence/__pycache__/`, but it is compiled `validate_ledger` bytecode, not an evidence document or runtime log.

No accessible Batch-5 ignored path is a SQLite database, WAL/SHM sidecar, log, report, mutation corpus, virtual environment, or operational evidence artifact. All ignored queries and recursive scans completed without permission errors.

## 8. Live process, lock, and permission checks

A `Win32_Process` snapshot found zero explicit Batch-5 path strings in process command lines or executable paths.

Exact searches of current `MTC_COMMAND_CENTER/_AI_MEMORY/SESSION_LOCK.md` found zero candidate names or paths. No selected Git worktree entry carried a `locked` or `prunable` marker.

Every recursive filesystem scan and ignored-file query completed without permission errors.

These checks are weaker than open-handle/current-directory proof and must be repeated before any later action.

## 9. Reachability and unique commits

Every Batch-5 HEAD is reachable from durable local and remote refs:

| HEAD | Worktrees | Durable refs | Containing-ref summary |
|---|---|---:|---|
| `779bd038...` | four `WP2A*` trees | 15 | current Bridge, Pathscope, RP7, Gemini, integration, and remote descendants |
| `313bc187...` | `WP2CL` | 15 | same later Bridge/integration family |
| `2bd4ae8d...` | `WP2PKG2` | 15 | same later Bridge/integration family |
| `3fa33555...` | `WP2PKG3` | 15 | same later Bridge/integration family |
| `40091b2b...` | `PSRETRY` | 15 | same later Bridge/integration family |
| `d4e90cb0...` | `R7AC`, `R7AX` | 15 | same later Bridge/integration family |
| `4d28debb...` | two RP7 T0 trees | 10 | Bridge-suite, P9, Pathscope, RP7, integration and remotes |
| `ddc8a9c8...` | `BRDG`, `FRZMAP`, `P10BASE`, `P11LED` | 10 | same five local release branches and remotes |
| `678d4be2...` | `AUTHCON`, `RELDES` | 10 | same five local release branches and remotes |
| `93479b0e...` | `CLAIMCHK`, `MRGRUN` | 6 | P9, Pathscope, RP7 and corresponding remotes |

For every HEAD:

`git rev-list <HEAD> --not --branches --remotes --tags --count`

returned **0**. No commit unique to a detached Batch-5 HEAD was found. Ref and unique-commit checks must be repeated immediately before removal because refs can move.

## 10. Tracked evidence references

Tracked records preserve many workstream names and exact SHAs. Examples include:

- `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_AUDIT_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPL_P2_COMMAND_GAP_PROPOSALS_DISPATCH_PACKAGE_ROUND2_AUDIT_2026-08-09.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_BLOCKS_DRAFT/RP7_CAP_OVERRIDE_FINAL_OWNER_BOUNDARY_2026-08-15.md`
- `MTC_COMMAND_CENTER/11_TRIAGE/WPI_PREREG_DRAFT_ROUND1/KICKOFF_CODEX_PATHSCOPE_FINAL_OVERRIDE_AUDIT_2026-08-14.md`

Tracked prose and SHA references do not preserve the ten unique untracked documents listed in Section 6. Their exact absence from the current checkout is the controlling HOLD fact.

## 11. Windows handle/current-directory blocker

Full process-use proof remains unavailable:

- Sysinternals `handle.exe` is not installed or discoverable.
- `openfiles /query` reports that the global “maintain objects list” flag is disabled for local handles.
- `Win32_Process` exposes executable paths and command lines but not each process's current working directory.

Therefore none of the ten conditional candidates is removal-ready. Do not install tools, enable global tracking, restart the machine, stop processes, or alter permissions as part of this audit.

## 12. Final disposition and future proof gate

### HOLD

`PSRETRY`, `R7T0CDX`, `R7T0CLA`, `BRDG`, `FRZMAP`, `P11LED`, `AUTHCON`, `RELDES`, `CLAIMCHK`, and `MRGRUN` each contain a unique untracked evidence document absent from the current checkout. They remain held even if handle proof later becomes available, until a separate owner-authorized preservation decision is completed.

### Conditional RETIRE-CANDIDATE

`WP2AC`, `WP2AD`, `WP2AG`, `WP2AUD`, `WP2CL`, `WP2PKG2`, `WP2PKG3`, `R7AC`, `R7AX`, and `P10BASE` pass tracked state, evidence-preservation, ignored-content, operational-residue, permissions, lock-name, explicit process-path, reachability, and unique-commit checks at this snapshot. They remain **not removal-authorized** because open-handle/current-directory proof is missing.

Before any future removal, at an owner-authorized cleanup window when agents are stopped:

1. reread `SESSION_LOCK.md` and the live worktree registry;
2. reproduce tracked cleanliness and ordinary untracked inventory;
3. reproduce ignored and operational-residue inventories with zero read errors;
4. reproduce containing refs and zero unique commits;
5. obtain approved open-handle and process-current-directory proof;
6. exclude all ten HOLD paths until their unique documents receive explicit preservation decisions;
7. write the exact retirement record and exact path list;
8. use `git worktree remove <exact-path>` only—never raw recursive filesystem deletion.

No removal is authorized by this report.
