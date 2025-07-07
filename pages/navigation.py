import streamlit as st
import os

def show_navigation():
    current_page = os.path.splitext(os.path.basename(__file__))[0]

    menu_labels = {
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

    current_label = menu_labels.get(current_page, f"{current_page}")

    menu_options = {label: name for name, label in menu_labels.items() if name != current_page}
    options = [f"📘 Stay on {current_label}"] + list(menu_options.keys())

    selected = st.selectbox("", options, label_visibility="collapsed")

    if selected != f"📘 Stay on {current_label}":
        target_file = menu_options[selected]
        st.experimental_set_query_params(page=target_file)
        st.markdown(f"<meta http-equiv='refresh' content='0; url=/{target_file}'/>", unsafe_allow_html=True)
        st.stop()
