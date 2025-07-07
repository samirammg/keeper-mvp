import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import re
from utils import hide_sidebar

st.set_page_config(page_title="app", layout="wide")


hide_sidebar()

st.title("🔐 Access Keeper MVP")

st.markdown("Please fill out the form below to view the MVP. All fields are required.")

# --- Form Fields ---
full_name = st.text_input("Full Name")
email = st.text_input("Email", placeholder="you@example.com")
role = st.selectbox("Your Role", ["", "Executive", "Leader / Manager", "Individual Contributor", "Advisor","Investor"])
access_code = st.text_input("Access Code", type="password")

# --- Access Code ---
SECRET_CODE = "keeper2025"

# --- Email format checker ---
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# --- Button + Validation ---
if st.button("Enter"):
    if not full_name.strip() or not email.strip() or role == "" or not access_code.strip():
        st.error("❌ Please fill out all fields.")
    elif not is_valid_email(email):
        st.error("❌ Please enter a valid email address.")
    elif access_code != SECRET_CODE:
        st.error("❌ Invalid access code.")
    else:
        # Save user info
        st.session_state["authenticated"] = True
        st.session_state["user_name"] = full_name.strip()
        st.session_state["user_email"] = email.strip()
        st.session_state["user_role"] = role

        st.success("✅ Access granted! Redirecting...")

        # 🔁 Make sure your target file (like app.py) is inside /pages and matches this name exactly




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
