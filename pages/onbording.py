import streamlit as st
import pandas as pd
import time
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
from navigation import show_navigation

# --- Streamlit Layout ---
st.set_page_config(page_title="Keeper Data", layout="centered")

hide_sidebar()






# --- Font Size Customization ---
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-size: 20px !important;
    }
    .stSelectbox label, .stTextInput label {
        font-size: 18px !important;
    }
    .stDataFrame {
        font-size: 18px !important;
    }
    .stTabs [data-baseweb="tab"] > button {
        font-size: 22px !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("\U0001F916 KeeperData")
#st.markdown("Your AI Onboarding Agent")
st.subheader("Integrate your data into Keeper")

# Descriptive text
st.markdown(
    """
    Welcome to the onboarding process! 🎉  
    Connect your data to Keeper to automatically start mapping, cleaning,  
    and preparing it to unlock insights and intelligent workflows — fast.
    """
)

st.markdown("---")


# --- Uploaded data (Support Tickets Example) ---
uploaded_data = {
    "ticket_id": ["T001", "T002", "T003"],
    "cust_id": [1001, 1002, 1003],
    "summ": ["Login issue", "Payment failed", "Account locked"],
    "desc": ["User cannot login after reset.", "Payment gateway timed out.", "Multiple failed login attempts."],
    "create_dt": ["2024-01-05", "2024-01-07", "2024-01-10"],
    "resolve_dt": ["2024-01-06", "2024-01-08", "2024-01-11"],
    "ticket_status": ["Closed", "Closed", "Open"],
    "prio": ["High", "Critical", "Medium"],
    "assigned_support": ["Alice", "Bob", "Charlie"],
    "resol_sum": ["Password reset", "Manual payment processed", "Pending user verification"]
}

uploaded_df = pd.DataFrame(uploaded_data)

# --- Mapping Results Example ---
initial_mapping_data = [
    {"Required Field": "Ticket ID", "Mapped Field": "ticket_id", "Confidence": 0.97, "Status": "✅ Auto-mapped", "Suggestions": ["ticket_id", "cust_id", "create_dt"]},
    {"Required Field": "Customer ID", "Mapped Field": "cust_id", "Confidence": 0.95, "Status": "✅ Auto-mapped", "Suggestions": ["cust_id", "ticket_id", "prio"]},
    {"Required Field": "Issue Summary", "Mapped Field": "summ", "Confidence": 0.92, "Status": "✅ Auto-mapped", "Suggestions": ["summ", "desc", "ticket_status"]},
    {"Required Field": "Issue Description", "Mapped Field": "desc", "Confidence": 0.90, "Status": "✅ Auto-mapped", "Suggestions": ["desc", "summ", "assigned_support"]},
    {"Required Field": "Created Date", "Mapped Field": "create_dt", "Confidence": 0.88, "Status": "⚠️ Needs Review", "Suggestions": ["create_dt", "resolve_dt", "ticket_status"]},
    {"Required Field": "Status", "Mapped Field": "ticket_status", "Confidence": 0.94, "Status": "✅ Auto-mapped", "Suggestions": ["ticket_status", "prio", "assigned_support"]},
    {"Required Field": "Priority", "Mapped Field": "prio", "Confidence": 0.91, "Status": "✅ Auto-mapped", "Suggestions": ["prio", "ticket_status", "assigned_support"]},
    {"Required Field": "Assigned Agent", "Mapped Field": "assigned_support", "Confidence": 0.79, "Status": "⚠️ Needs Review", "Suggestions": ["assigned_support", "prio", "ticket_status"]},
    {"Required Field": "Resolution Summary", "Mapped Field": "resol_sum", "Confidence": 0.60, "Status": "❓ Needs User Choice", "Suggestions": ["resol_sum", "desc", "summ"]}
]

mapping_df = pd.DataFrame(initial_mapping_data)

# --- Navigation Menu ---
col1, col3 = st.columns([4, 1])
with col3:
    show_navigation()

    
# --- Function: Prioritized Selectbox ---
def build_prioritized_selectbox(required_field, suggestions, all_options, key_prefix):
    prioritized_options = suggestions + [col for col in all_options if col not in suggestions]
    return st.selectbox(
        f"Select mapping for {required_field}",
        options=prioritized_options,
        key=f"{key_prefix}_{required_field}"
    )

# --- Session State ---
states = ["agent_step", "user_mappings", "current_question", "qa_completed", "quick_current_question", "quick_completed"]
def initialize_state():
    defaults = ["connect", {}, 0, False, 0, False]
    for key, default in zip(states, defaults):
        if key not in st.session_state:
            st.session_state[key] = default

initialize_state()

# --- Step 1: Connect ---
if st.session_state.agent_step == "connect":
    st.header("\U0001F4D1 Connect to Your Data Warehouse")
    st.write("Please provide your data warehouse details to proceed.")
    warehouse = st.selectbox("Choose your data warehouse:", ["Snowflake", "BigQuery", "Redshift"])
    host = st.text_input("Host", value="demo.warehouse.com")
    port = st.text_input("Port", value="5432")
    username = st.text_input("Username", value="demo_user")
    password = st.text_input("Password", type="password", value="password123")
    database = st.text_input("Database", value="demo_db")
    if st.button("\U0001F517 Connect"):
        with st.spinner("Connecting to warehouse and scanning schema..."):
            time.sleep(2)
        st.success(f"✅ Connected to {warehouse} and schema scanned!")
        st.session_state.agent_step = "mapping"
        st.rerun()

# Step 2: Mapping Flow
elif st.session_state.agent_step == "mapping":
    st.header("\U0001F4AA Onboarding and Mapping")
    full_flow_tab, quick_fuzzy_tab, final_mapping_tab = st.tabs(["\U0001F4AA AI Mapper", "\U0001F4A1 Quick Fuzzy Fix", "\U0001F4CB Final Mapping"])

    with full_flow_tab:
        st.subheader("\U0001F4AA Unmapped or Uncertain Fields")
        editable_fields = mapping_df[mapping_df['Status'].str.contains("Needs Review|Needs User Choice")]
        st.dataframe(editable_fields, use_container_width=True)

        st.subheader("\U0001F527 Step-by-Step Review")
        if st.session_state.current_question < len(editable_fields):
            row = editable_fields.iloc[st.session_state.current_question]
            st.write(f"**What should `{row['Required Field']}` map to?**")
            st.caption(f"Suggested: {row['Mapped Field']} (Confidence: {int(row['Confidence']*100)}%)")
            available_options = list(uploaded_df.columns)
            selected_mapping = st.selectbox(
                "Select mapping:",
                options=available_options,
                index=available_options.index(row['Mapped Field']) if row['Mapped Field'] in available_options else 0,
                key=f"mapping_select_full_{st.session_state.current_question}"
            )
            if st.button("Next"):
                st.session_state.user_mappings[row['Required Field']] = selected_mapping
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.success("✅ All fields reviewed!")
            st.session_state.qa_completed = True

        if st.session_state.qa_completed:
            st.subheader("\U0001F4CB Final Mapping After Review")
            final_mapping = []
            for _, row in mapping_df.iterrows():
                required_field = row['Required Field']
                if required_field in st.session_state.user_mappings:
                    mapped_field = st.session_state.user_mappings[required_field]
                else:
                    mapped_field = row['Mapped Field']
                final_mapping.append({"Required Field": required_field, "Mapped To": mapped_field})

            final_mapping_df = pd.DataFrame(final_mapping)
            st.dataframe(final_mapping_df, use_container_width=True)

            if st.button("✅ Approve Mappings"):
                st.success("🎉 Final mapping approved and saved!")

    with quick_fuzzy_tab:
        st.subheader("\U0001F4A1 Fields to Review (Quick Fuzzy Match)")
        fuzzy_fields = mapping_df[mapping_df['Confidence'] < 0.90]
        st.dataframe(fuzzy_fields, use_container_width=True)

        if st.session_state.quick_current_question < len(fuzzy_fields):
            row = fuzzy_fields.iloc[st.session_state.quick_current_question]
            st.write(f"**What should `{row['Required Field']}` map to?**")
            st.caption(f"Suggested Match: {row['Mapped Field']} ({int(row['Confidence']*100)}% confidence)")
            available_options = list(uploaded_df.columns)
            selected_mapping = st.selectbox(
                f"Select best match:",
                options=available_options,
                index=available_options.index(row['Mapped Field']) if row['Mapped Field'] in available_options else 0,
                key=f"mapping_select_quick_{st.session_state.quick_current_question}"
            )
            if st.button("Next (Quick Match)"):
                st.session_state.user_mappings[row['Required Field']] = selected_mapping
                st.session_state.quick_current_question += 1
                st.rerun()
        else:
            st.success("✅ Quick fuzzy review complete!")
            st.session_state.quick_completed = True

        if st.session_state.quick_completed:
            st.subheader("\U0001F4CB Final Mapping After Quick Review")
            final_mapping = []
            for _, row in mapping_df.iterrows():
                required_field = row['Required Field']
                if required_field in st.session_state.user_mappings:
                    mapped_field = st.session_state.user_mappings[required_field]
                else:
                    mapped_field = row['Mapped Field']
                final_mapping.append({"Required Field": required_field, "Mapped To": mapped_field})

            final_mapping_df = pd.DataFrame(final_mapping)
            st.dataframe(final_mapping_df, use_container_width=True)

            if st.button("✅ Approve Quick Mappings"):
                st.success("🎉 Quick fuzzy mappings approved and saved!")

    with final_mapping_tab:
        st.subheader("\U0001F4CB Final Mapping Summary")
        st.success("Here's the complete mapping overview after your confirmation!")

        final_mapping = []
        for _, row in mapping_df.iterrows():
            required_field = row['Required Field']
            if required_field in st.session_state.user_mappings:
                mapped_field = st.session_state.user_mappings[required_field]
            else:
                mapped_field = row['Mapped Field']
            final_mapping.append({"Required Field": required_field, "Mapped To": mapped_field})

        final_mapping_df = pd.DataFrame(final_mapping)
        st.dataframe(final_mapping_df, use_container_width=True)

        st.subheader("\U0001F4C2 Preview of Uploaded Data")
        st.dataframe(uploaded_df, use_container_width=True)

        st.success("🎉 Great work! Your data is now mapped and ready to proceed to onboarding!")

st.caption("\U0001F916 Powered by KeeperData \U0001F4AA")
