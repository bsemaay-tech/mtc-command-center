# Worktree Non-Retirement Classification

**Date:** 2026-08-17

**Mode:** read-only classification of every registered worktree outside the completed detached tracked-clean review pool

**Repository:** `C:\LAB\Tradingview_LAB_CLEAN`

**Result:** **155 registered paths reconciled; 88 detached tracked-clean review-pool paths already audited; 67 non-retirement paths classified; zero missing or duplicate paths**

## 1. Boundary and terminology

This is classification only. It assigns **no retirement verdict** to branch-attached, dirty, current, active, or unavailable worktrees.

No worktree, branch, ref, file, process, lock, permission, Git configuration, AI-memory file, `docs/30`, or earlier report was changed. No file was copied, moved, staged, stashed, reset, checked out, or committed.

“Tracked-clean” means Git reported no tracked modifications using `git status --porcelain --untracked-files=no`. It does **not** mean that ordinary untracked or ignored content is absent.

The 88-tree detached review pool in Retirement Batches 1–6 was selected using that tracked-only definition. Within it, 72 worktrees had no ordinary untracked paths and 16 had ordinary untracked content. Batches 1–6 separately inventoried ordinary untracked and ignored content; unique evidence, operational residue, permission uncertainty, active use, and lock ambiguity produced HOLD classifications where applicable.

“Branch-attached fully clean” means both no tracked modifications and no ordinary untracked paths. The 18 branch-attached dirty paths comprise 16 with tracked modifications and 2 with ordinary untracked content only (`GEMINI` and `MTC_AIONUI_PILOT`). The sole detached tracked-dirty path has tracked modifications.

Ignored files do not make a Git worktree dirty. Ignored content was inventoried for every dirty/current tree because it can contain operational evidence. It was not exhaustively expanded for the 47 branch-attached fully clean trees because this report does not evaluate them for retirement.

## 2. Full registry reconciliation

| Category | Count |
|---|---:|
| Detached tracked-clean review pool, already covered by Retirement Batches 1–6 | 88 |
| Branch-attached fully clean | 47 |
| Branch-attached dirty (16 tracked-dirty + 2 ordinary-untracked-only) | 18 |
| Detached tracked-dirty | 1 |
| Main/current checkout | 1 |
| Missing/unavailable | 0 |
| **Total registered** | **155** |

Set reconciliation found:

- unique registered paths: **155**;
- unique classified paths: **155**;
- paths missing from classification: **0**;
- duplicate classification paths: **0**.

The 67 paths in this report are exactly `47 + 18 + 1 + 1`.

## 3. Branch-attached fully clean — 47

These paths have a named local branch, no tracked modifications, and no ordinary untracked paths. Branch attachment is the controlling classification; no retirement conclusion is implied.

| Worktree | Branch | HEAD |
|---|---|---|
| `C:\BRIDGE_RELEASE_INTEGRATION_20260815` | `integration/bridge-release-20260815` | `be007fd8` |
| `C:\GA3BR2` | `codex/gate-a-3b-shm-validation` | `20de117f` |
| `C:\GA5E` | `codex/gatea-a5-readiness-e` | `7453ea7f` |
| `C:\GA5F` | `codex/gatea-a5-fail-checkpoint` | `c11d43c3` |
| `C:\GADISARM` | `codex/gate-a-disarmed-start-mode` | `2ce41e34` |
| `C:\GADTR` | `codex/gatea-d-transfer-checkpoint` | `470805c7` |
| `C:\GAREPORT` | `codex/gate-a-overnight-report` | `b5a48e6f` |
| `C:\GARESIDUAL` | `codex/gate-a-residual-evidence-tests` | `3121e7c7` |
| `C:\GATEA_A6_PASS_CLAUDE` | `codex/gatea-a6-pass-checkpoint` | `d42f16fd` |
| `C:\GATEA_A6_PREFLIGHT_GLM` | `codex/gatea-a6-preflight-checkpoint` | `e180c311` |
| `C:\GATEA_A7_PASS_CLAUDE` | `codex/gatea-a7-pass-checkpoint` | `c9d9d73f` |
| `C:\GATEA_A7_PREFLIGHT_GLM` | `codex/gatea-a7-preflight-checkpoint` | `ba302a1a` |
| `C:\GATEA_A8_PASS_CLAUDE` | `codex/gatea-a8-pass-checkpoint` | `9d7e20bc` |
| `C:\GATEA_A8_PREFLIGHT_GLM` | `codex/gatea-a8-preflight-checkpoint` | `2ae53735` |
| `C:\GATEA_A9_PASS_CLAUDE` | `codex/gatea-a9-pass-final-checkpoint` | `be15cba0` |
| `C:\GATEA_A9_PREFLIGHT_GLM` | `codex/gatea-a9-preflight-checkpoint` | `e993e1c6` |
| `C:\GATEA_HOUR_LEDGER_DS` | `codex/gatea-hour-ledger-checkpoint` | `d1da8191` |
| `C:\GATEA_POST_GATE_INVENTORY_GLM` | `codex/gatea-post-gate-inventory-checkpoint` | `5a291f62` |
| `C:\GATEA_POST_GATE_ROADMAP_CLAUDE` | `codex/gatea-post-gate-roadmap-checkpoint` | `35c03827` |
| `C:\GATEA4` | `codex/gate-a-credential-free-disarmed` | `a0275b5c` |
| `C:\GATEAFIX` | `codex/gate-a-build-determinism` | `0bdf8cf4` |
| `C:\GATEAINTEGRATION` | `codex/gate-a-integration` | `ebada020` |
| `C:\K2VPS` | `codex/kvm2-vps-bridge-readiness` | `6fe0130f` |
| `C:\LAB\MTC_HANDOFF_UI` | `codex/handoff-dashboard-prototype` | `d08a7078` |
| `C:\LAB\MTC_MODULAR` | `codex/modular-monorepo` | `d08a7078` |
| `C:\LAB\TIERPOL` | `feature/two-tier-policy` | `ef185d13` |
| `C:\LAB\worktrees\gatea-a5a9-prereg-d` | `codex/gatea-a5a9-prereg-d` | `8f4cd9c0` |
| `C:\P10FIX` | `codex/bridge-suite-anomaly-repairs-20260815` | `7d4e9a96` |
| `C:\P1IF` | `feature/interim-daily-loss-wiring` | `acb83b5b` |
| `C:\P9IMP` | `codex/p9-15-producer-20260816` | `08a8ac70` |
| `C:\PSC` | `codex/pathscope-accounting-redesign-20260815` | `e2102f46` |
| `C:\R7FINAL` | `codex/rp7-r1-r4-repair-20260815` | `6eb0698a` |
| `C:\tmp\glm-gatea-a3-postcheck-wt` | `codex/gatea-a3-postcheck` | `e234833e` |
| `C:\tmp\glm-gatea-a4-pass-wt` | `codex/gatea-a4-pass` | `3ced3b2c` |
| `C:\tmp\glm-gatea-checkpoint-a3-wt` | `codex/gatea-a3-checkpoint` | `237e80bd` |
| `C:\tmp\glm-gatea-runkit-c-wt` | `codex/gatea-runkit-c` | `4c3e78b5` |
| `C:\TSP0` | `feature/ts-p0-baseline` | `cfb08b81` |
| `C:\TSP1001` | `feature/ts-p1-001-order-state` | `8edf81ca` |
| `C:\TSP1002A5` | `feature/ts-p1-002-durable-identity-a5` | `eba350ce` |
| `C:\TSP1002A6` | `feature/ts-p1-002-durable-identity-a6` | `fbd63474` |
| `C:\TSP1003A6` | `feature/ts-p1-003-unknown-submission-a6` | `677c3a29` |
| `C:\TSP1004A3` | `feature/ts-p1-004-partial-fill-protection-a3` | `65eaedb0` |
| `C:\TSP1004A5` | `feature/ts-p1-004-partial-fill-protection-a5` | `7f72f71c` |
| `C:\TSP1009` | `feature/ts-p1-009-kill-evidence-recovery` | `f5438c5b` |
| `C:\TSP1009B` | `feature/ts-p1-009b-evidence-epoch` | `678e8b94` |
| `C:\WPL` | `codex/50h-wpl-verification` | `d9d38d9b` |
| `C:\WPS` | `feature/ts-p1-009b-s2-closure` | `16cbc717` |

Current `SESSION_LOCK.md` claims RP7 and Pathscope workstreams. Consequently `R7FINAL` and `PSC` remain operationally relevant despite tracked cleanliness. This report does not infer that any other clean branch is stale or disposable.

## 4. Branch-attached dirty — 18 (16 tracked-dirty + 2 ordinary-untracked-only)

All eighteen have a named local branch and either tracked modifications or ordinary untracked content. “Unique” below means commits reachable from HEAD but from no other branch, remote, or tag after excluding the worktree's own branch. Uncommitted changes are not included in that number.

| Worktree | Branch | Tracked | Untracked | Ignored | Containing refs | Unique | Classification note |
|---|---|---:|---:|---:|---:|---:|---|
| `C:\BRIDGE_HELP_IMPL` | `codex/bridge-help-wiki-impl` | 4 | 2 | 69 | 2 | 0 | Active Help lock; UI/tests plus Help assets |
| `C:\CDXFAILOVER` | `codex/codex-account-failover` | 1 | 0 | 0 | 40 | 0 | Dispatch helper modification |
| `C:\GEMINI` | `codex/gemini-coder` | 0 | 1 | 0 | 1 | 4 | Unique branch commits plus one dashboard/wiki draft |
| `C:\KVM2GLM` | `codex/kvm2-cycle4-glm` | 1 | 9 | 0 | 82 | 0 | Dirty AI memory plus nine KVM2 planning/audit docs |
| `C:\KVM2P03` | `codex/kvm2-p0-p3-readiness` | 52 | 0 | 69 | 84 | 0 | Broad deployment/readiness evidence package |
| `C:\LAB\MTC_AIONUI_PILOT` | `pilot/aionui-evaluation-2026-08-01` | 0 | 206 | 2,231 | 1 | 2 | **Active process; live DB/WAL/locks/data** |
| `C:\TSP1002` | `feature/ts-p1-002-durable-identity` | 1 | 12 | 3 | 102 | 0 | Store change plus assembly/test tooling |
| `C:\TSP1002A2` | `feature/ts-p1-002-durable-identity-a2` | 3 | 2 | 51 | 102 | 0 | Engine/orders/store changes plus test/doc residue |
| `C:\TSP1002A3` | `feature/ts-p1-002-durable-identity-a3` | 3 | 2 | 51 | 102 | 0 | Engine/orders/store changes plus test/doc residue |
| `C:\TSP1002A4` | `feature/ts-p1-002-durable-identity-a4` | 3 | 2 | 51 | 102 | 0 | Engine/orders/store changes plus test/doc residue |
| `C:\TSP1003A1` | `feature/ts-p1-003-unknown-submission-a1` | 7 | 1 | 64 | 96 | 0 | Broker/engine/store and identity-test changes |
| `C:\TSP1003A2` | `feature/ts-p1-003-unknown-submission-a2` | 3 | 0 | 34 | 96 | 0 | Engine/orders/store changes |
| `C:\TSP1003A3` | `feature/ts-p1-003-unknown-submission-a3` | 8 | 2 | 64 | 96 | 0 | Broker/engine/store and tests |
| `C:\TSP1003A4` | `feature/ts-p1-003-unknown-submission-a4` | 7 | 2 | 69 | 96 | 0 | Broker/engine/store and tests |
| `C:\TSP1003A5` | `feature/ts-p1-003-unknown-submission-a5` | 9 | 2 | at least 56 | 96 | 0 | Two unreadable pytest-cache directories |
| `C:\TSP1004` | `feature/ts-p1-004-partial-fill-protection` | 13 | 2 | 67 | 90 | 0 | Broker/order/store/docs/tests protected surface |
| `C:\TSP1004A2` | `feature/ts-p1-004-partial-fill-protection-a2` | 13 | 242 | at least 59 | 90 | 0 | 240 untracked test DBs; two unreadable cache dirs |
| `C:\TSP1004A4` | `feature/ts-p1-004-partial-fill-protection-a4` | 11 | 0 | 0 | 87 | 0 | Broker/order/store/docs/tests protected surface |

### Tracked-change inventory by surface

- `BRIDGE_HELP_IMPL`: `app.css`, `app.js`, `index.html`, and `test_dashboard_static.py`; untracked `help_map.json` and Help index documentation. Current `SESSION_LOCK.md` explicitly preserves this worktree under the claimed Bridge Help/System Map row.
- `CDXFAILOVER`: `MTC_COMMAND_CENTER/tools/resilient_dispatch.sh`.
- `GEMINI`: no tracked change; one 19,835-byte untracked Dashboard V2 visual Help/Wiki content-spec draft. Its branch has four commits not found in other refs. The Gemini lock row is currently UNCLAIMED, but the content remains uncommitted.
- `KVM2GLM`: `_AI_MEMORY/DECISIONS.md` plus nine untracked KVM2 master-plan, task, classification, and audit documents totaling 151,268 bytes. The shared-memory row is currently claimed elsewhere, so this is a write-surface collision.
- `KVM2P03`: 52 tracked paths comprising 12 `IBKR_PAPER_BRIDGE/deploy/linux` files, 32 triage/readiness records, 3 AI-memory files, one test, `.gitattributes`, and three other package/support paths. This includes host-touching deployment surfaces and is not cleanup material.
- `MTC_AIONUI_PILOT`: no tracked change; 206 ordinary untracked paths totaling 94,462,316 bytes, including `aionui-backend.db`, WAL/SHM, lock files, built-in skills, configuration/data, and one log. Its branch has two commits not present in other refs.
- `TSP1002`: `bridge/store/db.py`; 12 untracked assembly/transform/test helper artifacts including `test_order_identity.py` and database-assembly tools.
- `TSP1002A2/A3/A4`: `engine.py`, `orders.py`, and `store/db.py`; each also has one untracked document and one untracked code/test file.
- `TSP1003A1`: six broker/engine/store files plus `test_order_identity.py`.
- `TSP1003A2`: `engine.py`, `orders.py`, and `store/db.py`.
- `TSP1003A3`: six broker/engine/store files plus two tests.
- `TSP1003A4`: five broker/engine/store files plus two tests.
- `TSP1003A5`: six broker/engine/store files plus three tests.
- `TSP1004` and `TSP1004A2`: seven broker/engine/store files, one order-state contract, and five tests; each also has an untracked partial-fill contract and test.
- `TSP1004A4`: five broker/order/store files, two contracts, and four tests.

The TSP worktrees modify protected Bridge order, broker, persistence, and safety behavior. This report inventories paths only and does not inspect or evaluate trading logic.

## 5. Detached tracked-dirty — 1

| Worktree | HEAD | Tracked | Untracked | Ignored | Containing refs | Unique outside refs | Classification |
|---|---|---:|---:|---:|---:|---:|---|
| `C:\tmp\postgate_runkit_design_claude` | `851d2aa5` | 4 | 1 | 0 | 17 | 0 | Detached tracked-dirty evidence worktree |

Tracked modifications affect:

- `MTC_COMMAND_CENTER/11_TRIAGE/NEXT_SESSION_HANDOFF_2026-08-08.md`;
- `MTC_COMMAND_CENTER/11_TRIAGE/WP0_SCOPE_BASELINE_RECORD_2026-07-31.md`;
- `_AI_MEMORY/GLOBAL_HANDOFF.md`;
- `_AI_MEMORY/NEXT_STEPS.md`.

It also contains one 69,923-byte ordinary untracked file: `MTC_COMMAND_CENTER/11_TRIAGE/POST_GATE_WPL_WPI_RUN_KIT_DESIGN_2026-08-09.md`.

The detached HEAD has zero commits outside durable refs, but the dirty and untracked evidence is not represented by that commit. The shared-memory paths also overlap the currently claimed memory workstream.

## 6. Main/current checkout — 1

`C:\LAB\Tradingview_LAB_CLEAN` is the current working checkout on `codex/bridge-help-wiki`.

At the detailed snapshot:

- tracked modifications: **4** — `docs/30`, `GLOBAL_HANDOFF.md`, `NEXT_STEPS.md`, and `START_HERE.md`;
- ordinary untracked paths: **196**, totaling approximately 120.64 MB;
- untracked classification: 130 logs, 28 Markdown files, 17 code/config files, plus scratch and other evidence;
- ignored paths: **58,860**, totaling approximately 7.49 GB;
- ignored operational indicators: at least 47 DB/WAL/SHM-class paths, 112 log paths, 21 `Temp` paths, 5,686 Python-cache paths, and 42 pytest-cache paths;
- branch commits not contained by another branch/remote/tag: **25** at the snapshot;
- explicit process references: **2**.

The active processes were:

- `powershell.exe` running `MTC_COMMAND_CENTER/08_DASHBOARD_APP/run_dashboard_server.ps1` from this checkout;
- the Codex desktop Node runtime with this checkout as its working directory.

The shared AI-memory paths are currently claimed by the overnight Lead. This checkout is active, concurrent, operational, and categorically outside cleanup mutation.

No contents of logs, databases, credentials, or large evidence files were read.

## 7. Ignored and operational evidence in dirty trees

Across the 20 dirty/current trees:

- tracked status entries: **147**;
- ordinary untracked paths: **684**;
- ignored paths returned: **61,798**, before inaccessible-directory uncertainty.

High-impact operational residue:

- main/current: large ignored corpus with DB/WAL/log/Temp indicators and 130 ordinary untracked logs;
- `MTC_AIONUI_PILOT`: live database, WAL/SHM, lock files, process data, built-in skills, and active dashboard server;
- `TSP1004A2`: 240 ordinary untracked test databases totaling most of its 56,033,578 untracked bytes;
- `KVM2P03`: deployment and release-readiness changes on host-touching surfaces;
- `BRIDGE_HELP_IMPL`: active uncommitted Help implementation.

Inventory completeness exceptions:

- `TSP1003A5`: permission denied for root `.pytest_cache/` and `IBKR_PAPER_BRIDGE/.pytest_cache/`;
- `TSP1004A2`: the same two permission-denied cache directories.

Their ignored counts are lower bounds. No permission, ownership, or ACL was changed.

## 8. Explicitly active, locked, and process-referenced overlays

### Process-referenced

| Worktree | Process evidence |
|---|---|
| `C:\LAB\Tradingview_LAB_CLEAN` | dashboard-server PowerShell plus Codex desktop Node runtime |
| `C:\LAB\MTC_AIONUI_PILOT` | PID 11180 PowerShell running `run_dashboard_server.ps1` from that worktree |

No other outside-pool worktree path appeared in the independent process command-line/executable-path snapshot.

### Current SESSION_LOCK relevance

- `BRIDGE_HELP_IMPL`: explicitly named and preserved under the claimed Bridge Help/System Map row.
- main/current: contains the currently claimed shared-memory workstream and is the active Lead checkout.
- `KVM2GLM` and `postgate_runkit_design_claude`: dirty `_AI_MEMORY` paths intersect the currently claimed shared-memory surface.
- `R7FINAL`: branch identity corresponds to the currently claimed RP7 row.
- `PSC`: branch identity corresponds to the currently claimed Pathscope row.
- main/current also contains Audit-2 readiness and RP7/Pathscope untracked/scratch evidence covered by current claims.

### Git worktree metadata

- Git `locked` markers among these 67 paths: **0**;
- Git `prunable` markers among these 67 paths: **0**;
- missing or status-unavailable registered paths: **0**.

The absence of a Git `locked` marker is not authorization to modify or remove a worktree.

## 9. Branch/ref and unique-commit status

- Every branch-attached dirty worktree HEAD is contained by its own named local branch.
- All previously tracked-dirty branch heads except `GEMINI` and `MTC_AIONUI_PILOT` have **0** commits unique after excluding their own branch.
- `GEMINI` has **4** branch commits not contained by other branches/remotes/tags.
- `MTC_AIONUI_PILOT` has **2** branch commits not contained by other branches/remotes/tags.
- main/current has **25** such branch commits at the snapshot.
- the sole detached tracked-dirty HEAD is contained by 17 durable refs and has **0** commits outside refs.

These reachability statements do not preserve uncommitted tracked changes, untracked files, ignored databases, or operational state.

## 10. Classification conclusion

Batches 1–6 and this report now account for every currently registered worktree:

```text
155 registered
  = 88 detached tracked-clean, retirement-reviewed
  + 47 branch-attached fully clean
  + 18 branch-attached dirty (16 tracked-dirty + 2 ordinary-untracked-only)
  +  1 detached tracked-dirty
  +  1 main/current
  +  0 missing/unavailable
```

No branch-attached or dirty worktree receives a retirement verdict here. The safe next phase, if separately authorized, is an owner-reviewed preservation/branch-consolidation plan for dirty trees—not deletion or worktree removal.
