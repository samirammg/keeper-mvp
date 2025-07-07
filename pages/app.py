import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
    st.warning("🚫 Please log in first.")
    st.stop()

st.set_page_config(page_title="app", layout="wide")

st.title("🚀 Welcome to Keeper Strategic AI Suite")

st.markdown("""
Explore your customer data, trends, and strategic projections across the post-sales journey.

Use the dropdown below or the sidebar to dive into specific modules.
""")

# Quick navigator
menu = st.selectbox("🔍 Jump to a module:", [
    "🧩 Keeper Pulse",
    "📘 Customer Journey",
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

# Switch to the matching Streamlit page


if menu == "📘 Customer Journey":
    switch_page("Journey")
elif menu == "🧩 Keeper Pulse":
    switch_page("Pulse")
elif menu == "💓 Growth Pulse":
    switch_page("GrowthPulse")
elif menu == "🩺 Team Pulse":
    switch_page("TeamPulse")
elif menu == "↳  📌 CSM Activity":
    switch_page("Activity")
elif menu == "↳  💬 Support Trends":
    switch_page("Support")
elif menu == "↳  📊 Product Usage":
    switch_page("Usage")
elif menu == "📈 Vision Pulse":
    switch_page("VisionPulse")
elif menu == "↳  🧭 Strategy":
    switch_page("Strategy")
elif menu == "🚀 Keeper Agents":
    switch_page("agent")
elif menu == "🗄️ Keeper Data":
    switch_page("onbording")