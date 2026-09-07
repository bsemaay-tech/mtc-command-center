"""Regression fence for finding D7 (2026-09-07): ``app.py`` must bind ``pd`` at module scope.

``show_operator_page()`` evaluates ``pd.Timestamp.now()`` when the "Generate Run Plan" button is
pressed, but ``pandas`` used to be imported only inside other functions, so the button raised
``NameError``.  This test is deliberately static (``ast`` only): importing ``app.py`` would start
Streamlit, and executing the operator page is owner-gated.  It fails on the pre-fix source and
passes once ``import pandas as pd`` exists at module scope.
"""

from __future__ import annotations

import ast
from pathlib import Path

APP_PATH = Path(__file__).resolve().parents[1] / "app.py"


def _module_level_bindings(tree: ast.Module) -> set[str]:
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.asname or alias.name)
    return names


def _function_uses_name(tree: ast.Module, function_name: str, name: str) -> bool:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return any(
                isinstance(child, ast.Name) and child.id == name and isinstance(child.ctx, ast.Load)
                for child in ast.walk(node)
            )
    raise AssertionError(f"{function_name} not found in {APP_PATH}")


def _function_binds_name(tree: ast.Module, function_name: str, name: str) -> bool:
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            for child in ast.walk(node):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    for alias in child.names:
                        if (alias.asname or alias.name.split(".")[0]) == name:
                            return True
                if isinstance(child, ast.Name) and child.id == name and isinstance(child.ctx, ast.Store):
                    return True
            return False
    raise AssertionError(f"{function_name} not found in {APP_PATH}")


def test_operator_page_pd_reference_is_bound() -> None:
    tree = ast.parse(APP_PATH.read_text(encoding="utf-8"), filename=str(APP_PATH))
    # Precondition: the operator page really references ``pd`` (otherwise this fence is moot).
    assert _function_uses_name(tree, "show_operator_page", "pd")
    bound_at_module = "pd" in _module_level_bindings(tree)
    bound_locally = _function_binds_name(tree, "show_operator_page", "pd")
    assert bound_at_module or bound_locally, (
        "show_operator_page() uses pd but neither app.py's module scope nor the function binds it "
        "(D7 NameError on 'Generate Run Plan')"
    )
