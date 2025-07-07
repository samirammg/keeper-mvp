import streamlit as st

def show_navigation(current_label):
    menu_labels = {
        "📘 Customer Pulse": "Journey",
        "🧩 Keeper Pulse": "Pulse",
        "💓 Growth Pulse": "GrowthPulse",
        "🩺 Team Pulse": "TeamPulse",
        "↳  📌 CSM Activity": "Activity",
        "↳  💬 Support Trends": "Support",
        "↳  📊 Product Usage": "Usage",
        "📈 Vision Pulse": "VisionPulse",
        "↳  🧭 Strategy": "Strategy",
        "🚀 Keeper Agents": "agent",
        "🗄️ Keeper Data": "onbording"
    }

    # Fallback if current_label not found
    if current_label not in menu_labels:
        st.warning(f"⚠️ Navigation label '{current_label}' not found.")
        return

    # Build the menu, removing the current label
    other_labels = [label for label in menu_labels if label != current_label]
    options = [f"Stay on {current_label}"] + other_labels

    selected = st.selectbox("", options, label_visibility="collapsed")

    if selected != f"Stay on {current_label}":
        target_file = menu_labels.get(selected)
        if target_file:
            try:
                st.switch_page(target_file)
            except Exception as e:
                st.error(f"❌ Failed to navigate to `{target_file}`. Make sure the file is in `/pages/` and the name matches exactly.\n\nError: {e}")
        else:
            st.error("❌ Selected navigation target is missing.")
