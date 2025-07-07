import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
from navigation import show_navigation

    

st.set_page_config(page_title="Activity", layout="wide")
hide_sidebar()

def show():
    st.title("📌 CSM Activity & Insights")

    st.subheader("Engagement Trends, Best Practices & Impact")
    st.markdown(
    """
    **CSM Activity & Insights** highlights engagement patterns, time spent, and key interaction types.  
    AI insights help identify best practices, evaluate interventions, and measure impact on retention and expansion.  
    Visual trends and strategy tips support better team focus and execution.
    """
    )


    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            show_navigation( "↳  📌 CSM Activity")
    
    @st.cache_data
    def load_activity_data():
        df = pd.read_csv("data/5_activity_dashboard.csv")
        if 'FOM' not in df.columns:
            df['FOM'] = pd.date_range(start="2020-01-01", periods=len(df), freq='MS')
        if 'FOM_str' not in df.columns:
            df['FOM_str'] = pd.to_datetime(df['FOM']).dt.to_period('M').astype(str)
        df['FOM'] = pd.to_datetime(df['FOM_str'])
        return df.sort_values('FOM_str')
    
    @st.cache_data
    def load_insight_data():
        return pd.read_csv("data/5_activity_insight_dashboard.csv")
    
    @st.cache_data
    def load_activity_moc():
        df = pd.read_csv("data/0_sim_act_monthly_features_agg.csv")
        if 'FOM' not in df.columns:
            df['FOM'] = pd.date_range(start="2020-01-01", periods=len(df), freq='MS')
        if 'FOM_str' not in df.columns:
            df['FOM_str'] = pd.to_datetime(df['FOM']).dt.to_period('M').astype(str)
        return df
    
    @st.cache_data
    def load_activity_monthly():
        df = pd.read_csv("data/0_sim_activity_monthly_features.csv")
        if 'FOM' not in df.columns:
            df['FOM'] = pd.date_range(start="2020-01-01", periods=len(df), freq='MS')
        if 'FOM_str' not in df.columns:
            df['FOM_str'] = pd.to_datetime(df['FOM']).dt.to_period('M').astype(str)
        return df
    
    df = load_activity_data().fillna(0)
    df_insights = load_insight_data()
    df_moc = load_activity_moc()
    df_activity_m = load_activity_monthly()
    
    
    all_metrics = {
        "total_activities_sum": "📊 Total CSM Activities",
        "total_duration_sum": "⏱️ Total Time with Customers (hr)",
        "total_activities_median": "📈 Average CSM Activities",
        "average_duration_median": "🕒 Avg. Time per Customer (min)",
        "high_priority_pct": "🚨 Critical Interactions",
        "cancel_pct": "❌ Cancelled Activities",
        "not_attend_pct": "🚫 No Shows",
        "top_3_topics": "📌 Main Topics"
    }
    
    metrics = {k: v for k, v in all_metrics.items() if k in df.columns}
    if 'total_duration_sum' in df.columns:
        df['total_duration_sum'] = df['total_duration_sum'] / 60
    
    df_summary = df[['FOM_str'] + list(metrics.keys())].copy()
    df_summary = df_summary.sort_values('FOM_str')
    for col in metrics:
        if col != 'top_3_topics':
            df_summary[f"{col}_pct_change"] = df_summary[col].pct_change() * 100
        else:
            df_summary[f"{col}_pct_change"] = 0
    
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
    
    selected_fom_dt = pd.to_datetime(selected_fom)
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
    
    st.markdown("##### 🔍 Key Activity Metrics")
    
    # Split metrics into two rows of 4 columns
    first_row_keys = ["total_activities_sum", "total_duration_sum", "total_activities_median", "average_duration_median"]
    second_row_keys = ["high_priority_pct", "cancel_pct", "not_attend_pct", "top_3_topics"]
    
    # First row
    cols_top = st.columns(4)
    for idx, key in enumerate(first_row_keys):
        val = f"{row[key]:.0f}%" if 'rate' in key else int(row[key])
        cols_top[idx].markdown(metric_card(metrics[key], val, row[f"{key}_pct_change"]), unsafe_allow_html=True)
    
    # Second row
    cols_bottom = st.columns(4)
    for idx, key in enumerate(second_row_keys):
        if "topics" in key:
            val = f"{row[key]}  "
        else:
            val = f"{row[key]:.0f}%"
        cols_bottom[idx].markdown(metric_card(metrics[key], val, row[f"{key}_pct_change"]), unsafe_allow_html=True)
    
    st.markdown("---")
    
    
    # --- Main Two-Column Layout ---
    main_left, main_right = st.columns([1, 1.5])
    
    # --- LEFT: Generative Insights + Keeper ---
    with main_left:
        st.markdown("##### ✨Generative Insights")
        color_map = {"Red": "🔴", "Yellow": "🟡", "Green": "🟢"}
        def render_insight_box(title, items, use_icons=False):
            content = f"""
            <div style='border:1px solid #ddd; border-radius:8px; padding:10px; background-color:#f9f9f9; margin-bottom:12px;'>
                <h5 style='margin-bottom:8px; font-size:16px;'>{title}</h5>
                <ul style='padding-left:14px; font-size:10px; line-height:1; margin:0;'>
            """
            for topic, subject in items:
                bullet = color_map.get(topic, "") if use_icons else "•"
                content += f"<li style='list-style-type:none'>{bullet} {subject}</li>"
            content += "</ul></div>"
            st.markdown(content, unsafe_allow_html=True)
    
        insight_dict = {s: df_insights[df_insights['section'] == s] for s in df_insights['section'].unique()}
        render_insight_box("🧠 AI-Generated Key Insights for Executives", insight_dict.get("AI-Generated Key Insights for Executives", pd.DataFrame())[ ['topic','subject'] ].values.tolist(), use_icons=True)
        render_insight_box("⚡ AI-Driven Strategy Recommendations", insight_dict.get("AI-Driven Strategy Recommendations", pd.DataFrame())[ ['topic','subject'] ].values.tolist())
        render_insight_box("⚠️ Risk Alert System", insight_dict.get("Risk Alert System", pd.DataFrame())[ ['topic','subject'] ].values.tolist())
        render_insight_box("🚀 Action Recommend", insight_dict.get("Action Recommend", pd.DataFrame())[ ['topic','subject'] ].values.tolist())
    
        st.markdown("###### 🤖Ask Keeper")
        with st.container():
            st.markdown("""<div style='border:1px solid #ccc; border-radius:6px; padding:6px; background-color:#f9f9f9;'>
                <p style='font-size:14px; margin-bottom:4px;'>Need help interpreting the insights? Keeper is here for you.</p></div>""", unsafe_allow_html=True)
            user_question = st.text_input(label=" ", placeholder="Ask Keeper a quick question...", label_visibility="collapsed")
            col_q1, col_q2 = st.columns([6, 1])
            with col_q2:
                st.button("Ask", use_container_width=True)
                    
    
    # --- RIGHT: Visual Insights ---
    with main_right:
        st.markdown("##### ✨Visual Insights")
        col1, col2 = st.columns(2)
    
        with col1:
            fig1_df = df[df['FOM'] <= selected_fom_dt].melt(
                id_vars='FOM_str',
                value_vars=['meeting_count_sum', 'email_count_sum', 'postal_count_sum'],
                var_name='Activity Type', value_name='Count'
            ).replace({
                'meeting_count_sum': 'meeting',
                'email_count_sum': 'email',
                'postal_count_sum': 'postal'
            })
            fig1 = px.bar(fig1_df, x='FOM_str', y='Count', color='Activity Type',
                          title='CSM Activities', barmode='stack', height=250)
            fig1.update_layout(legend_orientation='h', legend_y=-0.2)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig7_df = df_moc.copy()
            fig7_df['FOM'] = pd.to_datetime(fig7_df['FOM'])
            fig7_df['FOM_str'] = fig7_df['FOM'].dt.to_period('M').astype(str)
            fig7_filtered = fig7_df[fig7_df['FOM_str'] == selected_fom].copy()
            all_mocs = pd.DataFrame({'MOC': list(range(1, 13))})
            fig7_complete = all_mocs.merge(fig7_filtered, on='MOC', how='left')
            fig7_complete['FOM_str'] = fig7_complete['FOM_str'].fillna(selected_fom)
            for col in ['attend_count', 'not_attend_count', 'cancel_count']:
                if col not in fig7_complete.columns:
                    fig7_complete[col] = 0
                fig7_complete[col] = fig7_complete[col].fillna(0)
            melted_fig7 = fig7_complete.melt(id_vars='MOC', value_vars=['attend_count', 'not_attend_count', 'cancel_count'],
                                             var_name='Status', value_name='Count')
            fig7 = px.bar(melted_fig7, x='MOC', y='Count', color='Status', barmode='stack',
                          title='Attendance Status by Month of Contract (MOC)', height=250)
            fig7.update_layout(xaxis=dict(tickmode='array', tickvals=list(range(1, 13))),
                               legend_orientation='h', legend_y=-0.2)
            st.plotly_chart(fig7, use_container_width=True)
        
        # --- Layer 2: Fig 3 and Fig 6 ---
        col3, col4 = st.columns(2)
        
        with col3:
            months_back = 12
            start_date = selected_fom_dt - pd.DateOffset(months=months_back)
            fig3_df = df[(df['FOM'] >= start_date) & (df['FOM'] <= selected_fom_dt)].copy()
            fig3_long = fig3_df.melt(id_vars='FOM_str',
                                     value_vars=['activity_score_p50', 'activity_score_p90', 'activity_score_p100'],
                                     var_name='Percentile', value_name='Score')
            fig3 = px.line(fig3_long, x='FOM_str', y='Score', color='Percentile',
                          title='Activity Score Percentiles Trend', markers=True, height=250)
            fig3.update_layout(legend_orientation='h', legend_y=-0.2)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            fig6_df = df_moc.copy()
            fig6_df['FOM'] = pd.to_datetime(fig6_df['FOM'])
            fig6_df['FOM_str'] = fig6_df['FOM'].dt.to_period('M').astype(str)
            fig6_filtered = fig6_df[(fig6_df['FOM_str'] == selected_fom) & (fig6_df['MOC'].between(1, 12))].copy()
            all_mocs = pd.DataFrame({'MOC': list(range(1, 13))})
            fig6_complete = all_mocs.merge(fig6_filtered, on='MOC', how='left')
            fig, ax = plt.subplots(figsize=(8, 3))
            sns.boxplot(x='MOC', y='total_duration', data=fig6_complete, ax=ax)
            plt.xlabel('Month of Contract (MOC)')
            plt.ylabel('Interaction Duration (min)')
            plt.title('Interaction Duration by MOC')
            plt.grid(False)
            plt.tight_layout()
            st.pyplot(plt.gcf())
        
        # --- Layer 3: Fig 4, Fig 5, Fig 2 ---
        col5, col6, col7 = st.columns(3)
        
        with col5:
            fig4_df = df[df['FOM_str'] == selected_fom].copy()
            label_cols = ['label_pct_healthy', 'label_pct_normal', 'label_pct_risky']
            if all(col in fig4_df.columns for col in label_cols):
                fig4_data = pd.DataFrame({
                    "Label": ['Healthy', 'Normal', 'Risky'],
                    "Value": [fig4_df['label_pct_healthy'].values[0],
                               fig4_df['label_pct_normal'].values[0],
                               fig4_df['label_pct_risky'].values[0]]
                }).dropna()
                fig4 = px.pie(fig4_data, names='Label', values='Value', title='Activity Score Labels', height=300,
                              color='Label',
                              color_discrete_map={"Risky": "red", "Normal": "yellow", "Healthy": "green"})
                fig4.update_traces(textinfo='label+percent',textposition='inside',insidetextorientation='auto')
                fig4.update_layout(legend_orientation='h', legend_y=-0.2,showlegend=False)
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.warning("skipped: missing activity score label columns.")
      
        with col6:
            fig5_df = df_activity_m[df_activity_m['FOM_str'] == selected_fom]
            fig5 = px.treemap(fig5_df, path=['activity_topic'], values='duration (minutes)', height=200,
                              title='Activity Topics ')
            fig5.update_layout(margin=dict(t=15, l=5, r=5, b=5))
            st.plotly_chart(fig5, use_container_width=True)
        
        with col7:
            fig2_df = df_activity_m[df_activity_m['FOM_str'] == selected_fom].dropna(subset=['sentiment_class'])
            fig2 = px.pie(fig2_df, names='sentiment_class', title='Interaction Sentiment ', height=300,
                          color='sentiment_class',
                          color_discrete_map={"negative": "red", "neutral": "yellow", "positive": "green"})
            fig2.update_traces(textinfo='label+percent',textposition='inside',insidetextorientation='auto')
            
            fig2.update_layout(legend_orientation='h', legend_y=-0.2,showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

if __name__ == "__main__":
    show()
