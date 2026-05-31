"""
Reusable UI Components for MTC Dashboard.

Provides consistent, professional UI components with
proper typography, spacing, and styling.
"""

import streamlit as st
from typing import Optional, Dict, Any, List, Tuple
import pandas as pd


# ============================================================================
# KPI & Metric Components
# ============================================================================

def metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    help_text: Optional[str] = None,
    color: Optional[str] = None
) -> None:
    """
    Display a professional metric card.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta/change (e.g., "+5%", "-10%")
        help_text: Optional help tooltip
        color: Optional color ('green', 'red', 'yellow', 'blue')
    """
    col = st.container()
    with col:
        if delta:
            # Parse delta for coloring
            delta_str = delta
            if delta.startswith('+'):
                delta_color = "normal" if color == "green" else "inverse"
            elif delta.startswith('-'):
                delta_color = "inverse" if color == "red" else "normal"
            else:
                delta_color = "normal"
            st.metric(label=label, value=value, delta=delta_str, help=help_text)
        else:
            st.metric(label=label, value=value, help=help_text)


def metric_row(*metrics: Tuple[str, str, Optional[str]]) -> None:
    """
    Display a row of metrics.
    
    Args:
        *metrics: Tuples of (label, value, optional_delta)
    """
    cols = st.columns(len(metrics))
    for i, (label, value, delta) in enumerate(metrics):
        with cols[i]:
            if delta:
                st.metric(label=label, value=value, delta=delta)
            else:
                st.metric(label=label, value=value)


def kpi_section(title: str, *metrics: Tuple[str, str, Optional[str]]) -> None:
    """
    Display a section of KPIs with a title.
    
    Args:
        title: Section title
        *metrics: Tuples of (label, value, optional_delta)
    """
    st.subheader(title)
    metric_row(*metrics)


# ============================================================================
# Section & Layout Components
# ============================================================================

def section_header(
    title: str,
    icon: Optional[str] = None,
    help_text: Optional[str] = None
) -> None:
    """
    Display a styled section header.
    
    Args:
        title: Section title
        icon: Optional emoji icon
        help_text: Optional help tooltip
    """
    if icon:
        st.markdown(f"### {icon} {title}")
    else:
        st.markdown(f"### {title}")
    
    if help_text:
        st.caption(help_text)


def divider() -> None:
    """Display a styled divider."""
    st.divider()


def card_container() -> None:
    """Begin a card container with styled border."""
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)


def card_container_end() -> None:
    """End a card container."""
    st.markdown('</div>', unsafe_allow_html=True)


def info_box(message: str, icon: str = "Info") -> None:
    """
    Display an info message box.
    
    Args:
        message: Message to display
        icon: Optional icon
    """
    st.info(f"{icon} {message}")


def success_box(message: str, icon: str = "OK") -> None:
    """
    Display a success message box.
    
    Args:
        message: Message to display
        icon: Optional icon
    """
    st.success(f"{icon} {message}")


def warning_box(message: str, icon: str = "Warning") -> None:
    """
    Display a warning message box.
    
    Args:
        message: Message to display
        icon: Optional icon
    """
    st.warning(f"{icon} {message}")


def error_box(message: str, icon: str = "Error") -> None:
    """
    Display an error message box.
    
    Args:
        message: Message to display
        icon: Optional icon
    """
    st.error(f"{icon} {message}")


# ============================================================================
# Data Display Components
# ============================================================================

def dataframe_display(
    df: pd.DataFrame,
    max_rows: int = 50,
    use_container_width: bool = True,
    hide_index: bool = True
) -> None:
    """
    Display a styled dataframe.
    
    Args:
        df: DataFrame to display
        max_rows: Maximum rows to show
        use_container_width: Use full container width
        hide_index: Hide DataFrame index
    """
    st.dataframe(
        df.head(max_rows),
        use_container_width=use_container_width,
        hide_index=hide_index
    )


def table_display(
    data: List[Dict[str, Any]],
    max_rows: int = 50
) -> None:
    """
    Display a list of dictionaries as a table.
    
    Args:
        data: List of dictionaries
        max_rows: Maximum rows to show
    """
    if data:
        df = pd.DataFrame(data)
        dataframe_display(df, max_rows=max_rows)
    else:
        st.info("No data to display")


# ============================================================================
# Loading & Progress Components
# ============================================================================

def loading_spinner(message: str = "Loading..."):
    """
    Create a loading spinner context manager.
    
    Args:
        message: Loading message
    
    Returns:
        Context manager for spinner
    """
    return st.spinner(message)


def progress_bar(progress: float, text: Optional[str] = None) -> None:
    """
    Display a styled progress bar.
    
    Args:
        progress: Progress value (0-1)
        text: Optional progress text
    """
    if text:
        st.progress(progress, text=text)
    else:
        st.progress(progress)


# ============================================================================
# Configuration Components
# ============================================================================

def config_section(
    title: str,
    expanded: bool = True,
    icon: Optional[str] = None
) -> None:
    """
    Begin a configuration section with expander.
    
    Args:
        title: Section title
        expanded: Whether expander is expanded by default
        icon: Optional icon
    
    Returns:
        Expander object
    """
    if icon:
        return st.expander(f"{icon} {title}", expanded=expanded)
    return st.expander(title, expanded=expanded)


def form_field(label: str, widget, help_text: Optional[str] = None):
    """
    Create a form field with consistent styling.
    
    Args:
        label: Field label
        widget: Streamlit widget
        help_text: Optional help text
    
    Returns:
        Widget with label and help
    """
    if help_text:
        return st.container()
    return widget


# ============================================================================
# Sidebar Components
# ============================================================================

def sidebar_section(title: str) -> None:
    """
    Display a styled sidebar section header.
    
    Args:
        title: Section title
    """
    st.sidebar.markdown(f"**{title}**")
    st.sidebar.divider()


def sidebar_nav(
    options: List[str],
    default: Optional[str] = None,
    key: str = "nav"
) -> str:
    """
    Display styled sidebar navigation.
    
    Args:
        options: Navigation options
        default: Default selection
        key: Session state key
    
    Returns:
        Selected option
    """
    return st.sidebar.radio(
        "Navigation",
        options,
        index=options.index(default) if default in options else 0,
        label_visibility="collapsed",
        key=key
    )


def sidebar_metric(label: str, value: Any, delta: Optional[str] = None) -> None:
    """
    Display a metric in the sidebar.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta
    """
    st.sidebar.metric(label=label, value=value, delta=delta)


# ============================================================================
# Chart Components
# ============================================================================

def chart_container(height: int = 400) -> None:
    """
    Begin a chart container with consistent styling.
    
    Args:
        height: Chart height in pixels
    """
    st.markdown('<div style="margin: 16px 0;">', unsafe_allow_html=True)


def chart_container_end() -> None:
    """End a chart container."""
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# Code & Export Components
# ============================================================================

def code_block(
    code: str,
    language: str = "python",
    expanded: bool = False
) -> None:
    """
    Display a styled code block.
    
    Args:
        code: Code to display
        language: Programming language
        expanded: Whether to show expanded by default
    """
    with st.expander(f"{language.upper()} Code", expanded=expanded):
        st.code(code, language=language)


def copy_button(key: str, value: str) -> None:
    """
    Display a copy-to-clipboard button.
    
    Args:
        key: Unique key for the button
        value: Value to copy
    """
    st.code(value, key=key)


# ============================================================================
# Status Components
# ============================================================================

def status_indicator(
    is_ok: bool,
    ok_message: str = "Ready",
    error_message: str = "Error"
) -> None:
    """
    Display a status indicator.
    
    Args:
        is_ok: Whether status is OK
        ok_message: Message for OK status
        error_message: Message for error status
    """
    if is_ok:
        st.success(ok_message)
    else:
        st.error(error_message)


def status_list(items: List[Tuple[str, bool]]) -> None:
    """
    Display a list of status items.
    
    Args:
        items: List of (label, is_ok) tuples
    """
    for label, is_ok in items:
        status_indicator(is_ok, ok_message=label, error_message=label)


# ============================================================================
# Tab Components
# ============================================================================

def tab_container(*tabs: str) -> Tuple:
    """
    Create a tab container.
    
    Args:
        *tabs: Tab names
    
    Returns:
        Tuple of tab objects
    """
    return st.tabs(tabs)


def metrics_tabs() -> Tuple:
    """
    Create standard metrics display tabs.
    
    Returns:
        Tuple of (config_tab, results_tab)
    """
    return st.tabs(["Configuration", "Results"])

