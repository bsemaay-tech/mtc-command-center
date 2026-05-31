import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_synthetic_l2_compare_passes():
    out_md = ROOT / "reports/test_synthetic_L2_compare.md"
    out_json = ROOT / "reports/test_synthetic_L2_compare.json"
    cmd = [
        sys.executable,
        str(ROOT / "parity_oracles/compare/parity_compare.py"),
        "--baseline-dir", str(ROOT / "examples/synthetic_outputs/baseline_python"),
        "--candidate-dir", str(ROOT / "examples/synthetic_outputs/candidate_pinets"),
        "--level", "L2",
        "--out-md", str(out_md),
        "--out-json", str(out_json),
    ]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert out_md.exists()
    assert out_json.exists()
