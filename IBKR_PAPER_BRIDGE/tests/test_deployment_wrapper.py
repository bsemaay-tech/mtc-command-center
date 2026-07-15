from pathlib import Path


def test_p2_supervisor_resolves_runtime_from_its_own_location() -> None:
    root = Path(__file__).resolve().parents[1]
    script = (root / "tools" / "run_bridge_p2.ps1").read_text(encoding="utf-8")

    assert "$root = Split-Path -Parent $PSScriptRoot" in script
    assert "C:\\LAB\\Tradingview_LAB_CLEAN\\IBKR_PAPER_BRIDGE" not in script
