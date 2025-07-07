import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
from navigation import show_navigation

st.set_page_config(page_title="Vision Pulse", layout="wide")
hide_sidebar()

def show():
    st.title("📈 Vision Keeper Pulse")   
    st.subheader("Executive-Level Pulse for Retention, Growth & Risk")
    st.markdown(
        """
        Provides enterprise-wide visibility into NRR, churn, expansion, and retention cost trends.  
        Highlights strategic risks, portfolio dynamics, and product impact to support executive  
        planning, scenario simulation, and outcome optimization.
        """
    )

    # --- Header: Team Filter + Menu ---
    with st.container():
        _, filter_col = st.columns([4,1])
        with filter_col:
            
           show_navigation("📈 Vision Pulse")
            selected_team = st.selectbox(
                "Select Region:",
                [f"Region {i}" for i in range(1,8)],
                index=0,
                key="region_filter"
            )
   
    
    
    
    # --- Static Key Metrics ---
    static_metrics = [
        ("💰 Customer Lifetime Value", "$180,000", 3.0),
        ("📊 Team NRR", "118%", 1.5),
        ("🔄 Expansion Rate", "24%", 4.0),
        ("📉 Churn Rate Trend", "4%", -0.5),
        ("🌍 Acquisition Volatility", "22%", 2.0),
        ("⭐ Product Stickiness", "68%", 3.0),
        ("💵 Customer Retention Cost", "$1,200", -1.0),
        ("🚀 Keeper Coverage", "60%", 5.0)
    ]

    def metric_card(title, value, delta=None):
        delta_html = ""
        if delta is not None:
            arrow = "🔺" if delta >= 0 else "🔻"
            delta_html = f"<p style='color:gray;font-size:10px;margin:0'>{arrow}{abs(delta):.1f}% MoM</p>"
        return f"""
        <div style="border:1px solid #e0e0e0; padding:7px; border-radius:8px; background-color:#f9f9f9; width: 100%; margin-bottom:7px">
            <h6 style="margin-bottom:0">{title}</h6>
            <p style="font-size: 18px; font-weight: bold; margin:3px 0">{value}</p>
            {delta_html}
        </div>
        """

    st.markdown("### Key Metrics")
    cols = st.columns(4)
    for i, (title, value, delta) in enumerate(static_metrics[:4]):
        cols[i].markdown(metric_card(title, value, delta), unsafe_allow_html=True)
    cols2 = st.columns(4)
    for i, (title, value, delta) in enumerate(static_metrics[4:]):
        cols2[i].markdown(metric_card(title, value, delta), unsafe_allow_html=True)


    # --- New Layout: Left with fig1, chatbot & table | Right with all other figs ---
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.markdown("### 🤖 Keeper To-Dos")
        agents_df = pd.DataFrame([
            {"Keepers": "Keeper Optimizer Doer on the full enterprise base", "Start Date": "2025-04-28 02:00 PM", "Targets Account": "N/A", "Completion": "100%", "Status": "Finished ✅<span style='color:blue; text-decoration:underline'>Keeper List</span>", "Blocker": "-"},
            {"Keepers": "Retention Scenario Generator Doer", "Start Date": "2025-04-29 10:00 AM", "Targets Account": "All Accts", "Completion": "100%", "Status": "Finished ✅<span style='color:blue; text-decoration:underline'>Generated Retention Scenarios</span>", "Blocker": "—"},
            {"Keepers": "Root Cause Analysis Thinker", "Start Date": "2025-05-01 8:00 AM", "Targets Account": "86 Accts", "Completion": "72%", "Status": "Running", "Blocker": "—"},
            {"Keepers": "Portfolio Risk Simulation Thinker", "Start Date": "2025-05-02 09:00 AM", "Targets Account": "All Accts", "Completion": "0%", "Status": "Scheduled", "Blocker": "—"}
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
        st.markdown("<br><br>", unsafe_allow_html=True)
        

        
        st.markdown("### ✅ Your To-Dos")
        todos_df = pd.DataFrame([
            {"To Do": "Eliminate <12-month contracts or require onboarding.", "Start Date": "2025-05-02 10:00 AM", "Target Accounts": "All Accts", "Completion": "0%", "Status": "Not Started", "Description": "<span style='color:blue; text-decoration:underline'>account list</span>", "Priority": "-"},
            {"To Do": "Revamp Product X to curb attrition.", "Start Date": "2025-05-01 09:00 AM", "Target Accounts": "All Accts", "Completion": "50%", "Status": "In Progress", "Description": "<span style='color:blue; text-decoration:underline'>Revenue Impact Doer🤖</span>", "Priority": "-"},
            {"To Do": "Refine ICP and reopen key segments.", "Start Date": "2025-05-03 11:00 AM", "Target Accounts": "N/A", "Completion": "0%", "Status": "Scheduled", "Description": "<span style='color:blue; text-decoration:underline'>ICP Recomendation Doer🤖</span>", "Priority": "-"}
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
        {"Suggestion": "If ‘risky’ customers don’t drop 5% this quarter, we risk $4 M ACV loss in 6 months."},
        {"Suggestion": "Fintech accounts outside the U.S. under $50 K ACV churn +30%."},
        {"Suggestion": "New‐customer acquisition is down 23% in 30 days."},        
        {"Suggestion": "Product X usage drives enterprise churn 5×."}
        ]

       
        with st.container(border=True):
            for r in recs:
                #st.write(f"⚠️ {r['Suggestion']}")
                st.markdown(f"⚠️ {r['Suggestion']} <span style='color:blue;text-decoration:underline'>(click)</span>", unsafe_allow_html=True)

        #st.markdown("---")

        # --- Recommendations Section ---
        st.markdown("#### 💡 Insights & Recommendations")
        recs = [
            {"Suggestion": "Customer retention costs fell 25% last quarter via Keeper Optimizer."},
            {"Suggestion": "Sub-12-month contracts double churn risk; extend initial terms."},
            {"Suggestion": "19% moved from Safe Renewal to Expansion, boosting ACV by 10%."},
            {"Suggestion": "Bundling Y + Z drove a 10% lift; pilot with top 20 fintech accounts for $2 M upside."},
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
