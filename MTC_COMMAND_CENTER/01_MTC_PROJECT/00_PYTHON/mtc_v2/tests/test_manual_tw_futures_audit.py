from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
AUDIT_SCRIPT = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/manual_tw_futures_audit.py"
CASE_001_XLSX = REPO_ROOT / "01_MASTER TEMPLATE_V2/05_PARITY/case_001/MTC_V2_BINANCE_BTCUSDT.P_2026-04-03_827c5.xlsx"


def _load_audit_module():
    spec = importlib.util.spec_from_file_location("manual_tw_futures_audit_module", AUDIT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load audit script from {AUDIT_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_case_001_export_rebuilds_critical_overrides_from_workbook_properties():
    audit = _load_audit_module()
    chart_tz = audit.parse_chart_timezone("UTC+3")
    xlsx_info = audit.read_tv_workbook(CASE_001_XLSX, chart_tz)

    overrides = audit.build_case_overrides(xlsx_info)

    assert "execution_profile_id" not in overrides
    assert "tw_audit_semantics_mode" not in overrides
    assert "tw_reversal_reentry_mode" not in overrides
    assert "tw_reversal_reentry_delay_bars" not in overrides
    assert "tw_margin_call_mode" not in overrides
    assert "tw_margin_call_split_entries" not in overrides
    assert "tw_be_semantics_mode" not in overrides
    assert "tw_trailing_semantics_mode" not in overrides
    assert overrides["allow_flip"] is False
    assert overrides["st_atr_len"] == 21
    assert overrides["st_factor"] == 4.0
    assert overrides["risk_per_long_pct"] == 1.0
    assert overrides["risk_per_short_pct"] == 1.0
    assert overrides["fallback_size_pct"] == 10.0
    assert overrides["max_leverage_cap"] == 1.0
    assert overrides["margin_long_pct"] == 100.0
    assert overrides["margin_short_pct"] == 100.0
    assert overrides["sl_mode"] == "None"
    assert overrides["tp_mode"] == "None"
    assert overrides["exit_on_opposite_signal"] is True


def test_open_reason_normalizes_to_terminal_close():
    audit = _load_audit_module()
    assert audit.normalize_reason("Open") == "TERMINAL_CLOSE"
