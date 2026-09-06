# Lane W — promoted-strategy reads resolved from the QuantLens root (D18)

Scope: `mcc_readonly/pine_builder_reader.py::_compile_observations` and
`mcc_readonly/liveops_reader.py::_paper_trade_plans`. Builds directly on Lane V's decision packet
(`OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md`, rows 18/20, Group B, Option A —
implemented exactly as recommended there).

## Where the data lives (evidence)

`git ls-files | grep -E "PINE_PARITY_PLAN.md|FORWARD_PAPER_TRADE_PLAN.md"` returns only:

```
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG001_ql_alpha_ada_two_candle_sr_1h/FORWARD_PAPER_TRADE_PLAN.md
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG001_ql_alpha_ada_two_candle_sr_1h/PINE_PARITY_PLAN.md
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG002_ql_alpha_link_8ema_1h/FORWARD_PAPER_TRADE_PLAN.md
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG002_ql_alpha_link_8ema_1h/PINE_PARITY_PLAN.md
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG003_ql_alpha_ltc_rsi_oversold_1h/FORWARD_PAPER_TRADE_PLAN.md
MTC_COMMAND_CENTER/03_QUANTLENS/strategies/STG003_ql_alpha_ltc_rsi_oversold_1h/PINE_PARITY_PLAN.md
```

Depth is exactly `strategies/<id>/<file>` (one level under `strategies/`), so the existing
`*/PINE_PARITY_PLAN.md` / `*/FORWARD_PAPER_TRADE_PLAN.md` glob (single `*`, not `*/**/`) still
matches unchanged once rooted at the correct parent. Neither reader module had any legacy-fallback
pattern already (both `mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` lines were
unconditional, no existence-gated alternate), so per the task brief no legacy fallback was
introduced — the migrated location is now the only candidate, matching the module's prior
(lack of) fallback style.

## Fix

Both `_compile_observations` and `_paper_trade_plans` gained a second parameter, `mcc_root: Path`
(callers already had `root` in scope and now pass it through unchanged otherwise). Each now computes
`promoted_root = default_quantlens_root(mcc_root) / "strategies"` instead of
`mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"` — mirroring the existing
`_promoted_dir()` pattern in `pipeline_reader.py` and `registry_reader.py:203`. The
`compile_observation_path` / `relative_path` fields now render relative to `mcc_root` (via the
existing generic `_relative_to_mtc` helper, unchanged) instead of `mtc_v2_root`, since the promoted
plan files no longer live under `mtc_v2_root` at all. `mtc_v2_root` remains a parameter of both
functions (extended, not replaced, per the task brief) even though it is no longer read inside
`_compile_observations`/`_paper_trade_plans` bodies; `liveops_reader.py`'s existing
`mtc_v2_root and mtc_v2_root.exists()` call-site guard is unchanged. Returned schema (keys) is
unchanged in both functions; fail-closed behaviour for a missing `strategies` directory is preserved
(`{}` / `[]`).

Diff (full, both files):

```diff
--- a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py
+++ b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py
@@ -5,7 +5,13 @@ from datetime import datetime, timezone
 from pathlib import Path
 from typing import Any
 
-from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path
+from .paths import (
+    canonicalize,
+    default_mcc_root,
+    default_quantlens_root,
+    load_path_config,
+    resolve_configured_path,
+)
 
 
 def build_liveops_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
@@ -13,7 +19,7 @@ def build_liveops_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
     status = _read_status_file(root / "03_STATUS" / "LIVEOPS_STATUS.json")
     path_config = load_path_config(root)
     mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
-    paper_plans = _paper_trade_plans(mtc_v2_root) if mtc_v2_root and mtc_v2_root.exists() else []
+    paper_plans = _paper_trade_plans(mtc_v2_root, root) if mtc_v2_root and mtc_v2_root.exists() else []
     safety_gates = _safety_gates(status)
 
     return {
@@ -55,8 +61,13 @@ def _read_status_file(path: Path) -> dict[str, Any]:
     return raw if isinstance(raw, dict) else {}
 
 
-def _paper_trade_plans(mtc_v2_root: Path) -> list[dict[str, Any]]:
-    promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"
+def _paper_trade_plans(mtc_v2_root: Path, mcc_root: Path) -> list[dict[str, Any]]:
+    # Promoted-strategy plan docs (FORWARD_PAPER_TRADE_PLAN.md) live under the
+    # migrated QuantLens root (03_QUANTLENS/strategies/<id>/...), not under
+    # mtc_v2_root. See
+    # MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md
+    # (rows 18/20, Group B) for the confirmed migrated location.
+    promoted_root = default_quantlens_root(mcc_root) / "strategies"
     if not promoted_root.exists():
         return []
 
@@ -71,7 +82,7 @@ def _paper_trade_plans(mtc_v2_root: Path) -> list[dict[str, Any]]:
                 "webhook_enabled": False,
                 "title": _markdown_title(path),
                 "source_path": str(path),
-                "relative_path": _relative_to_mtc(path, mtc_v2_root),
+                "relative_path": _relative_to_mtc(path, mcc_root),
                 "updated_at": _timestamp(stat.st_mtime),
             }
         )
diff --git a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py
@@ -5,7 +5,13 @@ from datetime import datetime, timezone
 from pathlib import Path
 from typing import Any
 
-from .paths import canonicalize, default_mcc_root, load_path_config, resolve_configured_path
+from .paths import (
+    canonicalize,
+    default_mcc_root,
+    default_quantlens_root,
+    load_path_config,
+    resolve_configured_path,
+)
 
 
 MAX_DRAFTS = 80
@@ -20,7 +26,7 @@ def build_pine_builder_status(mcc_root: str | Path | None = None) -> dict[str, A
     if not mtc_v2_root.exists():
         return _empty_status(str(mtc_v2_root))
 
-    observations = _compile_observations(mtc_v2_root)
+    observations = _compile_observations(mtc_v2_root, root)
     pine_files = sorted(mtc_v2_root.rglob("*.pine"))
     protected_core_files = [path for path in pine_files if _is_protected_core(path, mtc_v2_root)]
     draft_paths = [path for path in pine_files if _is_review_draft(path, mtc_v2_root)]
@@ -43,8 +49,12 @@ def build_pine_builder_status(mcc_root: str | Path | None = None) -> dict[str, A
     }
 
 
-def _compile_observations(mtc_v2_root: Path) -> dict[str, dict[str, Any]]:
-    promoted_root = mtc_v2_root / "06_QUANTLENS_LAB" / "06_PROMOTED_TO_PARITY"
+def _compile_observations(mtc_v2_root: Path, mcc_root: Path) -> dict[str, dict[str, Any]]:
+    # Promoted-strategy plan docs (PINE_PARITY_PLAN.md) live under the migrated
+    # QuantLens root (03_QUANTLENS/strategies/<id>/...), not under mtc_v2_root.
+    # See MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md
+    # (rows 18/20, Group B) for the confirmed migrated location.
+    promoted_root = default_quantlens_root(mcc_root) / "strategies"
     if not promoted_root.exists():
         return {}
 
@@ -58,7 +68,7 @@ def _compile_observations(mtc_v2_root: Path) -> dict[str, dict[str, Any]]:
             "candidate_id": candidate_id,
             "compile_status": compile_status,
             "chart_status": chart_status,
-            "compile_observation_path": _relative_to_mtc(plan_path, mtc_v2_root),
+            "compile_observation_path": _relative_to_mtc(plan_path, mcc_root),
             "updated_at": _timestamp(plan_path.stat().st_mtime),
         }
     return observations
```

## Tests (D026)

`tests/test_pine_builder_reader.py`: existing `test_classifies_review_drafts_and_compile_observations`
updated — `PINE_PARITY_PLAN.md` fixture moved from
`mtc/"06_QUANTLENS_LAB"/"06_PROMOTED_TO_PARITY"/"QL_ALPHA"` to
`root/"03_QUANTLENS"/"strategies"/"QL_ALPHA"` (this test now fails without the move, since the
candidate_id join key still has to match the drafts discovered under `mtc_v2_root`). Two new tests
added: `test_compile_observations_discovered_from_quantlens_strategies_root` (regression — builds a
temp root with `03_QUANTLENS/strategies/STG001/PINE_PARITY_PLAN.md` and no `06_QUANTLENS_LAB`
anywhere, asserts `compile_status`/`chart_status` join correctly) and
`test_compile_observations_empty_when_quantlens_strategies_root_missing` (negative — asserts
`UNKNOWN`/`NOT_OBSERVED` fail-closed defaults when the `strategies` dir is absent).

`tests/test_liveops_reader.py`: existing `test_reads_disabled_status_and_paper_plans` updated the
same way (fixture moved to `root/"03_QUANTLENS"/"strategies"/"QL_ALPHA"`). Two new tests added:
`test_paper_trade_plans_discovered_from_quantlens_strategies_root` (regression) and
`test_paper_trade_plans_empty_when_quantlens_strategies_root_missing` (negative, asserts `[]`).

### RED (stashed the two reader-source fixes, kept the updated tests; `pytest tests/test_pine_builder_reader.py tests/test_liveops_reader.py -v`)

```
FAILED tests/test_pine_builder_reader.py::PineBuilderReaderTests::test_classifies_review_drafts_and_compile_observations
FAILED tests/test_pine_builder_reader.py::PineBuilderReaderTests::test_compile_observations_discovered_from_quantlens_strategies_root
  AssertionError: 'UNKNOWN' != 'PASS'
FAILED tests/test_liveops_reader.py::LiveOpsReaderTests::test_paper_trade_plans_discovered_from_quantlens_strategies_root
  AssertionError: 0 != 1
FAILED tests/test_liveops_reader.py::LiveOpsReaderTests::test_reads_disabled_status_and_paper_plans
  AssertionError: 0 != 1
========================= 4 failed, 5 passed in 0.09s ==========================
```

The two "missing directory" negative tests passed in both RED and GREEN (unaffected by the fix,
as expected).

### GREEN (reader-source fixes restored via `git stash pop`)

```
$ PYTHONUTF8=1 pytest tests -q -p no:cacheprovider
....................................................................... [ 53%]
..............................................................          [100%]
133 passed, 1 subtests passed in 4.04s
```

129 baseline + 4 new tests = 133. `ruff check --isolated --no-cache --select E9,F821,F811` on all
four changed files: `All checks passed!`. `git diff --check` on all four changed files: clean (exit 0).

### Real-repo sanity check (read-only, no server started)

Calling the fixed private helpers directly against the real checkout
(`_compile_observations(None, default_mcc_root())`, `_paper_trade_plans(None, default_mcc_root())`)
discovers all three real strategies:
`STG001_ql_alpha_ada_two_candle_sr_1h`, `STG002_ql_alpha_link_8ema_1h`,
`STG003_ql_alpha_ltc_rsi_oversold_1h` — both the compile-observations dict and the paper-trade-plans
list now populate for the migrated layout, where before this fix they were always empty. Calling the
full `build_pine_builder_status()`/`build_liveops_status()` (no args, using the real
`paths.example.json`) still shows `total_drafts: 0` / draft-listing empty — this is the pre-existing,
already-documented Lane V sandbox artifact (`paths.example.json` stores Windows-absolute values;
`canonicalize()` treats `C:/LAB/...` as relative on Linux, resolving under `apps/api/C:/LAB/...`),
unrelated to and unaffected by this fix — it affects `mtc_v2_root` resolution generally, not the
`quantlens_root`-based promoted-strategy join this lane touched.

## Commands executed

```
git log --oneline -1 ; git merge-base --is-ancestor 431984e3 HEAD ; git merge --ff-only 431984e3
git ls-files | grep -E "PINE_PARITY_PLAN.md|FORWARD_PAPER_TRADE_PLAN.md"
Read: pine_builder_reader.py, liveops_reader.py, paths.py, registry_reader.py, pipeline_reader.py,
      test_pine_builder_reader.py, test_liveops_reader.py
git stash push -- mcc_readonly/pine_builder_reader.py mcc_readonly/liveops_reader.py   (RED)
PYTHONUTF8=1 pytest tests/test_pine_builder_reader.py tests/test_liveops_reader.py -v -p no:cacheprovider
git stash pop   (GREEN)
PYTHONUTF8=1 pytest tests -q -p no:cacheprovider
ruff check --isolated --no-cache --select E9,F821,F811 <4 changed files>
git diff --check -- <4 changed files>
python -c "... _compile_observations(None, default_mcc_root()) ... _paper_trade_plans(None, default_mcc_root()) ..."
```

No server started; no execution outside the read-only reader modules and the test suite.

## NEXT ACTION

None for this lane.

## WAITING FOR OWNER

Nothing.
