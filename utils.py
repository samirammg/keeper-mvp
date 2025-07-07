# utils.py
import streamlit as st

def hide_sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            [data-testid="collapsedControl"] {
                display: none !important;
            }
            .main {
                margin-left: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)
