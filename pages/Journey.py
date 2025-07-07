import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.tseries.offsets import DateOffset
from streamlit_extras.switch_page_button import switch_page
from utils import hide_sidebar
from navigation import show_navigation


######### 0_sim_contract.xlsx
######### 5_model_final_score_dashboard_data.csv
##################################################### 

st.set_page_config(page_title="Journey", layout="wide")

hide_sidebar()

def show():
    st.title("📘 Customer Pulse")
    st.subheader("Customer Journey & Risk Score Trend")    
    st.markdown(
        """
        **Customer Pulse** provides a complete view of an account’s journey, including contract history,  
        **Risk Score** trends and signals over time. This page highlights engagement levels across product usage,  
        support interactions, and CSM activity to help monitor changes in customer health.
        """
    )


    with st.container():
        col1, col3 = st.columns([4, 1])
        with col3:
            show_navigation("📘 Customer Pulse")
        
        
    # --- Config ---
      # Load and clean data
    df_contract = pd.read_excel("data/0_sim_contract.xlsx")
    df_contract.columns = df_contract.columns.str.strip().str.lower()

    # Load score data
    df_score = pd.read_csv("data/5_model_final_score_dashboard_data.csv")
    df_score.columns = df_score.columns.str.strip().str.lower()

    # Convert contract dates to datetime
    df_contract['contract_start_date'] = pd.to_datetime(df_contract['contract_start_date'])
    df_contract['contract_end_date'] = pd.to_datetime(df_contract['contract_end_date'])
    df_contract['first_contract_start_date'] = pd.to_datetime(df_contract['first_contract_start_date'])
    df_score['fom'] = pd.to_datetime(df_score['fom'], errors='coerce')
    df_score['fom_period'] = df_score['fom'].dt.to_period('M')

    # Derive 'fom' column from first_contract_start_date
    df_contract['fom'] = df_contract['first_contract_start_date'].dt.to_period('M')

    # Add contract duration
    df_contract['contract_duration_days'] = (df_contract['contract_end_date'] - df_contract['contract_start_date']).dt.days

    # --- Layout with filters on the right ---
    col_main, col_filters = st.columns([4, 1])

    with col_main:
        account_df = pd.DataFrame()
        selected_account_id = None

    with col_filters:
        # Load demo accounts from external CSV
        demo_accounts_df = pd.read_csv("data/6_demo_accounts_cj.csv")
        demo_account_ids = demo_accounts_df['account_name'].unique()

        filtered_df = df_contract[df_contract['account_name'].isin(demo_account_ids)].copy()

        # Merge 'order' info to ensure sorted selection
        merged_df = pd.merge(filtered_df, demo_accounts_df[['account_name', 'order']], how='left', left_on='account_name', right_on='account_name')
        merged_df = merged_df.sort_values(by='order')

        #account_ids_ordered = merged_df['account_id'].unique()
        account_ids_ordered = merged_df['account_name'].unique()
        selected_account_id = st.selectbox("Select Account Name", account_ids_ordered, key="account_id_selector")

        st.markdown("</div>", unsafe_allow_html=True)

    if selected_account_id:
        account_df = filtered_df[filtered_df['account_name'] == selected_account_id]

   
        if not account_df.empty:
            col_left, col_right = st.columns([2, 1], gap="large")
            first_row = account_df.iloc[0]
            last_row_contract = account_df.iloc[-1]
            name = first_row['account_id']
            account_name=first_row['account_name']
            industry = first_row['industry']
            size = first_row['business_size']
            revenue = first_row['annual_revenue']
            #revenue = account_df['annual_revenue'].dropna().values[0] if not account_df['annual_revenue'].dropna().empty else 0

            age = last_row_contract['age_at_contract']
            contract_acv = last_row_contract['contract_acv']
            duration = last_row_contract['contract_duration_days']
            num_contracts = len(account_df)
    
            with col_left:
                sub_col1, sub_col2 = st.columns([1, 2], gap="large")
                with sub_col1:
                    st.subheader(f"📘 Account Overview")
                    st.markdown(f"""
                    <div style='border: 1px solid #d3d3d3; border-radius: 10px; padding: 20px;'>
                        <table style='width: 100%; font-size: 16px;'>
                            <tr><td><b>Account Name</b></td><td>{account_name}</td></tr>
                            <tr><td><b>Industry</b></td><td>{industry}</td></tr>
                            <tr><td><b>Size</b></td><td>{size}</td></tr>
                            <tr><td><b>Age of the Customer</b></td><td>{age} months</td></tr>
                            <tr><td><b>Number of Contracts</b></td><td>{num_contracts}</td></tr>
                            <tr><td><b>Contract ACV</b></td><td>${contract_acv:,.0f}</td></tr>
                            <tr><td><b>Contract Date</b></td><td>{last_row_contract['contract_start_date'].date()} to {last_row_contract['contract_end_date'].date()}</td></tr>
                             </table>
                            </div>
                    """, unsafe_allow_html=True)
                with sub_col2:
                    st.markdown("")
                    # Load and filter score data for selected account
                    df = df_score[df_score['account_name'] == selected_account_id].copy()
                    contract_starts = df.groupby('contract_id').first().reset_index()
                    contract_starts['FOM_date'] = pd.to_datetime(contract_starts['fom'])
                    contract_starts = contract_starts.sort_values(by='FOM_date').reset_index(drop=True)
            
                    # Define color mapping
                    c_risky = '#6f6f6f'
                    c_adoption = '#9ccee1'
                    c_renew = '#2b6490'
                    c_expansion = '#f2c300'
                    c_unknown = 'white'
            
                    status_colors = {
                        'renewal': c_renew,
                        'expansion': c_expansion,
                        'churn': c_risky
                    }
            
                    # Set contract timeline
                    contract_starts['FOM_date'] = pd.to_datetime(contract_starts['fom'])
                    contract_starts['end_date'] = contract_starts['FOM_date'] + DateOffset(years=1)
                    start_date_range = pd.to_datetime("2020-01-01")
                    end_date_range = start_date_range + DateOffset(years=7)
            
                    # Plotting
                    fig, ax = plt.subplots(figsize=(12, 4))
            
                    for spine in ax.spines.values():
                        spine.set_visible(False)
            
                    ax.axhline(0, color='black', linewidth=0.8)
                    ax.axvline(start_date_range, color='black', linewidth=0.8)
            
                    for i, row in contract_starts.iterrows():
                        start_date = row['FOM_date']
                        end_date = row['end_date']
                        acv = row['contract_acv']
                        status = row['final_status']
            
                        if i < len(contract_starts) - 1:
                            next_row = contract_starts.iloc[i + 1]
                            next_start = next_row['FOM_date']
                            next_acv = next_row['contract_acv']
                            ax.plot([start_date, next_start], [acv, next_acv], color='black', linewidth=1)
            
                        if i == 0:
                            marker_color = c_adoption
                            edge_color = 'none'
                            y_pos = acv
                            ax.text(start_date, acv + 10000, start_date.strftime('%Y-%m-%d'), ha='center', va='bottom', fontsize=7, color='black')
                        else:
                            prev_status = contract_starts.loc[i - 1, 'final_status']
                            marker_color = status_colors.get(prev_status, c_unknown)
                            edge_color = 'black' if marker_color == c_unknown else 'none'
                            y_pos = acv
            
                        ax.scatter(start_date, y_pos, s=250, color=marker_color, edgecolors=edge_color, linewidth=2, zorder=5)
                        
    
                    
                    
                    # Annotate all contract end dates
                    for i, row in contract_starts.iterrows():
                        ax.text(row['end_date'], row['contract_acv'] + 10000, row['end_date'].strftime('%Y-%m-%d'),
                                ha='center', va='bottom', fontsize=7, color='black')
            
                    # Draw last line and end marker
                    last_row = contract_starts.iloc[-1]
                    ax.plot([last_row['FOM_date'], last_row['end_date']], [last_row['contract_acv'], last_row['contract_acv']], color='black', linewidth=1)
            
                    last_color = status_colors.get(last_row['final_status'], c_risky if last_row['final_status'] in ['churn', 'risky'] else c_unknown)
                    last_edge = 'black' if last_color == c_unknown else 'none'
                    ax.scatter(last_row['end_date'], last_row['contract_acv'], s=250, color=last_color, edgecolors=last_edge, linewidth=2, zorder=5)
            
                    # Axis formatting
                    ax.set_xticklabels([])
                    ax.set_xlabel("Date")
                    ax.set_ylabel("ACV")
                    ax.set_ylim(0, 200000)
                    ax.set_yticks(range(0, 200001, 50000))
                    ax.set_xlim(start_date_range, end_date_range)
                    ax.set_xticks([start_date_range, end_date_range])
                    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
                    st.pyplot(fig)
    
             # Get all score data for the selected account
            df_score_filtered = df_score[df_score['account_name'] == selected_account_id].copy()
            df_score_filtered = df_score_filtered.sort_values(by='fom')
    
            # Process score values
            df_score_filtered['score_percent'] = (df_score_filtered['score_final'] * 100).round(0)
    
            # Plotting trend
            fig2, ax2 = plt.subplots(figsize=(12, 3))
            ax2.plot(df_score_filtered['fom'], df_score_filtered['score_percent'], marker='o', linestyle='-', color='teal')
    
            # Add threshold line at 50
            ax2.axhline(50, color='red', linestyle='--', linewidth=1, label='Threshold (50)')
    
            # Format
            ax2.set_ylabel("Final Score (%)")
            ax2.set_ylim(0, 100)
            ax2.set_xlabel("Date")
            ax2.set_title(f"Final Score from First Contract for {selected_account_id}")
            ax2.legend()
            ax2.grid(True, linestyle=':', alpha=0.6)
            fig2.autofmt_xdate()
    
            with col_right:
                st.markdown("<div style='border: 1px solid #d3d3d3; border-radius: 10px; padding: 15px;'><h4>Risk Score</h4><p style='font-size: 34px; font-weight: bold;'>" + str(int(round(df_score[df_score['account_name'] == selected_account_id].sort_values(by='fom').iloc[-1]['score_final'] * 100))) + "</p></div>", unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top: 20px;'>Score Trend</h4>", unsafe_allow_html=True)
                st.pyplot(fig2)
               
    
               
    
    
    
               
     # Get the latest usage score for the selected account
                   # Get the latest usage score for the selected account
                latest_usage = df_score[df_score['account_name'] == selected_account_id].sort_values(by='fom').iloc[-1]
                usage_score = (latest_usage['usage_score'] + 1) * 50  # scale to 0-100
                usage_label = latest_usage['usage_score_label']
        
                # Color coding
                cc_risk = '#CB3541'
                cc_normal = '#F9E03D'
                cc_healthy = '#7BB73D'
                label_color_map = {
                    'risky': cc_risk,
                    'normal': cc_normal,
                    'healthy': cc_healthy
                }
                gauge_color = label_color_map.get(usage_label.lower(), 'gray')
        
            
               
                  # Draw gauge
                fig3, ax3 = plt.subplots(figsize=(2, 1.5), subplot_kw={'projection': 'polar'})
                ax3.set_theta_offset(np.pi/2)  # rotate flat side to bottom
                ax3.set_theta_direction(-1)      # clockwise
                theta = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 100)
                radii = np.ones_like(theta)
        
               # Background gradient (manually define segments)
                colors = [cc_risk if i < 33 else cc_normal if i < 66 else cc_healthy for i in range(100)]
                ax3.bar(theta, radii, width=np.pi/100, bottom=0.0, color=colors, edgecolor='white', linewidth=0.5)
                alfa= -np.pi/2
                # Needle
                angle = np.deg2rad(
    np.interp(latest_usage['usage_score'], [-1, 0], [-90, -30]) if latest_usage['usage_score'] < 0 else
    (0 if latest_usage['usage_score'] == 0 else np.interp(latest_usage['usage_score'], [0, 1], [30, 90]))
)
                a3=angle
                ax3.annotate('', xy=(angle, 0.8), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='black', lw=2))
                ax3.set_title(f"Product Usage ({latest_usage['usage_score']:.2f})", va='top', pad=10, fontsize=6, fontweight='bold')

                # Remove polar elements
                ax3.set_axis_off()
                ax3.set_ylim(0, 1)
        
                # Add score text
                ax3.text(0, -0.05, f"Today{usage_score:.0f}%{usage_label.title()}", ha='center', va='center', fontsize=10, fontweight='bold')
        
                
    
                # --- Support Score Gauge ---
                latest_support = df_score[df_score['account_name'] == selected_account_id].sort_values(by='fom').iloc[-1]
                support_score = (latest_support['support_score'] + 1) * 50
                fig4, ax4 = plt.subplots(figsize=(2, 1.5), subplot_kw={'projection': 'polar'})
                ax4.set_theta_offset(np.pi/2)
                ax4.set_theta_direction(-1)
                theta = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 100)
                radii = np.ones_like(theta)
                ax4.bar(theta, radii, width=np.pi/100, bottom=0.0, color=colors, edgecolor='white', linewidth=0.5)
                ax4.set_title(f"Support ({latest_support['support_score']:.2f})", va='top', pad=10, fontsize=6, fontweight='bold')
                angle = np.deg2rad(
    np.interp(latest_support['support_score'], [-1, 0], [-90, -30]) if latest_support['support_score'] < 0 else
    (0 if latest_support['support_score'] == 0 else np.interp(latest_support['support_score'], [0, 1], [30, 90]))
)
                a4=angle
                ax4.annotate('', xy=(angle, 0.8), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='black', lw=2))
                ax4.set_axis_off()
                ax4.set_ylim(0, 1)
                  
        
                # --- Activity Score Gauge ---
                latest_activity = df_score[df_score['account_name'] == selected_account_id].sort_values(by='fom').iloc[-1]
                activity_score = (latest_activity['activity_score'] + 1) * 50
                fig5, ax5 = plt.subplots(figsize=(2, 1.5), subplot_kw={'projection': 'polar'})
                ax5.set_theta_offset(np.pi/2)
                ax5.set_theta_direction(-1)
                theta = np.linspace(-0.5 * np.pi, 0.5 * np.pi, 100)
                radii = np.ones_like(theta)
                ax5.bar(theta, radii, width=np.pi/100, bottom=0.0, color=colors, edgecolor='white', linewidth=0.5)
                ax5.set_title(f"CSM Activity ({latest_activity['activity_score']:.2f})", va='top', pad=10, fontsize=6, fontweight='bold')
                angle = np.deg2rad(
    np.interp(latest_activity['activity_score'], [-1, 0], [-90, -30]) if latest_activity['activity_score'] < 0 else
    (0 if latest_activity['activity_score'] == 0 else np.interp(latest_activity['activity_score'], [0, 1], [30, 90]))
)
                ax5.annotate('', xy=(angle, 0.8), xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='black', lw=2))
                ax5.set_axis_off()
                ax5.set_ylim(0, 1)
                a5=angle
                import math
                
                
                gauge_cols = st.columns(3)
                with gauge_cols[0]:
                    st.pyplot(fig3)
                with gauge_cols[1]:
                    st.pyplot(fig4)
                with gauge_cols[2]:
                    st.pyplot(fig5)
                 # --- Display Image ---
                
                st.image("data/net.png.png", use_column_width=True)
           
                with col_left:
                    st.markdown("<h4 style='margin-top: 40px;'>💬 Ask Keeper</h4>", unsafe_allow_html=True)

                    story_df = pd.read_csv("data/6_customer_journey_story.csv", encoding='ISO-8859-1')
                    story_df.columns = story_df.columns.str.strip().str.lower()
                    story_df['account_name'] = story_df['account_name'].astype(str)

                    # Remove broken filtering logic
                    # Instead, directly validate column existence below
                    story_df.columns = story_df.columns.str.strip().str.lower()
                    if 'account_name' in story_df.columns:
                        story_df['account_name'] = story_df['account_name'].astype(str)
                        
                        story_row = story_df[story_df['account_name'] == str(selected_account_id)] if not story_df.empty else pd.DataFrame()
                        
                    else:
                        story_row = pd.DataFrame()

                    default_question = "Customer engagement is 25% lower than similar accounts, how can we improve their engagement?"

                    if not story_row.empty:
                        story_row = story_row.iloc[0]
                        custom_question = story_row.get("question", default_question)
                        keeper_input = st.text_input("", value=custom_question)
                        ask_keeper_clicked = st.button("Ask Keeper", key="ask_keeper_button")

                        if ask_keeper_clicked:
                            st.text_area("Keeper's Response", value=story_row.get("answer", "Keeper Processing..."), height=60)

                        st.markdown(f"""
                        <h3 style='margin-top: 30px;'>🧠 Generative Insight</h3>
                        <div style='display: flex; flex-direction: column; gap: 20px;'>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                        <h4>Summary of Account</h4>
                        <p>{story_row.get('summary of account', '')}</p>
                        </div>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                            <h4>Highlights of Activities</h4>
                            <p>{story_row.get('highlights of activities', '')}</p>
                        </div>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                            <h4>Actionable Insights & Next Steps</h4>
                            <ul>
                                <li><strong>{story_row.get('recommendation_1', '')}</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> {story_row.get('talking_1', '')}</li>
                                        <li><em>Actions:</em> {story_row.get('action_1', '')}</li>
                                    </ul>
                                </li>
                                <li><strong>{story_row.get('recommendation_2', '')}</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> {story_row.get('talking_2', '')}</li>
                                        <li><em>Actions:</em> {story_row.get('action_2', '')}</li>
                                    </ul>
                                </li>
                                <li><strong>{story_row.get('recommendation_3', '')}</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> {story_row.get('talking_3', '')}</li>
                                        <li><em>Actions:</em> {story_row.get('action_3', '')}</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        keeper_input = st.text_input("", value=default_question)
                        ask_keeper_clicked = st.button("Ask Keeper", key="ask_keeper_button")

                        if ask_keeper_clicked:
                            st.text_area("Keeper's Response", value="Keeper Processing...", height=60)

                        st.markdown("""
                        <h3 style='margin-top: 30px;'>🧠 Generative Insight</h3>
                        <div style='display: flex; flex-direction: column; gap: 20px;'>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                        <h4>Summary of Account</h4>
                        <p>This customer is a small business in the software and technology industry, with an annual revenue of $22,200,000.
                        They hold a small-sized contract, currently using only 1 out of 5 available products. Their contract history includes two 12-month renewals—the first at the same price and the second with an upsell.
                        They are now 8 months into their third contract (67% progress).</p>
                        </div>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                            <h4>Highlights of Activities</h4>
                            <p>Ann, the assigned CSM, has conducted regular monthly check-ins for the past eight months (~30 minutes each).
                            However, the latest call lasted 90 minutes, focusing on training and new dashboard features, with positive sentiment.<br>
                            Despite this engagement, product usage has declined by 27% and credit consumption has dropped 46% over the last three months.
                            This signals potential disengagement or workflow changes that need to be explored.</p>
                        </div>
                        <div style='flex: 1; padding: 15px; border: 1px solid #d3d3d3; border-radius: 10px;'>
                            <h4>Actionable Insights & Next Steps</h4>
                            <ul>
                                <li><strong>Address Usage Decline</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> Ask about any workflow changes affecting usage. Identify potential pain points.</li>
                                        <li><em>Actions:</em> Schedule a follow-up session to diagnose drop-off reasons and reinforce best practices.</li>
                                    </ul>
                                </li>
                                <li><strong>Leverage Training Interest</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> Recap the last session and offer additional guidance on feature adoption.</li>
                                        <li><em>Actions:</em> Share a quick guide or video, and check in within two weeks for progress.</li>
                                    </ul>
                                </li>
                                <li><strong>Prepare for Renewal</strong>
                                    <ul>
                                        <li><em>Talking Points:</em> Gauge renewal plans, budget considerations, and key decision-makers.</li>
                                        <li><em>Actions:</em> Start tracking renewal timelines and prepare retention/upsell strategies.</li>
                                    </ul>
                                </li>
                            </ul>
                        </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
        
if __name__ == "__main__":
    show()
       
                
                
        
                
                
        
