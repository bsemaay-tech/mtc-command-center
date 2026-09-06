# Lane R1 — adversarial review of the overnight code commits (read-only)

- Reviewer: Claude lane R1 (independent second read for the Lead; NOT acceptance).
- Base: `b42eb4e7` on `claude/overnight-autonomous-work-e94x3q`, isolated worktree
  `.claude/worktrees/agent-a2140b6ea3a376ed3`, fast-forwarded from `afe52ea8`.
- Method per commit: `git show` scope check, regression hunt, targeted Python probes (venv312,
  `PYTHONUTF8=1`), scoped test runs, and throwaway mutants on scratch copies under the session
  scratchpad (never in worktree files). No backtest, server, broker, launcher or orchestrator run.
- Every commit below stays a NONACCEPTED candidate; the exact T0–T2 audits were unreachable tonight.

## Verdict table

| sha | scope | verdict | one-line reason |
|---|---|---|---|
| 6a25e23a | dashboard tests platform-independent | PASS | Test-only; `discovery_source` is `str(Path(...))` in product code, so the Path-built expectation is the correct portable form; 129 dashboard tests green. |
| 5c617b3f | orchestrator dedent + regenerated runner | PASS-WITH-NITS | Fix is correct and discriminating (mutant RED); emitted body equals the committed runner byte-for-byte modulo `Generated:`; but the runner still imports a non-existent `PYTHON_PROTOTYPES` package (pre-existing template defect). |
| 91ccbba6 | seed warning as YAML comment + 7 yml | PASS | Only two YAML writers plus one comment-prefix line per file changed; all 8 tracked `parameter_library/**/*.yml` now `yaml.safe_load`; Markdown report writer untouched as stated. |
| 151e1700 | aggregate rename | PASS | `R100` rename, zero content change; only archival/ledger references name the old `.json`. |
| 361b6451 | mtc_cli audit router-era layout + tests | PASS-WITH-NITS | Real repo audits OK (`memory_files_ok`, 1 NEXT ACTION, 0 real WAITING items); "Nothing for this lane" is not mis-parsed; nits on `(none)`/`none` handling and section-order assumption. |
| f4455150 | 00_CONFIG path examples | PASS-WITH-NITS | Every new value exists repo-relative; but readers derive `reports/optimization` and `06_QUANTLENS_LAB` under `mtc_v2_root`, neither of which exists under `01_MTC_PROJECT` (pre-existing layout mismatch now surfaced). |
| f8fa3caf | Bridge hyperliquid.py one import + TESTS.md | PASS | Exactly one added line; `Any` is used only in a local-variable annotation, which CPython never evaluates, so the change is lint-only with zero runtime delta; TESTS.md/HANDOFF are docs. |
| 63de031a | orchestrator QLAB_ROOT | PASS | `PROTO_DIR`/`PROMOTED_DIR`/`TOOLS_DIR` remain the same relative children of `QLAB_ROOT`; all three exist under `03_QUANTLENS`; `relative_to(REPO_ROOT)` still valid. |
| 31e975f1 | README links | PASS | `LIB_ConfirmationLayer.pine` is a same-directory sibling; the copilot-instructions link is correctly demoted to plain text (file absent from tree). |
| a216b61f | generate_index.py + tests | PASS-WITH-NITS | `--check` is byte-identical against the committed INDEX.md; 33 tests green; two undocumented PS1 divergences (strict decode vs .NET replacement; `len()` code points vs .NET UTF-16 units) — no current file triggers them. |
| 79c77050 | mtc_v2_reader root from config | PASS | `load_path_config` never raises on a missing config (same as every other reader); unconfigured case renders the fixed `""`/`False` shape; both tests RED under the reverted mutant. |
| 68a2d601 | ds_agent report path | PASS-WITH-NITS | Default path fix is correct; but the new `mkdir(parents=True)` also applies to an explicit `report_out` (benign, contradicts the "unchanged" claim) and `_dump` itself is untested. |
| ec80222d | registry_reader fail-closed row repair | PASS | Old vs new agree on every real registry row (14 rows, one 19-field row repairs to 17 = header) and on every previously-correct shape; only formerly-misaligned rows now drop; both new tests RED under the mutant. |
| 44b11300 | four readers utf-8-sig | PASS | `utf-8-sig` is byte-identical to `utf-8` for every non-leading-BOM input under `strict`/`replace`/`ignore` (probe); no non-sig read remains in the four modules; all four BOM tests RED under the reverted mutant. |

No commit reaches REQUEST_CHANGES. All nits below are optional follow-ups, not acceptance blockers.

## Per-commit notes for the non-PASS verdicts

### 5c617b3f — PASS-WITH-NITS
- Scope check: `overnight_orchestrator.py` (4 lines: one join + three comment lines),
  `overnight_extended_run.py` (regenerated), lane B record. Nothing outside scope.
- Evidence: scratch copy of the orchestrator dry-emitted the runner; `py_compile` GREEN; content
  equals the committed runner except the `Generated:` timestamp. Mutant (`"\n".join`) emits a file
  whose first line begins with 8 spaces and `py_compile` raises `PyCompileError` — the fix
  discriminates.
- Nit (pre-existing, outside the lane's stated scope): the template emits
  `from PYTHON_PROTOTYPES import ..._prototype` after `sys.path.insert(0, str(ROOT.parent))`, but
  the prototypes live in `03_QUANTLENS/04_PYTHON_PROTOTYPES` and no `PYTHON_PROTOTYPES` package
  exists under `03_QUANTLENS`. The regenerated runner compiles but would fail at import if ever
  launched. Do not treat "compiles" as "runnable"; a later lane should fix the template
  (`overnight_orchestrator.py:575,585`) before any `--launch`.

### 361b6451 — PASS-WITH-NITS
- Scope check: `mtc_cli/commands/audit.py`, `mtc_cli/tests/test_audit.py`, `mtc_cli/HANDOFF.md`.
  The module-level `HEARTBEAT_PATH` constant was removed; no other module referenced it (grep).
  `__main__.py` calls `audit.run()` with defaults, so the new `repo_root=` kwarg is compatible.
- Real-repo probe: `python -m mtc_cli audit repo --json` -> `ok: true`, `memory_files_ok: true`,
  `handoff_next_actions: 1`, `handoff_waiting_for_owner: 0`, no findings. `_newest_section`
  selected `[Codex Lead] 2026-09-06 — Owner-delegated same-package repair scope`, the true newest
  section of the governance HANDOFF.
- `_handoff_waiting_for_owner_count` probes: `- **WAITING FOR OWNER:** Nothing for this lane.` -> 0;
  `WAITING FOR OWNER: Nothing for this lane` -> 0; `- **WAITING FOR OWNER**: approve PAYG.` -> 1;
  `nothing.` -> 0; `Nothing-yet decide X` -> 0 (the `\b` matches at `-`, so a real item phrased
  this way is hidden); `(none)` -> 1 and `none` -> 1 (counted as real items).
- Mutant: adding `GLOBAL_HANDOFF.md` back to `_required_memory_files` in a scratch copy fails
  `test_fixture_mirroring_router_layout_is_ok` and `test_fixture_waiting_for_owner_counted`
  (2 failed / 2 passed) — the fixture tests discriminate.
- Nits: (1) `_WAITING_NOTHING_RE` treats `none`/`(none)` as real owner items and `Nothing-…` as
  nothing; consider `^\s*(nothing|none)\b(?![-\w])` or an explicit allow-list. Data-only, no
  finding is emitted from the count, so no false FAIL today. (2) `_newest_section` assumes
  newest-first ordering; correct for the governance HANDOFF, but an appended section would go
  unchecked. (3) `_handoff_next_action_count` counts the substring anywhere in the section, so prose
  mentioning "NEXT ACTION" satisfies the check. (4) `test_real_repo_does_not_require_moved_files`
  depends on live repo state (acceptable for a repo-health CLI, but not hermetic).

### f4455150 — PASS-WITH-NITS
- Scope check: two example JSON files (5 values each, key set and `schema_version` unchanged) plus
  the lane E record. Both files are still identical copies of each other (pre-existing).
- Verified on disk: `01_MTC_PROJECT/01_PINE/MTC_V2.pine`, `01_MTC_PROJECT/03_DOCS/MTC_V2_ARCHITECTURE.md`,
  `01_MTC_PROJECT/05_PARITY/MTC_V2_PARITY_CASES.csv`, `04_REPORTS/`, `12_PARITY_PINETS/TW_EXPORT_CASES_V2/`
  all exist, so `mtc_v2_reader`, `health`, and the parity paths resolve under the new values.
- Nit / follow-up: `optimization_reader.py:27` reads `mtc_v2_root / "reports" / "optimization"` and
  `backtest_reader.py:114` the same; `registry_reader.py:27` and `backtest_reader.py:34` fall back to
  `mtc_v2_root / "06_QUANTLENS_LAB"`. Neither `01_MTC_PROJECT/reports` nor
  `01_MTC_PROJECT/06_QUANTLENS_LAB` exists (the project has `01_MTC_PROJECT/optimization/`). With the
  example as the only config, the optimization panel is empty-by-path. This is a pre-existing
  reader-vs-layout mismatch that the correct repoint now exposes, not a defect of this commit; it
  needs its own lane (reader sub-paths or a dedicated `optimization_root` key).

### a216b61f — PASS-WITH-NITS
- Scope check: new `generate_index.py`, new `test_generate_index.py`, lane G record. INDEX.md and
  `generate_index.ps1` untouched by this commit.
- Probes: `generate_index.py --check` in the worktree -> `OK: ... INDEX.md is byte-identical to the
  regenerated index.` 33 tests green. Scan of all 1,286 git-listed text-extension files under
  `11_TRIAGE`: 0 undecodable as UTF-8, 0 UTF-16 BOM files, 0 files containing the extra separators
  that Python `str.splitlines()` honors (`\x0b \x0c \x1c-\x1e \x85    `).
- Nits (documentation gaps; no current file triggers them): (1) the PS1 uses
  `[IO.File]::ReadAllLines`, which substitutes U+FFFD for invalid UTF-8 and honors UTF-16 BOMs; the
  port opens with `encoding="utf-8-sig", errors="strict"`, so an invalid-UTF-8 or UTF-16 file yields
  `Unreadable during index generation: UnicodeDecodeError` where the PS1 would emit heading/body.
  (2) `Clean-Cell` truncates on .NET `.Length` (UTF-16 code units) while `clean_cell` uses `len()`
  (code points), so a cell with astral characters (emoji) longer than its limit truncates one unit
  differently. (3) `splitlines()` vs .NET `\r`/`\n`-only splitting. The docstring's "exactly" and
  "byte-for-byte" claims should list these three alongside the two documented divergences.

### 68a2d601 — PASS-WITH-NITS
- Scope check: `ds_agent.py` (+`tempfile` import, new `default_report_path`, one `mkdir` line in
  `_dump`, one changed line in `run_task`), new test module, lane O record. `_BANNED_ATTRS` and
  provider code untouched.
- `report_out` given: `Path(task.get("report_out") or default_report_path(slug))` — the explicit
  branch is textually unchanged. However `_dump` now runs `out_path.parent.mkdir(parents=True,
  exist_ok=True)` for every call, so an explicit `report_out` whose parent is missing now succeeds
  where it previously raised inside the swallowed `try`. Benign improvement, but the commit message's
  "Explicit report_out behavior is unchanged" is imprecise; the `mkdir` sits inside the `try`, so
  permission errors are still logged-and-swallowed as before.
- Test discrimination: the three `default_report_path` tests are RED pre-fix only because the
  function did not exist; the two `run_task_*` tests re-evaluate a copied expression rather than
  calling `run_task` or `_dump`. Untested: the `_dump` `mkdir` line and the real `run_task` wiring.
  The module-level `sys.modules["openai"]` stub is process-global for the pytest session (harmless
  here: `openai` is not installed in venv312 and `provider.py` imports it lazily).

## Notes on PASS commits worth recording
- 44b11300: `utf-8-sig` strips exactly one leading BOM; a double-BOM file still fails `json.loads`
  as before (same failure class, not a regression). Two of the four new tests (audit, pipeline)
  exercise the legacy `root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"` fallback of
  `default_quantlens_root`, so they will need re-homing if that fallback is ever removed.
- ec80222d: the `len(fields) <= len(header)` branch still zips short rows (missing trailing columns
  are silently absent) — pre-existing and untested; skipped rows are dropped without any count in
  the payload, so a future header drift would be invisible except as missing candidates.
- 79c77050: when `mtc_v2_root` is unconfigured the payload still says `"source": "Pipeline + Audit
  + MTC_V2 parity tracker"` with no explicit `mtc_v2_root_not_configured` reason, unlike
  `backtest_reader`/`registry_reader`. Cosmetic inconsistency only.
- f8fa3caf: `IBKR_PAPER_BRIDGE` is broker-adjacent (T0 by overlap); the lane itself says so. The
  full non-root Bridge suite claim (1393 passed) was not re-run by this lane.

## Probes executed (all read-only; scratch mutants under the session scratchpad)
1. `git merge --ff-only b42eb4e7` -> HEAD `b42eb4e7`, clean tree.
2. `git show --stat` / `--name-status` on all 14 commits -> file sets match stated scopes
   (plus each lane's HANDOFF/record notes, which are documentation, not code).
3. Dashboard suite `pytest tests -q` (apps/api) -> `129 passed, 1 subtests passed`.
4. `pytest mtc_cli/tests -q` -> `13 passed`; `pytest 11_TRIAGE/test_generate_index.py _deepseek_driver/tests -q` -> `56 passed`.
5. `python -m mtc_cli audit repo --json` -> `ok: true`, data
   `{memory_files_ok: true, git_staged_count: 0, heartbeat_age_minutes: null, handoff_next_actions: 1, handoff_waiting_for_owner: 0}`.
6. `generate_index.py --check` -> byte-identical OK.
7. `yaml.safe_load` on all 8 `parameter_library/**/*.yml` -> all `OK dict`.
8. `py_compile` of `overnight_extended_run.py`, `overnight_orchestrator.py`, `hyperliquid.py`,
   `extract_parameter_library_seeds.py` -> `COMPILE_OK`.
9. utf-8 vs utf-8-sig decode matrix (plain, leading BOM, mid-text BOM, invalid byte, double BOM x
   strict/replace/ignore) -> identical for every input without a leading BOM; differs only by the
   stripped leading BOM.
10. Old (`ec80222d^`) vs new `_candidate_csv_row` on 17/17, 15/17, 18/17, 19/17, 17-vs-16, 21-vs-20
    shapes -> SAME except the two misaligned shapes (old zip-truncated; new `None`); on the real
    registry CSV (17-column header, 14 rows, one 19-field row) -> old == new for all 14 rows.
11. `_newest_section` / `_handoff_waiting_for_owner_count` probes on the real governance HANDOFF and
    nine synthetic WAITING lines (results in the 361b6451 subsection).
12. Local-annotation probe: `def f(): x: UndefinedName = {}` runs without error -> the missing
    `Any` import in `hyperliquid.py:1644` was never a runtime fault.
13. Scratch-copy mutants: reverting `utf-8-sig`->`utf-8` in the four readers, disabling the
    registry length guard, and restoring the legacy `mtc_root` line -> 8 targeted tests FAIL, the
    positive registry test still passes (RED as required). Adding `GLOBAL_HANDOFF.md` back to the
    mtc_cli required list -> 2 fixture tests FAIL. Reverting the orchestrator join to `"\n"` ->
    emitted runner `PyCompileError`; unmutated scratch emit compiles and equals the committed runner.
14. Scan of 1,286 `11_TRIAGE` text files for undecodable/UTF-16/extra-separator content -> none.
15. `git status --short` after all runs -> empty (only ignored `__pycache__` artifacts created).

No file changed other than this record; acceptance still requires the exact T0–T2 audits.
