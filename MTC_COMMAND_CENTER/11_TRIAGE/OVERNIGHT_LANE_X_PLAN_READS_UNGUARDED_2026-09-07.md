# Lane X — promoted-plan reads no longer gated on mtc_v2_root (D18 follow-up)

Scope: `mcc_readonly/pine_builder_reader.py::_compile_observations` and
`mcc_readonly/liveops_reader.py::_paper_trade_plans`. Follow-up nit (T1) on top of Lane W's fix
(`a508fc77`, `OVERNIGHT_LANE_W_PROMOTED_ROOT_READS_2026-09-07.md`).

## The bug

After Lane W, both helpers read promoted-strategy plan docs from
`default_quantlens_root(mcc_root) / "strategies"` — a path derived entirely from `mcc_root`, with
no dependency on `mtc_v2_root` left inside either function body (confirmed by reading both; neither
references its `mtc_v2_root` parameter anywhere in its logic). Yet their call sites still gated the
call on `mtc_v2_root`:

- `liveops_reader.py:22` (pre-fix): `_paper_trade_plans(mtc_v2_root, root) if mtc_v2_root and
  mtc_v2_root.exists() else []` — a direct ternary guard on the one call site.
- `pine_builder_reader.py:20-29` (pre-fix): `build_pine_builder_status` returned
  `_empty_status(...)` immediately (via `if mtc_v2_root is None:` / `if not mtc_v2_root.exists():`)
  *before* ever reaching the `_compile_observations(mtc_v2_root, root)` call a few lines later —
  functionally the same guard, written as early returns instead of a ternary.

Net effect: a missing/misconfigured `mtc_v2_root` (unset in `paths.local.json`, or pointing at a
path that no longer exists) hid promoted-strategy plan data that Lane W's fix had already made
independently readable from `mcc_root`.

## Fix

Both call sites now call the helper unconditionally; both helpers had their unused `mtc_v2_root`
parameter dropped (kept everywhere else it's still used — see per-file notes).

- **`liveops_reader.py`**: `_paper_trade_plans(mtc_v2_root: Path, mcc_root: Path)` → `(mcc_root:
  Path)`. `build_liveops_status` now calls `_paper_trade_plans(root)` unconditionally. The
  `mtc_v2_root`/`path_config` local variables and the `load_path_config`/`resolve_configured_path`
  imports are removed outright — they had no other use in this module (grepped `mtc_v2_root` and
  `path_config` across the file; the ternary guard was their only consumer), so nothing else in the
  module depends on them. `default_quantlens_root`/`canonicalize`/`default_mcc_root` imports kept
  (still used).
- **`pine_builder_reader.py`**: `_compile_observations(mtc_v2_root: Path, mcc_root: Path)` →
  `(mcc_root: Path)`. Unlike `liveops_reader.py`, `mtc_v2_root` in this module is genuinely used
  elsewhere in `build_pine_builder_status` (pine-file `rglob`, protected-core/draft classification,
  candidate-id parsing) — all of that stays exactly as-is, per the task brief ("keep every other
  `mtc_v2_root`-dependent behaviour ... unchanged"). The `_compile_observations(root)` call was
  moved *before* the `mtc_v2_root is None` / `not mtc_v2_root.exists()` early-return checks so it
  always runs. Since observations only ever join into the response via `drafts` (which requires
  actual `.pine` files under `mtc_v2_root` and therefore genuinely can't populate when `mtc_v2_root`
  is missing) or via `generated_at` (`_latest_timestamp` already folds in every observation's
  `updated_at` regardless of draft match — this was already true on the main return path), the
  observations are now threaded into both `_empty_status(...)` early-return calls too, so
  `generated_at` reflects a discovered plan's timestamp even when `mtc_v2_root` is unconfigured/
  missing, instead of unconditionally `None`. `_empty_status` gained an optional
  `observations: dict[str, dict[str, Any]] | None = None` parameter (all three existing call sites
  in this module updated; no other module has its own `_empty_status` — each reader defines its
  own local one, grepped to confirm). No new top-level schema key; `source`/`summary`/`drafts`
  keys and shapes are unchanged.

Fail-closed behaviour for a missing `strategies` directory (`{}` / `[]`) is preserved unchanged in
both helpers — untouched in this diff.

### Diff — source (both files)

```diff
diff --git a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py
index d04e5957..d5fae73b 100644
--- a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py
+++ b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/liveops_reader.py
@@ -5,21 +5,18 @@ from datetime import datetime, timezone
 from pathlib import Path
 from typing import Any
 
-from .paths import (
-    canonicalize,
-    default_mcc_root,
-    default_quantlens_root,
-    load_path_config,
-    resolve_configured_path,
-)
+from .paths import canonicalize, default_mcc_root, default_quantlens_root
 
 
 def build_liveops_status(mcc_root: str | Path | None = None) -> dict[str, Any]:
     root = canonicalize(mcc_root or default_mcc_root())
     status = _read_status_file(root / "03_STATUS" / "LIVEOPS_STATUS.json")
-    path_config = load_path_config(root)
-    mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
-    paper_plans = _paper_trade_plans(mtc_v2_root, root) if mtc_v2_root and mtc_v2_root.exists() else []
+    # Promoted-strategy plan discovery reads from the migrated QuantLens root
+    # (03_QUANTLENS/strategies/<id>/...) and no longer depends on mtc_v2_root
+    # at all, so it is called unconditionally rather than gated on
+    # mtc_v2_root being configured/existing. See
+    # MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LANE_X_PLAN_READS_UNGUARDED_2026-09-07.md.
+    paper_plans = _paper_trade_plans(root)
     safety_gates = _safety_gates(status)
 
     return {
@@ -61,7 +58,7 @@ def _read_status_file(path: Path) -> dict[str, Any]:
     return raw if isinstance(raw, dict) else {}
 
 
-def _paper_trade_plans(mtc_v2_root: Path, mcc_root: Path) -> list[dict[str, Any]]:
+def _paper_trade_plans(mcc_root: Path) -> list[dict[str, Any]]:
     # Promoted-strategy plan docs (FORWARD_PAPER_TRADE_PLAN.md) live under the
     # migrated QuantLens root (03_QUANTLENS/strategies/<id>/...), not under
     # mtc_v2_root. See
diff --git a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py
index 12197e03..b7281fe1 100644
--- a/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py
+++ b/MTC_COMMAND_CENTER/08_DASHBOARD_APP/apps/api/mcc_readonly/pine_builder_reader.py
@@ -21,12 +21,17 @@ def build_pine_builder_status(mcc_root: str | Path | None = None) -> dict[str, A
     root = canonicalize(mcc_root or default_mcc_root())
     path_config = load_path_config(root)
     mtc_v2_root = resolve_configured_path(path_config.config, "mtc_v2_root")
+    # Promoted-strategy plan discovery reads from the migrated QuantLens root
+    # (03_QUANTLENS/strategies/<id>/...) and no longer depends on mtc_v2_root
+    # at all, so it is called unconditionally rather than gated behind the
+    # mtc_v2_root configured/existing checks below. See
+    # MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LANE_X_PLAN_READS_UNGUARDED_2026-09-07.md.
+    observations = _compile_observations(root)
     if mtc_v2_root is None:
-        return _empty_status("mtc_v2_root_not_configured")
+        return _empty_status("mtc_v2_root_not_configured", observations)
     if not mtc_v2_root.exists():
-        return _empty_status(str(mtc_v2_root))
+        return _empty_status(str(mtc_v2_root), observations)
 
-    observations = _compile_observations(mtc_v2_root, root)
     pine_files = sorted(mtc_v2_root.rglob("*.pine"))
     protected_core_files = [path for path in pine_files if _is_protected_core(path, mtc_v2_root)]
     draft_paths = [path for path in pine_files if _is_review_draft(path, mtc_v2_root)]
@@ -49,7 +54,7 @@ def build_pine_builder_status(mcc_root: str | Path | None = None) -> dict[str, A
     }
 
 
-def _compile_observations(mtc_v2_root: Path, mcc_root: Path) -> dict[str, dict[str, Any]]:
+def _compile_observations(mcc_root: Path) -> dict[str, dict[str, Any]]:
     # Promoted-strategy plan docs (PINE_PARITY_PLAN.md) live under the migrated
     # QuantLens root (03_QUANTLENS/strategies/<id>/...), not under mtc_v2_root.
     # See MTC_COMMAND_CENTER/11_TRIAGE/OVERNIGHT_LANE_V_DASHBOARD_PATH_MODEL_DECISION_2026-09-07.md
@@ -243,10 +248,10 @@ def _timestamp(epoch_seconds: float) -> str:
     return datetime.fromtimestamp(epoch_seconds, timezone.utc).isoformat()
 
 
-def _empty_status(source: str) -> dict[str, Any]:
+def _empty_status(source: str, observations: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
     return {
         "schema_version": "1.0",
-        "generated_at": None,
+        "generated_at": _latest_timestamp([], observations or {}),
         "source": source,
         "summary": {
```

## Tests (D026)

One regression test added per reader, both following the required shape — a temp MCC root with the
promoted-strategy plan file present under `03_QUANTLENS/strategies/<id>/` and `mtc_v2_root: None`
in `paths.example.json` (no configured/existing `mtc_v2_root` at all):

- `tests/test_liveops_reader.py::test_paper_trade_plans_discovered_without_mtc_v2_root` — asserts
  `build_liveops_status(root)["paper_trade_plans"]` contains the `FORWARD_PAPER_TRADE_PLAN.md`
  plan (`paper_trade_plan_count == 1`, `candidate_id == "STG011"`) even though `mtc_v2_root` is
  unconfigured. This directly exercises the real, user-visible bug (the top-level
  `paper_trade_plans` list was always `[]` before the fix in this scenario).
- `tests/test_pine_builder_reader.py::test_compile_observations_discovered_without_mtc_v2_root` —
  asserts `build_pine_builder_status(root)["generated_at"]` is not `None` (reflecting the
  `PINE_PARITY_PLAN.md` timestamp) even though `mtc_v2_root` is unconfigured and the response still
  takes the `mtc_v2_root_not_configured` empty-status path. `generated_at` is the only place
  discovered-but-unmatched observations were already surfaced pre-existing (`drafts` genuinely
  cannot populate without real `.pine` files under `mtc_v2_root`, which can't exist when
  `mtc_v2_root` itself is unconfigured — so `generated_at` is the correct, minimal, and only
  currently-testable signal for "the observation is still discovered" in this reader).

### RED (stashed the two reader-source fixes via `git stash push -- <2 source files>`, kept the
updated tests; `pytest tests/test_pine_builder_reader.py tests/test_liveops_reader.py -v -p no:cacheprovider`)

```
FAILED tests/test_pine_builder_reader.py::PineBuilderReaderTests::test_compile_observations_discovered_without_mtc_v2_root
  AssertionError: unexpectedly None
FAILED tests/test_liveops_reader.py::LiveOpsReaderTests::test_paper_trade_plans_discovered_without_mtc_v2_root
  AssertionError: 0 != 1
========================= 2 failed, 9 passed in 0.08s ==========================
```

All other existing tests in both files (9) passed unaffected in RED, confirming the failures are
isolated to the two new regression tests.

### GREEN (reader-source fixes restored via `git stash pop`)

```
$ PYTHONUTF8=1 pytest tests -q -p no:cacheprovider
....................................................................... [ 52%]
................................................................ [100%]
135 passed, 1 subtests passed in 4.16s
```

133 baseline (post-Lane-W) + 2 new tests = 135. `ruff check --isolated --no-cache --select
E9,F821,F811` on all four changed files: `All checks passed!`. `git diff --check` on all four
changed files: clean (exit 0).

### Real-repo sanity check (read-only, no server started)

Calling the fixed private helpers directly against the real checkout
(`_compile_observations(default_mcc_root())`, `_paper_trade_plans(default_mcc_root())`) —
note both now take a single `mcc_root` argument, `mtc_v2_root` dropped:

```
observations keys: ['STG001_ql_alpha_ada_two_candle_sr_1h', 'STG002_ql_alpha_link_8ema_1h', 'STG003_ql_alpha_ltc_rsi_oversold_1h']
plans candidate_ids: ['STG001_ql_alpha_ada_two_candle_sr_1h', 'STG002_ql_alpha_link_8ema_1h', 'STG003_ql_alpha_ltc_rsi_oversold_1h']
```

All three real strategies discovered by both helpers, unchanged from Lane W's sanity check — this
lane's fix only affects behaviour when `mtc_v2_root` is missing/misconfigured, which is not the
case in this real checkout.

## Commands executed

```
git log --oneline -1 ; git merge-base --is-ancestor 3b3d06ae HEAD ; git merge --ff-only 3b3d06ae
Read: pine_builder_reader.py, liveops_reader.py, paths.py, test_pine_builder_reader.py,
      test_liveops_reader.py, OVERNIGHT_LANE_W_PROMOTED_ROOT_READS_2026-09-07.md,
      08_DASHBOARD_APP/{AGENTS.md,TESTS.md,HANDOFF.md}
grep -n "mtc_v2_root.exists()" mcc_readonly/pine_builder_reader.py mcc_readonly/liveops_reader.py
grep -rn "_compile_observations\|_paper_trade_plans" MTC_COMMAND_CENTER/08_DASHBOARD_APP
Edit: mcc_readonly/liveops_reader.py, mcc_readonly/pine_builder_reader.py,
      tests/test_liveops_reader.py, tests/test_pine_builder_reader.py
git stash push -- mcc_readonly/liveops_reader.py mcc_readonly/pine_builder_reader.py   (RED)
PYTHONUTF8=1 pytest tests/test_pine_builder_reader.py tests/test_liveops_reader.py -v -p no:cacheprovider
git stash pop   (GREEN)
PYTHONUTF8=1 pytest tests -q -p no:cacheprovider
ruff check --isolated --no-cache --select E9,F821,F811 <4 changed files>
git diff --check -- <4 changed files>
python -c "... _compile_observations(default_mcc_root()) ... _paper_trade_plans(default_mcc_root()) ..."
```

No server started; no execution outside the read-only reader modules and the test suite.

## NEXT ACTION

None for this lane.

## WAITING FOR OWNER

Nothing.
