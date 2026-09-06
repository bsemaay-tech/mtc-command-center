"""Tests for the default report-path helper in ds_agent.py (D13 fix).

Lane K finding #2: the old fallback hard-coded a Windows path
(`Path(r"C:\\tmp") / ...`). On POSIX, a backslash is not a path separator, so
that resolved to a literal relative path segment `C:\\tmp` under the CWD
instead of a real temp directory; `_dump()`'s `write_text()` then raised
`FileNotFoundError`, which was silently caught and only logged — the run
"succeeded" while losing its report/transcript.

`ds_agent.py` imports the `openai` package at module level, which this test
venv does not have installed; since these tests only exercise the pure,
network-free `default_report_path()` helper (never the OpenAI client), we
stub `openai` in `sys.modules` before importing so the module loads cleanly.
"""
import sys
import tempfile
import types
from pathlib import Path

if "openai" not in sys.modules:
    _fake_openai = types.ModuleType("openai")
    _fake_openai.OpenAI = object
    sys.modules["openai"] = _fake_openai

import ds_agent


def test_default_report_path_is_under_system_temp_dir():
    """RED before the fix: the old code built Path(r"C:\\tmp") / ... which,
    on this POSIX host, is a *relative* path ("C:\\tmp/ds_..._report.md")
    that does not start with the real system temp dir at all.
    """
    p = ds_agent.default_report_path("my_slug")
    assert p.is_absolute()
    assert str(p).startswith(str(Path(tempfile.gettempdir())))


def test_default_report_path_does_not_use_hardcoded_windows_path():
    p = ds_agent.default_report_path("my_slug")
    assert "C:\\tmp" not in str(p)
    assert "C:/tmp" not in str(p)


def test_default_report_path_includes_slug_in_filename():
    p = ds_agent.default_report_path("batch_b")
    assert p.name == "ds_batch_b_report.md"


def test_run_task_report_path_resolution_uses_default_when_absent():
    """Mirrors the exact expression run_task() uses to compute report_path
    when a task omits `report_out`, without invoking run_task() itself
    (which would construct a real OpenAI client / hit the network).
    """
    task = {"title": "some task"}
    slug = "some_task"
    report_path = Path(task.get("report_out") or ds_agent.default_report_path(slug))
    assert report_path == ds_agent.default_report_path(slug)
    assert str(report_path).startswith(str(Path(tempfile.gettempdir())))


def test_run_task_report_path_resolution_honors_explicit_report_out():
    """An explicit `report_out` must be used verbatim, unchanged by the fix."""
    task = {"title": "some task", "report_out": "/custom/explicit/out.md"}
    slug = "some_task"
    report_path = Path(task.get("report_out") or ds_agent.default_report_path(slug))
    assert report_path == Path("/custom/explicit/out.md")
