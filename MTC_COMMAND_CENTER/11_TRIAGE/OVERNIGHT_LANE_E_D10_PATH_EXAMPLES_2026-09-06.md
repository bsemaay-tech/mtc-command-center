# Lane E — canonical path examples (D10)

## Scope

D10 / T2: repoint `MTC_COMMAND_CENTER/00_CONFIG/paths.example.json` and
`paths.local.example.json` from the frozen legacy checkout
(`C:/LAB/tradingview-lab/...`, pre-migration `01_MASTER TEMPLATE_V2` layout)
to the canonical checkout (`C:\LAB\Tradingview_LAB_CLEAN`) and the
post-migration `MTC_COMMAND_CENTER` layout, per root `AGENTS.md` and the
`.gitignore` migration-prefix-rewrite header. This is a resumed session; a
previous worker was interrupted by an API limit after drafting the two JSON
files. This session verified the previous worker's draft values against the
repo rather than trusting them, deleted the stray test-defect directory, ran
before/after evidence, and committed.

## Preflight

- `git status --porcelain` (session start): two modified JSON files (previous
  worker's draft) plus an untracked stray
  `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/C:/` directory created by a
  known test defect (health-check / `test_audit_reader.py` writing a literal
  `C:/...` path segment on Linux). Deleted with `rm -rf` and never staged;
  recreated and deleted twice more after the before/after health runs and the
  pytest run, per the known-defect note in the task brief.
- Branch: `worktree-agent-ad07e265cd9731b3c`, HEAD `afe52ea89473300e25555325def111cac599bdf1` (unchanged before this lane's commit).

## Verification table — value → existing repo path

| Key | Final value (path suffix under mcc_root) | Verified against |
|---|---|---|
| `mcc_root` | `C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER` | Root `AGENTS.md` lines 3-5: "The canonical checkout is `C:\LAB\Tradingview_LAB_CLEAN`; ... The sibling `C:\LAB\tradingview-lab` is frozen legacy: do not read its onboarding, run it, or edit it." This repo *is* the `MTC_COMMAND_CENTER` subtree of that checkout. |
| `mtc_v2_root` | `.../MTC_COMMAND_CENTER/01_MTC_PROJECT` | `.gitignore` header: `01_MASTER TEMPLATE_V2/ → MTC_COMMAND_CENTER/01_MTC_PROJECT/`. Confirmed on disk: `MTC_COMMAND_CENTER/01_MTC_PROJECT/00_PYTHON/mtc_v2` exists (`find` hit), so `01_MTC_PROJECT` is the directory that holds the MTC_V2 project (its parent via `00_PYTHON/mtc_v2`), matching the old `mtc_v2_root` semantics (old value pointed at `01_MASTER TEMPLATE_V2` itself, which the rewrite table maps 1:1 to `01_MTC_PROJECT`). |
| `pinets_root` | `.../MTC_COMMAND_CENTER/12_PARITY_PINETS` | `MTC_COMMAND_CENTER/12_PARITY_PINETS/AGENTS.md` line 1-4: "# PineTS parity stage rules — This stage owns PineTS parity tooling/corpora outside the MTC-project-local cases. Parity artifacts, oracles, tolerances, and behavior are protected..." — confirmed this is the parity/PineTS stage. |
| `tradingview_exports_dir` | `.../MTC_COMMAND_CENTER/12_PARITY_PINETS/TW_EXPORT_CASES_V2` | `git ls-files \| grep -i tw_export` shows TWO tracked `TW_EXPORT_CASES_V2` trees: (a) `MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY/TW_EXPORT_CASES_V2` (325 files, all placeholders — `PLACE_EXPORT_XLSX_HERE.txt` / `case_plan.json` only, no real exports; `git log` last touch = the initial `2026-05-31` migration-as-is commit, never updated since) and (b) `MTC_COMMAND_CENTER/12_PARITY_PINETS/TW_EXPORT_CASES_V2` (488 files, including real `.xlsx` TradingView export files in dozens of case folders; `git log` last touch = `2026-07-05` "parity migration" commit). (b) is the actively-used, post-migration location; (a) is a stale pre-migration leftover never populated since the initial migration commit (also independently confirmed stale/superseded by `MTC_COMMAND_CENTER/11_TRIAGE/WP_P0_01_INVENTORY_2026-08-24/parity_dirs_resolution.md`, which as of 2026-08-24 already found `05_PARITY` empty and all real files only under `12_PARITY_PINETS`). Chose (b): it is both "tracked" and "the migrated equivalent under 12_PARITY_PINETS" per the task's two acceptance branches — they coincide here. |
| `reports_root` | `.../MTC_COMMAND_CENTER/04_REPORTS` | `MTC_COMMAND_CENTER/04_REPORTS` exists at top level (`ls MTC_COMMAND_CENTER`). Also confirmed by reader code: `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/server.py:118` computes `reports_root = (root / "04_REPORTS").resolve(strict=False)` — exact match. |

`schema_version` (`"1.0"`), key set (7 keys, same order), and
`mtc_v2_python_exe: null` are unchanged in both files, in both the previous
worker's draft and this session's confirmation.

## PATHS_RESOLUTION.md

`grep -n -i "tradingview-lab\|01_MASTER TEMPLATE_V2\|mtc_backtest/\|06_QUANTLENS_LAB" MTC_COMMAND_CENTER/00_CONFIG/PATHS_RESOLUTION.md` — **no matches**. The file does not name the legacy path, so no edit was needed there (task said "fix it only if it names one").

## Evidence — dashboard `mcc_readonly` health check (before / after)

Command (both runs): `python -m mcc_readonly --mcc-root <worktree>/MTC_COMMAND_CENTER health`, run from `<worktree>/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api`, using venv312 with `PYTHONUTF8=1`. BEFORE was captured by `git stash` on the two JSON files (restoring the previous worker's original — i.e. legacy — draft is not applicable here since the draft was already the *new* value; instead BEFORE reflects the committed-HEAD content of the two files, which still has the legacy values, via stash of the working-tree edits), then `git stash pop` to restore the fix.

**BEFORE** (`path_checks` excerpt, legacy values in effect):
```json
"mcc_root": {
  "configured": true, "resolvable": true, "exists": false,
  "path": ".../apps/api/C:/LAB/tradingview-lab/MTC_COMMAND_CENTER"
},
"mtc_v2_root": {
  "path": ".../apps/api/C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2"
},
"pinets_root": {
  "path": ".../apps/api/C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/05_PARITY"
},
"tradingview_exports_dir": {
  "path": ".../apps/api/C:/LAB/tradingview-lab/01_MASTER TEMPLATE_V2/05_PARITY/TW_EXPORTS"
},
"reports_root": {
  "path": ".../apps/api/C:/LAB/tradingview-lab/MTC_COMMAND_CENTER/04_REPORTS"
}
```
(`overall_ok: false`, `mtc_v2_root_reachable: false` — expected on Linux since these are Windows `C:/` paths joined onto the Linux cwd; `exists: false` for every entry both before and after, honestly, since the tool always joins the configured path under the current working directory when it's not an absolute POSIX path.)

**AFTER** (`path_checks` excerpt, fixed values in effect):
```json
"mcc_root": {
  "configured": true, "resolvable": true, "exists": false,
  "path": ".../apps/api/C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER"
},
"mtc_v2_root": {
  "path": ".../apps/api/C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/01_MTC_PROJECT"
},
"pinets_root": {
  "path": ".../apps/api/C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/12_PARITY_PINETS"
},
"tradingview_exports_dir": {
  "path": ".../apps/api/C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/12_PARITY_PINETS/TW_EXPORT_CASES_V2"
},
"reports_root": {
  "path": ".../apps/api/C:/LAB/Tradingview_LAB_CLEAN/MTC_COMMAND_CENTER/04_REPORTS"
}
```
`exists: false` for all entries on both runs (Linux sandbox has no `C:/LAB/...` filesystem) — the point of the AFTER run is that the paths now *name* the canonical `Tradingview_LAB_CLEAN` checkout and the correct post-migration `MTC_COMMAND_CENTER` subtree names (`01_MTC_PROJECT`, `12_PARITY_PINETS`, `TW_EXPORT_CASES_V2`, `04_REPORTS`), not that they resolve on this Linux box. `overall_ok` stays `false` for the same reason as BEFORE (Windows-rooted path, non-Windows sandbox) — no regression.

The stray `apps/api/C:/` directory the health command writes on Linux (component of the known test defect fixed by another lane) was deleted with `rm -rf` immediately after each of the two health runs and again after the pytest run below; it was never staged.

## Evidence — full dashboard pytest suite

`python -m pytest tests -q -p no:cacheprovider` from `<worktree>/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api`, venv312, `PYTHONUTF8=1`:

```
FAILED tests/test_pipeline_reader.py::PipelineReaderTests::test_discovers_extra_quantlens_jsonl_candidates
1 failed, 120 passed, 1 subtests passed in 4.22s
```

Matches the expected outcome named in the task brief exactly: the one failure
is the known pre-existing Windows-separator assertion defect
(`assertEqual(..., "research\\batch\\FINAL_LLM_KNOWLEDGE_BASE.jsonl")` against
a POSIX-separator actual value `research/batch/FINAL_LLM_KNOWLEDGE_BASE.jsonl`)
in `test_pipeline_reader.py`, owned by another lane. `test_audit_reader.py`'s
stray-`C:/`-directory defect did not manifest as a failure but did recreate
the stray directory as a side effect of running; it was deleted afterward.
No other test failed or errored.

## JSON / diff sanity

- `python -c "json.load(...)"` on both files: **OK**, same 7-key set
  (`schema_version`, `mcc_root`, `mtc_v2_root`, `mtc_v2_python_exe`,
  `pinets_root`, `tradingview_exports_dir`, `reports_root`) in both files.
- `git diff --check -- MTC_COMMAND_CENTER/00_CONFIG/paths.example.json MTC_COMMAND_CENTER/00_CONFIG/paths.local.example.json` — clean (exit 0, no output).

## Remaining legacy references (reported only — not edited; out of this task's scope)

Grep of `MTC_COMMAND_CENTER/08_DASHBOARD_APP` (dashboard code/tests/docs) for
`tradingview-lab` and `01_MASTER TEMPLATE_V2`:

- `git grep -l -i "tradingview-lab" -- MTC_COMMAND_CENTER/08_DASHBOARD_APP` → **no hits**.
- `git grep -l "01_MASTER TEMPLATE_V2" -- MTC_COMMAND_CENTER/08_DASHBOARD_APP` → 5 files, all legacy-layout *fallback* lookups (candidate paths a reader tries and skips if absent), not example/config values:
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/mtc_v2_reader.py:18` — `mtc_root = root.parent / "01_MASTER TEMPLATE_V2"` (fallback candidate)
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/paths.py:27` — `root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB"` (fallback candidate in `default_quantlens_root`)
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_audit_reader.py:136,150`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_mtc_v2_reader.py:14`
  - `MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/tests/test_pipeline_reader.py:18,163,215`

Repo-wide (all tracked files, for context only — well outside this task's
scope, not touched): `git grep -c -i "tradingview-lab"` hits **1066** distinct
files; `git grep -c "01_MASTER TEMPLATE_V2"` hits **787** distinct files.
These are almost entirely historical docs, audit prompts, handoff packages,
and triage records (e.g. `MTC_COMMAND_CENTER/01_MTC_PROJECT/03_DOCS/HANDOFF.md`,
`04_AUDIT/*.md`, `01_MTC_PROJECT/00_PYTHON/update_parity_files.py`,
`update_tracker.py`) that quote or reference the legacy path historically;
none were in scope for this D10/T2 task and none were edited.

## Deviations from the brief

None. The previous worker's draft values were verified correct against the
repo (with one additional cross-check the brief didn't strictly require: the
"05_PARITY" duplicate `TW_EXPORT_CASES_V2` tree was checked file-by-file
against the `12_PARITY_PINETS` one to make sure the chosen value was the
real, actively-used export directory and not a stale duplicate — see the
`tradingview_exports_dir` row above) and committed as-is; no value needed to
change.

## NEXT ACTION

None for this lane — D10/T2 is complete: both example JSON files point at
the canonical `Tradingview_LAB_CLEAN` / `MTC_COMMAND_CENTER` layout, evidence
matches the brief's expected outcome exactly, and the commit is made. The
dashboard code's own legacy-layout *fallback* candidates
(`mtc_v2_reader.py:18`, `paths.py:27`) and their tests are pre-existing,
functioning fallback logic, not defects introduced or required by this task;
whether to prune those fallbacks is a separate, out-of-scope decision for
whoever owns the dashboard reader code next.

## WAITING FOR OWNER

Nothing.
