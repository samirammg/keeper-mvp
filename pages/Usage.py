import streamlit as st
import pandas as pd
import plotly.express as px
from dateutil.relativedelta import relativedelta
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar

st.set_page_config(page_title="Usage", layout="wide")
hide_sidebar()

def show():
    st.title("📊 Product Usage & Behavior")
    st.subheader("Product Adoption Challenges & Retention Impact")
    st.markdown(
        """
        Analyzes product usage trends to identify which features drive engagement and where users struggle.  
        Surfaces actionable recommendations for the product team and quantifies how usage patterns  
        influence customer churn, retention, and expansion opportunities.
        """
    )


    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            menu = st.selectbox("", [
                "↳ 📊 Stay on Product Usage",
                "🩺 Team Pulse",
                "↳  📌 CSM Activity",
                "↳  💬 Support Trends",
                "📘 Customer Pulse",
                "🧩 Keeper Pulse",
                "💓 Growth Pulse",
                "📈 Vision Pulse",
                "↳  🧭 Strategy",
                "🚀 Keeper Agents",
                "🗄️ Keeper Data"

            ], label_visibility="collapsed")

    if menu == "↳ 📊 Stay on Product Usage":
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
    elif menu == "↳  💬 Support Trends":
        switch_page("Support")
    elif menu == "📈 Vision Pulse":
        switch_page("VisionPulse")
    elif menu == "↳  🧭 Strategy":
        switch_page("Strategy")
    elif menu == "🚀 Keeper Agents":
        switch_page("agent")
    elif menu == "🗄️ Keeper Data":
        switch_page("onbording")
    
    
    # --- Data Loaders ---
    @st.cache_data
    def load_summary_data():
        df = pd.read_csv("data/5_usage_dashboard.csv")
        df["FOM"] = pd.to_datetime(df["FOM"])
        df["FOM_str"] = df["FOM"].dt.strftime('%Y-%m')
        return df.sort_values("FOM")
    
    @st.cache_data
    def load_raw_usage_data():
        df = pd.read_csv("data/0_sim_usage_monthly_features.csv")
        df["FOM"] = pd.to_datetime(df["FOM"])
        df["FOM_str"] = df["FOM"].dt.strftime('%Y-%m')
        return df
    
    @st.cache_data
    def load_insight_data():
        return pd.read_csv("data/5_usage_insight_dashboard.csv")
    
    # --- Load Data ---
    df = load_summary_data().fillna(0)
    df_raw = load_raw_usage_data()
    df_insights = load_insight_data()
    
    # --- Define Metrics ---
    metrics = {
        "users": "👥Total Users",
        "active_users": "🟢Active Users",
        "feature_adoption_rate": "🚀Feature Adoption",
        "time_spent_per_session": "⏱️Time per Session",
        "retention_rate": "🔁Retention Rate",
        "feature_stickiness": "📌Feature Stickiness",
        "recency": "⏳Recency",
        "account": "🏢Total Accounts"
    }
    
    # --- Calculate MoM % ---
    df_summary = df[['FOM_str'] + list(metrics.keys())].copy().sort_values("FOM_str")
    for col in metrics:
        df_summary[f"{col}_mom_pct"] = df_summary[col].pct_change() * 100
    
    # --- FOM Selection ---
    with st.container():
        filter_col = st.columns([4, 1])[1]
        with filter_col:
            #selected_fom = st.selectbox("", df_summary["FOM_str"].unique()[::-1], label_visibility="collapsed")
            selected_fom = st.selectbox(
                "Selected Date",
                df_summary['FOM_str'].unique()[::-1],
                index=list(df_summary['FOM_str'].unique()[::-1]).index("2025-04")
                )

    row = df_summary[df_summary["FOM_str"] == selected_fom].iloc[0]
    
    # --- Date Calculations ---
    selected_fom_dt = pd.to_datetime(selected_fom)
    start_fom_dt = selected_fom_dt - relativedelta(months=12)
    df_viz = df[df["FOM"] <= selected_fom_dt].copy()
    df_viz_12mo = df[(df["FOM"] >= start_fom_dt) & (df["FOM"] <= selected_fom_dt)].copy()
    raw_selected = df_raw[df_raw["FOM_str"] == selected_fom]
    
    # --- Dashboard Header ---
    
    #st.markdown("---")
    st.markdown("##### 📏Key Usage Metrics")
    
    # --- KPI Cards ---
    top_metrics = ["users", "active_users", "retention_rate", "feature_adoption_rate"]
    bottom_metrics = ["account", "time_spent_per_session", "feature_stickiness", "recency"]
    
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
    
    cols_top = st.columns(len(top_metrics))
    for idx, key in enumerate(top_metrics):
        val = f"{row[key]:.1f}" if "rate" in key or "session" in key else int(row[key])
        cols_top[idx].markdown(metric_card(metrics[key], val, row[f"{key}_mom_pct"]), unsafe_allow_html=True)
    
    cols_bottom = st.columns(len(bottom_metrics))
    for idx, key in enumerate(bottom_metrics):
        val = f"{row[key]:.1f}" if key != "account" else int(row[key])
        cols_bottom[idx].markdown(metric_card(metrics[key], val, row[f"{key}_mom_pct"]), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- Main Layout ---
    left_col, right_col = st.columns([1, 1])
    
    # --- LEFT: Keeper + Insights ---
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
    
        st.markdown("###### 🤖 Ask Keeper")
        with st.container():
            st.markdown("""<div style='border:1px solid #ccc; border-radius:6px; padding:6px; background-color:#f9f9f9;'>
                <p style='font-size:14px; margin-bottom:4px;'>Need help interpreting the insights? Keeper is here for you.</p></div>""", unsafe_allow_html=True)
            user_question = st.text_input(label=" ", placeholder="Ask Keeper a quick question...", label_visibility="collapsed")
            if st.button("Ask", use_container_width=True):
                if user_question.strip():
                    st.success("✅ Keeper has noted your question!")
                else:
                    st.warning("⚠️ Please type your question first.")
    
    # --- RIGHT: Visual Insights ---
    with right_col:
        st.markdown("##### 💡Visual Insights")
    
        # Layer 1
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h6 style='text-align: center;'>📈 User Activity Over Time</h6>", unsafe_allow_html=True)
            fig1 = px.line(df_viz, x="FOM", y=["users", "active_users"], markers=True)
            fig1.update_layout(height=250, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig1, use_container_width=True)
    
        with col2:
            st.markdown("<h6 style='text-align: center;'>📈 Usage Score Trend (P50, P90, P100)</h6>", unsafe_allow_html=True)
            fig2 = px.line(df_viz_12mo, x="FOM", y=["usage_score_p50", "usage_score_p90", "usage_score_p100"])
            fig2.update_layout(height=250, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig2, use_container_width=True)
    
        # Layer 2
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<h6 style='text-align: center;'>📊 Usage Label Distribution</h6>", unsafe_allow_html=True)
            selected_row = df[df["FOM_str"] == selected_fom].iloc[0]
            fig3 = px.pie(
                names=["Healthy", "Normal", "Risky"],
                values=[selected_row["label_pct_healthy"], selected_row["label_pct_normal"], selected_row["label_pct_risky"]]
            )
            fig3.update_layout(height=220, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig3, use_container_width=True)
    
        with col4:
            st.markdown("<h6 style='text-align: center;'>🌳 Feature Adoption TreeMap</h6>", unsafe_allow_html=True)
            feature_counts = raw_selected["feature_adoption"].astype(str).value_counts().reset_index()
            feature_counts.columns = ["feature", "count"]
            fig4 = px.treemap(feature_counts, path=[px.Constant("All Features"), "feature"], values="count")
            fig4.update_layout(height=220, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig4, use_container_width=True)
    
        # Layer 3
            # --- Layer 3: Box plots over last 12 months ---
        col5, col6 = st.columns(2)
    
    # Filter 12-month window
        raw_12mo = df_raw[(df_raw["FOM"] >= start_fom_dt) & (df_raw["FOM"] <= selected_fom_dt)]
        
        with col5:
            st.markdown("<h6 style='text-align: center;'>📊 Frequency Distribution (Last 12 Months)</h6>", unsafe_allow_html=True)
            fig5 = px.box(raw_12mo, x="FOM_str", y="usage_frequency", points="outliers")
            fig5.update_layout(height=240, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig5, use_container_width=True)
        
        with col6:
            st.markdown("<h6 style='text-align: center;'>📊 Recency Distribution (Last 12 Months)</h6>", unsafe_allow_html=True)
            fig6 = px.box(raw_12mo, x="FOM_str", y="usage_recency_d", points="outliers")
            fig6.update_layout(height=240, margin=dict(t=30, l=10, r=10, b=10))
            st.plotly_chart(fig6, use_container_width=True)
    
if __name__ == "__main__":
    show()
