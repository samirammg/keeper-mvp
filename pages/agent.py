import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
from datetime import datetime, timedelta
from streamlit_extras.switch_page_button import switch_page  # 👈 Add this line
from utils import hide_sidebar
from navigation import show_navigation


# --- Set Streamlit Page Config ---
st.set_page_config(page_title="Keeper Agents", layout="wide")
hide_sidebar()

st.markdown("""
    <style>
    div[data-testid="stSelectbox"] label {display: none;}
    div[data-testid="stSelectbox"] > div:first-child {margin-top: -30px;}
    </style>
""", unsafe_allow_html=True)

# --- Title and Subtitle ---

def show(): 

    st.title("🚀 Keeper Agentic Intelligence")
    st.subheader("Thinkers, Doers & Customizers Driving Post-Sales Execution")
    st.markdown(
        """
       Explore Keeper’s modular network of agents built to reason, act, and adapt across the post-sales lifecycle.  
        Track active **Thinkers**, **Doers**, and **Customizers**, monitor their performance, and discover recommended agents aligned with business goals.  
        Users can also define their own objectives, enabling Keeper to customize and act on what matters most.
        """
        )

    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            show_navigation()
    
            # Load agents data only once
            if "agents_df_full" not in st.session_state:
                agents_df = pd.read_csv("data/7_agents.csv")
                agents_df = agents_df[agents_df["flag"] == 1]
                agents_df = agents_df.drop(columns=[col for col in agents_df.columns if 'id' in col.lower()], errors='ignore')
                st.session_state.agents_df_full = agents_df.copy()
            else:
                agents_df = st.session_state.agents_df_full.copy()
    
            persona_options = ["All"] + sorted(agents_df["persona"].unique())
            selected_persona = st.selectbox("Select Persona", persona_options, index=0)
    
            if selected_persona != "All":
                agents_df = agents_df[agents_df["persona"] == selected_persona]
    
    # --- Save the latest filtered agents_df to use for Thinkers/Doers ---
    st.session_state.agents_df = agents_df.copy()

    
   
    # --- Sample KPI Values (replace with real counts later) ---
    num_thinkers = 7
    num_doers = 20
    num_customizers = 5
    num_recommended_agents = 10
    
    # --- KPI Display Section ---
    kpi_cols = st.columns(4)
    
    def kpi_card(title, value):
        return f"""
        <div style="border:1px solid #e0e0e0; padding:10px; border-radius:8px; background-color:#f9f9f9; width: 100%; margin-bottom:10px">
            <h6 style="margin-bottom:0; font-size:14px;">{title}</h6>
            <p style="font-size: 22px; font-weight: bold; margin:5px 0">{value}</p>
        </div>
        """
    
    with kpi_cols[0]:
        st.markdown(kpi_card("🧐 Thinkers", num_thinkers), unsafe_allow_html=True)
    with kpi_cols[1]:
        st.markdown(kpi_card("🔧 Doers", num_doers), unsafe_allow_html=True)
    with kpi_cols[2]:
        st.markdown(kpi_card("🎨 Customizers", num_customizers), unsafe_allow_html=True)
    with kpi_cols[3]:
        st.markdown(kpi_card("🌟 Recommended Agents", num_recommended_agents), unsafe_allow_html=True)
    
    #st.markdown("---")
    
    # --- Use the already filtered agents_df ---
    agents_df = st.session_state.agents_df.copy()

# --- Simulate extra fields: Last Run Time, Status, Completion Rate ---
    def simulate_agent_metadata(df):
        statuses = ["Active"] * 8 + ["Idle"] * 2 + ["Failed"] * 1
        simulated = df.copy()
        simulated["Last Run"] = [datetime.now() - timedelta(days=random.randint(0,30)) for _ in range(len(df))]
        simulated["Status"] = [random.choice(statuses) for _ in range(len(df))]
        simulated["Completion Rate (%)"] = [round(random.uniform(85, 100), 1) for _ in range(len(df))]
        return simulated
    
    agents_df = simulate_agent_metadata(agents_df)
    

    
    # --- Two Columns for Thinkers and Doers ---
    col1, col2 = st.columns(2)
    
    num_rows = 5
    
    with col1:
        st.subheader("🧐 Thinkers")
        thinkers_df = agents_df[["Customer-Friendly Thinker Name", "Last Run", "Status", "Completion Rate (%)"]]
        thinkers_df = thinkers_df.drop_duplicates(subset=["Customer-Friendly Thinker Name"])
        thinkers_df = thinkers_df.rename(columns={
            "Customer-Friendly Thinker Name": "Thinker Name"
        }).reset_index(drop=True)
        while len(thinkers_df) < num_rows:
            thinkers_df = pd.concat([thinkers_df, pd.DataFrame([{"Thinker Name": "", "Last Run": "", "Status": "", "Completion Rate (%)": ""}])], ignore_index=True)
        st.dataframe(thinkers_df.head(num_rows), use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("🔧 Doers")
        doers_df = agents_df[["Customer-Friendly Doer Name", "Last Run", "Status", "Completion Rate (%)"]]
        doers_df = doers_df.rename(columns={
            "Customer-Friendly Doer Name": "Doer Name",
            "Completion Rate (%)": "Completion Rate (%)"
        }).reset_index(drop=True)
        while len(doers_df) < num_rows:
            doers_df = pd.concat([doers_df, pd.DataFrame([{"Doer Name": "", "Last Run": "", "Status": "", "Completion Rate (%)": ""}])], ignore_index=True)
        st.dataframe(doers_df.head(num_rows), use_container_width=True, hide_index=True)
    
    #st.markdown("---")
    
    # --- Recommended Thinkers and Doers Section ---
    recommended_agents_df = pd.read_csv("data/7_agents.csv")
    recommended_agents_df = recommended_agents_df[recommended_agents_df["flag"] == 2]
    
    col3, col4 = st.columns(2)
    
    num_recommended_rows = 3
    
    with col3:    

        st.subheader("🌟 Recommended Keepers")
        recommended_doers_df = recommended_agents_df[[
            "Customer-Friendly Thinker Name",
            "Customer-Friendly Doer Name",
            "reason_doers"
        ]]
        recommended_doers_df = recommended_doers_df.rename(columns={
            "Customer-Friendly Thinker Name": "Thinker Name",
            "Customer-Friendly Doer Name": "Doer Name",
            "reason_doers": "Reason for Recommendation"
        }).reset_index(drop=True)

        while len(recommended_doers_df) < num_recommended_rows:
            recommended_doers_df = pd.concat([recommended_doers_df, pd.DataFrame([{"Doer Name": "", "Reason for Recommendation": ""}])], ignore_index=True)
        st.dataframe(recommended_doers_df.head(num_recommended_rows), use_container_width=True, hide_index=True)
    
        # --- Add Show Recommendation Button ---
        if st.button("Show Recommendation", key="show_recommendation", use_container_width=True):
            st.markdown("---")
            tab1, tab2, tab3 = st.tabs(["Thinkers", "Flow", "Doers"])
        
            

            with tab1:
                st.markdown("### 🧠 Recommended Thinkers")
                st.image("data/thinkers.png", use_column_width=True)
            
            with tab2:
                st.markdown("### 🔧 Recommended Full Flow")
                st.image("data/doers.png", use_column_width=True)

            with tab3:
                st.markdown("### 🔎 Recommended Doers")
                flow_html = ""
                for idx, row in recommended_doers_df.iterrows():
                    doer_name = row["Doer Name"]
                    reason = row["Reason for Recommendation"]
                    flow_html += f"""
                    <div style='display:inline-block; text-align:left; margin-right:20px;'>
                        <div style='border:1px solid #e0e0e0; border-radius:10px; padding:8px 12px; background-color:#EBF5F9; width:160px; height:70px;'>
                            <div style='font-weight:bold; font-size:14px;'>{doer_name}</div>
                            <div style='font-size:12px; margin-top:5px; color:#555;'>{reason}</div>
                        </div>
                    </div>
                    """
                    if idx != len(recommended_doers_df) - 1:
                        flow_html += "<span style='font-size:24px; vertical-align:middle;'>➡️</span>"
        
                components.html(f"""
                <div style='display:flex; align-items:center; flex-wrap:nowrap; overflow-x:auto; justify-content:center; margin-top:20px;'>
                    {flow_html}
                </div>
                """, height=180)

        #st.markdown("---")
    
    with col4:
        # --- Customize Your Keeper Agent Section ---
        st.markdown("### 🛠️ Customize Your Keepers")
        
        # --- Mapping Objectives to Recommended Doers with descriptions ---
        doer_descriptions = {
            "Usage Monitoring Doer": "Tracks product usage trends and anomalies.",
            "Feature Stickiness Analyzer": "Analyzes adoption rates of key features.",
            "Enablement Action Recommender": "Suggests proactive enablement actions.",
            "Early Drop-Off Detector": "Detects early user disengagement patterns.",
            "Onboarding Progress Tracker": "Tracks onboarding milestones and delays.",
            "Usage Drop Detector": "Identifies sudden drops in product usage.",
            "Support Ticket Escalation Detector": "Detects escalation trends in support tickets.",
            "Risk Pattern Diagnoser": "Analyzes behavior for churn risk patterns.",
            "Sentiment Analysis on Support Tickets": "Evaluates sentiment in support interactions.",
            "Adoption Risk Score Builder": "Calculates adoption risk scores.",
            "CSM Activity Tracker": "Monitors CSM engagement activities.",
            "Engagement Recommendation Engine": "Recommends engagement strategies.",
            "Executive Sponsor Engagement Monitor": "Tracks engagement of executive sponsors.",
            "Event Participation Tracker": "Tracks account participation in events.",
            "Ticket Trend Analyzer": "Analyzes historical support ticket trends.",
            "Priority Escalation Predictor": "Predicts likely escalations early.",
            "First Response Time Optimizer": "Improves first response efficiency.",
            "Root Cause Pattern Identifier": "Identifies repeated root causes in issues.",
            "Renewal Risk Detector": "Detects early renewal risks.",
            "Adoption Campaign Launcher": "Launches adoption campaigns.",
            "Customer Health Score Builder": "Builds predictive health scores.",
            "Executive Business Review (EBR) Recommender": "Recommends EBRs based on account signals."
        }
        
        objective_to_doers = {
            "Improve product adoption in first 90 days": [
                "Usage Monitoring Doer",
                "Feature Stickiness Analyzer",
                "Enablement Action Recommender",
                "Early Drop-Off Detector",
                "Onboarding Progress Tracker"
            ],
            "Detect early churn signals for new customers": [
                "Usage Drop Detector",
                "Support Ticket Escalation Detector",
                "Risk Pattern Diagnoser",
                "Sentiment Analysis on Support Tickets",
                "Adoption Risk Score Builder"
            ],
            "Increase engagement from top accounts": [
                "CSM Activity Tracker",
                "Engagement Recommendation Engine",
                "Executive Sponsor Engagement Monitor",
                "Event Participation Tracker"
            ],
            "Shorten support resolution time": [
                "Ticket Trend Analyzer",
                "Priority Escalation Predictor",
                "First Response Time Optimizer",
                "Root Cause Pattern Identifier"
            ],
            "Boost renewal likelihood for Q3 accounts": [
                "Renewal Risk Detector",
                "Adoption Campaign Launcher",
                "Customer Health Score Builder",
                "Executive Business Review (EBR) Recommender"
            ]
        }
        
        # --- Objective Selection ---
        objective_options = list(objective_to_doers.keys())
        selected_objective = st.selectbox("", objective_options)
        
        # --- State Management ---
        if 'show_full_flow' not in st.session_state:
            st.session_state.show_full_flow = False
        if 'show_modify_box' not in st.session_state:
            st.session_state.show_modify_box = False
        
        if st.button("Submit Objective", key="submit_objective", use_container_width=True):
            if selected_objective:
                st.session_state.show_full_flow = False
                st.session_state.show_modify_box = False
                st.session_state.selected_objective = selected_objective
                st.session_state.original_doers = objective_to_doers[selected_objective]
                st.session_state.displayed_doers = st.session_state.original_doers.copy()
                # Remove the 3rd doer (index 2) initially
                if len(st.session_state.displayed_doers) > 2:
                    st.session_state.removed_doer = st.session_state.displayed_doers[2]
                    st.session_state.displayed_doers.pop(2)
        
        
        
        # --- Display the Recommended Flow ---
        if 'displayed_doers' in st.session_state:
            st.markdown("---")
            st.markdown("### 🔎 Keeper Flow")
        
            # Build HTML Flow
            flow_html = ""
            for idx, doer in enumerate(st.session_state.displayed_doers):
                description = doer_descriptions.get(doer, "")
                flow_html += f"""
                <div style='display:inline-block; text-align:left; margin-right:20px;'>
                    <div style='border:1px solid #e0e0e0; border-radius:10px; padding:8px 12px; background-color:#EBF5F9; width:160px; height:70px;'>
                        <div style='font-weight:bold; font-size:14px;'>{doer}</div>
                        <div style='font-size:12px; margin-top:5px; color:#555;'>{description}</div>
                    </div>
                </div>
                """
                if idx != len(st.session_state.displayed_doers) - 1:
                    flow_html += "<span style='font-size:24px; vertical-align:middle;'>➡️</span>"
        
            components.html(f"""
            <div style='display:flex; align-items:center; flex-wrap:nowrap; overflow-x:auto; justify-content:center;'>
                {flow_html}
            </div>
            """, height=150)
        
            # Always show Modify button initially
            if not st.session_state.show_full_flow and not st.session_state.show_modify_box:
                if st.button("Modify Flow", key="modify_flow", use_container_width=True):
                    st.session_state.show_modify_box = True
                    st.rerun()
        
            # Show Textbox and Submit after Modify clicked
            if st.session_state.show_modify_box and not st.session_state.show_full_flow:
                add_instruction = f"Add '{st.session_state.removed_doer}' after '{st.session_state.displayed_doers[1]}'"
                st.text_input("Modify Action", value=add_instruction, disabled=True)
                if st.button("Submit Modification", key="submit_modification", use_container_width=True):
                    st.session_state.displayed_doers.insert(2, st.session_state.removed_doer)
                    st.session_state.show_full_flow = True
                    st.rerun()

if __name__ == "__main__":
    show()

