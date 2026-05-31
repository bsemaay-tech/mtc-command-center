# Previous Code Inventory - CRABEL_RANGE_EXPANSION

## Located Files
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\src\features.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\src\backtest.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\src\exits.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\src\reports.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\tests\test_features.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\tests\test_backtest_rules.py
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\SPEC.md
- 06_QUANTLENS_LAB\research\strategy_batch_2026_05_03_AUDITED\strategies\04_crabel_range_expansion_stage2\config.yml
- 06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03_CLEAN\candidates\CANDIDATE_004_crabel_range_expansion.md
- 06_QUANTLENS_LAB\research\overnight_intake_batch_2026_05_03_AUDITED\candidates_audited\AUD_CAND_004_crabel_range_expansion.md
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\trades.csv
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\results.csv
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\config.json
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\baseline_comparison.csv
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\walkforward_results.csv
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\asset_results.csv
- 06_QUANTLENS_LAB\research\stage2_robustness_2026_05_03_CODEX_20260503_232808\strategies\CRABEL\fee_stress_results.csv

## Missing Expected Files

## Mechanical Inventory
- strategy_functions: previous batch `src/features.py`, `src/backtest.py`, and Stage-2 `run_stage2_codex.py` signal functions were inspected/copied where present.
- signal_generation_code: rolling indicators and prior-bar/next-bar signal logic are present in previous Python prototypes.
- entry_logic: mostly next-bar open; Crabel uses same-bar stop-trigger price in Stage-2, which is separately flagged.
- exit_logic: ATR/time/close exits; Stage-2 helper is stop-first for same-bar SL/TP conflict.
- cost_model: base round-trip cost recomputed here as 0.12 percent.
- slippage_model: previous reports collapse fee/slippage into one cost; this Stage-2B trace splits it evenly for explicit audit columns.
- position_sizing: one unit / percent return model; no real capital sizing.
- warmup_handling: implemented with fixed starting indexes; not uniformly contract-derived.
- timeframe_assumptions: 1D, mostly crypto proxy.
- asset_list: Stage-2 used Binance futures symbols where available.
- data_source: range_expansion_crypto_proxy.
