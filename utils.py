# utils.py

import streamlit as st
def fix_scaling():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            .main {
                margin-left: 0rem !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
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
    #fix_scaling()
