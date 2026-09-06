# Lane O — ds_agent default report path (D13)

Scope: `_deepseek_driver/ds_agent.py` (supplemental, non-protected tool). Fixes lane K
finding #2 (hard-coded Windows fallback path for the run report/transcript). Finding #1
(duplicate `"remove"` in `_BANNED_ATTRS`) is explicitly **not** touched here — see note below.

## Problem (lane K finding #2)

```python
report_path = Path(task.get("report_out") or (Path(r"C:\tmp") / f"ds_{slug}_report.md"))
```

When a task omits `report_out`, the fallback used a Windows-only literal. On POSIX, a
backslash is not a path separator, so `Path(r"C:\tmp")` is a single relative path segment
(`"C:\tmp"`) under the current working directory, not a real temp directory. `_dump()`'s
`out_path.write_text(...)` then raised `FileNotFoundError` (parent doesn't exist), which was
silently caught in `_dump()`'s `except Exception as e: print(f"[warn] ...")` — the run
"succeeds" (`run_task` still returns 0) while the report/transcript is lost.

## Fix (minimal)

- Added `import tempfile`.
- Extracted a tiny pure helper:
  ```python
  def default_report_path(slug: str) -> Path:
      return Path(tempfile.gettempdir()) / "mtc_ds_reports" / f"ds_{slug}_report.md"
  ```
- `run_task()` now does `report_path = Path(task.get("report_out") or default_report_path(slug))`
  — explicit `report_out` behavior is byte-for-byte unchanged (still just wrapped in `Path(...)`).
- `_dump()` now does `out_path.parent.mkdir(parents=True, exist_ok=True)` immediately before
  `out_path.write_text(...)`, so the default path's `mtc_ds_reports/` subdirectory (and any
  parent directory of an explicit `report_out`) always exists before the write, on any platform.
- No network/provider code touched. No other line changed.

### Diff

```diff
diff --git a/_deepseek_driver/ds_agent.py b/_deepseek_driver/ds_agent.py
index 8ab21e54..22a09e29 100644
--- a/_deepseek_driver/ds_agent.py
+++ b/_deepseek_driver/ds_agent.py
@@ -36,6 +36,7 @@ import os
 import re
 import subprocess
 import sys
+import tempfile
 from pathlib import Path
 
 from openai import OpenAI
@@ -209,6 +210,16 @@ SYSTEM = (
 )
 
 
+def default_report_path(slug: str) -> Path:
+    """Default report/transcript location when a task omits `report_out`.
+
+    Uses the OS temp dir so this resolves on both POSIX and Windows, unlike
+    the old hard-coded `C:\\tmp` fallback (which, on POSIX, produced a
+    literal relative path segment instead of a real temp directory).
+    """
+    return Path(tempfile.gettempdir()) / "mtc_ds_reports" / f"ds_{slug}_report.md"
+
+
 def _dump(out_path: Path, messages: list, report: str, writes: list) -> None:
     try:
         lines = [f"# DeepSeek run report  ({_dt.datetime.now().isoformat(timespec='seconds')})",
@@ -221,6 +232,7 @@ def _dump(out_path: Path, messages: list, report: str, writes: list) -> None:
             for tc in (m.get("tool_calls") or []):
                 fn = tc.get("function", {})
                 lines.append(f"### {role} tool_call {fn.get('name')}\n{fn.get('arguments')}\n")
+        out_path.parent.mkdir(parents=True, exist_ok=True)
         out_path.write_text("\n".join(lines), encoding="utf-8")
         print(f"\n[saved] full report + transcript -> {out_path}", flush=True)
     except Exception as e:
@@ -237,7 +249,7 @@ def run_task(task: dict) -> int:
     client = OpenAI(api_key=key, base_url=base)
     sb = Sandbox(task.get("allow", []), task.get("read_extra", []), task.get("schema_allow", []))
     slug = re.sub(r"[^a-z0-9]+", "_", task.get("title", "task").lower())[:40]
-    report_path = Path(task.get("report_out") or (Path(r"C:\tmp") / f"ds_{slug}_report.md"))
+    report_path = Path(task.get("report_out") or default_report_path(slug))
     dispatch = {"read_file": sb.read_file, "edit_file": sb.edit_file,
                 "write_file": sb.write_file, "py_compile": sb.py_compile,
                 "run_python": sb.run_python}
```

## Tests (D026)

New file `_deepseek_driver/tests/test_report_path.py`, 5 tests. `ds_agent.py` imports `openai`
at module level; the test venv doesn't have that package installed, and since these tests only
exercise the pure, network-free `default_report_path()` helper (never the OpenAI client), the
test file stubs `openai` in `sys.modules` (a fake module with `OpenAI = object`) before
`import ds_agent`, so the module loads without needing the real dependency or any network call.

Tests:
- `test_default_report_path_is_under_system_temp_dir`
- `test_default_report_path_does_not_use_hardcoded_windows_path`
- `test_default_report_path_includes_slug_in_filename`
- `test_run_task_report_path_resolution_uses_default_when_absent`
- `test_run_task_report_path_resolution_honors_explicit_report_out`

### RED (before the fix — `ds_agent.py` reverted to pre-fix via `git stash`, new test file
present)

```
FFFF.                                                                    [100%]
=================================== FAILURES ===================================
______________ test_default_report_path_is_under_system_temp_dir _______________
    p = ds_agent.default_report_path("my_slug")
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AttributeError: module 'ds_agent' has no attribute 'default_report_path'
_________ test_default_report_path_does_not_use_hardcoded_windows_path _________
E       AttributeError: module 'ds_agent' has no attribute 'default_report_path'
______________ test_default_report_path_includes_slug_in_filename ______________
E       AttributeError: module 'ds_agent' has no attribute 'default_report_path'
________ test_run_task_report_path_resolution_uses_default_when_absent _________
E       AttributeError: module 'ds_agent' has no attribute 'default_report_path'
=========================== short test summary info ============================
FAILED _deepseek_driver/tests/test_report_path.py::test_default_report_path_is_under_system_temp_dir
FAILED _deepseek_driver/tests/test_report_path.py::test_default_report_path_does_not_use_hardcoded_windows_path
FAILED _deepseek_driver/tests/test_report_path.py::test_default_report_path_includes_slug_in_filename
FAILED _deepseek_driver/tests/test_report_path.py::test_run_task_report_path_resolution_uses_default_when_absent
4 failed, 1 passed in 0.04s
```
(the 5th test, honoring an explicit `report_out`, does not depend on the helper and already
passed pre-fix — as required, "explicit `report_out` behavior unchanged").

### GREEN (after the fix — full suite)

```
PYTHONUTF8=1 python -m pytest _deepseek_driver/tests -q -p no:cacheprovider
.........................                                                [100%]
25 passed in 0.06s
```
(20 pre-existing + 5 new = 25, all green.)

### Runtime sanity check (no provider call — `_dump()` exercised directly, not the agent loop)

Ran a standalone script (not committed) that stubbed `openai`, imported `ds_agent`, called
`default_report_path("sanity")` -> `/tmp/mtc_ds_reports/ds_sanity_report.md`, deleted that
directory if present, then called `ds_agent._dump(...)` directly and confirmed the file now
exists with the expected report content — proving the `mkdir(parents=True, exist_ok=True)`
actually creates the missing parent before the write, which is exactly the failure mode lane K
identified (write to a non-existent parent, silently swallowed).

### Lint / diff hygiene

```
ruff check --isolated --no-cache --select E9,F821,F811 _deepseek_driver/ds_agent.py _deepseek_driver/tests/test_report_path.py
All checks passed!

git diff --check -- _deepseek_driver/ds_agent.py _deepseek_driver/tests/test_report_path.py
(no output, exit 0)
```

## Note on finding #1 (not touched, per task scope)

`_BANNED_ATTRS` in `ds_agent.py` still contains `"remove"` twice (lines ~59-62 pre-fix, same
lines post-fix — this change does not touch that set). As a `set` literal it silently drops
the duplicate at parse time, so the set has no fewer *effective* entries than if it were
written once, but it strongly suggests a second, distinct attribute name was intended and
lost to a copy/paste — lane K's proposed candidates were `"delete"`, an `"rmdir"` variant, or
`"kill"`. The intended second attribute is **unknown** and is left for the owner to confirm;
no attribute was added or removed from this guard set in this change, and no other
`_BANNED_*` set was touched.

## Files changed

- `_deepseek_driver/ds_agent.py` — `default_report_path()` helper, `_dump()` mkdir, `run_task()`
  now calls the helper.
- `_deepseek_driver/tests/test_report_path.py` — new, 5 tests (RED before, GREEN after).

## NEXT ACTION

None required from this lane — fix is minimal, tested, and scoped exactly to D13/finding #2.
Owner may separately want to confirm the intended second `_BANNED_ATTRS` entry (finding #1,
explicitly out of scope here).

## WAITING FOR OWNER

Nothing.
