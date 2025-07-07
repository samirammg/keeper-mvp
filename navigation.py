import streamlit as st
import os

def show_navigation(_=None):  # The input is ignored
    current_page = os.path.splitext(os.path.basename(__file__))[0]

    # Page name → label mapping
    page_labels = {
        "Journey": "📘 Customer Pulse",
        "Pulse": "🧩 Keeper Pulse",
        "GrowthPulse": "💓 Growth Pulse",
        "TeamPulse": "🩺 Team Pulse",
        "Activity": "↳  📌 CSM Activity",
        "Support": "↳  💬 Support Trends",
        "Usage": "↳  📊 Product Usage",
        "VisionPulse": "📈 Vision Pulse",
        "Strategy": "↳  🧭 Strategy",
        "agent": "🚀 Keeper Agents",
        "onbording": "🗄️ Keeper Data"
    }

    current_label = page_labels.get(current_page, f"{current_page}")
    other_pages = {k: v for k, v in page_labels.items() if k != current_page}

    options = [f"Stay on {current_label}"] + list(other_pages.values())
    selected = st.selectbox("", options, label_visibility="collapsed")

    if selected != f"Stay on {current_label}":
        # Reverse map: label → filename
        target_page = next((k for k, v in other_pages.items() if v == selected), None)
        if target_page:
            st.switch_page(target_page)
