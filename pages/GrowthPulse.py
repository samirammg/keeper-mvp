import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
import pandas as _pd
from navigation import show_navigation


st.set_page_config(page_title="Growth Pulse", layout="wide")
hide_sidebar()

def show():
    st.title("💓 Growth Keeper Pulse")
    st.subheader("Frontline Metrics, Actions & Recommendations")

    st.markdown(
        """
        **Growth Keeper Pulse** empowers CSMs, RevOps, AEs, and Support teams with real-time insights across  
        the accounts they manage including engagement metrics, active agents, and emerging risks.  
        Personalized to-dos and intelligent recommendations help prioritize action, boost productivity,  
        and drive retention and expansion outcomes.
        """
    )


    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
           show_navigation("💓 Growth Pulse")
            
    c_risky='#6f6f6f'
    c_adoption='#9ccee1'
    c_renew='#2b6490'
    c_expansion='#f2c300'

    
    
    @st.cache_data
    def load_score_data():
        df = pd.read_csv("data/5_model_final_score_dashboard.csv")
        if 'FOM' not in df.columns:
            df['FOM'] = pd.date_range(start="2020-01-01", periods=len(df), freq='MS')
        if 'FOM_str' not in df.columns:
            df['FOM_str'] = pd.to_datetime(df['FOM']).dt.to_period('M').astype(str)
        df['FOM'] = pd.to_datetime(df['FOM_str'])
        return df.sort_values('FOM_str')
    
    @st.cache_data
    def load_score_details():
        df = pd.read_csv("data/5_model_final_score_dashboard_data.csv")
        if 'FOM' not in df.columns:
            df['FOM'] = pd.date_range(start="2020-01-01", periods=len(df), freq='MS')
        if 'FOM_str' not in df.columns:
            df['FOM_str'] = pd.to_datetime(df['FOM']).dt.to_period('M').astype(str)
        df['FOM'] = pd.to_datetime(df['FOM_str'])
        return df   
    df_score = load_score_data().fillna(0)
    df_score_c = load_score_details().fillna(0)
    
    # --- Metrics to Display ---
    score_metrics = {
        'adoption': "✅ Adoption",
        'expansion': "📈 Expansion",
        'renewal': "🔁 Renewal",
        'risky': "⚠️ Risky",
        'adoption_acv': "💰 Adoption ACV",
        'expansion_acv': "💸 Expansion ACV",
        'renewal_acv': "💵 Renewal ACV",
        'risky_acv': "🔥 Risky ACV"
    }
    
    # Calculate % change for primary metrics (if not already present)
    for key in ['adoption', 'expansion', 'renewal', 'risky']:
        if f"{key}_mom_pct" not in df_score.columns:
            df_score[f"{key}_mom_pct"] = df_score[key].pct_change().replace([float('inf'), -float('inf')], 0).fillna(0) * 100
    
    df_score_summary = df_score[['FOM_str'] + list(score_metrics.keys()) + [f"{k}_mom_pct" for k in ['adoption', 'expansion', 'renewal', 'risky']]]
    df_score_summary = df_score_summary.sort_values('FOM_str')
    
    # --- Top-right Filter ---
    with st.container():
        filter_col = st.columns([4, 1])[1]
        with filter_col:
            selected_fom = st.selectbox(
                "Selected Date",
                df_score_summary['FOM_str'].unique()[::-1],
                index=list(df_score_summary['FOM_str'].unique()[::-1]).index("2025-04")
            )
            
            #selected_fom = st.selectbox("Selected Date", df_score_summary['FOM_str'].unique()[::-1], label_visibility="collapsed")
    selected_fom_dt = pd.to_datetime(selected_fom)
    row = df_score_summary[df_score_summary['FOM_str'] == selected_fom].iloc[0]
    
    # --- Metric Card Renderer ---
    def metric_card(title, value, delta=None):
        delta_str = ""
        if delta is not None:
            arrow = "🔺+" if delta >= 0 else "🔻-"
            delta_str = f"<p style=\"color:gray; font-size: 10px; margin:0\">{arrow} {abs(delta):.1f}% from last period</p>"
        return f"""
        <div style="border:1px solid #e0e0e0; padding:7px; border-radius:8px; background-color:#f9f9f9; width: 100%; margin-bottom:7px">
            <h6 style="margin-bottom:0">{title}</h6>
            <p style="font-size: 18px; font-weight: bold; margin:3px 0">{value}</p>
            {delta_str}
        </div>
        """    
    
# --- CSM & Agent Metrics ---
    csm_agent_metrics = [
        ("Avg Touchpoints per Customer", "avg_touchpoints"),
        ("Average Activity Duration", "avg_activity_duration (min)"),
        ("Open Action Items", "open_action_items"),
        ("Alerts", "alerts_count"),
        ("# Agents Running", "agents_running"),
        ("Overall Progress %", "agents_progress_pct"),
        ("Agent Tasks Needing CSM Action", "agent_pending_tasks"),
        ("Recommended New Agents", "recommended_agents_count"),
    ]

    # Dummy values for now; replace with real data
    csm_agent_values = [12, 45, 4, 3, 5, 76, 1, 2]
    csm_agent_deltas = [None]*8

    # Render first row of 4
    cam_cols1 = st.columns(4)
    for idx in range(4):
        title = csm_agent_metrics[idx][0]
        val = csm_agent_values[idx]
        cam_cols1[idx].markdown(metric_card(title, val, csm_agent_deltas[idx]), unsafe_allow_html=True)

    # Render second row of 4
    cam_cols2 = st.columns(4)
    for idx in range(4,8):
        title = csm_agent_metrics[idx][0]
        val = csm_agent_values[idx]
        cam_cols2[idx-4].markdown(metric_card(title, val, csm_agent_deltas[idx]), unsafe_allow_html=True)

    df_fom = df_score_c[df_score_c['FOM_str'] == selected_fom].copy()
    
    left_col, right_col = st.columns([2, 1])
    # --- Prepare df_fom earlier for both columns ---
    df_fom = df_score_c[df_score_c['FOM_str'] == selected_fom].copy()
    
    # --- New Layout: Left with fig1, chatbot & table | Right with all other figs ---
    left_col, right_col = st.columns([2, 1])
    
    with left_col:

        st.markdown("### 🤖 Keeper To-Dos")
        # Agent table: Name, Objective, Tasks, Completion, Status, Blocker, Modify
        import pandas as _pd
        agents_df = _pd.DataFrame([
            {"Keepers": "Boost Customer Engagement Health Thinker", "Start Date": "2025-04-27 08:00 AM", "Target Account": 50, "Completion": "100%", "Status": "Finished ✅ <span style='color:blue;text-decoration:underline'>(see the recommendations)</span>", "Blocker": "None"},
            {"Keepers": "Identify Priority Accounts Thinker", "Start Date": "2025-04-27 10:00 AM", "Target Account": 17, "Completion": "100%", "Status": "Finished ✅ <span style='color:blue;text-decoration:underline'>(see the account list)</span>", "Blocker": "None"},
            {"Keepers": "Journey Health Monitor Doer", "Start Date": "2025-04-28 10:00 AM", "Target Account": 120, "Completion": "85%", "Status": "Running", "Blocker": "None"},
            {"Keepers": "Engagement Meeting Setup Doer", "Start Date": "2025-04-28 2:00 PM", "Target Account": 80, "Completion": "63%", "Status": "Paused", "Blocker": "<span style='color:blue;text-decoration:underline'>Invalid Email</span>"},
            {"Keepers": "Strengthen Customer Sentiment and Loyalty Thinker", "Start Date": "2025-04-29 9:00 AM", "Target Account": 200, "Completion": "79%", "Status": "Running", "Blocker": "None"},
        ])

        display_df = agents_df.copy()
        # Style columns as HTML
        display_html = display_df.to_html(escape=False, index=False)
        # Center headers and cells via inline CSS
        styled_html = display_html.replace('<table','<table style="width:100%; text-align:center; border-collapse: collapse;font-size:10px;"')
        styled_html = styled_html.replace('<th>','<th style="border:1px solid #ddd; padding:8px; text-align:left;font-size:10px;">')
        styled_html = styled_html.replace('<td>','<td style="border:1px solid #ddd; padding:8px; text-align:left;font-size:10px;">')
        st.write(styled_html, unsafe_allow_html=True)
       # Modify button spanning table width
        st.button("Modify", use_container_width=True)
        #st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### ✅ Your To-Dos")

        todos_df = _pd.DataFrame([
            {"To Do": "Call Data Integration Team to confirm connection status", "Start Date": "2025-04-30 09:00 AM", "Target Account": 5, "Completion": "0%", "Status": "Not Started", "Description": "<span style='color:blue; text-decoration:underline'>Account List/email</span>", "Priority": "P0"},
            {"To Do": "Review and mitigate renewal risk accounts", "Start Date": "2025-04-28 03:00 PM", "Target Account": 17, "Completion": "70%", "Status": "In Progress", "Description": "<span style='color:blue; text-decoration:underline'>Active Next Best Action Doer 🤖 </span>", "Priority": "P0"},
            {"To Do": "Verify and update customer contact details", "Start Date": "2025-04-29 08:00 AM", "Target Account": 30, "Completion": "54%", "Status": "In Progress", "Description": "<span style='color:blue; text-decoration:underline'>Submit DA team ticket</span>", "Priority": "P1"},
            {"To Do": "Schedule enablement training session", "Start Date": "2025-04-28 09:00 AM", "Target Account": 27, "Completion": "0%", "Status": "Not Started", "Description": "<span style='color:blue; text-decoration:underline'>Activate Engagement Meeting Setup Doer 🤖 </span>", "Priority": "P2"},
        ])
        # Reorder columns: To Do, Priority, Target Account, Completion, Status, Start Date, End Date
        # Reorder columns: To Do, Priority, Start Date, Target Account, Completion, Status, Description
        # Reorder columns: To Do, Start Date, Target Account, Completion, Status, Description, Priority
        todos_html = todos_df[['To Do','Start Date','Target Account','Completion','Status','Description','Priority']].to_html(index=False, escape=False)
        # Center table and style borders
        todos_html = todos_html.replace(
            '<table',
            '<table style="width:100%; border-collapse: collapse; text-align:center;font-size:10px;"'
        )
        todos_html = todos_html.replace('<th>', '<th style="border:1px solid #ddd; padding:8px; text-align:left;font-size:10px;">')
        todos_html = todos_html.replace('<td>', '<td style="border:1px solid #ddd; padding:8px; text-align:left;font-size:10px;">')
        st.write(todos_html, unsafe_allow_html=True)
        st.button("Review", use_container_width=True)

        #st.markdown("---")


        
        
        
    with right_col:
        st.markdown("---")
        st.markdown("###### 🚨 Alert System for Emerging Risks")
        recs = [
        {"Suggestion": "5 enterprise customers have data outage since 2025-04-30 09:00 AM"},
        {"Suggestion": "6 of 17 accounts have renewal risk; renewal date end of this month"},
        {"Suggestion": "Your top 10 highest-value customers are engaging less — consider reaching out"},
    ]
        with st.container(border=True):
            for r in recs:
                st.markdown(
                    f"<span style='font-size:10px;line-height:1.2; margin-bottom:4px;'>⚠️ {r['Suggestion']} "
                    "<span style='color:blue;text-decoration:underline'>(click)</span></span>",
                    unsafe_allow_html=True
                )
        
        #st.markdown("---")

        # --- Recommendations Section ---
        st.markdown("###### 💡 Recommendations")
        recs = [
            {"Suggestion": "Churn Prevention Agent drove a 15% drop in churn; follow up with top 5 at-risk accounts"},
            {"Suggestion": "Meeting Setup Doer boosted attendance by 30%, increasing renewal likelihood by 12%"},
            {"Suggestion": "Usage Monitoring Agent lifted feature adoption by 20%; expand to next tier accounts"},
            {"Suggestion": "Next Best Action Doer cut ticket volume by 25%; add for top 10 at-risk accounts"},
            {"Suggestion": "Increasing 1:1 touchpoints from 45 to 60 minutes boosted expansion chances by 30% for new customers"},
        ]
        with st.container(border=True):
            for r in recs:
                st.markdown(f"<span style='font-size:10px; line-height:1.2; margin-bottom:4px;'>🎯 {r['Suggestion']} <span style='color:blue;text-decoration:underline'>(click)</span>", unsafe_allow_html=True)
        #st.markdown("---")


        #st.markdown("###### 🤖 Ask Keeper")
        default_q = "Why Pulse of company 1 is risky?"
        user_input = st.text_area("#### 🤖 Ask Keeper", value=default_q, height=100)
        if st.button("Ask Keeper"):
            st.info("""
        ❌ Declining product usage (↓40% in last 2 months)  
        ❌ Unresolved support tickets (3 high-priority issues open for 30+ days)  
        ❌ Low CSM engagement (No touchpoints in last 60 days)  
        👉 **Suggested Action**: Schedule a recovery call & offer an incentive to stay engaged.
                """)   
        
    
    
if __name__ == "__main__":
    show()
