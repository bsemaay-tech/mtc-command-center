# Gate A overnight morning report — 2026-08-03

## Executive result

The ordered Gate A queue reached an honest terminal **PASS** for all three source candidates under
Barış's explicit no-Claude owner waiver. Each accepted line is published on its own feature/evidence
branch. None is merged into `master`; Queue D, integration, artifact rebuild, deployment, runtime,
broker, trading, and economic action remain stopped.

| Ordered item | Original frozen candidate | Final product SHA | Published evidence head | Result |
|---|---|---|---|---|
| Gate A 3b SHM validation | `7aad0377` | `7aad0377` | `20de117f` | **PASS** |
| Build determinism | `c5a4070a` | `82e92c98` | `0bdf8cf4` | **PASS** after repair |
| Queue C credential-free DISARMED | `5a9bb922` | `17402a58` | `a0275b5c` | **PASS** after one audit repair round |

## Validation and audit evidence

### Gate A 3b

- Exact product scope: `tools/wal_state_bundle.py` and `tests/test_wal_state_bundle.py`.
- D026: nine named guard mutations **RED `9 failed` → GREEN `9 passed`**.
- Windows full: candidate `1 failed, 1338 passed`; exact parent `1 failed, 1309 passed`.
- Locked Linux full: candidate `2 failed, 1337 passed`; exact parent `2 failed, 1308 passed`.
- Independent executing verdicts: `gpt-5.6-sol` xhigh **PASS**; GLM-5.2
  **PASS-WITH-NITS** with optional wording only.

### Build determinism

- Exact product scope: `deploy/linux/lib/common.sh`, `deploy/linux/package.sh`, and
  `tests/test_linux_deployment.py`.
- The frozen candidate's locale and comment-coupled test defects were reproduced and repaired.
- D026: removing the real `-c core.eol=lf` guard made the new repository-EOL regression test RED;
  restoring the candidate made it GREEN. The locale control reproduced RED on the frozen parent and
  safe SKIP/PASS behavior on the repair.
- Windows full: `2 failed, 1317 passed`; locked Linux full: `25 failed, 1294 passed`, with no new
  failure node ID over the frozen parent.
- Independent executing verdicts: `gpt-5.6-sol` xhigh **PASS**; GLM-5.2
  **PASS-WITH-NITS** with an optional skip-wording nit only.

### Queue C

- Original cycle scope: `bridge/api/routes.py`, `bridge/app.py`, and the new focused test. Repair
  scope after `5a9bb922` is exactly `bridge/app.py` plus its focused test.
- Original D026: frozen app with repair tests `2 failed, 4 passed` → repaired `6 passed`.
- The first Codex audit then reproduced a production CLI-precedence regression at `21f82133`.
  Repair `17402a58` makes explicit `--start-mode` win before invalid environment evaluation while
  preserving environment-aware ASGI imports.
- Final D026: exact pre-fix app `1 failed, 6 passed` → final candidate `7 passed`.
- Windows full: `2 failed, 1311 passed`; locked Linux full: `25 failed, 1288 passed`, exactly the
  prior frozen-parent failure set plus two added passing tests.
- Final independent executing verdicts: `gpt-5.6-sol` xhigh **PASS** and GLM-5.2 **PASS**.

The residual Windows/Linux failures cited above are pre-existing KVM2 ledger/WAL evidence mismatches,
Python-3.12 order-state GC assertions, or the known locked-Linux WAL capture cascade. Candidate and
parent failure-name comparisons show no new full-suite failure in any accepted line.

## Refs, ancestry, and worktrees

- Remote `master` and local `origin/master` both resolve to
  `637307e83951ffe23e768ed8e50ddaf8712b0660`.
- Published heads:
  - `codex/gate-a-3b-shm-validation` → `20de117f4a7d57e131803a195627e2af9c208cd9`
  - `codex/gate-a-build-determinism` → `0bdf8cf44941501180c319886701abfeddd8f952`
  - `codex/gate-a-credential-free-disarmed` → `a0275b5ce90ea57018bdd6a699917a3222564d5b`
- All three descend from `637307e8`; they are respectively 4, 5, and 5 commits ahead. None is an
  ancestor of `origin/master`.
- Read-only pairwise `git merge-tree` simulations over the final product commits reported zero
  case-sensitive conflict markers for 3b+build, 3b+Queue C, and build+Queue C. This is conflict
  readiness evidence only, not an integration verdict.
- Candidate and audit worktrees ended at their recorded SHAs with empty index/worktree status.
- The primary root worktree is clean. The global registry is **not** wholly clean: unrelated,
  pre-existing dirty worktrees remain at `C:/CDXFAILOVER` (1 entry), `C:/KVM2GLM` (10),
  `C:/KVM2P03` (52), `C:/LAB/MTC_AIONUI_PILOT` (206), the `C:/TSP1002*` group
  (13/5/5/5), the `C:/TSP1003*` group (8/3/10/9/11), and the dirty `C:/TSP1004*` members
  (15/255/11). They are outside this queue and were not modified or cleaned.

## Safety boundary

No Queue D, integration, artifact rebuild, Gate A rerun, `master` merge, deployment, service/runtime
change, credential access, broker/exchange call, ARM, order, TESTNET/mainnet, Pine/parity/MTC/trading
change, wallet action, or economic action occurred. Any such next phase requires a separately
authorized scope beyond this report.
