# FABLE TS-P0 BUILD REPORT — 2026-07-19

Builder: Claude Fable 5 (owner-directed build session; supersedes backlog
"Recommended AI" routing for this run). Chain: TS-P0-001 → 002 → 003 → 004,
STOP at Phase 1 boundary. Independent Fable audit follows — see
`FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md`.

## Workspace facts (verified this session)

- Canonical repo `C:\LAB\Tradingview_LAB_CLEAN`; `origin/master` = `008e065e`
  (PR #24 merge). Local `master` ref is stale at ancestor `8721bce0` — NOT
  touched; the worktree pins the commit directly.
- Build worktree: `C:\TSP0`, branch `feature/ts-p0-baseline`, base `008e065e`.
  Final state: clean at `7777273f` (3 commits, one per code task). NO push,
  NO PR, NO merge.
- Runtime `C:\P2RT`: detached `008e065e`, porcelain clean, bridge RUNNING +
  ARMED in Day 1 v1 window (`paper-20260719185026`) — read-only throughout;
  unchanged-proof below.
- Baseline suite at `008e065e` re-verified this session: **164 passed**.

## Task A — TS-P0-001 baseline manifest + drift checker — DONE

- Commit: **`fa449ce2`** — `IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py`
  (main symbols: `build_manifest`, `compute` helpers `_read_git_facts`,
  `_walk_scope`, `_hash_side`, `_hash_file`, `_render_markdown`, `main`;
  `SCHEMA_VERSION="1.0.0"`), `tests/test_runtime_baseline.py` (14 tests),
  `docs/RUNTIME_BASELINE_CONTRACT.md`.
- RED proof (pre-implementation, captured): pytest collection error
  `ImportError: cannot import name 'check_runtime_baseline' from 'tools'`.
- GREEN: `python -m pytest IBKR_PAPER_BRIDGE/tests/test_runtime_baseline.py -q`
  → **14 passed** from `C:\TSP0`; **14 passed** from
  `C:\TSP0\IBKR_PAPER_BRIDGE` (`python -m pytest tests/test_runtime_baseline.py -q`).
- Full regression after task: **177 passed** (164 baseline intact).
- Exit-code contract: 0 exact clean match / 2 drift/dirty/missing-runtime /
  3 invalid evidence input (single stderr line, no traceback). Deterministic:
  sorted keys/files, LF, byte-stable except declared `generated_at_utc`
  (`--timestamp` injectable). Secret denylist (`.env*`, `secret*`, `*.key`,
  `*.pem`, `*.db`, `*.log`, …) never opened/hashed — proven by spy test.
- **Engineering finding:** raw-byte hashing false-flagged drift between the
  real pair — the two checkouts smudged line endings differently
  (TSP0 uniform CRLF, P2RT mixed) while git reports both clean and blob-equal
  (`git hash-object` identical: `40a6ce5e…`, `6f3154c1…`). Fix: CRLF→LF
  normalization before hashing text files (git clean-filter equality); binary
  (NUL-sniff) hashed raw. Documented in contract + dedicated test.
- **Integration run (read-only, real pair) — exact command:**
  ```
  python IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py \
    --repo-root C:/TSP0 --runtime-root C:/P2RT --expected-commit 008e065e \
    --json-out <scratch>/tsp0001_integration_manifest.json --md-out <scratch>/tsp0001_integration_manifest.md
  ```
  **Raw exit code: 2** (expected — TSP0 HEAD was the Task A commit, not
  `008e065e`). Manifest: verdict `DRIFT`; drift_reasons exactly
  `["repo_commit_mismatch_expected", "repo_runtime_commit_mismatch"]`;
  runtime commit `008e065e…` matches expected ✓, both trees clean ✓,
  `source_tree_hash_equal: true`, `config_hash_equal: true`.
  P2RT porcelain empty and HEAD `008e065e` identical before and after the run.
- **Open item for Barış:** confirm hash scope (`bridge/**`, `config/**`,
  `requirements.txt`, `tools/run_bridge_p2.ps1`; tests/docs/data excluded) —
  rationale table in `RUNTIME_BASELINE_CONTRACT.md`.

## Task B — TS-P0-002 release/rollback evidence — DONE

- Commit: **`42d0ca9f`** — `IBKR_PAPER_BRIDGE/tools/release_evidence.py`
  (`create`/`validate` subcommands; `_build_manifest`, `_validate_manifest`,
  `_integrity_hash`; `SCHEMA_VERSION="1.0.0"`; reuses Task A primitives via
  import — no duplication), `tests/test_release_evidence.py` (11 tests),
  `docs/RELEASE_EVIDENCE_CONTRACT.md` (**DRAFT — pending Barış approval**,
  as required), plus one fixture line added to `test_runtime_baseline.py`
  (`bridge/store/db.py` in the temp repo — schema-hash source).
- RED proof: collection error `ImportError … release_evidence` (module
  absent at parent commit).
- GREEN: **11 passed** from repo root; **11 passed** from bridge CWD.
  Full regression after task: **189 passed**.
- Validates: release commit pinned to repo HEAD at create; rollback commit
  must exist and differ; commit/tree/config/lock/schema/runtime hashes +
  `integrity_sha256` self-hash. Negative tests: tamper (integrity mismatch),
  missing field, old schema version, unknown rollback, post-release drift,
  corrupt/missing manifest. Lock hash = `requirements.txt` (no lockfile yet →
  TS-P1-011 note); schema hash = `bridge/store/db.py` (proxy until TS-P2-006)
  — both documented as such in the contract.
- **Open item for Barış:** approve `RELEASE_EVIDENCE_CONTRACT.md` (it stays
  DRAFT/non-binding until then).

## Task C — TS-P0-003 honest monitoring-window state — DONE

- Commit: **`7777273f`** — new `bridge/engine/window.py` (pure
  `compute_window_state` + `window_status` read model + `record_window_start`
  / `record_liveness` / `detect_interruption` / `reset_window`; meta keys
  `window_started_ts|last_alive_ts|interrupted_ts|reset_ts`), minimal
  additive wiring in `bridge/engine/engine.py` (arm → window start; startup +
  reconcile-success → liveness; startup → interruption stamp + WARN event;
  `status()` gains `window` block; new field `window_stale_after_s=300`),
  additive `window` key in `bridge/api/routes.py::init_runtime_state`,
  `tests/test_window_state.py` (21 tests),
  `docs/21_WINDOW_STATE_CONTRACT.md`.
- RED proof: `ModuleNotFoundError: No module named 'bridge.engine.window'`.
- GREEN: **21 passed**. Full regression after task from BOTH CWDs:
  **210 passed / 210 passed** — the pre-existing 164 tests all green,
  proving no behavior change for current callers.
- Acceptance: DOWN can never present as active — exhaustive product-sweep
  test asserts RUNNING requires fresh liveness AND ARMED AND no recorded
  interruption; stale-age boundary tested at exactly `stale_after_s` and
  just over; store-unreadable → DOWN with `error: store_unreadable`.
  Transitions all tested: fresh→DOWN, arm+liveness→RUNNING, stale→DOWN,
  gap→INTERRUPTED (sticky across re-arm), reset→RESET→new window RUNNING.
- NO restart/ARM/scheduler action; P2RT NOT redeployed (later Barış gate).
- **Open item for Barış:** confirm reset policy (sticky interruption until
  explicit `reset_window`; ≤300s gap tolerance; no HTTP reset endpoint) —
  marked PROPOSED in `21_WINDOW_STATE_CONTRACT.md`.

## Task D — TS-P0-004 ADR-0018/0025 status closure — DONE (verify-and-record)

- No TSP0 commit — the ADR directory exists only as UNTRACKED files in the
  main worktree (user-managed); edits left uncommitted per existing
  convention. Docs-only.
- Verified: D016 + addendum (read directly) ratify ADR-0018..0029; all twelve
  files say `Status: Accepted`; index table consistent with qualifications;
  0018/0025 ratification lines cite D016 and declare TS-P0-004 resolved.
- Fixed three stale status wordings (ADR-0025 §Context "remains Proposed",
  ADR-0018 §Rationale "conservative `Proposed` status reflects",
  ADR_INDEX blockers "their Proposed status"). Decision content untouched.
- Full report: `FABLE_TSP0004_ADR_CLOSURE_REPORT_2026-07-19.md`. Notes one
  stale pre-addendum sentence INSIDE D016 itself — flagged, not edited
  (owner record).

## Test-count ledger

| Point | Command (repo root CWD) | Count |
| --- | --- | --- |
| Baseline `008e065e` | `python -m pytest IBKR_PAPER_BRIDGE/tests -q` | 164 passed |
| After Task A | same | 177 passed |
| After Task B | same | 189 passed |
| After Task C | same (both CWDs) | 210 passed / 210 passed |

`PYTHONUTF8=1` set for all runs; Python 3.14.2; Windows 11.

## Safety confirmation block

- Push / PR / merge: **NO** (branch local only; guard `repo_guard.ps1` PASS
  before every commit).
- Deploy / runtime change: **NO**.
- `C:\P2RT` writes / checkout / restart / stop / ARM / DISARM / scheduler /
  task / DB actions: **NO** — read-only git + file-hash reads plus ONE
  permitted `GET /api/status` at session end.
- Exchange/testnet/network calls from tools or tests: **NO** (offline; the
  single status GET is localhost read-only).
- Threshold / strategy / signal / Pine / parity / schema changes: **NO**.
- Protected scopes (`01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `MTC_V2`):
  **untouched**.
- Credentials: never read; tools provably never open denylisted secret files.
- Dependencies added: **NONE** (stdlib only).

**Window-unaffected proof (2026-07-19T19:37:46Z):** `git -C C:\P2RT rev-parse
HEAD` = `008e065e8e0ffa68f46134da6698d58f91ef2dcb` (unchanged, checked at
session start, after every task, and at session end); porcelain empty;
`GET http://127.0.0.1:8790/api/status` → `state=ARMED`, `mode=paper`,
`network=testnet`, `run_id=paper-20260719185026`, `reconcile_ready=true`,
`last_reconcile_ts=2026-07-19T19:37:14Z` (fresh). Day 1 v1 window intact.

## Open items needing Barış (consolidated)

1. TS-P0-001 hash-scope confirmation (contract §Hash scope).
2. TS-P0-002 release-evidence contract approval (currently DRAFT).
3. TS-P0-003 window reset-policy confirmation (currently PROPOSED).
4. Optional: D016 internal stale-sentence cleanup note.

## Final report (guard format)

```
branch:            feature/ts-p0-baseline (worktree C:\TSP0)
files changed:     Task A fa449ce2: tools/check_runtime_baseline.py, tests/test_runtime_baseline.py, docs/RUNTIME_BASELINE_CONTRACT.md
                   Task B 42d0ca9f: tools/release_evidence.py, tests/test_release_evidence.py, docs/RELEASE_EVIDENCE_CONTRACT.md, tests/test_runtime_baseline.py
                   Task C 7777273f: bridge/engine/window.py, bridge/engine/engine.py, bridge/api/routes.py, tests/test_window_state.py, docs/21_WINDOW_STATE_CONTRACT.md
                   Task D (main worktree, untracked docs): ADR-0018, ADR-0025, ADR_INDEX.md wording fixes
checks run:        repo_guard.ps1 (PASS ×3), pytest suites per ledger above, read-only integration run vs C:\P2RT
guard:             PASS
commit:            fa449ce2, 42d0ca9f, 7777273f (local only)
pushed:            no
remaining dirty:   C:\TSP0 clean; main worktree carries pre-existing user files + this session's memory/triage/ADR doc updates (uncommitted by convention)
next action:       independent Fable audit via FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md; then Barış items 1-3 above
```
