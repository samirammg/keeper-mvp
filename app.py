import streamlit as st

menu = st.selectbox("🔍 Jump to a module:", [
    "🧩 Stay on Keeper Pulse",
    "📘 Customer Pulse",
    "💓 Growth Pulse",
    "🩺 Team Pulse",
    "↳  📌 CSM Activity",
    "↳  💬 Support Trends",
    "↳  📊 Product Usage",
    "📈 Vision Pulse",
    "↳  🧭 Strategy",
    "🚀 Keeper Agents",
    "🗄️ Keeper Data"
])

if menu != "🧩 Stay on Keeper Pulse":
    page_map = {
        "📘 Customer Pulse": "Journey",
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
    page = page_map[menu]
    st.markdown(f'<meta http-equiv="refresh" content="0; url=/{page}">', unsafe_allow_html=True)
st.markdown('<meta http-equiv="refresh" content="0; url=/Pulse">', unsafe_allow_html=True)
