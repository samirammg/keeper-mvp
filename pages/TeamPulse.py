import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar

st.set_page_config(page_title="Growth Pulse", layout="wide")

hide_sidebar()

def show():
    st.title("🩺 Team Keeper Pulse")
    st.subheader("Leadership Metrics & Insights")
    st.markdown(
        """
        **Team Keeper Pulse** empowers leaders and managers assess performance, 
        monitor maturityand engagement trends, and uncover patterns across  
        **CSM activity**, **support**, and **product usage**.  Intelligent agents surface teamwide actions, risks, recommendation and opportunities.
        """
    )
    

    # --- Header: Team Filter + Menu ---
    with st.container():
        _, filter_col = st.columns([4,1])
        with filter_col:
            
            menu = st.selectbox(
                "",[
                    "🩺 Stay on Team Pulse",
                    "↳  📌 CSM Activity",
                    "↳  💬 Support Trends",
                    "↳  📊 Product Usage",
                    "📘 Customer Pulse",
                    "🧩 Keeper Pulse",
                    "💓 Growth Pulse",
                    "📈 Vision Pulse",
                    "↳  🧭 Strategy",
                    "🚀 Keeper Agents",
                    "🗄️ Keeper Data"
                ],label_visibility="collapsed",key="nav_menu"
            )
            selected_team = st.selectbox(
                "Select Team:",
                [f"Team {i}" for i in range(1,8)],
                index=0,
                key="team_filter"
            )
        if menu == "🩺 Stay on Team Pulse":
            pass
        elif menu == "📘 Customer Pulse":
            switch_page("Journey")
        elif menu == "🧩 Keeper Pulse":
            switch_page("Pulse")
        elif menu == "💓 Growth Pulse":
            switch_page("GrowthPulse")
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

    


    # --- Static Key Metrics ---
    static_metrics = [
        ("🏢 Total Active Accounts", "146"),
        ("⚠️ At-Risk Accounts ACV", "$698,700"),
        ("🔄 Renewal Pipeline", "$6,338,100"),
        ("🚀 Expansion ACV", "$1,882,900"),
        ("👥 Avg Accounts / CSM", "12 ± 2"),
        ("👤 Avg ACV / CSM", "$685,000 ± $115,000"),
        ("📊 Avg Risk Score", "38"),
        ("⚡ Keeper Opportunity Gap", "42%")
    ]

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
        

    st.markdown("### Key Metrics")
    cols = st.columns(4)
    for i, (title, value) in enumerate(static_metrics[:4]):
        cols[i].markdown(metric_card(title, value), unsafe_allow_html=True)
    cols2 = st.columns(4)
    for i, (title, value) in enumerate(static_metrics[4:]):
        cols2[i].markdown(metric_card(title, value), unsafe_allow_html=True)

    st.markdown("---")
    # --- New Layout: Left with fig1, chatbot & table | Right with all other figs ---
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.markdown("### 🤖 Keeper To-Dos")
        agents_df = pd.DataFrame([
            {"Keepers": "Diagnose Resource Gaps Doer", "Start Date": "2025-04-28 02:00 PM", "Targets Account": "Teamwide", "Completion": "100%", "Status": "Finished ✅<span style='color:blue; text-decoration:underline'>see the report</span>", "Blocker": "-"},
            {"Keepers": "Empower Personalized Customer Journeys Thinker", "Start Date": "2025-04-30 10:00 AM", "Targets Account": "120 Accts", "Completion": "45%", "Status": "Running", "Blocker": "—"},
            {"Keepers": "Risk Pattern Analyzer Doer", "Start Date": "2025-05-01 11:00 AM", "Targets Account": "75 Accts", "Completion": "65%", "Status": "Running", "Blocker": "—"},
            {"Keepers": "Advance Customer Maturity and Growth Thinker", "Start Date": "2025-05-02 09:00 AM", "Targets Account": "All Accts", "Completion": "0%", "Status": "Scheduled", "Blocker": "—"}
        ])
        # Render Keeper To-Dos as HTML table to preserve emojis and links
        #st.markdown(agents_df.to_html(index=False, escape=False), unsafe_allow_html=True)       
        display_df = agents_df.copy()
        # Style columns as HTML
        display_html = display_df.to_html(escape=False, index=False)
        # Center headers and cells via inline CSS
        styled_html = display_html.replace('<table','<table style="width:100%; text-align:center; border-collapse: collapse;"')
        styled_html = styled_html.replace('<th>','<th style="border:1px solid #ddd; padding:8px; text-align:left;">')
        styled_html = styled_html.replace('<td>','<td style="border:1px solid #ddd; padding:8px; text-align:left;">')
        st.write(styled_html, unsafe_allow_html=True)
       # Modify button spanning table width
        st.button("Modify", use_container_width=True)
        #st.markdown("<br><br>", unsafe_allow_html=True)
        
        
        st.markdown("### ✅ Your To-Dos")
        todos_df = pd.DataFrame([
            {"To Do": "Analyze customer churn patterns over last 6 months & propose mitigation playbooks", "Start Date": "2025-05-02 10:00 AM", "Target Accounts": "53", "Completion": "0%", "Status": "Not Started", "Description": "<span style='color:blue; text-decoration:underline'>account list</span>", "Priority": "P0"},
            {"To Do": "Share product improvement areas based on adoption patterns with the Product team", "Start Date": "2025-05-01 09:00 AM", "Target Accounts": "all Accts", "Completion": "50%", "Status": "In Progress", "Description": "<span style='color:blue; text-decoration:underline'>Active Recommend Journey Corrections Doer🤖</span>", "Priority": "P1"},
            {"To Do": "Present Keeper usage gap & best-practice opportunities to the team", "Start Date": "2025-05-03 11:00 AM", "Target Accounts": "N/A", "Completion": "0%", "Status": "Scheduled", "Description": "<span style='color:blue; text-decoration:underline'>Active Monitor CSM Behaviors Doer🤖</span>", "Priority": "P1"},
            {"To Do": "Prepare hiring plan with potential ARR per new hire", "Start Date": "2025-04-29 08:00 AM", "Target Accounts": "N/A", "Completion": "85%", "Status": "In Progress", "Description": "<span style='color:blue; text-decoration:underline'>Resource Gaps Report</span>", "Priority": "P2"}
        ])
        # Reorder columns: To Do, Priority, Target Account, Completion, Status, Start Date, End Date
        # Reorder columns: To Do, Priority, Start Date, Target Account, Completion, Status, Description
        # Reorder columns: To Do, Start Date, Target Account, Completion, Status, Description, Priority
        todos_html = todos_df[['To Do','Start Date','Target Accounts','Completion','Status','Description','Priority']].to_html(index=False, escape=False)
        # Center table and style borders
        todos_html = todos_html.replace(
            '<table',
            '<table style="width:100%; border-collapse: collapse; text-align:center;"'
        )
        todos_html = todos_html.replace('<th>', '<th style="border:1px solid #ddd; padding:8px; text-align:left;">')
        todos_html = todos_html.replace('<td>', '<td style="border:1px solid #ddd; padding:8px; text-align:left;">')
        st.write(todos_html, unsafe_allow_html=True)
        st.button("Review", use_container_width=True)

        #st.markdown("---")
        
    with right_col:

        st.markdown("#### 🚨 Alert System for Emerging Risks")
        recs = [
        {"Suggestion": "First Response Time (avg. time between ticket creation and first response) increased 23% in the last week."},
        {"Suggestion": "Repeat Touch Rate: 45% of tickets for Feature X are persistent issues this month."},
        {"Suggestion": "Feature Y Abandonment: North American users are dropping off—investigate usability"},
    ]
        with st.container(border=True):
            for r in recs:
                #st.write(f"⚠️ {r['Suggestion']}")
                st.markdown(f"⚠️ {r['Suggestion']} <span style='color:blue;text-decoration:underline'>(click)</span>", unsafe_allow_html=True)

        #st.markdown("---")

        # --- Recommendations Section ---
        st.markdown("#### 💡 Insights & Recommendations")
        recs = [
            {"Suggestion": "Shipping Feature Z projects $0.5 M expansion ACV."},
            {"Suggestion": "First Response Time spike aligns with rising negative sentiment. Run the “Support Sentiment Analyzer” Doer to pinpoint root causes."},
            {"Suggestion": "The quality of CSM conversation and growth-focused questions results with +15% upsell. Distribute best-practice talking points via the “Call Coaching” Doer."},
            {"Suggestion": "Churn accelerates after Month 3 post-onboarding for new customers. Implement proactive “Month 3 Check In” playbook and automate reminders via Keeper."},
            {"Suggestion": "Hand-offs between Support and CSMs are delaying resolutions. Run the “Diagnose Coordination Gaps” Doer to align workflows"},
        ]
        with st.container(border=True):
            for r in recs:
                st.markdown(f"🎯 {r['Suggestion']} <span style='color:blue;text-decoration:underline'>(click)</span>", unsafe_allow_html=True)
        #st.markdown("---")
        
        
        #st.markdown("#### 🤖 Ask Keeper")
        default_q = "Why Pulse of company 1 is risky?"
        user_input = st.text_area("##### 🤖 Ask Keeper", value=default_q, height=1)
        if st.button("Ask Keeper"):
            st.info("""
        ❌ Declining product usage (↓40% in last 2 months)  
        ❌ Unresolved support tickets (3 high-priority issues open for 30+ days)  
        ❌ Low CSM engagement (No touchpoints in last 60 days)  
        👉 **Suggested Action**: Schedule a recovery call & offer an incentive to stay engaged.
                """)   
        
    
    
if __name__ == "__main__":
    show()