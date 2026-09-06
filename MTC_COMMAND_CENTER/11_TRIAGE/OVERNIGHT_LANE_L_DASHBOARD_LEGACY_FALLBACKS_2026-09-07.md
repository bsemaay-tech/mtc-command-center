# Lane L — dashboard legacy-path fallbacks (read-only review)

Scope: `MTC_COMMAND_CENTER/08_DASHBOARD_APP` (apps/api/mcc_readonly, tests, docs, launchers).
Read-only review per Lane E's finding that `mcc_readonly/paths.py:27` and
`mcc_readonly/mtc_v2_reader.py:18` carry legacy-layout fallback lookups. No source, test, or
launcher file was edited. No server was started.

## Hit table

Grep patterns: `01_MASTER TEMPLATE_V2`, `06_QUANTLENS_LAB`, `mtc_backtest`, `tradingview-lab`,
`TW_EXPORTS`, `05_PARITY`, scoped to `08_DASHBOARD_APP`.

No hits for `mtc_backtest`, `tradingview-lab`, or `TW_EXPORTS` anywhere under `08_DASHBOARD_APP`,
and no hits in any README/docs file. `START_DASHBOARD.bat` and `run_dashboard_server.ps1` carry no
legacy-layout string at all (see Launchers section).

| # | File:line | Excerpt | Kind |
|---|---|---|---|
| 1 | `mcc_readonly/paths.py:26-27` | `root / "06_QUANTLENS_LAB",` / `root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB",` | shared fallback list in `default_quantlens_root()` |
| 2 | `mcc_readonly/mtc_v2_reader.py:18` | `mtc_root = root.parent / "01_MASTER TEMPLATE_V2"` | sole (non-fallback) root for MTC_V2 readiness |
| 3 | `mcc_readonly/mtc_v2_reader.py:246` | `tracker = mtc_root / "05_PARITY" / "MTC_V2_PARITY_CASES.csv"` | parity CSV path, built on #2's root |
| 4 | `mcc_readonly/registry_reader.py:27` | `quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"` | fallback when `default_quantlens_root()` result is missing |
| 5 | `mcc_readonly/backtest_reader.py:31,34` | comment + `quantlens_root = mtc_v2_root / "06_QUANTLENS_LAB"` | same fallback pattern as #4 |
| 6 | `mcc_readonly/pine_builder_reader.py:47` | `promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` | reads under configured `mtc_v2_root`, legacy sub-path name |
| 7 | `mcc_readonly/liveops_reader.py:59` | `promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` | same pattern as #6 |
| 8 | `tests/test_mtc_v2_reader.py:14` | `mtc_root = Path(tmp) / "01_MASTER TEMPLATE_V2"` | pins #2 exactly (sibling-of-root layout) |
| 9 | `tests/test_audit_reader.py:79,137-152` | transcript/intake fixtures under `06_QUANTLENS_LAB/...` and `01_MASTER TEMPLATE_V2/06_QUANTLENS_LAB/...` | exercises `default_quantlens_root()` fallback (#1) via `audit_reader.py` |
| 10 | `tests/test_pipeline_reader.py:18-19,97,163-164,218-219` | same two-segment legacy fixture tree | exercises #1 via `pipeline_reader.py` |
| 11 | `tests/test_pine_builder_reader.py:19-20` | `mtc / "06_QUANTLENS_LAB" / ...` | exercises #6 |
| 12 | `tests/test_backtest_reader.py:20,118` | `mtc / "06_QUANTLENS_LAB" / "05_BACKTEST_RESULTS"` | exercises #5 |
| 13 | `tests/test_liveops_reader.py:19` | `mtc / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY" / "QL_ALPHA"` | exercises #7 |
| 14 | `tests/test_registry_reader.py:20,35` | `lab = mtc / "06_QUANTLENS_LAB"` (+ CSV cell referencing the same relative path) | exercises #4 |

`05_PARITY` hits in `test_pine_builder_reader.py:62`, `test_backtest_reader.py:150`,
`test_optimization_reader.py:73`, `test_liveops_reader.py:85`, `test_registry_reader.py:82`, and
`test_mtc_v2_reader.py:17-18` are **not legacy markers** — `05_PARITY` is a real subfolder name
under the *migrated* `01_MTC_PROJECT` tree too (`MTC_COMMAND_CENTER/01_MTC_PROJECT/05_PARITY`
exists in this checkout), so these are fixture paths for whichever `mtc_v2_root` the test wires
up, legacy or migrated. Only the *parent* segment (`01_MASTER TEMPLATE_V2` vs the configured
`01_MTC_PROJECT`) carries migration meaning.

## Runtime analysis

**Resolution order for `mcc_root` and `mtc_v2_root`.** `default_mcc_root()`
(`paths.py:18-19`) is `Path(__file__).resolve().parents[4]` — always the on-disk
`MTC_COMMAND_CENTER` directory the code is running from, never configurable. `mtc_v2_root` for
`registry_reader.py`, `backtest_reader.py`, `pine_builder_reader.py`, and `liveops_reader.py`
comes from `load_path_config()` → `00_CONFIG/paths.local.json` (falling back to
`paths.example.json`), i.e. from `resolve_configured_path(config, "mtc_v2_root")`. Both
`00_CONFIG/paths.example.json` and `paths.local.example.json` in this repo set
`mtc_v2_root` to `.../MTC_COMMAND_CENTER/01_MTC_PROJECT` — the migrated location. So on a
correctly configured checkout, `mtc_v2_root` in readers #4–#7 is already the migrated path, and
`.../06_QUANTLENS_LAB` appended to it is a **subfolder that does not exist under `01_MTC_PROJECT`**
— a dead branch, not a route to the frozen repo.

**`default_quantlens_root()` (paths.py:22-36, hit #1).** Builds three candidates in order:
`root/"03_QUANTLENS"` (migrated), `root/"06_QUANTLENS_LAB"` (would be inside
`MTC_COMMAND_CENTER` itself — never valid in either layout), and
`root.parent/"01_MASTER TEMPLATE_V2"/"06_QUANTLENS_LAB"`. It picks the first candidate that
**exists and is non-empty**; in this checkout `03_QUANTLENS` exists and has content
(`00_INBOX_REPORTS`, `05_BACKTEST_RESULTS`, `06_PROMOTED_TO_PARITY`, …), so it wins immediately
and the other two candidates are never reached. The fallback only fires if `03_QUANTLENS` is
missing or empty (e.g. a partial checkout) or the caller's `root` isn't the true `mcc_root`.

**`mtc_v2_reader.py:18` (hit #2) — the one true unconditional hard-code.** Unlike #4-#7, this is
*not* a fallback guarded by an existence check and it never calls `load_path_config()`. It always
computes `mtc_root = root.parent / "01_MASTER TEMPLATE_V2"` and uses that for `pine_path`,
`architecture_path`, and (via #3) the parity CSV, regardless of what `paths.local.json` says
`mtc_v2_root` is. So MTC_V2 readiness data is the one dashboard panel that structurally ignores
the migrated config and always looks for a directory literally named `01_MASTER TEMPLATE_V2`
sitting **next to** `MTC_COMMAND_CENTER` (i.e. `<checkout>/01_MASTER TEMPLATE_V2`, not inside it).

**Does any of this read the frozen repo `C:\LAB\tradingview-lab`?** No path computed anywhere in
`08_DASHBOARD_APP` resolves to `C:\LAB\tradingview-lab`. `default_mcc_root()` is always derived
from where the running code physically sits (inside the canonical checkout, e.g.
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER`), so `root.parent` in hit #2 is
`C:\LAB\Tradingview_LAB_CLEAN`, not `C:\LAB\tradingview-lab` — a different top-level directory.
The configured `mtc_v2_root` in both path-config files is likewise
`C:\LAB\Tradingview_LAB_CLEAN\MTC_COMMAND_CENTER\01_MTC_PROJECT`. None of hits #1–#7 can address
the frozen sibling checkout by construction.

What they **can** do is read a **stray, legacy-named directory left inside the canonical
checkout** if the owner's real `C:\LAB\Tradingview_LAB_CLEAN` still has an un-deleted
`01_MASTER TEMPLATE_V2` (sibling of `MTC_COMMAND_CENTER`) or a `06_QUANTLENS_LAB` folder under
`01_MTC_PROJECT` left over from before/during the migration. This repo checkout has neither (only
`03_QUANTLENS` and `01_MTC_PROJECT` exist), so the fallback is dead code here; whether it is dead
on the owner's actual Windows machine cannot be verified from this sandbox — that is exactly the
condition an owner check should confirm. If such a leftover exists, the failure mode is **silent
staleness** (old pre-migration data rendered as if current), not a read of the frozen repo, and not
a crash — readers degrade to "not found" (`_empty_status`/`_empty_registry`) only when *no*
candidate, legacy or migrated, exists.

**When both legacy and migrated paths are absent (today's normal owner state for hit #2/#3):**
`mtc_v2_reader.py` renders `pine_exists: false`, `architecture_exists: false`, and
`parity_tracker: {"exists": false, "total_cases": 0, "pass_cases": 0}` — a fail-closed, explicit
"missing" state consistent with `08_DASHBOARD_APP/AGENTS.md`'s "never render absence ... as
PASS/healthy" rule. For #4–#7, when neither the migrated nor legacy quantlens path exists, callers
return `_empty_registry(...)` / `_empty_status(...)` carrying the attempted path string, also
fail-closed.

**Tests pinning this behavior.** `test_mtc_v2_reader.py` pins hit #2's exact legacy-sibling
computation (it never exercises a migrated-path variant, so there is currently no regression test
proving `mtc_v2_reader.py` also works against `01_MTC_PROJECT`). `test_audit_reader.py` and
`test_pipeline_reader.py` pin the `default_quantlens_root()` fallback (hit #1) through
`audit_reader.py`/`pipeline_reader.py`. `test_registry_reader.py`, `test_backtest_reader.py`,
`test_pine_builder_reader.py`, and `test_liveops_reader.py` each pin their respective
`mtc_v2_root / "06_QUANTLENS_LAB"` fallback (hits #4, #5, #6, #7) by constructing a fixture tree
under a `mtc` temp directory with no `03_QUANTLENS` sibling, forcing the fallback branch.

## Launchers — hard-coded paths

- `START_DASHBOARD.bat:7` hard-codes `C:\LAB\MTC_CHATGPT_MENTOR_BUNDLES\2026-06-22\tunnel_logs` as
  the Cloudflare tunnel log directory. This is unrelated to the legacy-layout patterns (no hit on
  any of the six greps) but is a machine-specific absolute path baked into a checked-in launcher;
  it will simply fail to `mkdir` gracefully or write logs to a path that may not exist on another
  machine — it does not gate startup (the `if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"` line creates
  it if missing).
- `START_DASHBOARD.bat:16` hard-codes the WinGet `cloudflared.exe` install path as a fallback when
  `cloudflared` is not on `PATH` — a legitimate, guarded fallback (checks `if not exist` and prints
  an install hint), not a legacy-repo reference.
- `run_dashboard_server.ps1` has no hard-coded absolute paths; it uses `$PSScriptRoot`-relative
  resolution only.
- Neither launcher references `01_MASTER TEMPLATE_V2`, `06_QUANTLENS_LAB`, `mtc_backtest`,
  `tradingview-lab`, or `TW_EXPORTS`.

## Proposal (owner-decidable)

**Option A — remove legacy fallbacks, always resolve from config/migrated layout.**

Exact lines to change:
- `mcc_readonly/paths.py:22-36` — drop the `root/"06_QUANTLENS_LAB"` and
  `root.parent/"01_MASTER TEMPLATE_V2"/"06_QUANTLENS_LAB"` candidates from
  `default_quantlens_root()`; keep only `root/"03_QUANTLENS"` (optionally add a config-driven
  override so a non-standard checkout can still point elsewhere explicitly, e.g. a
  `quantlens_root` key in `paths.local.json`, instead of guessing a legacy directory name).
- `mcc_readonly/mtc_v2_reader.py:17-18` — replace the hard-coded
  `root.parent / "01_MASTER TEMPLATE_V2"` with the configured `mtc_v2_root`
  (`load_path_config()` + `resolve_configured_path(config, "mtc_v2_root")`), matching the pattern
  already used by `registry_reader.py`/`backtest_reader.py`/`pine_builder_reader.py`/
  `liveops_reader.py`. `build_mtc_v2_readiness()` would need an `mtc_v2_root` fallback branch to
  `_empty_status`-style output when `mtc_v2_root` is unconfigured, for parity with the other
  readers.
- `mcc_readonly/registry_reader.py:24-29`, `backtest_reader.py:26-34`,
  `pine_builder_reader.py:47`, `liveops_reader.py:59` — change the sub-path segment from
  `"06_QUANTLENS_LAB"` to `"03_QUANTLENS"` (matching the migrated tree) or drop the fallback
  entirely and rely solely on `default_quantlens_root()`.

Diff sketch (illustrative, not applied):

```diff
--- a/mcc_readonly/paths.py
+++ b/mcc_readonly/paths.py
@@ def default_quantlens_root(mcc_root):
-    candidates = [
-        root / "03_QUANTLENS",
-        root / "06_QUANTLENS_LAB",
-        root.parent / "01_MASTER TEMPLATE_V2" / "06_QUANTLENS_LAB",
-    ]
+    candidates = [root / "03_QUANTLENS"]

--- a/mcc_readonly/mtc_v2_reader.py
+++ b/mcc_readonly/mtc_v2_reader.py
@@ def build_mtc_v2_readiness(mcc_root=None, ...):
-    root = canonicalize(mcc_root or default_mcc_root())
-    mtc_root = root.parent / "01_MASTER TEMPLATE_V2"
+    root = canonicalize(mcc_root or default_mcc_root())
+    path_config = load_path_config(root)
+    mtc_root = resolve_configured_path(path_config.config, "mtc_v2_root")
+    if mtc_root is None:
+        return _empty_readiness("mtc_v2_root_not_configured")
```

Tests that would need to change: `test_mtc_v2_reader.py:14` (fixture must build
`01_MTC_PROJECT`-shaped tree, or pass `mtc_v2_root` explicitly, and cover the
"unconfigured" empty case); `test_audit_reader.py:76-200-ish` and
`test_pipeline_reader.py:12-230-ish` (rewrite legacy fixture trees to a `03_QUANTLENS`-shaped
tree — a mechanical rename of directory literals, no assertion logic changes expected);
`test_registry_reader.py`, `test_backtest_reader.py`, `test_pine_builder_reader.py`,
`test_liveops_reader.py` (rename `"06_QUANTLENS_LAB"` fixture segments to `"03_QUANTLENS"` in
their `mtc_v2_root`-relative setups, or restructure the fixture so the primary
`default_quantlens_root()` candidate is what's exercised).

**Option B — keep the fallback, but log/flag when it fires.**

Add a `warnings` entry (mirroring `PathConfig.warnings`) whenever `default_quantlens_root()` or
`mtc_v2_reader.py` actually resolves through the legacy branch (not just when nothing exists), and
surface it in `/api/read-model` so a stale/legacy read is visible in the dashboard rather than
silent. Minimal-diff, but leaves the double-meaning of "01_MASTER TEMPLATE_V2"/"06_QUANTLENS_LAB"
in source and tests indefinitely, and still cannot distinguish "reading a stray leftover legacy
folder in the canonical checkout" from "correctly falling through because migration is genuinely
incomplete on this machine" — the flag would fire in both cases.

**Recommendation.** Prefer Option A for `mtc_v2_reader.py:18` specifically, since it is not a
guarded fallback at all — it is the *only* path used and it silently diverges from every other
reader's config-driven resolution, which is a correctness bug independent of the legacy-layout
question. For the shared `default_quantlens_root()` fallback (paths.py:27) and the
`mtc_v2_root/"06_QUANTLENS_LAB"` fallbacks (registry/backtest/pine_builder/liveops), Option A is
still preferred once the owner confirms no live checkout still has legacy-named directories in
active use, since keeping them costs five files' worth of double-meaning path logic and test
fixtures for a migration that root `AGENTS.md`/`DECISIONS.md` already treat as final; Option B is
the safer interim if the owner is not yet certain every relevant machine has been fully migrated.

**Risk.** Low for Option A: removing the fallback cannot start reading the frozen repo (it never
could), so the only regression risk is a real, currently-relied-upon legacy directory going dark,
which would show up immediately as an explicit "not found"/empty dashboard state (fail-closed by
design) rather than a wrong-but-plausible value. Recommend the owner confirm on the real machine
that `01_MTC_PROJECT`/`03_QUANTLENS` are fully populated and no sibling `01_MASTER TEMPLATE_V2` or
nested `06_QUANTLENS_LAB` directories remain before merging Option A.

## Commands executed

```
git log --oneline -1
git merge-base --is-ancestor 31e975f1 HEAD
git merge --ff-only 31e975f1
grep -rn -E "01_MASTER TEMPLATE_V2|06_QUANTLENS_LAB|mtc_backtest|tradingview-lab|TW_EXPORTS|05_PARITY" MTC_COMMAND_CENTER/08_DASHBOARD_APP
grep -rn "tradingview-lab" MTC_COMMAND_CENTER/08_DASHBOARD_APP
grep -rn "TW_EXPORTS" MTC_COMMAND_CENTER/08_DASHBOARD_APP
grep -rn -E "..." MTC_COMMAND_CENTER/08_DASHBOARD_APP --include="*.md"
find MTC_COMMAND_CENTER/08_DASHBOARD_APP -iname "START_DASHBOARD.bat" -o -iname "run_dashboard_server.ps1"
find . -maxdepth 2 -iname "*MASTER TEMPLATE*"
ls MTC_COMMAND_CENTER/03_QUANTLENS ; test -d MTC_COMMAND_CENTER/06_QUANTLENS_LAB
find MTC_COMMAND_CENTER/01_MTC_PROJECT -maxdepth 1 -type d
Read: paths.py, mtc_v2_reader.py, registry_reader.py, backtest_reader.py, pine_builder_reader.py,
liveops_reader.py, audit_reader.py, pipeline_reader.py (grep -n on the latter two),
paths.example.json, paths.local.example.json, START_DASHBOARD.bat, run_dashboard_server.ps1,
test_mtc_v2_reader.py, test_audit_reader.py, test_pipeline_reader.py, test_registry_reader.py,
test_backtest_reader.py (fixture helper _write_paths)
```

No source changed; no server started.
