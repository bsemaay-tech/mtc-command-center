# Gate A overnight morning report — 2026-08-03

## Executive result

The ordered Gate A queue reached an honest terminal **PASS** for all three source candidates under
Barış's explicit no-Claude owner waiver. Each accepted line is published on its own feature/evidence
branch. None is merged into `master`; Queue D, integration, artifact rebuild, deployment, runtime,
broker, trading, and economic action remain stopped.

The two pre-existing Windows-only evidence-test failures observed during the queue were subsequently
repaired and independently accepted on a fourth isolated evidence branch. That repair is likewise
not integrated into `master`.

| Ordered item | Original frozen candidate | Final product SHA | Published evidence head | Result |
|---|---|---|---|---|
| Gate A 3b SHM validation | `7aad0377` | `7aad0377` | `20de117f` | **PASS** |
| Build determinism | `c5a4070a` | `82e92c98` | `0bdf8cf4` | **PASS** after repair |
| Queue C credential-free DISARMED | `5a9bb922` | `17402a58` | `a0275b5c` | **PASS** after one audit repair round |
| Residual evidence tests | `637307e8` | `ebb750da` | `3121e7c7` | **PASS** after isolated repair |

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

Read-only residual diagnosis sharpened the two Windows failures:

- The ledger row expects SHA-256 `f4cdece5...`, which exactly matches the committed LF
  `ledger_schema.json` bytes. The Windows checkout is `i/lf w/crlf` under `text=auto` and hashes to
  `b6580e31...`; the validator hashes converted working-tree bytes. This is EOL-sensitive evidence
  validation, not a changed canonical ledger artifact.
- `test_invariants_preserve_risk_and_history` hardcodes schema version `2`, while
  `SCHEMA_VERSION_BASELINE = 4` and the fixture calls ordinary `Store.initialize()`. The failure is a
  stale test expectation.

### Residual evidence-test repair

- Exact scope: `.gitattributes` and `tests/test_wal_state_bundle.py`; the ledger blob and all runtime
  code are unchanged.
- D026: exact parent `637307e8` **RED `2 failed` → candidate GREEN `2 passed`**.
- Windows full: `1306 passed`, including canonical LF ledger hash `f4cdece5...`.
- Locked Linux full: candidate and parent each `25 failed, 1281 passed`, with identical failure node
  IDs; candidate ledger node `1 passed`.
- Independent executing verdicts: `gpt-5.6-sol` xhigh **PASS** and GLM-5.2 **PASS**, both with no
  required findings.
- Acceptance record:
  `11_TRIAGE/GATE_A_RESIDUAL_EVIDENCE_TEST_REPAIR_ACCEPTANCE_2026-08-03.md` on the residual branch.

No artifact regeneration occurred.

## Refs, ancestry, and worktrees

- Remote `master` and local `origin/master` both resolve to
  `637307e83951ffe23e768ed8e50ddaf8712b0660`.
- Published heads:
  - `codex/gate-a-3b-shm-validation` → `20de117f4a7d57e131803a195627e2af9c208cd9`
  - `codex/gate-a-build-determinism` → `0bdf8cf44941501180c319886701abfeddd8f952`
  - `codex/gate-a-credential-free-disarmed` → `a0275b5ce90ea57018bdd6a699917a3222564d5b`
  - `codex/gate-a-residual-evidence-tests` → `3121e7c7ffe0921fed7340af5be34dbf412e3774`
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
