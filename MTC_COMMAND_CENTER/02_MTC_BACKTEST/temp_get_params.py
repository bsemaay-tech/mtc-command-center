import json
import os

from src.config.case_schema import CaseConfig
from src.config.loader import load_case_config, apply_candidate_to_config

base_path = r"C:\LAB\tradingview-lab\mtc_backtest\configs\cases\range_filter_hybrid_signal_baseline_15m_jun2025_jan2026.json"
cand_path = r"C:\LAB\tradingview-lab\mtc_backtest\results\autopilot_rf_deep\staged_opt\autopilot_20260307_210016Z\money\candidates\candidate_004__ddpct_0_62__net_m1_17__key_da39a3ee5e6b.json"

base_case = load_case_config(base_path)
merged_case = apply_candidate_to_config(base_case, cand_path)

print(json.dumps(merged_case.config.model_dump(), indent=2))
