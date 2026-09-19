"""Validate a derived benchmark plan through the REAL driver without touching the benchmark package.

Imports run_bounded_benchmark.py from its real directory (so ROOT, MANIFEST_PATH, COMPATIBILITY_PATH and
RECORD_PATHS resolve to the pinned files), points PLAN_PATH at the plan under validation, and calls
_validate_plan(_load_plan()). Read-only: nothing is written anywhere. Never runs --run.

Usage: python validate_derived_plan_harness.py [PLAN_PATH]
"""
import datetime
import hashlib
import importlib.util
import sys
from pathlib import Path

DRIVER = Path("C:/tmp/P020_LEAD_20260912/benchmark/run_bounded_benchmark.py")
DEFAULT_PLAN = Path("C:/tmp/CLAUDE_P0_RUN_20260913/P020_DERIVED_PLAN_20260914/BENCHMARK_PLAN_DERIVED.json")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    plan_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PLAN
    print("run:", datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"))
    print("driver sha256:", sha256(DRIVER))
    print("plan under validation:", plan_path.as_posix(), sha256(plan_path))
    spec = importlib.util.spec_from_file_location("run_bounded_benchmark", DRIVER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PLAN_PATH = plan_path
    try:
        plan = module._load_plan()
        manifest = module._validate_plan(plan)
    except SystemExit as exc:
        print("REFUSED:", exc)
        return 2
    families = [t["strategy_id"] for t in plan["trials"]]
    sizes = sorted({t["input_rows"] for t in plan["trials"]})
    print(
        "PLAN_VALID via run_bounded_benchmark._validate_plan:",
        f"manifest datasets={len(manifest.get('datasets', []))},",
        f"trials={len(plan['trials'])}, distinct families={len(set(families))}, sizes={sizes},",
        f"derivation.family_order={len(plan.get('derivation', {}).get('family_order', []))} ids",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
