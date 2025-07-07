import streamlit as st
import re
from utils import hide_sidebar

st.set_page_config(page_title="Keeper Access", layout="wide")
hide_sidebar()

st.title("🔐 Access Keeper MVP")
st.markdown("Please fill out the form below to view the MVP. All fields are required.")

# --- Form Fields ---
full_name = st.text_input("Full Name")
email = st.text_input("Email", placeholder="you@example.com")
role = st.selectbox("Your Role", ["", "Executive", "Leader / Manager", "Individual Contributor", "Advisor", "Investor"])
access_code = st.text_input("Access Code", type="password")

# --- Access Code ---
SECRET_CODE = "keeper2025"

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

if st.button("Enter"):
    if not full_name.strip() or not email.strip() or role == "" or not access_code.strip():
        st.error("❌ Please fill out all fields.")
    elif not is_valid_email(email):
        st.error("❌ Please enter a valid email address.")
    elif access_code != SECRET_CODE:
        st.error("❌ Invalid access code.")
    else:
        st.session_state["authenticated"] = True
        st.session_state["user_name"] = full_name.strip()
        st.session_state["user_email"] = email.strip()
        st.session_state["user_role"] = role

        st.success("✅ Access granted! You can now explore the MVP below.")

        st.markdown("---")
        st.subheader("📂 Jump to a Module:")

        st.page_link("pages/Pulse.py", label="🧩 Keeper Pulse")
        st.page_link("pages/Journey.py", label="📘 Customer Journey")
        st.page_link("pages/GrowthPulse.py", label="💓 Growth Pulse")
        st.page_link("pages/TeamPulse.py", label="🩺 Team Pulse")
        st.page_link("pages/Activity.py", label="↳  📌 CSM Activity")
        st.page_link("pages/Support.py", label="↳  💬 Support Trends")
        st.page_link("pages/Usage.py", label="↳  📊 Product Usage")
        st.page_link("pages/VisionPulse.py", label="📈 Vision Pulse")
        st.page_link("pages/Strategy.py", label="↳  🧭 Strategy")
        st.page_link("pages/agent.py", label="🚀 Keeper Agents")
        st.page_link("pages/onbording.py", label="🗄️ Keeper Data")
