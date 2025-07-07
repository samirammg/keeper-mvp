import streamlit as st

def show_navigation(current_label=None):
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

    current_label = current_label or "Unknown"
    other_labels = [label for label in page_labels.values() if label != current_label]
    options = [f"Stay on {current_label}"] + other_labels

    selected = st.selectbox("", options, label_visibility="collapsed")

    if selected != f"Stay on {current_label}":
        target_file = [k for k, v in page_labels.items() if v == selected][0]
        st.experimental_set_query_params(page=target_file)
        st.markdown(f"<meta http-equiv='refresh' content='0; url=/{target_file}'/>", unsafe_allow_html=True)
        st.stop()
