import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
from navigation import show_navigation


st.set_page_config(page_title="Pulse", layout="wide")
hide_sidebar()
def show():
    st.title("🧩 Keeper Pulse")

    st.subheader("Health Stages & Signals")

    st.markdown(
    """
    **Keeper Pulse** classifies account health into four strategic stages:  
    **Expansion**, **Renewal**, **Adoption** and **Risky**.  
    This view surfaces key signals to support proactive decision-making and portfolio management.    
    """
    )
    
    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            show_navigation("🧩 Keeper Pulse")
    
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
            fom_list = df_score_summary['FOM_str'].unique()[::-1]
            selected_fom = st.selectbox("Selected Date", fom_list, index=list(fom_list).index("2025-04"))
            
            #selected_fom = st.selectbox("Selected Date", df_score_summary['FOM_str'].unique()[::-1], label_visibility="collapsed")
    selected_fom_dt = pd.to_datetime(selected_fom)
    row = df_score_summary[df_score_summary['FOM_str'] == selected_fom].iloc[0]


    
    
    # --- Metric Card Renderer ---
    def metric_card(title, value, delta=None):
        delta_str = ""
        if delta is not None:
            arrow = "🔺+" if delta >= 0 else "🔻-"
            delta_str = f"<p style=\"color:gray; font-size: 8px; margin:0\">{arrow} {abs(delta):.1f}% from last period</p>"
        return f"""
        <div style="border:1px solid #e0e0e0; padding:4px; border-radius:6px; background-color:#f9f9f9; width: 100%; margin-bottom:2px">
            <h8 style="margin-bottom:0">{title}</h8>
            <p style="font-size: 18px; font-weight:bold; margin:0">{value}</p>
            {delta_str}
        </div>
        """
    
    # --- Page Header --- 
    # --- Display Cards ---
    # Top row = classification counts
    top_keys = ['adoption', 'expansion', 'renewal', 'risky']
    top_cols = st.columns(4)
    for i, key in enumerate(top_keys):
        val = int(row[key])
        delta = row[f"{key}_mom_pct"]
        top_cols[i].markdown(metric_card(score_metrics[key], val, delta), unsafe_allow_html=True)
    
    # Bottom row = ACV per classification (no MoM shown)
    bottom_keys = ['adoption_acv', 'expansion_acv', 'renewal_acv', 'risky_acv']
    bottom_cols = st.columns(4)
    for i, key in enumerate(bottom_keys):
        val = f"${row[key]:,.0f}"
        bottom_cols[i].markdown(metric_card(score_metrics[key], val), unsafe_allow_html=True)
    
    #st.markdown("---")
    
    ...
    # --- Prepare df_fom earlier for both columns ---
    df_fom = df_score_c[df_score_c['FOM_str'] == selected_fom].copy()
    

    # --- New Layout: Left with fig1, chatbot & table | Right with all other figs ---
    left_col, right_col = st.columns([1.6, 1.4])
    
    with left_col:
        # --- FIGURE 1: Stage Distribution (left) ---
        #st.markdown("###### 📊 Stage Distribution")
        stage_count_data = pd.DataFrame({
            'stage': [ 'Expansion', 'Renewal', 'Adoption','Risky'],
            'count': [ row['expansion'], row['renewal'],row['adoption'], row['risky']]
        })
        fig1 = px.bar(stage_count_data, x='stage', y='count', color='stage', title='📊 Stage Distribution',
                      color_discrete_map={"Risky": c_risky, "Adoption": c_adoption, "Expansion":c_expansion, "Renewal": c_renew})
        fig1.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            xaxis=dict(showgrid=False, tickfont=dict(size=18)),
            yaxis=dict(showgrid=False, tickfont=dict(size=12)),
            title_font=dict(size=18)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
        # --- Chat + Alert System (left) ---
        
        
        chat_col1, chat_col2 = st.columns(2)
        
        with chat_col1:
            st.markdown("##### 🚨 Alert System for Emerging Risks")
            with st.container(border=True):
                st.markdown("""
                - **5 enterprise customers** are at high churn risk due to declining product usage. **Immediate action recommended.**
                - Your **top 10 highest-value customers** are engaging less — consider reaching out.
                """)
        
        with chat_col2:
            #st.markdown("##### 🤖 Ask Keeper")
            default_q = "Why Pulse of company 1 is risky?"
            user_input = st.text_area("##### 🤖 Ask Keeper", value=default_q, height=100)
            if st.button("Ask Keeper"):
                st.info("""
        ❌ Declining product usage (↓40% in last 2 months)  
        ❌ Unresolved support tickets (3 high-priority issues open for 30+ days)  
        ❌ Low CSM engagement (No touchpoints in last 60 days)  
        👉 **Suggested Action**: Schedule a recovery call & offer an incentive to stay engaged.
                """)
    
        
        # --- Table (left) ---
        st.markdown("#### 📋 Account Breakdown")
        df_table = df_fom[['account_name', 'activity_score_label', 'support_score_label', 'usage_score_label', 'score_final', 'stage']].copy()
        df_table.rename(columns={
            'account_name': 'Account',
            'activity_score_label': 'CSM activity',
            'support_score_label': 'Support',
            'usage_score_label': 'Usage',
            'score_final': 'Risk Score',
            'stage': 'Pulse'
        }, inplace=True)
        df_table['Risk Score'] = (df_table['Risk Score'] * 100).round(0).astype(int)
        
        pulse_options = df_table['Pulse'].unique().tolist()
        selected_pulses = st.multiselect("Filter by Pulse", options=pulse_options, default=pulse_options)
        df_table = df_table[df_table['Pulse'].isin(selected_pulses)]
        
        color_map = {
            'risky': c_risky,
            'adoption': c_adoption,
            'expansion': c_expansion,
            'renewal': c_renew
        }
        
        # Replace pulse text with empty string to show only colored cell
        df_table['Pulse_display'] = ''
        df_table_display = df_table.drop(columns=['Pulse']).rename(columns={'Pulse_display': 'Pulse'})
        df_table_display['Pulse'] = df_table['Pulse']  # Keep original values for styling reference
        
        # Apply styling
        styled_df = df_table_display.style
        styled_df = styled_df.set_table_styles(
            [
                {'selector': 'th', 'props': [('text-align', 'center')]},
                {'selector': 'td', 'props': [('text-align', 'center')]},
                {'selector': 'td', 'props': [('vertical-align', 'middle')]},
            ], overwrite=False
        )
        styled_df = styled_df.set_properties(**{'text-align': 'center'})
        styled_df = styled_df.applymap(lambda val: f'background-color: {color_map.get(val, "#ffffff")}; color: {color_map.get(val, "#ffffff")}', subset=['Pulse'])
        
        st.dataframe(styled_df, use_container_width=True, height=500)
        
    
    
    with right_col:
        # --- First Row: FIG 1 and FIG 6 ---
        fig_row1_col1, fig_row1_col2 = st.columns(2)
    
        with fig_row1_col1:
            st.markdown("#### ⏳ Stage Trends: Contracts Over Time")
            df_score_c_trimmed = df_score[df_score['FOM'] <= selected_fom_dt].copy()
            df_score_c_melted = df_score_c_trimmed.melt(id_vars='FOM_str', value_vars=['adoption', 'expansion', 'renewal', 'risky'],
                                                        var_name='stage', value_name='count')
    
            fig2 = px.bar(df_score_c_melted, x='FOM_str', y='count', color='stage', barmode='stack',
                          title='Number of Contracts Over Time by Stage',
                          color_discrete_map={"risky": c_risky, "adoption": c_adoption, "expansion": c_expansion, "renewal": c_renew})
            fig2.update_layout(plot_bgcolor='white', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=1500)
            st.plotly_chart(fig2, use_container_width=True)
    
    
        with fig_row1_col2:
            st.markdown("#### 🗺️ Industry for Risky Customers")
            risky_fom = df_fom[df_fom['stage'] == 'risky']
            risky_fom['contract_count'] = 1
            fig3 = px.treemap(risky_fom, path=['industry'], values='contract_count',
                              title='Industry Composition (Risky)',
                              color_discrete_sequence=[c_risky])
            st.plotly_chart(fig3, use_container_width=True)
    
        # --- Second Row: FIG 2 and FIG 5 ---
        fig_row2_col1, fig_row2_col2 = st.columns(2)
    
        with fig_row2_col1:
            st.markdown("#### 📈 Contracts by MOC")
            fig4 = px.histogram(df_fom, x='MOC', color='stage', barmode='stack',
                                title='Number of Contracts by MOC',
                                color_discrete_map={"risky": c_risky, "adoption": c_adoption, "expansion":c_expansion, "renewal": c_renew})
            fig4.update_layout(plot_bgcolor='white', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), width=1500)
            st.plotly_chart(fig4, use_container_width=True)
    
        with fig_row2_col2:
            st.markdown("#### 🧩 Business Size Distribution for Risky Customers")
            risky_fom = df_fom[df_fom['stage'] == 'risky']
            fig5 = px.pie(risky_fom, names='business_size', title='Business Size Breakdown (Risky)',
                          color_discrete_sequence=[c_risky])
            st.plotly_chart(fig5, use_container_width=True)
    
    st.markdown("---")
    
if __name__ == "__main__":
    show()
