"""
Custom CSS Styles for Professional MTC Dashboard.

This module provides a design system with consistent typography,
spacing, and color palette for the Streamlit dashboard.
"""

import streamlit as st


def get_custom_css() -> str:
    """
    Get custom CSS with professional design system.
    
    Includes:
    - Typography scale
    - Color palette (GitHub-inspired dark theme)
    - Spacing system
    - Component styling
    """
    return """
    <style>
    /* ====== CSS Variables (Design Tokens) ====== */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --bg-hover: #30363d;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --text-tertiary: #6e7681;
        --accent-green: #238636;
        --accent-blue: #1f6feb;
        --accent-yellow: #d29922;
        --accent-red: #f85149;
        --accent-purple: #8957e5;
        --border-color: #30363d;
        --shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        
        /* Spacing */
        --space-xs: 4px;
        --space-sm: 8px;
        --space-md: 16px;
        --space-lg: 24px;
        --space-xl: 32px;
    }

    /* ====== Typography Scale ====== */
    h1 {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin-bottom: var(--space-md) !important;
    }
    
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: var(--space-sm) !important;
    }
    
    h3 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-bottom: var(--space-sm) !important;
    }
    
    html, body, [class*="css"] {
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif !important;
    }

    p, .stMarkdown {
        font-size: 0.98rem !important;
        line-height: 1.55 !important;
        color: var(--text-primary) !important;
    }

    label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextInput label, .stCheckbox label {
        color: var(--text-primary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    .stCaption {
        color: #aeb6c1 !important;
        font-size: 0.82rem !important;
    }
    
    .stMarkdown p {
        margin-bottom: var(--space-sm) !important;
    }

    /* ====== Links ====== */
    a {
        color: var(--accent-blue) !important;
        text-decoration: none !important;
    }
    
    a:hover {
        text-decoration: underline !important;
    }

    /* ====== Sidebar Styling ====== */
    [data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color) !important;
        min-width: 320px !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
    }

    /* ====== Button Styling ====== */
    .stButton > button {
        border-radius: 6px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid var(--border-color) !important;
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
    }
    
    .stButton > button:hover {
        background: var(--bg-hover) !important;
        border-color: var(--accent-blue) !important;
    }
    
    .stButton > button[kind="primary"] {
        background: var(--accent-blue) !important;
        border-color: var(--accent-blue) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #388bfd !important;
    }

    /* ====== Input Styling ====== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div,
    .stDateInput > div > div > input {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-primary) !important;
        border-radius: 6px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 2px rgba(31, 111, 235, 0.2) !important;
    }

    /* ====== Checkbox Styling ====== */
    .stCheckbox > label > div:first-child {
        border-color: var(--border-color) !important;
    }
    
    .stCheckbox > label > div:first-child:checked {
        background: var(--accent-blue) !important;
        border-color: var(--accent-blue) !important;
    }

    /* ====== Expander Styling ====== */
    .streamlit-expander {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        margin-bottom: var(--space-sm) !important;
    }
    
    .streamlit-expanderHeader {
        background: var(--bg-tertiary) !important;
        border-radius: 7px 7px 0 0 !important;
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--bg-hover) !important;
    }

    /* ====== Metric Cards ====== */
    [data-testid="stMetric"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: var(--space-md) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 1.15rem !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
    }

    /* ====== DataFrame Styling ====== */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        font-size: 0.9rem !important;
    }
    
    /* ====== Tabs Styling ====== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px 6px 0 0 !important;
        color: var(--text-secondary) !important;
        padding: 8px 16px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        border-bottom-color: var(--bg-tertiary) !important;
    }

    /* ====== Divider ====== */
    hr {
        border-color: var(--border-color) !important;
        margin: var(--space-md) 0 !important;
    }

    /* ====== Success/Error/Warning Messages ====== */
    .stSuccess {
        background: rgba(35, 134, 54, 0.15) !important;
        border: 1px solid var(--accent-green) !important;
        border-radius: 6px !important;
    }
    
    .stError {
        background: rgba(248, 81, 73, 0.15) !important;
        border: 1px solid var(--accent-red) !important;
        border-radius: 6px !important;
    }
    
    .stWarning {
        background: rgba(210, 153, 34, 0.15) !important;
        border: 1px solid var(--accent-yellow) !important;
        border-radius: 6px !important;
    }
    
    .stInfo {
        background: rgba(31, 111, 235, 0.15) !important;
        border: 1px solid var(--accent-blue) !important;
        border-radius: 6px !important;
    }

    .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: var(--text-primary) !important;
    }

    /* ====== Code Blocks ====== */
    .stCode {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
    }

    /* ====== Progress Bar ====== */
    .stProgress > div > div > div {
        background: var(--accent-blue) !important;
    }

    /* ====== Spinner ====== */
    .stSpinner {
        color: var(--accent-blue) !important;
    }

    /* ====== Radio Button ====== */
    [data-testid="stRadio"] > label > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
    }
    
    [data-testid="stRadio"] > label > div:hover {
        background: var(--bg-hover) !important;
    }
    
    [data-testid="stRadio"] > label > div[data-checked="true"] {
        background: var(--accent-blue) !important;
        border-color: var(--accent-blue) !important;
    }

    /* ====== Slider ====== */
    .stSlider [data-baseweb="slider"] {
        color: var(--accent-blue) !important;
    }

    /* ====== Custom Card Class ====== */
    .custom-card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: var(--space-md);
        margin-bottom: var(--space-md);
    }
    
    .custom-card-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--space-sm);
        padding-bottom: var(--space-sm);
        border-bottom: 1px solid var(--border-color);
    }
    
    /* ====== Navigation Highlight ====== */
    .nav-item {
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 4px;
        color: var(--text-secondary);
        transition: all 0.2s ease;
    }
    
    .nav-item:hover {
        background: var(--bg-tertiary);
        color: var(--text-primary);
    }
    
    .nav-item.active {
        background: var(--accent-blue);
        color: white;
    }

    /* ====== Scrollbar Styling ====== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-tertiary);
    }

    /* ====== Responsive Tweaks ====== */
    @media (max-width: 1200px) {
        [data-testid="stSidebar"] {
            min-width: 280px !important;
        }

        h1 {
            font-size: 1.5rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.15rem !important;
        }
    }
    </style>
    """


def apply_styles():
    """Apply custom styles to the Streamlit app."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)
