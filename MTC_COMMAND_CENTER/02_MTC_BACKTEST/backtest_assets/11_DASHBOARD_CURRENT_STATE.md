# 11_DASHBOARD_CURRENT_STATE.md — Dashboard Status
Last Updated: 2026-03-05

## 1. Discovery Status
**Status:** CONFIRMED

**Operator v2** implemented in `app.py`.
Streamlit-based "Golden Workflow" controller.

## 2. Frontend Location
- **Root:** `C:\LAB\tradingview-lab\mtc_backtest`
- **Entrypoint:** `app.py`
- **UI Modules:** `src/ui/` (implied by project structure)
- **Framework:** Streamlit

## 3. Execution Method
- **Launcher:** `run_app.bat` (Windows)
- **Core Command:** `python -m streamlit run app.py`
- **Port:** Default 8501 (configurable via arg)
- **Environment:** Auto-managed `venv` + `requirements.txt`

## 4. Data Consumption
- **Inputs:** `data/` (OHLCV datasets)
- **Outputs:** `exports/` (Backtest results, run artifacts)
- **Logs:** `logs/`

## 5. Operator v2 Capabilities
- **Primary Signal:** Registry-driven (`module_registry.yaml`).
- **Asset/TF:** Auto-discovery from `data/` + multi-TF download.
- **Workflow Methods:**
  - Parity Smoke (Raw + Clip)
  - Optimization Scopes (Signal, Exits, Filters, Money, Full)
  - Robustness (WFO, Regime)
  - Monte Carlo (Bootstrap)
- **Execution:** Generates copy-paste CLI commands (Safe by Default) with optional local execution.

## 6. Command Mapping (Source of Truth)
- Backtest: `scripts/run_case.py`
- Parity: `scripts/compare_tv_web_trades.py`
- Optimize: `src.optimizer_v0` / `scripts/staged_optimize.py`
- Robustness: `scripts/walk_forward_validate.py` / `scripts/robustness_runner.py`