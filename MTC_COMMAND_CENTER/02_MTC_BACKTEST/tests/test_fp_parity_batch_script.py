import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import run_fp_parity_batch  # noqa: E402


def test_discover_templates_returns_expected_fp_cases():
    items = run_fp_parity_batch.discover_templates()
    names = [x.name for x in items]
    assert len(items) == 13
    assert names == sorted(names)
    assert names[0].startswith("fp01_")
    assert names[-1].startswith("fp13_")
