"""
Session State Management for MTC Dashboard.

Provides centralized session state management across all pages.
"""

import streamlit as st
from typing import Any, Optional, Dict
from pathlib import Path


# ============================================================================
# Session State Keys
# ============================================================================

# Backtest state keys
KEY_BT_DATASET = "bt_dataset"
KEY_BT_CONFIG = "bt_config"
KEY_BT_RESULTS = "bt_results"
KEY_BT_START_DATE = "bt_start_date"
KEY_BT_END_DATE = "bt_end_date"
KEY_BT_WARMUP_BARS = "bt_warmup_bars"
KEY_BT_PREROLL_DAYS = "bt_preroll_days"

# Optimization state keys
KEY_OPT_STATE = "_opt_state"
KEY_OPT_DATASET = "opt_dataset"
KEY_OPT_RESULTS = "opt_results"

# Navigation
KEY_CURRENT_PAGE = "current_page"

# Data
KEY_DATASETS = "datasets"
KEY_SELECTED_DATASET = "selected_dataset"


# ============================================================================
# Initialization Functions
# ============================================================================

def init_session():
    """
    Initialize session state with default values.
    Call this at the beginning of every page.
    """
    # Initialize backtest state if not exists
    if KEY_BT_DATASET not in st.session_state:
        st.session_state[KEY_BT_DATASET] = None
    
    if KEY_BT_RESULTS not in st.session_state:
        st.session_state[KEY_BT_RESULTS] = None
    
    # Initialize optimization state if not exists
    if KEY_OPT_STATE not in st.session_state:
        st.session_state[KEY_OPT_STATE] = {}
    
    # Initialize navigation if not exists
    if KEY_CURRENT_PAGE not in st.session_state:
        st.session_state[KEY_CURRENT_PAGE] = "Home"
    
    # Initialize datasets cache
    if KEY_DATASETS not in st.session_state:
        st.session_state[KEY_DATASETS] = []


def reset_backtest_state():
    """Reset backtest session state."""
    st.session_state[KEY_BT_RESULTS] = None
    # Keep dataset selection


def reset_optimization_state():
    """Reset optimization session state."""
    st.session_state[KEY_OPT_RESULTS] = None


def clear_cache():
    """Clear all cached data."""
    st.session_state[KEY_DATASETS] = []


# ============================================================================
# Getter Functions
# ============================================================================

def get_backtest_dataset() -> Optional[str]:
    """Get selected backtest dataset."""
    return st.session_state.get(KEY_BT_DATASET)


def get_backtest_results() -> Optional[Dict[str, Any]]:
    """Get backtest results."""
    return st.session_state.get(KEY_BT_RESULTS)


def get_current_page() -> str:
    """Get current page."""
    return st.session_state.get(KEY_CURRENT_PAGE, "Home")


def get_datasets() -> list:
    """Get cached datasets list."""
    return st.session_state.get(KEY_DATASETS, [])


# ============================================================================
# Setter Functions
# ============================================================================

def set_backtest_dataset(dataset: str):
    """Set backtest dataset."""
    st.session_state[KEY_BT_DATASET] = dataset


def set_backtest_results(results: Dict[str, Any]):
    """Set backtest results."""
    st.session_state[KEY_BT_RESULTS] = results


def set_current_page(page: str):
    """Set current page."""
    st.session_state[KEY_CURRENT_PAGE] = page


def set_datasets(datasets: list):
    """Set datasets list."""
    st.session_state[KEY_DATASETS] = datasets


# ============================================================================
# Config Persistence
# ============================================================================

def save_config_to_session(key: str, value: Any):
    """
    Save configuration to session state.
    
    Args:
        key: Configuration key
        value: Configuration value
    """
    st.session_state[key] = value


def load_config_from_session(key: str, default: Any = None) -> Any:
    """
    Load configuration from session state.
    
    Args:
        key: Configuration key
        default: Default value if not found
    
    Returns:
        Configuration value or default
    """
    return st.session_state.get(key, default)


# ============================================================================
# Utility Functions
# ============================================================================

def get_data_dir() -> Path:
    """Get data directory path."""
    return Path("data")


def get_exports_dir() -> Path:
    """Get exports directory path."""
    return Path("exports/runs")


def get_logs_dir() -> Path:
    """Get logs directory path."""
    return Path("logs")


def ensure_directories():
    """Ensure all required directories exist."""
    for dir_path in [get_data_dir(), get_exports_dir(), get_logs_dir()]:
        dir_path.mkdir(exist_ok=True, parents=True)


def get_dataset_count() -> int:
    """Get count of available datasets."""
    data_path = get_data_dir()
    return (
        len(list(data_path.glob("*.parquet"))) +
        len(list(data_path.glob("*.csv")))
    )


def get_export_count() -> int:
    """Get count of export runs."""
    exports_path = get_exports_dir()
    return len(list(exports_path.glob("*"))) if exports_path.exists() else 0
