import streamlit as st

def apply_styles():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown("""
        <style>
        /* Compact headers */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Sidebar tweaks */
        [data-testid="stSidebar"] {
            background-color: #262730;
        }
        </style>
    """, unsafe_allow_html=True)