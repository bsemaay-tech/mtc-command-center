# Dashboard handoff

## Current state — 2026-08-25

- WP-P0-05 changes onboarding only; dashboard source and runtime are untouched.
- The accepted shell remains vanilla HTML/JS/CSS, dark command-center style, and read-only.
- OPEN-01 is still conditional: a bounded framework/build step may be considered only if WP-V2B-05
  measures less custom table/freshness code without weakening private/read-only/security boundaries.
- No build-step choice, deploy, network, broker, paper/live, or write capability is authorized here.

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
