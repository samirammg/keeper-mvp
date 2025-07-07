import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar

st.set_page_config(page_title="Support Trends", layout="wide")
hide_sidebar()

def show():
    st.title("💬 Support Trends & Insights")
    st.subheader("Escalation Signals, Root Causes & Resolution Planning")

    st.markdown(
        """
        Tracks support trends, resolution performance, and workload patterns.  
        Surfaces recurring issues, enables root cause analysis, and supports planning  
        to improve efficiency, reduce escalations, and enhance customer experience.
        """
    )


    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            menu = st.selectbox("", [
                "↳ 💬 Stay on Support Trends",
                "🩺 Team Pulse",
                "↳  📌 CSM Activity",
                "↳  📊 Product Usage",
                "📘 Customer Pulse",
                "🧩 Keeper Pulse",
                "💓 Growth Pulse",
                "📈 Vision Pulse",
                "↳  🧭 Strategy",
                "🚀 Keeper Agents",
                "🗄️ Keeper Data"
            ], label_visibility="collapsed")

    if menu == "↳ 💬 Stay on Support Trends":
        pass
    elif menu == "📘 Customer Pulse":
        switch_page("Journey")
    elif menu == "🧩 Keeper Pulse":
        switch_page("Pulse")
    elif menu == "💓 Growth Pulse":
        switch_page("GrowthPulse")
    elif menu == "🩺 Team Pulse":
        switch_page("TeamPulse")
    elif menu == "↳  📌 CSM Activity":
        switch_page("Activity")
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
       
    # --- Load Data ---
    @st.cache_data
    def load_data():
        df = pd.read_csv("data/5_support_dashboard.csv")
        df['FOM'] = pd.to_datetime(df['FOM'])
        df['FOM_str'] = df['FOM'].dt.strftime('%Y-%m')
        df['total_resolution_time'] = df['total_resolution_time'] * 280
        df['open_rate'] = df['open_ratio']
        df['close_rate'] = df['close_ratio']
        return df.sort_values('FOM')
    
    @st.cache_data
    def load_ticket_data():
        df_tickets = pd.read_csv("data/0_sim_support_tickets.csv")
        df_tickets['ticket_creation_date'] = pd.to_datetime(df_tickets['ticket_creation_date'])
        df_tickets['FOM'] = df_tickets['ticket_creation_date'].dt.to_period('M').astype(str)
        return df_tickets
    
    @st.cache_data
    def load_insight_data():
        return pd.read_csv("data/5_support_insight_dashboard.csv")
    
    # --- Load DataFrames ---
    df = load_data().fillna(0)
    df_support_tickets = load_ticket_data()
    df_insights = load_insight_data()
    
    # --- Metrics ---
    metrics = {
        "total_tickets": "🌼Ticket Volume",
        "median_response_time": "⏱️Response Time",
        "median_resolution_time": "🛠️Resolution Time",
        "total_resolution_time": "💵Support Cost",
        "total_high_priority": "🔥High Priority Tickets",
        "escalation_rate": "🚨Escalation Rate",
        "repeat_contact_rate": "🔁Repeat Contact Rate(RCR)",
        "open_rate": "📬Open Rate",
        "close_rate": "✅Close Rate"
    }
    
    # --- MoM Change ---
    df_summary = df[['FOM_str'] + list(metrics.keys()) + [col for col in df.columns if col.startswith('subject_')]].copy()
    df_summary = df_summary.sort_values('FOM_str')
    for col in metrics:
        df_summary[f"{col}_pct_change"] = df_summary[col].pct_change() * 100
    
    # --- Top-right Filter ---
    with st.container():
        filter_col = st.columns([4, 1])[1]
        with filter_col:
            #selected_fom = st.selectbox("", df_summary['FOM_str'].unique()[::-1], label_visibility="collapsed")
            selected_fom = st.selectbox(
                "Selected Date",
                df_summary['FOM_str'].unique()[::-1],
                index=list(df_summary['FOM_str'].unique()[::-1]).index("2025-04")
            )

    row = df_summary[df_summary['FOM_str'] == selected_fom].iloc[0]
    
    # --- KPI Cards ---
    def metric_card(title, value, delta):
        arrow = "🔺+" if delta >= 0 else "🔻-"
        delta_str = f"{arrow} {abs(delta):.1f}%"
        return f"""
        <div style="border:1px solid #e0e0e0; padding:7px; border-radius:8px; background-color:#f9f9f9; width: 100%; margin-bottom:7px">
            <h6 style="margin-bottom:0">{title}</h6>
            <p style="font-size: 18px; font-weight: bold; margin:3px 0">{value}</p>
            <p style="color:gray; font-size: 10px; margin:0">{delta_str} from last period</p>
        </div>
        """
    
    # --- Dashboard Header ---
    #st.title(f"🎯 Support Overview|Trend|AI Insight – {selected_fom}")
    #st.title(f"💬 Support Trends & Insights ")
    
    st.markdown("---")
    
    st.markdown("##### 📏Key Support Metrics")
    
    cols_top = st.columns(4)
    for idx, key in enumerate(["total_tickets", "open_rate", "close_rate", "escalation_rate"]):
        val = f"{row[key]:.0f}%" if 'rate' in key else int(row[key])
        cols_top[idx].markdown(metric_card(metrics[key], val, row[f"{key}_pct_change"]), unsafe_allow_html=True)
    
    cols_bottom = st.columns(4)
    for idx, key in enumerate(["median_response_time", "median_resolution_time", "total_resolution_time", "repeat_contact_rate"]):
        if key == "total_resolution_time":
            val = f"{row[key]:.0f} $"
        elif "time" in key:
            val = f"{row[key]:.2f} hrs"
        else:
            val = f"{row[key]:.0f}%"
        cols_bottom[idx].markdown(metric_card(metrics[key], val, row[f"{key}_pct_change"]), unsafe_allow_html=True)
    
    st.markdown("---")
    # --- Main Two-Column Layout ---
    left_col, right_col = st.columns([1, 1])
    st.markdown("---")
    # --- LEFT: Generative Insights + Keeper ---
    with left_col:
        st.markdown("##### ✨Generative Insights")
        color_map = {"Red": "🔴", "Yellow": "🟡", "Green": "🟢"}
        def render_insight_box(title, items, use_icons=False):
            content = f"""
            <div style='border:1px solid #ddd; border-radius:8px; padding:10px; background-color:#f9f9f9; margin-bottom:12px;'>
                <h5 style='margin-bottom:8px; font-size:16px;'>{title}</h5>
                <ul style='padding-left:14px; font-size:6px; line-height:1; margin:0;'>
            """
            for topic, subject in items:
                bullet = color_map.get(topic, "") if use_icons else "•"
                content += f"<li style='list-style-type:none'>{bullet} {subject}</li>"
            content += "</ul></div>"
            st.markdown(content, unsafe_allow_html=True)
    
        insight_dict = {s: df_insights[df_insights['section'] == s] for s in df_insights['section'].unique()}
        render_insight_box("🧠 AI-Generated Key Insights for Executives", insight_dict["AI-Generated Key Insights for Executives"][['topic','subject']].values.tolist(), use_icons=True)
        render_insight_box("⚡ AI-Driven Strategy Recommendations", insight_dict["AI-Driven Strategy Recommendations"][['topic','subject']].values.tolist())
        render_insight_box("⚠️ Risk Alert System", insight_dict["Risk Alert System"][['topic','subject']].values.tolist())
        render_insight_box("🚀 Action Recommend", insight_dict["Action Recommend"][['topic','subject']].values.tolist())
    
    
        st.markdown("###### 🤖Ask Keeper")
        with st.container():
            st.markdown("""<div style='border:1px solid #ccc; border-radius:6px; padding:6px; background-color:#f9f9f9;'>
                <p style='font-size:14px; margin-bottom:4px;'>Need help interpreting the insights? Keeper is here for you.</p></div>""", unsafe_allow_html=True)
            user_question = st.text_input(label=" ", placeholder="Ask Keeper a quick question...", label_visibility="collapsed")
            col_q1, col_q2 = st.columns([6, 1])
            with col_q2:
                if st.button("Ask", use_container_width=True):
                    if user_question.strip():
                        st.success("✅ Keeper has noted your question!")
                    else:
                        st.warning("⚠️ Please type your question first.")
    
    # --- RIGHT: Visual Insights (Layered Order) ---
    with right_col:
        st.markdown("##### 💡Visual Insights")
    
        df_viz = df[df['FOM_str'] <= selected_fom].copy()
        df_viz['cumulative_total_tickets'] = df_viz['total_tickets'].cumsum()
        df_status = df_viz[['FOM'] + [c for c in df.columns if c.startswith('status_')]].melt(id_vars='FOM', var_name='status', value_name='count')
    
        df_support_tickets_raw = df_support_tickets
        selected_fom_dt = pd.to_datetime(selected_fom)
        start_fom_dt = selected_fom_dt - relativedelta(months=12)
        df_tickets_viz_raw = df_support_tickets_raw[(pd.to_datetime(df_support_tickets_raw['FOM']) >= start_fom_dt) & (pd.to_datetime(df_support_tickets_raw['FOM']) <= selected_fom_dt)]
    
       # Layer 1
        col_layer1a, col_layer1b = st.columns(2)
        with col_layer1a:
            #st.markdown("###### 📈 Support Ticket Trend")
            st.markdown("<h6 style='text-align: center; font-size: 10px; margin-bottom: 6px;'>📈 Support Ticket Trend </h6>", unsafe_allow_html=True)
    
            st.plotly_chart(px.line(df_viz, x='FOM', y='cumulative_total_tickets').update_layout(height=220, margin=dict(l=5, r=5, t=30, b=10)), use_container_width=True)
         
        with col_layer1b:
            #st.markdown("###### 📈 Ticket Status Distribution")
            st.markdown("<h6 style='text-align: center; font-size: 10px; margin-bottom: 6px;'>📈 Ticket Status Distribution </h6>", unsafe_allow_html=True)
            fig2 = px.bar(df_status, x='FOM', y='count', color='status', barmode='stack')
            fig2.update_layout(
                legend=dict(orientation='h', y=-0.3, font=dict(size=8)),
                height=200,
                margin=dict(l=5, r=5, t=30, b=10)
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        # Layer 2
        col_layer2a, col_layer2b, col_layer2c = st.columns(3)
        with col_layer2a:
             #st.markdown("###### 📈 Support Health Distribution")
            st.markdown("<h6 style='text-align: center; font-size: 12px; margin-bottom: 6px;'>📈 Support Health Distribution </h6>", unsafe_allow_html=True)
            latest_row = df_viz[df_viz['FOM_str'] == selected_fom].iloc[0]
            fig3 = px.pie(
                names=['Healthy', 'Normal', 'Risky'],
                values=[latest_row['label_count_healthy'], latest_row['label_count_normal'], latest_row['label_count_risky']],
            )
            fig3.update_layout(height=160, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig3, use_container_width=True) 
        
        with col_layer2b:
            st.markdown("<h6 style='text-align: center; font-size: 12px; margin-bottom: 6px;'>📈 Support Score (Last 12 Months)</h6>", unsafe_allow_html=True)
        
            # Filter only last 12 months for support score trend
            selected_fom_dt = pd.to_datetime(selected_fom)
            start_score_dt = selected_fom_dt - relativedelta(months=12)
            df_score_trend = df[(df['FOM'] >= start_score_dt) & (df['FOM'] <= selected_fom_dt)]
        
            fig_score = px.line(
                df_score_trend,
                x='FOM',
                y=['support_score_p50', 'support_score_p90', 'support_score_p100']
            )
        
            fig_score.update_layout(
                legend=dict(orientation='h', y=-0.3, font=dict(size=6)),
                height=260,
                margin=dict(l=10, r=10, t=30, b=10)
            )
        
            st.plotly_chart(fig_score, use_container_width=True)
    
       
      
        with col_layer2c:        
            #st.markdown("###### 🔍 Ticket Subjects")
            st.markdown("<h6 style='text-align: center; font-size: 12px; margin-bottom: 6px;'>🔍 Ticket Subjects </h6>", unsafe_allow_html=True)
            subject_cols = [col for col in df.columns if col.startswith("subject_issue_")]
            filtered_df = df[df['FOM_str'] == selected_fom]
            if not filtered_df.empty:
                row_issues = filtered_df.iloc[0]
                issue_counts = [int(row_issues[f"subject_issue_{i}"]) for i in range(1, 5)]
                if sum(issue_counts) > 0:
                    issue_df = pd.DataFrame({"Issue": [f"Issue {i}" for i in range(1, 5)], "Count": issue_counts})
                    st.plotly_chart(px.treemap(issue_df, path=[px.Constant("All Issues"), "Issue"], values="Count").update_layout(height=140, margin=dict(l=10, r=10, t=30, b=10)), use_container_width=True)
               
    
        st.markdown("---")
        # Layer 3
        col_layer3a, col_layer3b = st.columns(2)
        with col_layer3a:
            #st.markdown("###### 📊 Response Time ")
            st.markdown("<h6 style='text-align: center; font-size: 12px; margin-bottom: 6px;'>📊 Response Time </h6>", unsafe_allow_html=True)
    
            st.plotly_chart(px.box(df_tickets_viz_raw, x='FOM', y='response_time').update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10)), use_container_width=True)
        with col_layer3b:
            #st.markdown("###### 📊 Resolution Time ")
            st.markdown("<h6 style='text-align: center; font-size: 12px; margin-bottom: 6px;'>📊 Resolution Time  </h6>", unsafe_allow_html=True)
    
            st.plotly_chart(px.box(df_tickets_viz_raw.dropna(subset=['resolution_time']), x='FOM', y='resolution_time').update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10)), use_container_width=True)

if __name__ == "__main__":
    show()

    
