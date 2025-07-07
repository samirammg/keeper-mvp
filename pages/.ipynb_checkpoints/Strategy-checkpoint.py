import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar


st.set_page_config(page_title="Strategy", layout="wide")
hide_sidebar()

def show(): 
    st.title("🎯 Dynamic Strategic Planning (Post-Sales)")
    st.subheader("Project Revenue, Simulate Risk & Optimize Post-Sale Growth")

    st.markdown(
        """
        Empowers executive leaders (CEO, CRO, CCO, etc.) to project revenue, simulate risk, and guide growth strategy.  
        Provides a high-level view of customer trends, revenue forecasts, and churn impact simulations.  
        Enables ARR risk assessment, upsell modeling, and identification of key levers for post-sale expansion.  
        Includes scenario planning, alert systems, and benchmarking to support data-driven strategic decisions.
        """
    )



    with st.container():
        col1, col3 = st.columns([4, 1])
        
        menu = col3.selectbox(
            "",
            [
                "↳  🧭 Stay on Strategy",
                "📈 Vision Pulse",
                "📘 Customer Pulse",
                "🧩 Keeper Pulse",
                "💓 Growth Pulse",
                "🩺 Team Pulse",
                "↳  📌 CSM Activity",
                "↳  💬 Support Trends",
                "↳  📊 Product Usage",
                "🚀 Keeper Agents",
                "🗄️ Keeper Data"
                
            ],
            label_visibility="collapsed"
        )

        if menu == "↳  🧭 Stay on Strategy":
            pass
        elif menu == "📘 Customer Pulse":
            switch_page("Journey")
        elif menu == "💓 Growth Pulse":
            switch_page("GrowthPulse")
        elif menu == "🩺 Team Pulse":
            switch_page("TeamPulse")
        elif menu == "↳  📌 CSM Activity":
            switch_page("Activity")
        elif menu == "↳  💬 Support Trends":
            switch_page("Support")
        elif menu == "↳  📊 Product Usage":
            switch_page("Usage")
        elif menu == "📈 Vision Pulse":
            switch_page("VisionPulse")
        elif menu == "🚀 Keeper Agents":
            switch_page("agent")
        elif menu == "🗄️ Keeper Data":
            switch_page("onbording")

        
        
    
    # --- Load data ---
    df = pd.read_csv("5-trend_simulation_dashboard.csv")
    # Round all rate columns to 4 decimal places
    rate_cols = [col for col in df.columns if 'Rate' in col or 'rate' in col]
    df[rate_cols] = df[rate_cols].round(2)
    df['FOM'] = pd.to_datetime(df['FOM'])
    
    # --- Simulation projection data ---
    df_sim = df.copy()
    df_sim['Month'] = df_sim['FOM']
    
    # --- Projection functions ---
    def calculate_6_month_projection(start_month):
        start_month = pd.to_datetime(start_month)
        row = df_sim[df_sim['Month'] == start_month]
        if row.empty:
            return pd.DataFrame()
        row = row.iloc[0]
    
        active = row.get('Active Accounts', 0)
        avg_new_rate = row.get('avg_new_rate', 0)
        avg_new_acv = row.get('avg_new_acv', 0)
    
        records = []
        cum_churn = cum_new = cum_renew = 0
        cum_churn_acv = cum_new_acv = cum_renewal_acv = 0
    
        for i in range(1, 7):
            ch = row.get(f'ch{i}', 0)
            ex = row.get(f'ex{i}', 0)
            re = row.get(f're{i}', 0)
            ch_d = row.get(f'ch{i}_d', 0)
            ex_d = row.get(f'ex{i}_d', 0)
            re_d = row.get(f're{i}_d', 0)
            new1 = round((avg_new_rate * (active + re + ex - ch) / (1 - avg_new_rate)), 0) if (1 - avg_new_rate) != 0 else 0
            new_acv = new1 * avg_new_acv
            active_calc = active + re + ex - ch + new1
            active_acv_calc = new_acv + re_d + ex_d - ch_d
            ch_rate = ch / active_calc if active_calc != 0 else 0
    
            cum_churn += ch
            cum_new += new1
            cum_renew += re + ex
            cum_churn_acv += ch_d
            cum_new_acv += new_acv
            cum_renewal_acv += re_d + ex_d
    
            records.append({
                'Month': start_month + pd.DateOffset(months=i),
                'Healthy & Engaged': re + ex + new1,
                'Upsell Potential': ex,
                'At Risk of Churn': ch,
                'Churn Rate': ch_rate,
                'New Accounts': new1,
                'Active Acv': active_acv_calc,
                'Active Accounts': active_calc,
                'Cumulative Churn Accounts': cum_churn,
                'Cumulative New Accounts': cum_new,
                'Cumulative Renew Accounts': cum_renew,
                'Churn ACV': ch_d,
                'Expansion ACV': ex_d,
                'Renewal ACV': re_d,
                'Cumulative Churn ACV': cum_churn_acv,
                'Cumulative New ACV': cum_new_acv,
                'Cumulative Renewal ACV': cum_renewal_acv,
                'New Accounts Rate':avg_new_rate
            })
    
        return pd.DataFrame(records)
    
    def summarize_projection(results):
        if results.empty:
            return {}
        return {
            'prj_acv': results['Active Acv'].sum(),
            'prj_churn_rate': results['Churn Rate'].mean(),
            'prj_new_rate': results['New Accounts Rate'].mean(),
            'prj_lose_acv': results['Churn ACV'].sum(),
            'prj_up_acv': results['Expansion ACV'].sum(),
            'prj_active': results['Active Accounts'].iloc[-1] if not pd.isna(results['Active Accounts'].iloc[-1]) else 0
        }
    
    # --- Prepare month options ---
    month_options = df['FOM'].dt.strftime('%b %Y').unique()
    unique_months = sorted(df['FOM'].dt.to_period('M').unique())
    month_options = [m.strftime('%b %Y') for m in unique_months]
    
    # --- FOM filter selection ---
    col_main, col_filter = st.columns([4, 1])
    with col_filter:
        selected_month = st.selectbox("Selected Date", month_options, index=month_options.index('Jan 2024'))
    try:
        selected_period = pd.to_datetime(selected_month)
    except Exception:
        selected_period = None
    
    df_selected = df[df['FOM'].dt.to_period('M') == selected_period.to_period('M')] if selected_period is not None else df[df['FOM'].dt.strftime('%b %Y') == selected_month]
    data_row = df_selected.iloc[0] if not df_selected.empty else None
    
    if data_row is not None:
        # --- Customer Base Overview ---
        st.markdown("## Customer Base Overview")
        active_accounts = int(data_row["Active Accounts"])
        new_accounts = int(data_row["New Accounts"])
        renew_accounts = int(data_row["Renew Accounts"])
        upsell_accounts = int(data_row["Upsell Accounts"])
        churn_accounts = int(data_row["Churn Accounts"])
    
        active_acv = data_row["Active ACV"]
        new_acv = data_row["New ACV"]
        renew_acv = data_row["Renew ACV"]
        upsell_acv = data_row["Upsell ACV"]
        churn_acv = data_row["Churn ACV"]
    
        active_accounts_str = f"{active_accounts:,}"
        new_accounts_str = f"{new_accounts:,}"
        renew_accounts_str = f"{renew_accounts:,}"
        upsell_accounts_str = f"{upsell_accounts:,}"
        churn_accounts_str = f"{churn_accounts:,}"
    
        active_acv_str = f"${active_acv:,.0f}"
        new_acv_str = f"${new_acv:,.0f}"
        renew_acv_str = f"${renew_acv:,.0f}"
        upsell_acv_str = f"${upsell_acv:,.0f}"
        churn_acv_str = f"${churn_acv:,.0f}"
    
        st.markdown(f"""<div style='background-color: #F5F5F5; padding: 15px; border-radius: 8px;'>
            <div style='display: flex; justify-content: space-between; gap: 10px;'>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Active Accounts</div><div style='font-size: 1.5em;'>{active_accounts_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>New Accounts</div><div style='font-size: 1.5em;'>{new_accounts_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Renew Accounts</div><div style='font-size: 1.5em;'>{renew_accounts_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Upsell Accounts</div><div style='font-size: 1.5em;'>{upsell_accounts_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Churn Accounts</div><div style='font-size: 1.5em;'>{churn_accounts_str}</div></div>
            </div></div>""", unsafe_allow_html=True)
    
        # --- Revenue Overview ---data
        st.markdown("## Revenue Overview")
        st.markdown(f"""<div style='background-color: #F5F5F5; padding: 15px; border-radius: 8px;'>
            <div style='display: flex; justify-content: space-between; gap: 10px;'>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Active ACV</div><div style='font-size: 1.5em;'>{active_acv_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>New ACV</div><div style='font-size: 1.5em;'>{new_acv_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Renew ACV</div><div style='font-size: 1.5em;'>{renew_acv_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Upsell ACV</div><div style='font-size: 1.5em;'>{upsell_acv_str}</div></div>
                <div style='flex: 1; text-align: center;'><div style='font-weight: 600;'>Churn ACV</div><div style='font-size: 1.5em;'>{churn_acv_str}</div></div>
            </div></div>""", unsafe_allow_html=True)
    
    
    projection_df = calculate_6_month_projection(selected_period)
    projection_summary = summarize_projection(projection_df)
    prj_acv = projection_summary.get('prj_acv', 0)
    prj_churn_rate = projection_summary.get('prj_churn_rate', 0)
    prj_new_rate = projection_summary.get('prj_new_rate', 0)
    prj_lose_acv = projection_summary.get('prj_lose_acv', 0)
    prj_up_acv = projection_summary.get('prj_up_acv', 0)
    prj_active = projection_summary.get('prj_active', 0)
    
    
    # --- Strategic Growth History Chart ---
    
    def plot_customer_base_chart(df_input, title='Customer Base Trend', highlight_date=None):
        fig, ax = plt.subplots(figsize=(5, 2.5))
        ax.plot(df_input['FOM'], df_input['Cumulative Renew Accounts'] + df_input['Cumulative New Accounts'], label='Max Potential', linewidth=2, color='#2b6490')
        ax.plot(df_input['FOM'], df_input['Cumulative New Accounts'], label='New Accounts', linewidth=2, color='#9ccee1')
        ax.plot(df_input['FOM'], df_input['Active Accounts'], label='Active Accounts', linewidth=2, color='#f2c300')
        ax.plot(df_input['FOM'], df_input['Cumulative Churn Accounts'], label='Churn Accounts', linewidth=2, color='#6f6f6f')
    
        if highlight_date is not None:
            ax.axvline(highlight_date, color='gray', linewidth=1, label='Selected FOM')
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=5)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=5)
        ax.set_title(title, fontsize=7)
        ax.set_xlabel("Month",  fontsize=7)
        ax.set_ylabel("Accounts", fontsize=7)
        ax.legend(fontsize=6)
        ax.grid(False)
        st.pyplot(fig)
    
    
    # Layout split after revenue overview
    main_col, side_col = st.columns([3, 1])
    with side_col:
        st.markdown("", unsafe_allow_html=True)
        st.markdown("""
            <div style="background-color: #FFF6D1; border-left: 6px solid #ffc107; padding: 16px; margin-bottom: 20px; border-radius: 6px;">
                <h4 style="margin-top: 0;">🧠 Action Recommend</h4>
                <ul style="padding-left: 20px; margin: 0;">
                    <li>If churn is reduced by <strong>X%</strong>, ARR will increase by <strong>$Y M</strong></li>
                    <li>Upsell engagement is below industry average. Consider targeting <strong>Segment A</strong> for expansion.</li>
                    <li>High-risk customers identified: <a href="#">View full list</a></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
        st.markdown("""
                <div style="background-color: #D5D5D5; border-left: 6px solid #dc3545; padding: 16px; margin-bottom: 20px; border-radius: 6px;">
                <h4 style="margin-top: 0;">🚨 Risk Alert System</h4>
                <ul style="padding-left: 20px; margin: 0;">
                    <li><strong>High Risk:</strong> Churn increasing in Mid-Market customers (<em>-X% engagement</em>).</li>
                    <li><strong>Medium Risk:</strong> Support tickets rising in Enterprise accounts (Potential renewal risk).</li>
                    <li><strong>Low Risk:</strong> Feature adoption lagging in new customers (May affect long-term retention).</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
        
    
        st.markdown("""
            <div style="background-color: #EBECED; border-left: 6px solid #6c757d; padding: 16px; margin-bottom: 20px; border-radius: 6px;">
                <h4 style="margin-top: 0;">🔧 Custom Alerts & Thresholds</h4>
                <ul style="padding-left: 20px; margin: 0;">
                    <li><strong>Churn threshold:</strong> e.g., Alert me if churn exceeds <strong>X%</strong></li>
                    <li><strong>Support escalations:</strong> e.g., Alert me if support tickets increase <strong>Y%</strong></li>
                    <li><strong>Feature adoption levels:</strong> e.g., Alert me if adoption drops below <strong>Z%</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #EBF5F9; border-left: 6px solid #0d6efd; padding: 16px; border-radius: 6px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">📊 Industry Benchmarking & Competitive Insights</h4>
            <table style="width: 100%; font-size: 13px;">
                <tr style="font-weight: bold;">
                    <td>Metric</td>
                    <td>Your Value</td>
                    <td>Industry Avg</td>
                    <td>+/- vs Industry</td>
                </tr>
                <tr><td>Churn Rate vs. Industry Average</td><td>X.X%</td><td>Y.Y%</td><td>Z%</td></tr>
                <tr><td>Customer Acquisition Growth vs. Industry</td><td></td><td></td><td></td></tr>
                <tr><td>Upsell Success Rate vs. Industry</td><td></td><td></td><td></td></tr>
                <tr><td>Net Revenue Retention (NRR)</td><td></td><td></td><td></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    
        st.markdown("""
            <div style="background-color: #d1ecf1; border-left: 6px solid #C5DBED; padding: 16px; margin-bottom: 20px; border-radius: 6px;">
                <h4 style="margin-top: 0;">📊 AI-Generated Competitive Insights</h4>
                <ul style="padding-left: 20px; margin: 0;">
                    <li>Your churn rate is <strong>X%</strong> higher than the industry average. Consider retention-focused initiatives.</li>
                    <li>Your upsell rate is leading the market by <strong>Y%</strong>. Explore doubling down on expansion strategies.</li>
                    <li>Your customer acquisition growth is lagging by <strong>Z%</strong>. Evaluate sales conversion strategies.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with st.expander("📷 Show Strategic Insight Image"):
            col_img_center = st.columns([1, 2, 1])  # centers the image
        
            with col_img_center[1]:
                st.image("data/SD.jpg", caption="Strategic Dimensions of Customer Dynamics", width=400)
        
            st.markdown("""
                <div style="background-color: #f4f4f4; padding: 12px; border-radius: 6px; border-left: 5px solid #0d6efd; margin-top: 10px;">
                    <strong>Insight Box:</strong><br>
                    <ul style="margin-top: 8px;">
                        <li><strong>Exponential Growth</strong>: Healthy acceleration. Ensure support systems can scale.</li>
                        <li><strong>Goal Seeking</strong>: Stabilization toward a limit. Revisit targets or constraints.</li>
                        <li><strong>S-Shaped Growth</strong>: Maturity approaching. Time for expansion strategy.</li>
                        <li><strong>Oscillation</strong>: Instability in systems. Strengthen feedback and monitoring.</li>
                        <li><strong>S-Shaped with Overshoot</strong>: Over-extension risk. Improve foresight.</li>
                        <li><strong>Overshoot and Collapse</strong>: Warning of breakdown. Prioritize recovery and resilience planning.</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
                
    with main_col:
        top_left, top_right = st.columns([1,1])
    
        with top_left:
            st.markdown("## Trend Analysis & Future Projection")
            st.markdown(f"""
                <div style="border: 2px solid #888; padding: 20px; border-radius: 8px; background-color: #FFFFFF;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr><td style="padding: 6px 12px; font-weight: 600;">Projected ARR (Next 6 months)</td><td>$ {prj_acv:.1f}</td></tr>
                        <tr><td style="padding: 6px 12px; font-weight: 600;">Projected Churn Impact</td><td>If churn continues at {prj_churn_rate:.0%}, ARR loss will be $ {prj_lose_acv:.1f}</td></tr>
                        <tr><td style="padding: 6px 12px; font-weight: 600;">Expected Upsell Growth</td><td>Potential revenue increase of $ {prj_up_acv:.1f}</td></tr>
                        <tr><td style="padding: 6px 12px; font-weight: 600;">Customer Growth Projection</td><td>Projected active customers in next 6 months: {prj_active:,}</td></tr>
                    </table>
                </div>
            """, unsafe_allow_html=True)
    
    
    
     # --- Future Projection & Strategic Growth ---
            st.markdown("")
            #show_simulation = st.button("Project next 6 months", key="run_simulation_button")
            show_simulation = st.button("Project next 6 months", key="run_simulation_button", help="Click to simulate future growth and churn impact")
            st.markdown("""
            <style>
            div[data-testid="stButton"] button {
                font-size: 16px !important;
                padding: 0.6em 1.2em;
            }
            </style>
            """, unsafe_allow_html=True)
            # Run projection once and store results
            #st.markdown("## Historical Customer Base Growth")
            if show_simulation:
                df_chart = df[df['FOM'] <= selected_period].copy()
                df_chart = df_chart.sort_values('FOM')
                future_dates = pd.date_range(start=df_chart['FOM'].min(), end=(selected_period + pd.DateOffset(months=12)), freq='MS')
                def extract_projection_summary(results):
                    columns_to_keep = [
                        'Cumulative Renew Accounts',
                        'Cumulative New Accounts',
                        'Active Accounts',
                        'Cumulative Churn Accounts'
                    ]
                    return results[columns_to_keep].copy()
                df_proj = extract_projection_summary(projection_df)
                df_proj = df_proj.copy()
                df_proj['FOM'] = projection_df['Month']
    
                for col in ['Cumulative Renew Accounts', 'Cumulative New Accounts', 'Cumulative Churn Accounts']:
                    df_proj[col] += df_chart.iloc[-1][col]
    
                df_combined = pd.concat([
                    df_chart[['FOM', 'Cumulative Renew Accounts', 'Cumulative New Accounts', 'Active Accounts', 'Cumulative Churn Accounts']],
                    df_proj[['FOM', 'Cumulative Renew Accounts', 'Cumulative New Accounts', 'Active Accounts', 'Cumulative Churn Accounts']]
                ], ignore_index=True)
    
                plot_customer_base_chart(df_combined, title="Customer Base Trend with Simulation", highlight_date=selected_period)
            else:
                df_chart = df[df['FOM'] <= selected_period].copy()
                df_chart = df_chart.sort_values('FOM')
                future_dates = pd.date_range(start=df_chart['FOM'].min(), end=(selected_period + pd.DateOffset(months=12)), freq='MS')
                df_padding = pd.DataFrame({'FOM': future_dates})
                for col in ['Cumulative Renew Accounts', 'Cumulative New Accounts', 'Active Accounts', 'Cumulative Churn Accounts']:
                    df_padding[col] = np.nan
                df_chart_extended = pd.concat([df_chart, df_padding], ignore_index=True)
                plot_customer_base_chart(df_chart_extended, highlight_date=selected_period)
    
        
    
        # --- Input Row: Historical Month, Churn & Acquisition Rate ---
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            available_past_months = df[df['FOM'] < selected_period]['FOM'].dt.strftime('%b %Y').tolist()
            user_selected_month = st.selectbox("📅 Set Simulation Date", available_past_months, key="compare_month")
            user_selected_period = pd.to_datetime(user_selected_month)
        user_churn_multiplier = 1.0
        user_acq_multiplier = 1.0
        
        with col2:
            df_user_month = df[df['FOM'].dt.to_period('M') == user_selected_period.to_period('M')]
            default_churn = float(df_user_month['Churn Accounts Rate'].values[0]) if not df_user_month.empty else 0
            user_churn_multiplier = st.number_input("Set Churn Rate Multiplier (e.g., 2 = 2x current rate)", min_value=0.0, value=1.0, step=0.1, key="user_churn_multiplier")
        
        with col3:
            default_acq = float(df_user_month['New Accounts Rate'].values[0]) if not df_user_month.empty else 0
            user_acq_multiplier = st.number_input("Set Acquisition Rate Multiplier (e.g., 0.5 = 50% of current)", min_value=0.0, value=1.0, step=0.1, key="user_acq_multiplier")
    
    
        # --- Ask Keeper ---
        # --- Ask Keeper ---
        with st.expander("🤖 Ask Keeper"):
            st.markdown("""
            <div style="background-color: #f4f4f4; padding: 16px; border-left: 6px solid #6366f1; border-radius: 6px; margin-bottom: 10px;">
                <ul style="margin: 0; padding-left: 20px;">
                    <li>What signals should I track to detect upcoming churn trends?</li>
                    <li>Are we approaching a growth plateau? How do I know when to pivot?</li>
                    <li>What’s the earliest point I can intervene before overshoot and collapse?</li>
                    <li>Can I simulate multiple “what-if” scenarios side by side?</li>
                    <li>How do I know which segment is contributing most to upsell momentum?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
            user_question = st.text_input("Or ask your own strategic question:", placeholder="e.g., What would happen if churn increases 10%?")
            if user_question:
                st.info(f"You asked: {user_question}")
    
        
    
            
        with top_right:
            st.markdown("## Dynamic Growth Simulation")
        
            # --- Simulation & Scenario Planning Table ---
            last_churn_rate = data_row.get("Churn Accounts Rate", 0)
            last_acq_rate = data_row.get("New Accounts Rate", 0)
            projection_period = f"{(selected_period + pd.DateOffset(months=1)).strftime('%b %Y')} - {(selected_period + pd.DateOffset(months=7)).strftime('%b %Y') }"
            prj_new_rate = summarize_projection(calculate_6_month_projection(selected_period)).get('prj_new_rate', 0)
        
            st.markdown(f"""
            <div style="border: 2px solid #888; padding: 20px; border-radius: 8px; background-color: #FFFFFF;">
                            <table style="width: 100%; border-collapse: collapse;">
                    <tr style="background-color: #f5f5f5;"><th></th><th>Date</th><th>Churn Rate (%)</th><th>Customer Acquisition Rate (%)</th></tr>
                    <tr><td style="padding: 6px 12px;">Last Month</td><td>{selected_period.strftime('%b %Y')}</td><td>{last_churn_rate:.2%}</td><td>{last_acq_rate:.2%}</td></tr>
                    <tr><td style="padding: 6px 12px;">Project Period</td><td>{projection_period}</td><td>{summarize_projection(calculate_6_month_projection(selected_period)).get('prj_churn_rate', 0):.2%}</td><td>{prj_new_rate:.2%}</td></tr>
                    <tr><td style="padding: 6px 12px;">Set Simulation Date</td><td>{user_selected_month}</td><td>{user_churn_multiplier:.2f}× ({user_churn_multiplier * default_churn:.2%})</td><td>{user_acq_multiplier:.2f}× ({user_acq_multiplier * default_acq:.2%})</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
    
            
            st.markdown("&nbsp;\n&nbsp;", unsafe_allow_html=True)
            st.markdown(f"""<div style="border: 2px solid #888; ... </div>""", unsafe_allow_html=True)
            st.markdown("&nbsp;\n&nbsp;", unsafe_allow_html=True)
     
    
           
            
            def plot_simulated_churn_chart(df_simulated, selected_period, highlight_date=None):
                df_simulated = df_simulated[df_simulated['FOM'] <= selected_period]
                fig, ax = plt.subplots(figsize=(5, 2.5))
                ax.plot(df_simulated['FOM'], round(df_simulated['Active Accounts']), label='Current Active Accounts', linewidth=1, color='#f2c300')
                ax.plot(df_simulated['FOM'], round(df_simulated['Active Accounts_c']), label='Simulated Active', linestyle='--', color='#f2c300')
                #ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative Renew Accounts']+ df_simulated['Cumulative New Accounts']), label='Current Max Potential', linewidth=2, color='#2b6490')
                #ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative Renew Accounts_c']+ df_simulated['Cumulative New Accounts_c']), label='Simulated Max Potential', linestyle='--',  color='#2b6490')
                ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative Churn Accounts']), label='Current Churn Accounts', linewidth=1, color='#6f6f6f')
                ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative Churn Accounts_c']), label='Simulated Churn Accounts', linestyle='--',  color='#6f6f6f')
                ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative New Accounts']), label='Current New Accounts', linewidth=1, color='#9ccee1')
                ax.plot(df_simulated['FOM'], round(df_simulated['Cumulative New Accounts_c']), label='Simulated New Accounts', linestyle='--',  color='#9ccee1')
    
                if highlight_date is not None:
                    ax.axvline(highlight_date, color='gray', linewidth=1, linestyle='-', label='User Selected')
                ax.set_title("Churn Rate Simulation Impact", fontsize=7)
               
                ax.set_xticklabels(ax.get_xticklabels(), fontsize=6)
                ax.set_yticklabels(ax.get_yticklabels(), fontsize=6)
                ax.set_xlabel("Month",  fontsize=8)
                ax.set_ylabel("Accounts", fontsize=8)
                ax.legend(fontsize=4)
                ax.grid(False)
                st.pyplot(fig)
    
        # --- Combine both simulations ---
            def run_combined_simulation(df, fom_start, churn_multiplier, acq_multiplier):
                df = df.copy()  
                df.sort_values('FOM', inplace=True)
                df.reset_index(drop=True, inplace=True)
                df['FOM'] = pd.to_datetime(df['FOM'])
                
                start_index = df[df['FOM'] == pd.to_datetime(fom_start)].index[0]
                
                df['Cumulative Renew Accounts_c'] = df['Cumulative Renew Accounts']
                df['Cumulative New Accounts_c'] = df['Cumulative New Accounts']
                df['Cumulative Churn Accounts_c'] = df['Cumulative Churn Accounts']
                df['Active Accounts_c'] = df['Active Accounts']
                df['Churn Accounts Rate_c'] = df['Churn Accounts Rate']
                df['New Accounts Rate_c'] = df['New Accounts Rate']
                if churn_multiplier == 1 and acq_multiplier == 1:
                    return df
                else:    
                    for i in range(start_index, len(df)):
                        if i == 0:
                            continue
                
                        churn_rate_prev = df.loc[i , 'Churn Accounts Rate_c']
                        churn_rate_updated = churn_rate_prev * churn_multiplier
                        df.loc[i, 'Churn Accounts Rate_c'] = churn_rate_updated
                        churn_c = df.loc[i, 'Churn Accounts'] * churn_multiplier
                        
                        
                        new_rate_prev = df.loc[i , 'New Accounts Rate_c']
                        new_rate_updated = acq_multiplier * new_rate_prev
                        df.loc[i, 'New Accounts Rate_c'] = new_rate_updated
                        new_c = df.loc[i, 'New Accounts'] * acq_multiplier
                        
                        renew_c = df.loc[i, 'Renew Accounts'] - (churn_multiplier-1)*df.loc[i, 'Churn Accounts']/2
                        upsell_c = df.loc[i, 'Upsell Accounts'] - (churn_multiplier-1)*df.loc[i, 'Churn Accounts']/2
    
                        #active_c = df.loc[i-1, 'Active Accounts_c'] + new_c - churn_c + renew_c + upsell_c
    
                        
                        
                        active_c = df.loc[i-1, 'Active Accounts_c'] + new_c - churn_c
                        df.loc[i, 'Cumulative Renew Accounts_c'] = df.loc[i - 1, 'Cumulative Renew Accounts_c'] + renew_c + upsell_c
                        df.loc[i, 'Cumulative New Accounts_c'] = df.loc[i - 1, 'Cumulative New Accounts_c'] + new_c
                        df.loc[i, 'Cumulative Churn Accounts_c'] = df.loc[i - 1, 'Cumulative Churn Accounts_c'] + churn_c
                        df.loc[i, 'Active Accounts_c'] = active_c
                
                    return df
                    # --- Run combined simulation and plot ---
             
            
            sim_result_final = run_combined_simulation(df, fom_start=user_selected_period, churn_multiplier=user_churn_multiplier, acq_multiplier=user_acq_multiplier)
            plot_simulated_churn_chart(sim_result_final, selected_period=selected_period, highlight_date=user_selected_period)


if __name__ == "__main__":
    show()
