# utils.py
import streamlit as st

def hide_sidebar():
    hide_sidebar_style = """
        <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        [data-testid="stSidebar"] {
            width: 0px !important;
            padding: 0 !important;
        }
        </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)
