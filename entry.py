import streamlit as st
import re
from utils import hide_sidebar




# --- Page Config ---
st.set_page_config(page_title="Keeper MVP Access", layout="centered")

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

        st.switch_page("app.py")  # NOT app.py — just the filename without extension
