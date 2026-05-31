"""
MTC Python Backtest & Optimization System.

Main Streamlit application entry point.
"""

import streamlit as st
import logging
from pathlib import Path
import json
import yaml
import subprocess
import sys

# Create required directories FIRST (before logging setup)
Path("data").mkdir(exist_ok=True)
Path("exports").mkdir(exist_ok=True)
Path("exports/runs").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)
Path("debug").mkdir(exist_ok=True)

# Configure logging (after logs dir exists)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# Page config - must be first Streamlit call
st.set_page_config(
    page_title="MTC Backtest",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styles
try:
    from utils.styles import apply_styles
    apply_styles()
except ImportError:
    logging.warning("utils.styles not found, using default styles.")



def main():
    """Main application."""
    
    # Sidebar
    with st.sidebar:
        st.title("MTC Backtest")
        st.caption("v1.0.0 | MASTER_TEMPLATE_CORE Python Port")
        
        st.divider()
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["Operator", "Data Download", "Runs & Artifacts", "Classic Backtest", "Classic Optimize"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick stats
        st.subheader("Quick Stats")
        
        # Count datasets
        data_path = Path("data")
        dataset_count = len(list(data_path.glob("*.parquet"))) + len(list(data_path.glob("*.csv")))
        st.metric("Datasets", dataset_count)
        
        # Count exports
        exports_path = Path("exports/runs")
        export_count = len(list(exports_path.glob("*"))) if exports_path.exists() else 0
        st.metric("Backtest Runs", export_count)
    
    # Main content based on selection
    if page == "Operator":
        show_operator_page()
    elif page == "Data Download":
        show_download_page()
    elif page == "Runs & Artifacts":
        show_runs_page()
    elif page == "Classic Backtest":
        show_backtest_page()
    elif page == "Classic Optimize":
        show_optimize_page()


def show_operator_page():
    """Operator v2 Main Entrypoint."""
    st.title("MTC Operator v2")
    st.caption("Golden Workflow Controller (Parity-Locked)")

    # --- 1. Inputs ---
    st.subheader("1. Setup")
    col1, col2, col3 = st.columns(3)
    
    # Load Registry
    registry_path = Path("backtest_assets/module_registry.yaml")
    modules = []
    if registry_path.exists():
        try:
            with open(registry_path, 'r') as f:
                reg = yaml.safe_load(f)
                modules = reg.get('modules', [])
        except Exception as e:
            st.error(f"Failed to load registry: {e}")
    
    signal_options = [m['id'] for m in modules if m['type'] == 'signal']
    if not signal_options: signal_options = ["supertrend", "range_filter_hybrid"] # Fallback

    with col1:
        primary_signal = st.selectbox("Primary Signal", signal_options, index=0)
    
    # Asset Selection
    from src.data.io import list_datasets
    datasets = list_datasets("./data")
    dataset_map = {ds['filename']: ds for ds in datasets}
    dataset_files = sorted(list(dataset_map.keys()))
    
    with col2:
        selected_dataset = st.selectbox("Asset / Dataset", dataset_files if dataset_files else ["No Data"])
        
    # Timeframe (Derived from dataset or manual)
    with col3:
        # Try to infer TF from filename
        inferred_tf = "15m"
        if selected_dataset != "No Data":
            parts = selected_dataset.split('_')
            for p in parts:
                if p.endswith('m') or p.endswith('h') or p.endswith('d'):
                    inferred_tf = p
                    break
        timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "2h", "4h", "1d"], index=["1m", "5m", "15m", "1h", "2h", "4h", "1d"].index(inferred_tf) if inferred_tf in ["1m", "5m", "15m", "1h", "2h", "4h", "1d"] else 2)

    # Date Range
    with st.expander("Test Window & Engine Settings", expanded=False):
        c_d1, c_d2 = st.columns(2)
        with c_d1:
            start_date = st.date_input("Start Date", value=None)
            preroll_days = st.number_input("Preroll Days", value=90)
        with c_d2:
            end_date = st.date_input("End Date", value=None)
            warmup_bars = st.number_input("Warmup Bars", value=200)

    # --- 2. Workflow Methods ---
    st.subheader("2. Workflow Methods")
    
    # Parity
    use_parity = st.checkbox("A) Parity Smoke Test (Raw + Clip)", value=False)
    if use_parity:
        st.caption("Classifiers: TV_EARLY_TRADE_END_CANDIDATE, gap_days")
        c_p1, c_p2 = st.columns(2)
        tv_csv = c_p1.text_input("TV Trades CSV", "debug/tv_trades.csv")
        py_csv = c_p2.text_input("Py Trades CSV", "debug/debug_python_trades.csv")

    # Optimization
    opt_scope = st.selectbox(
        "B) Optimization Scope", 
        ["F: Validation-only (No Opt)", "A: Signal-only", "B: Exits-only", "C: Filters Ablation", "D: Money Management", "E: Full Staged"]
    )
    
    # Robustness
    c_r1, c_r2, c_r3 = st.columns(3)
    use_wfo = c_r1.checkbox("C) Walk-Forward", value=False)
    use_regime = c_r2.checkbox("Regime Eval", value=False)
    use_mc = c_r3.checkbox("D) Monte Carlo", value=False)
    
    # Multi-objective
    st.caption("E) Multi-objective: profit_dd_ratio (default)")

    # --- 3. Run Settings ---
    st.subheader("3. Run Settings")
    c_s1, c_s2, c_s3 = st.columns(3)
    trials = c_s1.number_input("Trials", value=30, min_value=1)
    seed = c_s2.number_input("Seed", value=42)
    workers = c_s3.number_input("Workers", value=1, help="Keep 1 for determinism")

    # --- 4. Action ---
    st.subheader("4. Execution")
    
    if st.button("Generate Run Plan"):
        plan_text = []
        plan_text.append("# MTC Operator v2 Run Plan")
        plan_text.append(f"# Date: {pd.Timestamp.now()}")
        plan_text.append(f"# Signal: {primary_signal} | Asset: {selected_dataset}")
        plan_text.append("")
        
        # 1. Generate Case JSON (Virtual Step)
        case_filename = f"configs/cases/temp_operator_{primary_signal}.json"
        plan_text.append(f"# Step 1: Ensure Case File Exists")
        plan_text.append(f"# (Operator would generate {case_filename} with selected settings)")
        
        # 2. Backtest / Parity
        if use_parity:
            plan_text.append("\n# Step 2: Parity Check")
            plan_text.append(f"python scripts/run_case.py {case_filename}")
            plan_text.append(f"python scripts/compare_tv_web_trades.py --tv {tv_csv} --py {py_csv} --dual-report")
        
        # 3. Optimization
        if opt_scope.startswith("F"):
            plan_text.append("\n# Step 3: Single Backtest (No Opt)")
            plan_text.append(f"python scripts/run_case.py {case_filename}")
        elif opt_scope.startswith("E"):
            plan_text.append("\n# Step 3: Staged Optimization")
            plan_text.append(f"python scripts/staged_optimize.py --case {case_filename} --stages-file configs/spaces/staged_{primary_signal}.json --seed {seed} --workers {workers}")
        else:
            plan_text.append(f"\n# Step 3: Optimization ({opt_scope})")
            plan_text.append(f"python -m src.optimizer_v0 run --case {case_filename} --mode random --iters {trials} --seed {seed}")

        # 4. Robustness
        if use_wfo:
            plan_text.append("\n# Step 4: Walk-Forward Analysis")
            plan_text.append(f"python scripts/walk_forward_validate.py --train-case {case_filename} --iters {trials} --seed {seed}")
        
        if use_regime:
            plan_text.append("\n# Step 5: Robustness (Regime)")
            plan_text.append(f"python scripts/robustness_runner.py --case {case_filename} --candidate results/latest/best.json")

        # 5. Monte Carlo
        if use_mc:
            plan_text.append("\n# Step 6: Monte Carlo Analysis")
            plan_text.append(f"python scripts/monte_carlo_bootstrap.py results/backtest_runs/latest/results.json")

        st.code("\n".join(plan_text), language="bash")
        st.session_state['run_plan'] = plan_text
        st.session_state['run_config'] = {
            'signal': primary_signal,
            'dataset': selected_dataset,
            'tf': timeframe,
            'start': str(start_date) if start_date else None,
            'end': str(end_date) if end_date else None,
            'preroll': preroll_days,
            'warmup': warmup_bars
        }

    execute_toggle = st.checkbox("I understand this runs local commands", value=False)
    if execute_toggle and 'run_plan' in st.session_state:
        if st.button("EXECUTE RUN PLAN", type="primary"):
            st.warning("Execution started... Check console for logs.")
            
            # Generate the temp case file
            cfg = st.session_state['run_config']
            case_data = {
                "dataset": cfg['dataset'],
                "strategy": {"signal_mode": cfg['signal']}, # Simplified
                "config": {} # Would populate full config here
            }
            # In a real impl, we'd dump this to json
            # with open(f"configs/cases/temp_operator_{cfg['signal']}.json", 'w') as f:
            #    json.dump(case_data, f)
            
            # Execute commands
            log_container = st.empty()
            full_logs = ""
            
            for line in st.session_state['run_plan']:
                if line.startswith("python"):
                    cmd = line.strip()
                    full_logs += f"> {cmd}\n"
                    log_container.code(full_logs)
                    
                    try:
                        # Use shell=True for Windows python command parsing
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        full_logs += result.stdout + "\n"
                        if result.stderr:
                            full_logs += f"[STDERR] {result.stderr}\n"
                    except Exception as e:
                        full_logs += f"[ERROR] {e}\n"
                    
                    log_container.code(full_logs)
            
            st.success("Execution Complete")


def show_runs_page():
    """Unified Runs & Artifacts Browser."""
    st.title("Runs & Artifacts")
    
    # Scan directories
    roots = [
        Path("results/backtest_runs"),
        Path("results/parity_runs"),
        Path("results/staged_opt"),
        Path("results/robustness")
    ]
    
    runs = []
    for root in roots:
        if root.exists():
            for run_dir in root.iterdir():
                if run_dir.is_dir():
                    runs.append({
                        "Type": root.name,
                        "ID": run_dir.name,
                        "Path": str(run_dir),
                        "Manifest": (run_dir / "manifest.json").exists(),
                        "Report": (run_dir / "report.md").exists()
                    })
    
    if runs:
        import pandas as pd
        df = pd.DataFrame(runs)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No runs found.")


def show_download_page():
    """Data download page."""
    st.title("Data Download")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Download Settings")
        
        symbol = st.text_input("Symbol", value="BTCUSDT")
        timeframes = st.multiselect(
            "Timeframes",
            ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"],
            default=["15m"]
        )
        
        from datetime import datetime, timedelta
        default_end = datetime.now()
        default_start = default_end - timedelta(days=365)
        
        start_date = st.date_input("Start Date", value=default_start)
        end_date = st.date_input("End Date", value=default_end)
        
        force_download = st.checkbox("Force redownload", value=False)
        
        if st.button("Download", type="primary", use_container_width=True):
            with st.spinner(f"Downloading {symbol} {timeframes}..."):
                try:
                    from src.data.cache import get_or_download
                    from datetime import timezone
                    
                    start_dt = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=timezone.utc)
                    end_dt = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)
                    for tf in timeframes:
                        df = get_or_download(
                            symbol=symbol,
                            timeframe=tf,
                            start_date=start_dt,
                            end_date=end_dt,
                            force=force_download,
                        )
                        st.write(f"Downloaded {tf}: {len(df)} bars")
                        
                    st.success(f"Download complete for {symbol}")
                    st.dataframe(df.head(10))
                    
                except Exception as e:
                    st.error(f"Download failed: {e}")
    
    with col2:
        st.subheader("Available Datasets")
        
        from src.data.io import list_datasets
        datasets = list_datasets("./data")
        
        if datasets:
            # Create table
            table_data = []
            for ds in datasets:
                table_data.append({
                    "File": ds['filename'],
                    "Bars": ds.get('bar_count', 'N/A'),
                    "Size": f"{ds['size_bytes'] / 1024:.1f} KB",
                    "Symbol": ds.get('symbol', 'N/A'),
                    "TF": ds.get('timeframe', 'N/A'),
                })
            
            st.dataframe(table_data, use_container_width=True)
        else:
            st.info("No datasets found. Download some data first!")
        
        # CSV Upload
        st.subheader("Upload CSV")
        uploaded = st.file_uploader("Upload OHLCV CSV", type=["csv"])
        
        if uploaded:
            import pandas as pd
            df = pd.read_csv(uploaded)
            st.write(f"Uploaded {len(df)} rows")
            st.dataframe(df.head())
            
            if st.button("Save to Data Directory"):
                save_path = Path("data") / uploaded.name
                df.to_csv(save_path, index=False)
                st.success(f"Saved to {save_path}")


def show_backtest_page():
    """Backtest page."""
    st.title("Backtest")
    st.caption("Step 1: Setup")

    from src.data.io import list_datasets
    from src.config.defaults import MTCConfig
    from src.ui.dataset_defaults import choose_default_dataset
    from src.ui.parity_case_loader import build_backtest_state_from_case, diff_backtest_state_with_case

    datasets = list_datasets("./data")
    if not datasets:
        st.warning("No datasets available. Please download data first.")
        return

    dataset_options = [ds['filename'] for ds in datasets]
    preferred_dataset = choose_default_dataset(datasets)
    if preferred_dataset is None:
        preferred_dataset = dataset_options[0]
    if "bt_dataset" not in st.session_state:
        st.session_state["bt_dataset"] = preferred_dataset
    if st.session_state["bt_dataset"] not in dataset_options:
        st.session_state["bt_dataset"] = preferred_dataset

    with st.expander("Parity Case Loader", expanded=False):
        case_dir = Path("configs/cases")
        case_files = sorted(str(p.as_posix()) for p in case_dir.glob("*.json")) if case_dir.exists() else []
        if case_files:
            selected_case = st.selectbox("Case File", case_files, key="bt_case_file")
            if st.button("Load Case into Backtest Settings", key="bt_load_case"):
                try:
                    state = build_backtest_state_from_case(Path(selected_case))
                    missing_dataset = None
                    if state.get("bt_dataset") not in dataset_options:
                        missing_dataset = state.get("bt_dataset")
                        state["bt_dataset"] = preferred_dataset
                    for k, v in state.items():
                        st.session_state[k] = v
                    if missing_dataset:
                        st.warning(f"Case dataset not found locally: {missing_dataset}. Fallback dataset selected.")
                    st.success(f"Loaded parity case: {selected_case}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load case: {e}")
            if st.button("Validate Current Settings vs Case", key="bt_validate_case"):
                try:
                    mismatches = diff_backtest_state_with_case(Path(selected_case), dict(st.session_state))
                    if mismatches:
                        st.warning(f"Case mismatch ({len(mismatches)} key): " + ", ".join(mismatches[:10]))
                    else:
                        st.success("Current settings match case values.")
                except Exception as e:
                    st.error(f"Case validation failed: {e}")
        else:
            st.info("No case JSON files found under configs/cases.")

    selected_dataset = st.selectbox("Select Dataset", dataset_options, key="bt_dataset")

    with st.expander("Test Range (Backtest)"):
        col_bt_tr1, col_bt_tr2 = st.columns(2)
        with col_bt_tr1:
            from datetime import date
            bt_start_date = st.date_input("Start Date", value=date(2025, 12, 1), key="bt_range_start")
            bt_warmup_bars = st.number_input("Warmup Bars", min_value=0, value=200, key="bt_warmup")
        with col_bt_tr2:
            bt_end_date = st.date_input("End Date", value=date(2025, 12, 31), key="bt_range_end")
            bt_preroll_days = st.number_input("Preroll Days", min_value=0, value=90, key="bt_preroll_days",
                                             help="Days before test start for indicator warmup (RMA/ATR convergence). 90 recommended.")

    config = MTCConfig()

    with st.sidebar:
        st.divider()
        st.subheader("Advanced Settings")
        st.caption("Collapsed by default for cleaner workflow. Expand only what you need.")

        with st.expander("Signal Settings", expanded=True):
            config.signal_mode = st.selectbox(
                "Signal Mode",
                ["Supertrend", "Range Filter Hybrid (ADX+Chop+BB)", "None"],
                index=0,
                key="bt_signal_mode",
            )
            col_sig_l, col_sig_r = st.columns(2)
            with col_sig_l:
                config.supertrend.atr_len = st.number_input("ATR Len", min_value=1, value=int(config.supertrend.atr_len), key="bt_st_atr_len")
                config.supertrend.use_ha = st.checkbox("Use HA", value=bool(config.supertrend.use_ha), key="bt_st_ha")
            with col_sig_r:
                config.supertrend.factor = st.number_input("Factor", min_value=0.1, value=float(config.supertrend.factor), step=0.1, key="bt_st_factor")
                config.supertrend.use_wicks = st.checkbox("Use Wicks", value=bool(config.supertrend.use_wicks), key="bt_st_wicks")

            st.caption("Range Filter params are visible for parity mapping; Python module is not implemented yet.")
            col_rf_l, col_rf_r = st.columns(2)
            with col_rf_l:
                config.range_filter.adx_trend_threshold = st.number_input("RF ADX Trend", min_value=15, max_value=50, value=int(config.range_filter.adx_trend_threshold), key="bt_rf_adx_tr")
                config.range_filter.chop_trend_threshold = st.number_input("RF Chop Trend", min_value=30, max_value=70, value=int(config.range_filter.chop_trend_threshold), key="bt_rf_chop_tr")
                config.range_filter.rsi_len = st.number_input("RF RSI Len", min_value=5, max_value=50, value=int(config.range_filter.rsi_len), key="bt_rf_rsi_len")
                config.range_filter.rsi_oversold = st.number_input("RF RSI Oversold", min_value=10, max_value=40, value=int(config.range_filter.rsi_oversold), key="bt_rf_rsi_os")
                config.range_filter.bb_len = st.number_input("RF BB Len", min_value=10, max_value=50, value=int(config.range_filter.bb_len), key="bt_rf_bb_len")
            with col_rf_r:
                config.range_filter.adx_range_threshold = st.number_input("RF ADX Range", min_value=10, max_value=30, value=int(config.range_filter.adx_range_threshold), key="bt_rf_adx_rg")
                config.range_filter.chop_range_threshold = st.number_input("RF Chop Range", min_value=50, max_value=80, value=int(config.range_filter.chop_range_threshold), key="bt_rf_chop_rg")
                config.range_filter.rsi_overbought = st.number_input("RF RSI Overbought", min_value=60, max_value=90, value=int(config.range_filter.rsi_overbought), key="bt_rf_rsi_ob")
                config.range_filter.bb_mult = st.number_input("RF BB Mult", min_value=1.0, max_value=3.0, step=0.1, value=float(config.range_filter.bb_mult), key="bt_rf_bb_mult")
                config.range_filter.use_bb_filter = st.checkbox("RF Use BB", value=bool(config.range_filter.use_bb_filter), key="bt_rf_use_bb")

        with st.expander("Trade Settings", expanded=False):
            col_trade_l, col_trade_r = st.columns(2)
            with col_trade_l:
                config.trade.enable_long = st.checkbox("Enable Long", value=bool(config.trade.enable_long), key="bt_enable_long")
                config.trade.enable_short = st.checkbox("Enable Short", value=bool(config.trade.enable_short), key="bt_enable_short")
                config.trade.allow_flip = st.checkbox("Allow Flip", value=bool(config.trade.allow_flip), key="bt_allow_flip")
                config.trade.use_regime_lock = st.checkbox("Regime Lock", value=bool(config.trade.use_regime_lock), key="bt_regime_lock")
                config.trade.entry_mode = st.selectbox("Entry Mode", ["Edge", "Signal"], index=1 if config.trade.entry_mode == "Signal" else 0, key="bt_entry_mode")
            with col_trade_r:
                config.trade.exit_on_opposite_signal = st.checkbox("Exit on Opposite", value=bool(config.trade.exit_on_opposite_signal), key="bt_exit_opp")
                config.trade.exit_on_filter_block = st.checkbox("Exit on Filter Block", value=bool(config.trade.exit_on_filter_block), key="bt_exit_fb", help="Per-filter exit controls are handled below.")
                config.trade.max_pyramid_positions = st.number_input("Max Pyramid", min_value=1, max_value=5, value=int(config.trade.max_pyramid_positions), key="bt_pyr_max")
                config.trade.signal_mode_max_entries = st.number_input("Signal Max Entries", min_value=1, max_value=3, value=int(config.trade.signal_mode_max_entries), key="bt_sig_max_ent")
                config.trade.signal_mode_cooldown_bars = st.number_input("Signal Cooldown", min_value=1, value=int(config.trade.signal_mode_cooldown_bars), key="bt_sig_cd")

        with st.expander("Time Stop", expanded=False):
            config.time_stop.enabled = st.checkbox("Use Time Stop", value=bool(config.time_stop.enabled), key="bt_ts_en")
            config.time_stop.bars = st.number_input("Time Stop Bars", min_value=1, value=int(config.time_stop.bars), key="bt_ts_bars")
            config.time_stop.eod = st.checkbox("Exit at End of Day (EOD)", value=bool(config.time_stop.eod), key="bt_ts_eod")
            config.time_stop.eow = st.checkbox("Exit at End of Week (EOW)", value=bool(config.time_stop.eow), key="bt_ts_eow")
            config.time_stop.condition = st.selectbox("Time Stop Condition", ["Always", "Profit Only", "Loss Only"], index=["Always", "Profit Only", "Loss Only"].index(config.time_stop.condition), key="bt_ts_cond")
            st.caption("EOD/EOW time stop is available in Python engine.")

        with st.expander("Exit Filter Block Triggers", expanded=False):
            st.caption("Per-filter exit triggers (requires 'Exit on Filter Block' ON above)")
            config.exit_filter_block.exit_on_ma_block = st.checkbox("Exit on MA Block", value=False, key="bt_efb_ma")
            config.exit_filter_block.exit_on_ma_slope_block = st.checkbox("Exit on MA Slope Block", value=False, key="bt_efb_maslope")
            config.exit_filter_block.exit_on_mcginley_block = st.checkbox("Exit on McGinley Block", value=bool(config.exit_filter_block.exit_on_mcginley_block), key="bt_efb_mcg")
            config.exit_filter_block.exit_on_htf_trend_block = st.checkbox("Exit on HTF Trend Block", value=False, key="bt_efb_htf")
            config.exit_filter_block.exit_on_vol_part_block = st.checkbox("Exit on Volume Block", value=bool(config.exit_filter_block.exit_on_vol_part_block), key="bt_efb_vol")
            config.exit_filter_block.exit_on_atr_vol_block = st.checkbox("Exit on ATR Vol Block", value=False, key="bt_efb_atrvol")
            config.exit_filter_block.exit_on_range_block = st.checkbox("Exit on Range Block", value=False, key="bt_efb_range")
            st.caption("Filter-block exits are supported (global and granular).")

        with st.expander("Risk Settings", expanded=False):
            col_risk_l, col_risk_r = st.columns(2)
            with col_risk_l:
                config.risk.risk_long_percent = st.number_input("Long Risk %", min_value=0.01, value=float(config.risk.risk_long_percent), step=0.1, key="bt_risk_long")
                config.risk.max_leverage_cap = st.number_input("Max Leverage", min_value=1.0, value=float(config.risk.max_leverage_cap), step=0.5, key="bt_lev_cap")
                config.risk.fallback_qty_pct = st.number_input("Fallback Qty %", min_value=0.1, max_value=100.0, value=float(config.risk.fallback_qty_pct), step=0.1, key="bt_fallback_qty")
                config.risk.risk_equity_mode = st.selectbox(
                    "Risk Equity Source",
                    ["Initial", "Realized"],
                    index=["Initial", "Realized"].index(config.risk.risk_equity_mode),
                    key="bt_risk_equity_mode",
                )
                config.risk.use_notional_hard_assert = st.checkbox(
                    "Notional Hard Assert",
                    value=bool(config.risk.use_notional_hard_assert),
                    key="bt_notional_hard_assert",
                )
            with col_risk_r:
                config.risk.risk_short_percent = st.number_input("Short Risk %", min_value=0.01, value=float(config.risk.risk_short_percent), step=0.1, key="bt_risk_short")
                config.risk.use_daily_loss_limit = st.checkbox("Use Daily Loss Limit", value=bool(config.risk.use_daily_loss_limit), key="bt_daily_loss_en")
                config.risk.max_daily_loss_percent = st.number_input("Max Daily Loss %", min_value=0.1, value=float(config.risk.max_daily_loss_percent), step=0.1, key="bt_daily_loss")
                config.risk.use_max_trades_per_day = st.checkbox("Use Max Trades/Day", value=bool(config.risk.use_max_trades_per_day), key="bt_max_trades_en")
                config.risk.max_trades_per_day = st.number_input("Max Trades/Day", min_value=1, value=int(config.risk.max_trades_per_day), key="bt_max_trades")

        with st.expander("SL / TP / BE / Trailing", expanded=False):
            config.stop_loss.enabled = st.checkbox("Use Stop Loss", value=bool(config.stop_loss.enabled), key="bt_sl_en")
            config.stop_loss.mode = st.selectbox("SL Mode", ["ATR", "%", "Swing+ATR", "SWING_ATR"], index=["ATR", "%", "Swing+ATR", "SWING_ATR"].index(config.stop_loss.mode), key="bt_sl_mode")
            config.stop_loss.atr_len = st.number_input("SL ATR Length", min_value=1, value=int(config.stop_loss.atr_len), key="bt_sl_atr_len")
            config.stop_loss.atr_mult = st.number_input("SL ATR Mult", min_value=0.1, value=float(config.stop_loss.atr_mult), step=0.1, key="bt_sl_atr_mult")
            config.stop_loss.percent = st.number_input("SL Percent", min_value=0.1, value=float(config.stop_loss.percent), step=0.1, key="bt_sl_pct")
            config.stop_loss.swing_basis = st.selectbox("Swing SL Basis", ["Wick", "Body"], index=0 if config.stop_loss.swing_basis == "Wick" else 1, key="bt_sl_swing_basis")
            config.stop_loss.swing_lookback = st.number_input("Swing SL Lookback", min_value=1, value=int(config.stop_loss.swing_lookback), key="bt_sl_swing_lb")
            config.stop_loss.swing_atr_len = st.number_input("Swing SL ATR Length", min_value=1, value=int(config.stop_loss.swing_atr_len), key="bt_sl_swing_atr_len")
            config.stop_loss.swing_atr_mult = st.number_input("Swing SL ATR Mult", min_value=0.0, value=float(config.stop_loss.swing_atr_mult), step=0.1, key="bt_sl_swing_atr_mult")

            config.take_profit.enabled = st.checkbox("Use Take Profit", value=bool(config.take_profit.enabled), key="bt_tp_en")
            config.take_profit.mode = st.selectbox("TP Mode", ["ATR", "%", "R"], index=["ATR", "%", "R"].index(config.take_profit.mode), key="bt_tp_mode")
            config.take_profit.atr_len = st.number_input("TP ATR Length", min_value=1, value=int(config.take_profit.atr_len), key="bt_tp_atr_len")
            config.take_profit.atr_mult = st.number_input("TP ATR Mult", min_value=0.1, value=float(config.take_profit.atr_mult), step=0.1, key="bt_tp_atr_mult")
            config.take_profit.percent = st.number_input("TP Percent", min_value=0.1, value=float(config.take_profit.percent), step=0.1, key="bt_tp_pct")
            config.take_profit.rr = st.number_input("TP R Multiple", min_value=0.1, value=float(config.take_profit.rr), step=0.1, key="bt_tp_rr")

            config.multi_tp.enabled = st.checkbox("Use Multi-TP", value=bool(config.multi_tp.enabled), key="bt_mtp_en")
            config.multi_tp.tp1_rr = st.number_input("TP1 R", min_value=0.1, value=float(config.multi_tp.tp1_rr), step=0.1, key="bt_tp1_rr")
            config.multi_tp.tp1_pct = st.number_input("TP1 Close %", min_value=1.0, max_value=99.0, value=float(config.multi_tp.tp1_pct), step=1.0, key="bt_tp1_pct")
            config.multi_tp.tp2_rr = st.number_input("TP2 R", min_value=0.1, value=float(config.multi_tp.tp2_rr), step=0.1, key="bt_tp2_rr")

            config.break_even.enabled = st.checkbox("Use Break-Even", value=bool(config.break_even.enabled), key="bt_be_en")
            config.break_even.rr = st.number_input("BE Trigger (R)", min_value=0.1, value=float(config.break_even.rr), step=0.1, key="bt_be_rr")
            config.break_even.buffer_r = st.number_input("BE Buffer (R)", min_value=0.0, value=float(config.break_even.buffer_r), step=0.1, key="bt_be_buf")

            config.trailing.enabled = st.checkbox("Use Trailing", value=bool(config.trailing.enabled), key="bt_trail_en")
            config.trailing.atr_len = st.number_input("Trailing ATR Length", min_value=1, value=int(config.trailing.atr_len), key="bt_trail_atr_len")
            config.trailing.start_r = st.number_input("Trailing Start (R)", min_value=0.1, value=float(config.trailing.start_r), step=0.1, key="bt_trail_start")
            config.trailing.dist_r = st.number_input("Trailing Distance (R)", min_value=0.1, value=float(config.trailing.dist_r), step=0.1, key="bt_trail_dist")

        with st.expander("Filter Settings", expanded=False):
            config.filters.use_ma_filter = st.checkbox("Enable MA Filter", value=bool(config.filters.use_ma_filter), key="bt_use_ma")
            config.filters.use_ma_slope_filter = st.checkbox("Enable MA Slope Filter", value=bool(config.filters.use_ma_slope_filter), key="bt_use_ma_slope")
            config.filters.ma_type = st.selectbox("MA Type", ["SMA", "EMA", "DEMA", "TEMA", "RMA", "WMA", "VWMA", "KAMA"], index=["SMA", "EMA", "DEMA", "TEMA", "RMA", "WMA", "VWMA", "KAMA"].index(config.filters.ma_type), key="bt_ma_type")
            config.filters.ma_length = st.number_input("MA Length", min_value=1, value=int(config.filters.ma_length), key="bt_ma_len")
            config.filters.ma_slope_len = st.number_input("MA Slope Length", min_value=1, value=int(config.filters.ma_slope_len), key="bt_ma_slope_len")
            config.filters.ma_slope_min_pct = st.number_input("MA Slope Min %", min_value=0.0, value=float(config.filters.ma_slope_min_pct), step=0.001, format="%.6f", key="bt_ma_slope_pct")

            config.filters.use_volume_filter = st.checkbox("Enable Volume Filter", value=bool(config.filters.use_volume_filter), key="bt_use_vol")
            config.filters.vol_filter_len = st.number_input("VOL SMA Length", min_value=1, value=int(config.filters.vol_filter_len), key="bt_vol_len")
            config.filters.vol_filter_mult = st.number_input("VOL Min SMA Mult", min_value=0.1, value=float(config.filters.vol_filter_mult), step=0.05, key="bt_vol_mult")

            config.filters.use_atr_vol_filter = st.checkbox("Enable ATR Vol Filter", value=bool(config.filters.use_atr_vol_filter), key="bt_use_atr_vol")
            config.filters.atr_vol_len = st.number_input("ATR Vol Length", min_value=1, value=int(config.filters.atr_vol_len), key="bt_atr_vol_len")
            config.filters.atr_vol_smooth_len = st.number_input("ATR Baseline Length", min_value=2, value=int(config.filters.atr_vol_smooth_len), key="bt_atr_vol_smooth")
            config.filters.atr_vol_floor_mult = st.number_input("ATR Floor Mult", min_value=0.1, value=float(config.filters.atr_vol_floor_mult), step=0.05, key="bt_atr_vol_mult")

            config.filters.use_htf_trend_filter = st.checkbox("Enable HTF Trend Filter", value=bool(config.filters.use_htf_trend_filter), key="bt_use_htf")
            config.filters.htf_trend_timeframe = st.text_input("HTF Trend Timeframe", value=config.filters.htf_trend_timeframe, key="bt_htf_tf")
            config.filters.htf_trend_ma_type = st.selectbox("HTF MA Type", ["SMA", "EMA", "RMA", "WMA", "KAMA"], index=["SMA", "EMA", "RMA", "WMA", "KAMA"].index(config.filters.htf_trend_ma_type), key="bt_htf_ma_type")
            config.filters.htf_trend_ma_len = st.number_input("HTF MA Length", min_value=1, value=int(config.filters.htf_trend_ma_len), key="bt_htf_len")
            config.filters.htf_trend_buffer_pct = st.number_input("HTF Buffer %", min_value=0.0, value=float(config.filters.htf_trend_buffer_pct), step=0.05, key="bt_htf_buf")

        with st.expander("Guard Settings", expanded=False):
            config.guards.use_dd_guard = st.checkbox("Enable Drawdown Guard", value=bool(config.guards.use_dd_guard), key="bt_g_dd_en")
            config.guards.dd_guard_pct = st.number_input("Drawdown %", min_value=0.1, value=float(config.guards.dd_guard_pct), step=0.5, key="bt_g_dd_pct")
            config.guards.use_consec_loss_guard = st.checkbox("Enable Consecutive Loss Guard", value=bool(config.guards.use_consec_loss_guard), key="bt_g_cl_en")
            config.guards.consec_loss_max = st.number_input("Max Consecutive Losses", min_value=1, value=int(config.guards.consec_loss_max), key="bt_g_cl_max")
            config.guards.use_cooldown_guard = st.checkbox("Enable Cooldown Guard", value=bool(config.guards.use_cooldown_guard), key="bt_g_cd_en")
            config.guards.cooldown_bars = st.number_input("Cooldown Bars", min_value=1, value=int(config.guards.cooldown_bars), key="bt_g_cd_bars")
            config.guards.use_eq_curve_guard = st.checkbox("Enable Equity Curve Guard", value=bool(config.guards.use_eq_curve_guard), key="bt_g_eq_en")
            config.guards.eq_curve_ma_len = st.number_input("Equity Curve MA Len", min_value=5, value=int(config.guards.eq_curve_ma_len), key="bt_g_eq_len")
            config.guards.use_mae_guard = st.checkbox("Enable MAE Guard", value=bool(config.guards.use_mae_guard), key="bt_g_mae_en")
            config.guards.mae_max_pct = st.number_input("MAE Max %", min_value=0.1, value=float(config.guards.mae_max_pct), step=0.1, key="bt_g_mae_pct")

        with st.expander("Strategy Settings", expanded=False):
            col_strat_l, col_strat_r = st.columns(2)
            with col_strat_l:
                config.strategy.initial_capital = st.number_input("Initial Capital", min_value=100.0, value=float(config.strategy.initial_capital), step=100.0, key="bt_init_cap")
                config.strategy.commission_percent = st.number_input("Commission %", min_value=0.0, value=float(config.strategy.commission_percent), step=0.01, key="bt_comm")
                config.strategy.slippage_ticks = st.number_input("Slippage (ticks)", min_value=0, value=int(config.strategy.slippage_ticks), key="bt_slip")
            with col_strat_r:
                config.strategy.mintick = st.number_input("Min Tick", min_value=0.00000001, value=float(config.strategy.mintick), step=0.01, format="%.8f", key="bt_mintick")
                config.strategy.pyramiding = st.number_input("Pyramiding", min_value=1, value=int(config.strategy.pyramiding), key="bt_pyramiding")

        with st.expander("Parity / Debug", expanded=True):
            config.parity.enabled = st.checkbox("Enable Parity Mode", value=True, key="bt_parity_en", help="Use deterministic Pine-style fill contract.")
            config.parity.fill_contract = st.selectbox("Exit Detection Mode", ["touch", "close"], index=0, key="bt_fill_mode", disabled=not config.parity.enabled, help="touch=OHLC touch checks, close=close-based checks.")
            config.parity.export_debug_csv = st.checkbox("Enable Parity Debug Export", value=False, key="bt_debug_export", help="Writes debug_python_trades.csv and debug_python_signals.csv under ./debug.")
            config.parity.debug_dir = st.text_input("Debug Directory", value="debug", key="bt_debug_dir")

    st.info(
        "Python engine feature status is synced with current implementation. "
        "Use config toggles directly from the sections above."
    )

    # Load Dataset Reactively (Outside Run Button)
    # Using session_state effectively caches the load for THIS run if streamlit rerun happens
    # but we should use st.cache_data for performance across reruns
    @st.cache_data
    def load_and_prep_data(filename):
        try:
            from src.data.io import load_dataset
            import pandas as pd
            df = load_dataset(f"./data/{filename}")
            if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                # Heuristic: 2000-01-01 is ~946684800000 ms. 
                if df['timestamp'].iloc[0] > 946684800000:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
                else:
                    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
            
            if df['timestamp'].dt.tz is None:
                df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
            else:
                df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')
            return df
        except Exception:
            return None

    df = load_and_prep_data(selected_dataset)
    
    if df is not None:
        # --- Test Range Filtering (Reactive) ---
        import pandas as pd
        from datetime import datetime, time, timezone, timedelta

        # Prepare filter bounds
        start_dt = datetime.combine(bt_start_date, time.min).replace(tzinfo=timezone.utc)
        end_dt = datetime.combine(bt_end_date, time.max).replace(tzinfo=timezone.utc)
        
        # Apply preroll
        filter_start_dt = start_dt
        if bt_preroll_days > 0:
            filter_start_dt = start_dt - timedelta(days=bt_preroll_days)
        
        # Filter
        mask = (df['timestamp'] >= filter_start_dt) & (df['timestamp'] <= end_dt)
        df_filtered = df.loc[mask].copy()

        # Stats Calculation
        total_bars = len(df)
        filtered_bars = len(df_filtered)
        
        mask_test_only = (df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)
        test_window_bars = len(df.loc[mask_test_only])

        # UI Display (Outside Button)
        st.info(
            f"**DataSet Stats**\n\n"
            f"- Total Bars: `{total_bars}`\n"
            f"- Filtered (w/ Preroll): `{filtered_bars}` (from {filter_start_dt.date()} to {end_dt.date()})\n"
            f"- Test Window: `{test_window_bars}` (from {start_dt.date()} to {end_dt.date()})\n"
            f"- Preroll Days: `{bt_preroll_days}`"
        )
        
        if len(df_filtered) == 0:
            st.error("No bars in selected range!")
            # Disable run button effectively by context
    else:
        st.error("Failed to load dataset.")
        df_filtered = None

    st.caption("Step 2: Run")
    if st.button("Run Backtest", type="primary", use_container_width=True):
        if df_filtered is None or len(df_filtered) == 0:
            st.error("Cannot run backtest: Invalid data or empty range.")
        else:
            with st.spinner("Running backtest..."):
                try:
                    from src.engine.mtc_runner import MTCRunner
                    
                    logging.info(f"Backtest Run: Filtered={len(df_filtered)}")
                    
                    runner = MTCRunner(config)
                    # Pass eval_start/eval_end so that:
                    # 1. trade_start gate blocks entries before start_dt (preroll is indicator-only)
                    # 2. Metrics are computed only for the test window
                    results = runner.run(
                        df_filtered,
                        warmup_bars=bt_warmup_bars,
                        eval_start=start_dt if bt_preroll_days > 0 else None,
                        eval_end=end_dt,
                    )

                    st.success(f"Backtest complete: {results['metrics']['total_trades']} trades")
                    st.caption("Step 3: Results")

                    st.subheader("Performance Metrics")

                    metrics = results['metrics']
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Net Profit", f"${metrics['net_profit']:.2f}")
                        st.metric("Win Rate", f"{metrics['win_rate']:.1f}%")

                    with col2:
                        st.metric("Max Drawdown", f"{metrics['max_drawdown']:.1f}%")
                        st.metric("Profit/DD", f"{metrics.get('profit_dd_ratio', 0.0):.2f}")

                    with col3:
                        st.metric("Total Trades", metrics['total_trades'])
                        st.metric("Total Entries", metrics.get('total_entries', 0))
                        st.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")

                    with col4:
                        st.metric("Avg Trade", f"${metrics['avg_trade']:.2f}")
                        st.metric("Largest Win", f"${metrics['largest_win']:.2f}")

                    st.subheader("Equity Curve")
                    import plotly.graph_objects as go

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(y=results['equity_curve'], mode='lines', name='Equity', line=dict(color='#00ff88', width=2)))
                    fig.update_layout(template='plotly_dark', height=400, margin=dict(l=0, r=0, t=30, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                    st.subheader("Trades")
                    trades_data = []
                    for t in results['trades'][:50]:
                        trades_data.append({
                            "ID": t.trade_id,
                            "Direction": t.direction.value,
                            "Entry": f"${t.entry_price:.2f}",
                            "Exit": f"${t.exit_price:.2f}",
                            "PnL": f"${t.pnl:.2f}",
                            "PnL%": f"{t.pnl_pct:.2f}%",
                            "Exit Reason": t.exit_reason.value,
                            "Bars": t.bars_held,
                        })
                    st.dataframe(trades_data, use_container_width=True)

                    if results.get('debug_exports'):
                        st.subheader("Parity Debug Exports")
                        st.code("\n".join([
                            f"Trades: {results['debug_exports'].get('debug_python_trades')}",
                            f"Signals: {results['debug_exports'].get('debug_python_signals')}",
                        ]))
                    
                except Exception as e:
                    st.error(f"Backtest failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())
def show_optimize_page():
    """Optimization page."""
    st.title("Parameter Optimization")
    st.caption("Step 1: Setup")
    
    # Dataset selection
    from src.data.io import list_datasets
    datasets = list_datasets("./data")
    
    if not datasets:
        st.warning("No datasets available. Please download data first.")
        return
    
    dataset_options = [ds['filename'] for ds in datasets]

    # --- Initialize Shadow State (Persistence) ---
    # Moved to top to ensure all widgets can bind to save_opt_state and defaults are ready
    if "_opt_state" not in st.session_state:
        # We need ds_start/ds_end for defaults only if we want dynamic defaults.
        # But if we rely on "last saved", we use that.
        # Initial defaults can use a safe fallback or we can calculate them later?
        # Let's peek at the first dataset to get initial range if needed, or just use today.
        
        # Helper to get dataset range (defined early for init usage)
        @st.cache_data
        def get_initial_range(filename):
            try:
                from src.data.io import load_dataset
                import pandas as pd
                df = load_dataset(f"./data/{filename}")
                if 'timestamp' in df.columns:
                    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                    return df['timestamp'].min().date(), df['timestamp'].max().date()
            except Exception:
                pass
            from datetime import datetime, timedelta
            return datetime.now().date() - timedelta(days=30), datetime.now().date()
            
        initial_ds = dataset_options[0] if dataset_options else "data.csv"
        ds_start_init, ds_end_init = get_initial_range(initial_ds)

        st.session_state["_opt_state"] = {
            "opt_start_date": ds_start_init, 
            "opt_warmup": 200, 
            "opt_end_date": ds_end_init, 
            "opt_preroll": 0,
            "opt_st_atr_en": False, "st_atr_min": 7, "st_atr_max": 50,
            "opt_st_fac_en": False, "st_fac_min": 1.0, "st_fac_max": 8.0,
            "opt_sl_mult_en": False, "sl_min": 1.0, "sl_max": 8.0,
            "opt_tp_rr_en": False, "tp_min": 1.0, "tp_max": 6.0,
            "opt_init_cap": 10000.0, "opt_comm": 0.04,
            "opt_slip": 5, "opt_pyramiding": 1,
            "opt_lev": 5.0, "opt_risk_long": 4.0, "opt_risk_short": 3.0,
            "opt_parity_enabled": True, "opt_fill_contract": "touch",
            "opt_export_debug": False, "opt_debug_dir": "debug",
            "opt_objective": "profit_dd_ratio", "opt_trials": 100, "opt_min_trades": 30,
            "opt_dataset": initial_ds
        }

    # Callback to save state
    def save_opt_state():
        # Ensure _opt_state exists
        if "_opt_state" not in st.session_state: return
        
        for k in st.session_state["_opt_state"].keys():
            if k in st.session_state:
                st.session_state["_opt_state"][k] = st.session_state[k]

    # Restore State from Shadow
    for k, v in st.session_state["_opt_state"].items():
        if k not in st.session_state:
             st.session_state[k] = v

    # Now create widgets
    
    # Persist dataset selection (handled by key="opt_dataset")
    selected_dataset = st.selectbox("Select Dataset", dataset_options, key="opt_dataset", on_change=save_opt_state)
    
    # Helper to get dataset range (Runtime)
    @st.cache_data
    def get_dataset_range(filename):
        try:
            from src.data.io import load_dataset
            import pandas as pd
            df = load_dataset(f"./data/{filename}")
            if 'timestamp' in df.columns:
                if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                return df['timestamp'].min().date(), df['timestamp'].max().date()
        except Exception:
            pass
        from datetime import datetime, timedelta
        return datetime.now().date() - timedelta(days=30), datetime.now().date()

    ds_start, ds_end = get_dataset_range(selected_dataset)

    with st.expander("Test Range (Optimizer)"):
        col_tr1, col_tr2 = st.columns(2)
        with col_tr1:
            # Handle potential date bounds changes if dataset changed
            # Refetch from shadow state or current session state
            current_start = st.session_state.get("opt_start_date", ds_start)
            if current_start < ds_start: current_start = ds_start
            if current_start > ds_end: current_start = ds_end
            st.session_state["opt_start_date"] = current_start
            
            start_date = st.date_input("Start Date", min_value=ds_start, max_value=ds_end, key="opt_start_date", on_change=save_opt_state)
            warmup_bars = st.number_input("Warmup Bars", min_value=0, key="opt_warmup", on_change=save_opt_state)
        with col_tr2:
            current_end = st.session_state.get("opt_end_date", ds_end)
            if current_end < ds_start: current_end = ds_start
            if current_end > ds_end: current_end = ds_end
            st.session_state["opt_end_date"] = current_end
            
            end_date = st.date_input("End Date", min_value=ds_start, max_value=ds_end, key="opt_end_date", on_change=save_opt_state)
            preroll_days = st.number_input("Preroll Days", min_value=0, help="Expand start date backwards to prime indicators", key="opt_preroll", on_change=save_opt_state)

    # Parameter selection
    st.subheader("Select Parameters")
    st.caption("Choose parameters and define min/max ranges.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        opt_st_atr = st.checkbox("Supertrend ATR Length", key="opt_st_atr_en", on_change=save_opt_state)
        if opt_st_atr:
            range_col_1, range_col_2 = st.columns(2)
            with range_col_1:
                st_atr_min = st.number_input("ATR Min", key="st_atr_min", on_change=save_opt_state)
            with range_col_2:
                st_atr_max = st.number_input("ATR Max", key="st_atr_max", on_change=save_opt_state)
        
        opt_st_factor = st.checkbox("Supertrend Factor", key="opt_st_fac_en", on_change=save_opt_state)
        if opt_st_factor:
            range_col_1, range_col_2 = st.columns(2)
            with range_col_1:
                st_fac_min = st.number_input("Factor Min", key="st_fac_min", on_change=save_opt_state)
            with range_col_2:
                st_fac_max = st.number_input("Factor Max", key="st_fac_max", on_change=save_opt_state)
    
    with col2:
        opt_sl_mult = st.checkbox("SL ATR Multiplier", key="opt_sl_mult_en", on_change=save_opt_state)
        if opt_sl_mult:
            range_col_1, range_col_2 = st.columns(2)
            with range_col_1:
                sl_mult_min = st.number_input("SL Min", key="sl_min", on_change=save_opt_state)
            with range_col_2:
                sl_mult_max = st.number_input("SL Max", key="sl_max", on_change=save_opt_state)

        
        opt_tp_rr = st.checkbox("TP1 R-Multiple", key="opt_tp_rr_en", on_change=save_opt_state)
        if opt_tp_rr:
            range_col_1, range_col_2 = st.columns(2)
            with range_col_1:
                tp_rr_min = st.number_input("TP Min", key="tp_min", on_change=save_opt_state)
            with range_col_2:
                tp_rr_max = st.number_input("TP Max", key="tp_max", on_change=save_opt_state)

    # Strategy Settings (Added for Parity)
    with st.expander("Strategy & Risk Settings", expanded=False):
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            opt_init_cap = st.number_input("Initial Capital", step=100.0, key="opt_init_cap", on_change=save_opt_state)
            opt_commission = st.number_input("Commission %", step=0.01, key="opt_comm", on_change=save_opt_state)
        with col_s2:
            opt_slippage = st.number_input("Slippage (ticks)", key="opt_slip", on_change=save_opt_state)
            opt_pyramiding = st.number_input("Pyramiding", key="opt_pyramiding", on_change=save_opt_state)
        with col_s3:
            opt_max_leverage = st.number_input("Max Leverage", step=0.5, key="opt_lev", on_change=save_opt_state)
            opt_risk_long = st.number_input("Risk Long %", step=0.1, key="opt_risk_long", on_change=save_opt_state)
            opt_risk_short = st.number_input("Risk Short %", step=0.1, key="opt_risk_short", on_change=save_opt_state)
    
    # Parity Defaults
    parity_enabled = True
    fill_contract = "touch"
    with st.expander("Parity / Debug (Optimizer)"):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            parity_enabled = st.checkbox("Enable Parity Mode", key="opt_parity_enabled", on_change=save_opt_state)
            fill_contract = st.selectbox(
                "Fill Contract", 
                ["touch", "close"], 
                disabled=not parity_enabled,
                key="opt_fill_contract", on_change=save_opt_state
            )
        with col_p2:
            export_debug_csv = st.checkbox("Export Debug CSV", key="opt_export_debug", on_change=save_opt_state)
            debug_dir = st.text_input("Debug Directory", key="opt_debug_dir", on_change=save_opt_state)

    # Optimization settings
    st.subheader("Optimization Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        objective = st.selectbox("Objective", ["profit_dd_ratio", "net_profit_pct", "sharpe", "profit_factor"], key="opt_objective", on_change=save_opt_state)
    
    with col2:
        n_trials = st.slider("Number of Trials", 10, 500, key="opt_trials", on_change=save_opt_state)
    
    with col3:
        min_trades = st.number_input("Min Trades", min_value=1, key="opt_min_trades", on_change=save_opt_state)
    
    # Run button
    st.caption("Step 2: Run")
    if st.button("Run Optimization", type="primary", use_container_width=True):
        # Build param space
        from src.config.schema import ParamRange
        param_space = {}
        
        if opt_st_atr:
            param_space['supertrend.atr_len'] = ParamRange(
                param_type='int', low=st_atr_min, high=st_atr_max
            )
        if opt_st_factor:
            param_space['supertrend.factor'] = ParamRange(
                param_type='float', low=st_fac_min, high=st_fac_max, step=0.5
            )
        if opt_sl_mult:
            param_space['stop_loss.atr_mult'] = ParamRange(
                param_type='float', low=sl_mult_min, high=sl_mult_max, step=0.5
            )
        if opt_tp_rr:
            param_space['multi_tp.tp1_rr'] = ParamRange(
                param_type='float', low=tp_rr_min, high=tp_rr_max, step=0.5
            )
        
        if not param_space:
            st.error("Please select at least one parameter to optimize.")
            return
        
        with st.spinner(f"Running {n_trials} optimization trials..."):
            try:
                from src.data.io import load_dataset
                from src.config.defaults import MTCConfig
                from src.optimize.runner import OptimizationRunner
                
                df = load_dataset(f"./data/{selected_dataset}")

                # Filter logic
                import pandas as pd
                from datetime import datetime, time, timezone, timedelta

                # Ensure timestamp is datetime UTC
                if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                if df['timestamp'].dt.tz is None:
                    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
                else:
                    df['timestamp'] = df['timestamp'].dt.tz_convert('UTC')

                # Prepare filter bounds
                start_dt = datetime.combine(start_date, time.min).replace(tzinfo=timezone.utc)
                end_dt = datetime.combine(end_date, time.max).replace(tzinfo=timezone.utc)
                
                # Apply preroll
                filter_start_dt = start_dt
                if preroll_days > 0:
                    filter_start_dt = start_dt - timedelta(days=preroll_days)
                
                # Filter
                mask = (df['timestamp'] >= filter_start_dt) & (df['timestamp'] <= end_dt)
                df = df.loc[mask].copy()
                
                # Validation
                if len(df) < (warmup_bars + 50):
                    st.error(f"Dataset too small after filtering: {len(df)} bars. Need at least {warmup_bars + 50}.")
                    return

                # Info
                st.info(f"Optimizer range: {start_date}..{end_date} | bars={len(df)} | warmup={warmup_bars} | preroll_days={preroll_days}")
                if preroll_days > 0:
                    st.info(f"Preroll active: {preroll_days} days added before start for indicator warmup. Metrics scored on eval window only.")

                config = MTCConfig()

                # Inject Strategy Settings
                config.strategy.initial_capital = opt_init_cap
                config.strategy.commission_percent = opt_commission
                config.strategy.slippage_ticks = opt_slippage
                config.strategy.pyramiding = opt_pyramiding
                config.risk.max_leverage_cap = opt_max_leverage
                config.risk.risk_long_percent = opt_risk_long
                config.risk.risk_short_percent = opt_risk_short
                
                # Inject Parity settings for Optimizer
                config.parity.enabled = parity_enabled
                config.parity.fill_contract = fill_contract
                config.parity.export_debug_csv = export_debug_csv
                config.parity.debug_dir = debug_dir

                st.info(f"Parity={parity_enabled}, Export={export_debug_csv}, DebugDir={debug_dir}, FillContract={fill_contract}")

                runner = OptimizationRunner(
                    df=df,
                    base_config=config,
                    param_space=param_space,
                    objective=objective,
                    min_trades=min_trades,
                    warmup_bars=warmup_bars,
                    eval_start=start_dt,
                    eval_end=end_dt,
                )
                
                results = runner.run(n_trials=n_trials)
                
                st.success(f"Optimization complete. Best {objective}: {results['best_value']:.4f}")
                st.caption("Step 3: Results")
                
                # Best parameters
                st.subheader("Best Parameters")
                st.json(results['best_params'])
                
                # Pine preset
                st.subheader("Pine Script Preset")
                preset = runner.generate_pine_preset()
                st.code(preset, language="pine")
                
                # Top trials
                st.subheader("Top 10 Trials")
                top_trials = runner.get_top_n(10)
                st.dataframe(top_trials)
                
            except Exception as e:
                st.error(f"Optimization failed: {e}")
                import traceback
                st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
