# CODEX PROMPT — INDEPENDENT AUDIT: TS-P0-001..004 build (Fable, 2026-07-19)

You are Codex in a FRESH session, acting as the INDEPENDENT AUDITOR of the Phase 0
baseline chain that Claude Fable 5 built on 2026-07-19. You did not build this code.
Trust nothing in the builder's report until you reproduce it on real code and real
commands. Your verdict gates any push/PR of this branch.

## 0. Read first

1. `AGENTS.md` (repo root), then `MTC_COMMAND_CENTER\_AI_MEMORY\START_HERE.md`.
2. Builder evidence (claims to verify, not truth):
   - `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0_BUILD_REPORT_2026-07-19.md`
   - `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0_AUDIT_HANDOFF_2026-07-19.md`
   - `MTC_COMMAND_CENTER\11_TRIAGE\FABLE_TSP0004_ADR_CLOSURE_REPORT_2026-07-19.md`
3. Task cards: `MTC_COMMAND_CENTER\09_DOCS\ROADMAPS\TRADING_SYSTEM\05_IMPLEMENTATION_BACKLOG.md`
   — read the TS-P0-001 full card and the Phase 0 table rows for 002/003/004. NOTE: the
   ROADMAPS directory is UNTRACKED and exists only in the MAIN worktree
   (`C:\LAB\Tradingview_LAB_CLEAN`), not in `C:\TSP0`.

## 1. Canonical facts (verify each yourself before auditing)

- Canonical repo: `C:\LAB\Tradingview_LAB_CLEAN` (never `C:\LAB\tradingview-lab`).
- `origin/master` = `008e065e` (PR #24 merge). Local `master` ref is stale at ancestor
  `8721bce0` — expected, leave it alone.
- Audit target worktree: **`C:\TSP0`**, branch `feature/ts-p0-baseline`, expected HEAD
  **`7777273f`**, porcelain clean. Commit chain off `008e065e`:
  `fa449ce2` (TS-P0-001) → `42d0ca9f` (TS-P0-002) → `7777273f` (TS-P0-003).
  TS-P0-004 has NO commit: docs-only edits to UNTRACKED ADR files in the main worktree.
- Runtime: **`C:\P2RT`**, detached at `008e065e`, bridge RUNNING + ARMED in the LIVE
  Day 1 v1 monitoring window (run `paper-20260719185026`, paper/testnet, port 8790).

## 2. Hard boundaries (identical to builder's)

- **`C:\P2RT` is READ-ONLY.** Never write, checkout, restart, stop, ARM, DISARM, or
  touch its scheduler/task/DB. Allowed: `git -C C:\P2RT` read commands, file reads,
  and AT MOST one `GET http://127.0.0.1:8790/api/status` for the window-unaffected proof.
- NO push, NO PR, NO merge, NO deploy. NO dependency installs. NO network calls from
  tools/tests (offline; the single localhost GET above is the only exception).
- Main worktree (`C:\LAB\Tradingview_LAB_CLEAN`) is DIRTY with protected user files —
  never clean/reset/stash/checkout there. A repo hook can flip the MAIN worktree's HEAD
  between commands; `C:\TSP0` is unaffected.
- In `C:\TSP0` you may create throwaway fixture repos under temp dirs and temporarily
  delete/restore COMMITTED files for RED proofs — but you MUST leave `C:\TSP0` clean at
  `7777273f` at session end (`git status --porcelain` empty). No new commits.
- Protected scopes (`01_PINE`, `02_MTC_BACKTEST`, `07_ADAPTERS`, `MTC_V2`, parity,
  schemas): read-only; report if the diff touches them (it must not).

## 3. Mandatory reproductions (evidence, not trust)

All test runs: Windows, `PYTHONUTF8=1`, Python 3.14.x. Record EXACT counts and exit codes.

1. **Scope check:** `git -C C:\TSP0 diff --stat 008e065e..7777273f` — confirm the file
   set matches the build report exactly (3 new tools/tests/docs sets + minimal
   `engine.py`/`routes.py` wiring + 1 fixture line). Any file outside
   `IBKR_PAPER_BRIDGE/` = finding. Confirm NO pre-existing test file was modified except
   the one declared fixture line in `tests/test_runtime_baseline.py`.
2. **Green suites, BOTH CWDs (expect 210 passed / 210 passed):**
   ```
   cd C:\TSP0                   && python -m pytest IBKR_PAPER_BRIDGE/tests -q
   cd C:\TSP0\IBKR_PAPER_BRIDGE && python -m pytest tests -q
   ```
3. **Baseline integrity:** in a THROWAWAY worktree (`git -C C:\LAB\Tradingview_LAB_CLEAN
   worktree add C:\TSP0AUD 008e065e`), run the suite — expect **164 passed** — then
   `git worktree remove C:\TSP0AUD`. Confirms the 46 new tests are additive.
4. **RED proofs (committed-state only; restore after each):**
   - A: `rm IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py` → run
     `tests/test_runtime_baseline.py` → expect collection ImportError → `git checkout -- <file>`.
   - B: same pattern with `tools/release_evidence.py` / `tests/test_release_evidence.py`.
   - C: `git restore --source=7777273f^ -- IBKR_PAPER_BRIDGE/bridge/engine/engine.py
     IBKR_PAPER_BRIDGE/bridge/api/routes.py` + `rm IBKR_PAPER_BRIDGE/bridge/engine/window.py`
     → run `tests/test_window_state.py` → expect ModuleNotFoundError →
     `git checkout -- IBKR_PAPER_BRIDGE/bridge`.
5. **Integration re-run (read-only, real pair):**
   ```
   cd C:\TSP0
   python IBKR_PAPER_BRIDGE/tools/check_runtime_baseline.py --repo-root C:/TSP0 --runtime-root C:/P2RT --expected-commit 008e065e
   ```
   Expect raw exit **2**; drift_reasons exactly `repo_commit_mismatch_expected` +
   `repo_runtime_commit_mismatch`; `runtime_commit_matches_expected: true`;
   `source_tree_hash_equal: true`; `config_hash_equal: true`; both dirty flags false.
   Capture `git -C C:\P2RT rev-parse HEAD` + `status --porcelain` BEFORE and AFTER —
   must be `008e065e` + empty both times.

## 4. Adversarial checklist (execute each; fixture repos in temp dirs)

1. **Hash-scope bypass:** file planted outside declared scope (e.g. `docs/x.py`) must
   not affect hashes; inside `bridge/` must change `source_tree_hash`. Contract doc
   (`RUNTIME_BASELINE_CONTRACT.md`) scope must equal code (`SOURCE_SCOPE`/`CONFIG_SCOPE`).
2. **CRLF-normalization abuse (new surface, builder-disclosed):** `_hash_file` strips
   `\r\n` for text files (NUL-sniff first 8KB = binary). Verify (a) a real content
   change that also flips line endings IS detected; (b) a file crafted with an early NUL
   plus differing text is still detected (hashed raw); (c) a line-ending-ONLY change is
   intentionally NOT drift — judge whether that matches git-equality semantics as
   documented, and whether git status would catch a worktree-only CRLF tamper.
3. **Secret denylist:** plant `.env`, `secrets.key`, AND edge names (`prod.env`,
   `my.secrets`, `key.txt`) in fixture scope. Sentinel string must appear nowhere in
   stdout/stderr/JSON/MD; denylisted files listed under `excluded` and never opened.
   Assess the `prod.env` case: pattern is `^\.env(\..*)?$` — basename `prod.env` is NOT
   denylisted. It WILL be hashed (hash only, no content). Finding or acceptable? Judge
   against ADR-0027 and say so explicitly.
4. **Dirty-state false negative:** untracked file in fixture runtime → `runtime_dirty`
   true; gitignored file → not dirty (matches porcelain). Confirm P2RT's ignored
   `data/`, `__pycache__` cannot mask drift INSIDE hashed scope.
5. **Exit-code lies:** subprocess-level exit codes (not just `main()` return): clean
   MATCH→0; each drift class→2; RUNTIME_MISSING→2; missing repo root→3; malformed HEAD
   (monkeypatch or fixture)→3; argparse garbage→3. Manifest `exit_code` field must equal
   the real process exit code in every case.
6. **Byte-stability:** two runs with identical `--timestamp` → byte-identical JSON+MD
   (`fc /b`). Without `--timestamp`, only `generated_at_utc` differs.
7. **Release-evidence integrity (TS-P0-002):** (a) tamper a hash WITHOUT re-signing →
   `integrity_hash_mismatch`, exit 2; (b) **re-sign attack**: tamper `config_hash` AND
   recompute `integrity_sha256` via `_integrity_hash` → integrity passes, but validate
   must STILL fail via live comparison (`config_hash_mismatch`); (c) `create` refuses
   `--release-commit` ≠ repo HEAD (exit 3) and rollback==release (exit 3); (d) old
   `schema_version` 0.9.0 → `unsupported_schema_version`, exit 2; (e) missing field →
   `missing_field:<name>`, exit 2; (f) corrupt JSON / absent file → exit 3, no traceback.
8. **Window false-active (TS-P0-003 core acceptance):** try to construct ANY meta
   combination (`window_started_ts` / `window_last_alive_ts` / `window_interrupted_ts`
   / `window_reset_ts` × app_state ARMED/DISARMED/KILLED × fresh/stale clock) where
   `window_status` returns RUNNING with stale or missing liveness. The exhaustive sweep
   test claims impossible — verify the decision order in `compute_window_state` and
   attack edges: exactly-at-threshold age, naive (tz-less) timestamps, garbage meta
   strings, `store.get_meta` raising (must yield DOWN + `error: store_unreadable`).
   Confirm `record_window_start` does NOT clear `window_interrupted_ts` (re-arm stays
   INTERRUPTED until explicit `reset_window`), and `init_runtime_state`'s engine-less
   `window` block fails safe (`no_store` → DOWN).
9. **Engine wiring regression risk:** diff `engine.py`/`routes.py` against `42d0ca9f` —
   wiring must be purely additive (window import/field, `record_*`/`detect_*` calls,
   `window` key). No existing status key changed, no control flow altered, no new
   endpoint added, no scheduler/network/DB side effects.
10. **No-mutation:** after ALL your tool runs, `git -C C:\TSP0 status --porcelain` and
    `git -C C:\P2RT status --porcelain` both empty; P2RT HEAD unchanged.
11. **TS-P0-004 (docs, main worktree):** confirm all twelve ADR-0018..0029 files say
    `Status: Accepted`; the three claimed wording fixes (ADR-0025 §Context, ADR-0018
    §Rationale, ADR_INDEX blockers paragraph) changed status-wording ONLY; D016 in
    `_AI_MEMORY\DECISIONS.md` was NOT edited; no decision content invented.
12. **Card compliance:** each deliverable matches its card (files, acceptance criteria,
    required tests present by name); RELEASE_EVIDENCE_CONTRACT.md carries the
    **DRAFT — pending Barış approval** header; reset policy marked PROPOSED; no runtime
    operation included anywhere.

## 5. Verdict + report

Write `MTC_COMMAND_CENTER\11_TRIAGE\CODEX_TSP0_AUDIT_2026-07-19.md`:

- Per task (A–D): reproduced evidence (exact commands, exact counts/exit codes),
  findings with file:line, severity (FATAL / MAJOR / NIT).
- Explicit adversarial-checklist results, 1–12, each PASS/FAIL/N-A with one-line proof.
- Window-unaffected proof (P2RT HEAD + porcelain before/after, optional single
  status GET).
- **Verdict: PASS / PASS-WITH-NITS / BLOCK.** BLOCK requires a reproducible failing
  command or a concrete violated constraint (card text, safety boundary, or false claim
  in the builder report). List required edits if BLOCK.
- Safety confirmation block: explicit NO for push/deploy/P2RT-write/scheduler/ARM/
  threshold/strategy/credential actions.

Update `_AI_MEMORY\GLOBAL_HANDOFF.md` (section header format
`## [Codex] 2026-07-19 — TS-P0 audit <verdict>`), `NEXT_STEPS.md`, `ACTIVE_FILES.md`
(main worktree, leave uncommitted). Report facts only from evidence produced in YOUR
session; distinguish "builder claimed" from "verified now" everywhere.
