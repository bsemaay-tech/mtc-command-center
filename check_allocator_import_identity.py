"""Mechanical proof of WP-P0-20's import-identity criterion.

The acceptance gate says the canonical path must be "shown to import and run the one
shared Risk Allocator implementation delivered here, together with the kernel -- proven by
import, not asserted". A behavioural test cannot prove that: a copy of the allocator
pasted into the engine passes every behavioural test and still leaves two implementations
in the system, which is the exact failure D-13 exists to prevent. Only object identity
distinguishes them, so that is what this tool checks.

It reports the truth about the current tree rather than asserting a conclusion. Today the
canonical path performs no sizing at all -- ``simulate_slice`` simulates percent returns
with a flat ``COST_BPS`` -- so the binding this checks for does not yet exist, and saying
so precisely is the point. Run with ``--require-bound`` (what an acceptance run would use)
to make an unproven binding a non-zero exit.
"""
from __future__ import annotations

import argparse
import ast
import importlib
import sys
from pathlib import Path

ALLOCATOR_MODULE = "shared_risk_calculator"
ALLOCATOR_ENTRY = "resolve_proposed_qty"
CANONICAL_PATH = Path("MTC_COMMAND_CENTER/03_QUANTLENS/tools/mega_walk_forward.py")

NOT_BOUND = "NOT_BOUND"
BOUND_IDENTICAL = "BOUND_IDENTICAL"
BOUND_NOT_IDENTICAL = "BOUND_NOT_IDENTICAL"


class IdentityCheckRefused(ValueError):
    """The check could not be performed; never a silent pass."""


def imports_allocator(source: str) -> bool:
    """True when the module imports the allocator by module identity, not by name.

    A local function or class called ``resolve_proposed_qty`` is deliberately not a
    binding: re-implementation under the same name is the failure mode being excluded.
    """
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == ALLOCATOR_MODULE:
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module == ALLOCATOR_MODULE and node.level == 0:
                return True
    return False


def static_status(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise IdentityCheckRefused(f"canonical path unreadable: {path}") from error
    return BOUND_IDENTICAL if imports_allocator(source) else NOT_BOUND


def runtime_status(module_name: str) -> str:
    """Import both modules and compare the objects, not their names."""
    allocator = importlib.import_module(ALLOCATOR_MODULE)
    expected = getattr(allocator, ALLOCATOR_ENTRY)
    canonical = importlib.import_module(module_name)
    bound = getattr(canonical, ALLOCATOR_ENTRY, None)
    if bound is None:
        bound = getattr(getattr(canonical, ALLOCATOR_MODULE, None), ALLOCATOR_ENTRY, None)
    if bound is None:
        return NOT_BOUND
    return BOUND_IDENTICAL if bound is expected else BOUND_NOT_IDENTICAL


def self_test() -> int:
    """Prove the check cannot be fooled by a same-named re-implementation.

    Three synthetic canonical modules are built and checked. The middle one is the case
    the whole tool exists for: identical name, identical behaviour, different object.
    """
    import tempfile
    cases = (
        ("genuine import", BOUND_IDENTICAL,
         "import shared_risk_calculator\n"
         "resolve_proposed_qty = shared_risk_calculator.resolve_proposed_qty\n"),
        ("same-named re-implementation", BOUND_NOT_IDENTICAL,
         "def resolve_proposed_qty(**kwargs):\n"
         "    raise NotImplementedError('a second implementation')\n"),
        ("no binding at all", NOT_BOUND, "COST_BPS = 6.0\n"),
    )
    failures = 0
    with tempfile.TemporaryDirectory() as directory:
        sys.path.insert(0, directory)
        try:
            for index, (label, expected, source) in enumerate(cases):
                name = f"_identity_case_{index}"
                path = Path(directory) / f"{name}.py"
                path.write_text(source, encoding="utf-8")
                static = static_status(path)
                runtime = runtime_status(name)
                # The static tier may only ever be as strict as the runtime tier: it must
                # never report a binding the objects do not support.
                static_ok = (static == NOT_BOUND) or (runtime == BOUND_IDENTICAL)
                if runtime == expected and static_ok:
                    print(f"SELF TEST ({label}): {runtime} as expected")
                else:
                    failures += 1
                    print(f"SELF TEST ({label}): FAIL -- runtime {runtime}, "
                          f"expected {expected}, static {static}")
        finally:
            sys.path.remove(directory)
    print("IMPORT IDENTITY SELF TEST:", "PASS" if not failures else "FAIL")
    return 1 if failures else 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--canonical-path", type=Path, default=CANONICAL_PATH)
    parser.add_argument("--canonical-module", default=None,
                        help="Import this module and compare objects at runtime. "
                             "Omit to stay static, which imports no engine.")
    parser.add_argument("--require-bound", action="store_true",
                        help="Exit non-zero unless identity is proven (acceptance mode).")
    parser.add_argument("--self-test", action="store_true",
                        help="Prove the check rejects a same-named re-implementation.")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    status = static_status(args.canonical_path)
    print(f"STATIC BINDING ({args.canonical_path}): {status}")
    if args.canonical_module:
        status = runtime_status(args.canonical_module)
        print(f"RUNTIME OBJECT IDENTITY ({args.canonical_module}): {status}")
    else:
        print("RUNTIME OBJECT IDENTITY: NOT ATTEMPTED (no --canonical-module)")

    if status == BOUND_NOT_IDENTICAL:
        print("IMPORT IDENTITY: FAIL -- a same-named object that is not the delivered one")
        return 1
    if status == NOT_BOUND:
        print("IMPORT IDENTITY: NOT BOUND -- WP-P0-20's migration has not been performed")
        print("  The canonical path simulates percent returns with a flat COST_BPS and has")
        print("  no sizing stage to bind. Binding it is the migration itself, and it needs")
        print("  the WP-P0-12 kernel, which is stopped by OD-20260826-1 / OD-20260826-8.")
        return 1 if args.require_bound else 0
    print("IMPORT IDENTITY: PASS -- the canonical path uses the delivered implementation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
