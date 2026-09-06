# Dashboard handoff

## Current state — 2026-08-25

- WP-P0-05 changes onboarding only; dashboard source and runtime are untouched.
- The accepted shell remains vanilla HTML/JS/CSS, dark command-center style, and read-only.
- OPEN-01 is still conditional: a bounded framework/build step may be considered only if WP-V2B-05
  measures less custom table/freshness code without weakening private/read-only/security boundaries.
- No build-step choice, deploy, network, broker, paper/live, or write capability is authorized here.

## [Claude lane N] 2026-09-07 — MTC_V2 readiness root from path config (D12)

- `mcc_readonly/mtc_v2_reader.py::build_mtc_v2_readiness` no longer computes
  `mtc_root = root.parent / "01_MASTER TEMPLATE_V2"` unconditionally. It now
  resolves `mtc_v2_root` via `load_path_config()` +
  `resolve_configured_path(config, "mtc_v2_root")`, matching
  `backtest_reader.py`/`registry_reader.py`/`pine_builder_reader.py`/
  `liveops_reader.py`. When `mtc_v2_root` is unconfigured, `mtc_v2_root`,
  `pine_path`, `architecture_path` render `""`, `pine_exists`/
  `architecture_exists` render `false`, and `_read_mtc_v2_parity(None)`
  returns `{"path": "", "exists": false, "total_cases": 0, "pass_cases": 0}`
  — the same fail-closed shape it already returned for a missing directory.
  Readiness rows are unaffected (they only depend on pipeline/audit
  candidates). Schema keys and function signature unchanged.
- Evidence: `tests/test_mtc_v2_reader.py` rewritten — one test now builds a
  `00_CONFIG/paths.example.json` pointing `mtc_v2_root` at a temp migrated
  dir and asserts `readiness["mtc_v2_root"]` equals that configured path
  (RED against the pre-fix code: asserted the legacy sibling path instead;
  GREEN after). A new negative test asserts the exact unconfigured
  fail-closed shape above. Full suite (Linux, Python 3.12,
  `PYTHONUTF8=1 -p no:cacheprovider`): 122 passed (121 baseline + net +1).
  `ruff --select E9,F821,F811` clean on both changed files.
- Scope: only `mtc_v2_reader.py:18`, per lane L's recommendation. `paths.py:27`
  and the `mtc_v2_root/"06_QUANTLENS_LAB"` fallbacks in
  registry/backtest/pine_builder/liveops readers were left untouched —
  owner decision pending per
  `11_TRIAGE/OVERNIGHT_LANE_L_DASHBOARD_LEGACY_FALLBACKS_2026-09-07.md`.
- NEXT ACTION: none for this lane.
- WAITING FOR OWNER: Nothing.

## [Claude lane A] 2026-09-06 — test portability repair

- Test-only change under `apps/api/tests/`; no product code touched.
- `test_pipeline_reader.py`: `discovery_source` expectation now uses
  `str(Path("research") / "batch" / "FINAL_LLM_KNOWLEDGE_BASE.jsonl")` instead of a Windows literal.
- `test_audit_reader.py`: both `C:/TEMP/MTC_COMMAND_CENTER` fixtures replaced with
  `tempfile.TemporaryDirectory()` roots, so no literal `C:` directory is created inside `apps/api`.
- Evidence (Linux, Python 3.12, `PYTHONUTF8=1 -p no:cacheprovider`): RED = 1 failed on the
  separator assertion and a stray `apps/api/C:/...` tree after `test_audit_reader.py`; GREEN =
  `pytest tests -q` 121 passed, no `C:` directory; mutant `"X/" + str(...)` in
  `_relative_to_quantlens` fails the patched test and was reverted exactly.
- NEXT ACTION: none for this lane; run the suite on Windows once to confirm parity.
- WAITING FOR OWNER: Nothing.
