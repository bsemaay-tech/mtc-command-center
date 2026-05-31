import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TPL_DIR = PROJECT_ROOT / "configs" / "cases" / "fp_parity_templates"


EXPECTED = [
    "fp01_range_filter_hybrid_template.json",
    "fp02_htf_trend_filter_template.json",
    "fp03_mcginley_filter_template.json",
    "fp04_confirmation_layer_template.json",
    "fp05_range_regime_filter_template.json",
    "fp06_filter_block_exit_template.json",
    "fp07_pending_queue_template.json",
    "fp08_guard_recovery_template.json",
    "fp09_macd_hub_filter_template.json",
    "fp10_daily_limits_template.json",
    "fp11_mae_guard_template.json",
    "fp12_consec_loss_reset_template.json",
    "fp13_time_stop_eod_eow_template.json",
]


def test_fp_parity_template_pack_exists_and_is_well_formed():
    assert TPL_DIR.exists(), f"Missing template dir: {TPL_DIR}"
    for name in EXPECTED:
        p = TPL_DIR / name
        assert p.exists(), f"Missing template: {p}"
        with open(p, encoding="utf-8-sig") as f:
            data = json.load(f)
        assert data.get("dataset"), f"dataset missing in {name}"
        assert data.get("tv_csv"), f"tv_csv missing in {name}"
        cfg = data.get("config", {})
        parity = cfg.get("parity", {})
        assert parity.get("enabled") is True, f"parity.enabled must be true in {name}"
        assert parity.get("fill_contract") == "touch", f"fill_contract must be touch in {name}"
