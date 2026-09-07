"""Tests for overnight_orchestrator.write_runner_extension (pytest + stdlib).

D17: the generated runner must import each candidate's prototype module from
the prototypes directory itself (sys.path gets the 04_PYTHON_PROTOTYPES dir),
never via a non-existent "PYTHON_PROTOTYPES" package name. Covers: py_compile
of the emitted file, absence of the stale package token, the sys.path line
inserting ROOT (not ROOT.parent), and that every emitted import line names a
prototype module that actually exists on disk as "<id>_prototype.py" under
04_PYTHON_PROTOTYPES.
"""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import re
import sys
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().with_name("overnight_orchestrator.py")


def _load_module():
    name = "overnight_orchestrator_under_test"
    spec = importlib.util.spec_from_file_location(name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # The orchestrator's @dataclass Candidate needs its defining module
    # resolvable via sys.modules while exec_module runs (dataclasses looks
    # up cls.__module__ for its from __future__ import annotations handling).
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


oo = _load_module()


@pytest.fixture()
def generated_runner(tmp_path, monkeypatch):
    """Regenerate the runner into tmp_path (never the real tools dir)."""
    monkeypatch.setattr(oo, "TOOLS_DIR", tmp_path)
    runner_path = oo.write_runner_extension(True)
    assert runner_path == tmp_path / "overnight_extended_run.py"
    assert runner_path.exists()
    return runner_path


def test_generated_runner_compiles(generated_runner, tmp_path):
    py_compile.compile(str(generated_runner), cfile=str(tmp_path / "compiled.pyc"), doraise=True)


def test_generated_runner_has_no_stale_package_token(generated_runner):
    """The directory is literally named "04_PYTHON_PROTOTYPES" (a legitimate,
    expected substring in ROOT's path literal and in the trailing comment),
    but "PYTHON_PROTOTYPES" must never appear as an importable module/package
    name on its own -- i.e. no `import PYTHON_PROTOTYPES` / `from
    PYTHON_PROTOTYPES import ...` line."""
    text = generated_runner.read_text(encoding="utf-8")
    assert not re.search(r"\bfrom PYTHON_PROTOTYPES\b", text), (
        "generated runner still imports from the non-existent PYTHON_PROTOTYPES "
        "package name (D17 regression)"
    )
    assert not re.search(r"^import PYTHON_PROTOTYPES\b", text, re.M), (
        "generated runner still imports the non-existent PYTHON_PROTOTYPES "
        "package name (D17 regression)"
    )


def test_generated_runner_sys_path_inserts_root_not_parent(generated_runner):
    text = generated_runner.read_text(encoding="utf-8")
    assert 'ROOT = Path(__file__).resolve().parent.parent / "04_PYTHON_PROTOTYPES"' in text
    assert 'sys.path.insert(0, str(ROOT))' in text
    assert 'sys.path.insert(0, str(ROOT.parent))' not in text


def test_generated_runner_imports_are_bare_module_imports(generated_runner):
    """Every candidate import line is `import <id>_prototype`, a plain
    top-level import (not `from PYTHON_PROTOTYPES import ...`), and the
    indent-join marker from lane B (8-space continuation) is preserved."""
    tree = ast.parse(generated_runner.read_text(encoding="utf-8"), filename=str(generated_runner))
    import_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.endswith("_prototype"):
                    import_names.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            assert node.module != "PYTHON_PROTOTYPES"

    expected = [f"{c.id}_prototype" for c in oo.CANDIDATES]
    assert import_names == expected


def test_every_candidate_prototype_file_exists_on_disk(generated_runner):
    """Every `import <id>_prototype` line in the generated runner must name
    a real `<id>_prototype.py` file under 04_PYTHON_PROTOTYPES. Report any
    candidate id that has no matching file rather than assuming one exists.
    """
    missing = [c.id for c in oo.CANDIDATES if not (oo.PROTO_DIR / f"{c.id}_prototype.py").exists()]
    assert missing == [], f"CANDIDATES with no matching *_prototype.py file: {missing}"


def test_generated_runner_indent_join_intact(generated_runner):
    """Lane-B fix: import lines after the first are joined with a newline
    plus 8 spaces so textwrap.dedent still strips the template's common
    leading whitespace."""
    text = generated_runner.read_text(encoding="utf-8")
    import_lines = [
        line for line in text.splitlines() if re.match(r"^import \w+_prototype  # noqa: F401$", line)
    ]
    assert len(import_lines) == len(oo.CANDIDATES)
    # None of the import lines should carry leading whitespace after dedent.
    for line in import_lines:
        assert not line.startswith(" ")


def test_find_spec_resolves_every_prototype_with_root_on_syspath(generated_runner, monkeypatch):
    """End-to-end (static) check: with sys.path set exactly as the generated
    runner sets it (ROOT, i.e. the prototypes dir), importlib can locate
    every candidate's module spec. Does not import/execute the prototypes.
    """
    monkeypatch.syspath_prepend(str(oo.PROTO_DIR))
    for c in oo.CANDIDATES:
        modname = f"{c.id}_prototype"
        spec = importlib.util.find_spec(modname)
        assert spec is not None, f"find_spec could not locate {modname} with ROOT on sys.path"

# ---------------------------------------------------------------------------
# Gate-5 finding G4-1 (claude-opus-5, 2026-09-07): after D11 repointed the path
# constants to the live 03_QUANTLENS layout, --apply would write producer specs
# into 06_PROMOTED_TO_PARITY (owner-gated promotion/parity scope) with no guard.
# materialize_candidate must refuse unless the explicit flag is passed.
# ---------------------------------------------------------------------------
@pytest.fixture()
def sandboxed_dirs(tmp_path, monkeypatch):
    promoted = tmp_path / "06_PROMOTED_TO_PARITY"
    proto = tmp_path / "04_PYTHON_PROTOTYPES"
    monkeypatch.setattr(oo, "REPO_ROOT", tmp_path)  # summaries use relative_to(REPO_ROOT)
    monkeypatch.setattr(oo, "PROMOTED_DIR", promoted)
    monkeypatch.setattr(oo, "PROTO_DIR", proto)
    return promoted, proto


def test_apply_refuses_without_allow_quantlens_writes(sandboxed_dirs):
    promoted, proto = sandboxed_dirs
    with pytest.raises(PermissionError, match="allow-quantlens-writes"):
        oo.materialize_candidate(oo.CANDIDATES[0], apply=True)
    assert not promoted.exists()
    assert not proto.exists()


def test_apply_writes_only_with_allow_quantlens_writes(sandboxed_dirs):
    promoted, proto = sandboxed_dirs
    c = oo.CANDIDATES[0]
    summary = oo.materialize_candidate(c, apply=True, allow_quantlens_writes=True)
    assert summary["written"] is True
    assert (promoted / c.id / "producer_spec.json").is_file()
    assert (proto / f"{c.id}_prototype.py").is_file()


def test_dry_run_never_needs_the_flag(sandboxed_dirs):
    promoted, proto = sandboxed_dirs
    summary = oo.materialize_candidate(oo.CANDIDATES[0], apply=False)
    assert summary["written"] is False
    assert not promoted.exists() and not proto.exists()


def test_cli_apply_without_flag_refuses_through_main(sandboxed_dirs, tmp_path, monkeypatch):
    """The CLI wiring itself is fenced: `--apply` alone must raise before any write."""
    promoted, proto = sandboxed_dirs
    monkeypatch.setattr(oo, "TOOLS_DIR", tmp_path / "tools")
    monkeypatch.setattr(sys, "argv", ["overnight_orchestrator.py", "--apply"])
    with pytest.raises(PermissionError, match="allow-quantlens-writes"):
        oo.main()
    assert not promoted.exists() and not proto.exists()
    assert not (tmp_path / "tools").exists()


def test_cli_apply_with_flag_writes_through_main(sandboxed_dirs, tmp_path, monkeypatch, capsys):
    promoted, proto = sandboxed_dirs
    monkeypatch.setattr(oo, "TOOLS_DIR", tmp_path / "tools")
    monkeypatch.setattr(sys, "argv", ["overnight_orchestrator.py", "--apply", "--allow-quantlens-writes"])
    assert oo.main() == 0
    assert (promoted / oo.CANDIDATES[0].id / "producer_spec.json").is_file()
    assert (proto / f"{oo.CANDIDATES[0].id}_prototype.py").is_file()
    assert (tmp_path / "tools" / "overnight_extended_run.py").is_file()
    assert "WROTE" in capsys.readouterr().out
