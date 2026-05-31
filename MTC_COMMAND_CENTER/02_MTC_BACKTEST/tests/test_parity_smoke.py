"""
Smoke test: verify parity_regression script is importable and the
canonical case file exists.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))


def test_parity_regression_importable():
    """parity_regression.py can be imported without error."""
    import parity_regression
    assert hasattr(parity_regression, "run")
    assert hasattr(parity_regression, "MAX_MISMATCH")
    assert hasattr(parity_regression, "MAX_PNL_DELTA")


def test_canonical_case_exists():
    """The canonical parity case JSON exists."""
    case_path = PROJECT_ROOT / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    assert case_path.exists(), f"Missing: {case_path}"


def test_tv_reference_csv_exists():
    """TV reference CSV referenced in case file exists."""
    import json
    case_path = PROJECT_ROOT / "configs" / "cases" / "full_jul2025_jan2026_parity.json"
    with open(case_path, encoding="utf-8") as f:
        case = json.load(f)
    tv_csv = PROJECT_ROOT / case.get("tv_csv", "")
    assert tv_csv.exists(), f"Missing TV CSV: {tv_csv}"


def test_acceptance_thresholds():
    """Verify acceptance thresholds match docs."""
    import parity_regression
    assert parity_regression.MAX_MISMATCH == 0
    assert parity_regression.MAX_PNL_DELTA == 10.0
    assert parity_regression.MAX_DD_PCT_DELTA == 10.0
