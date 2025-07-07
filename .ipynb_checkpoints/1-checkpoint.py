import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go


# Load data for Dashboard 1
try:
    stats_df=pd.read_csv('cc_monthlystat_sim.csv')  # Replace with your actual path
except FileNotFoundError:
    st.error("Data file not found for Dashboard 1. Please check the path.")
    st.stop()

# Load data for Dashboard 2
try:
    df2 = pd.read_csv('cc_usage.csv')  # Replace with your actual path
    df2=df2[['FOM','number_of_contract', 'MOC', 'contract_year',
       'contract_start_date', 'contract_end_date', 'contract_acv',
       'acv_label','raim_abm__num_active_users_label', 'num_product1_1_label',
       'amount_product1_2_label', 'total_product1_3_created_label',
       'product1_3_used_in_any_activation_label',
       'product1_3_used_in_any_activation_median_renew', 'POC', 'ID_s',
       'account_name_s', 'org_name_x_s', 'contract_id_s']]
    df2.rename(columns={'FOM':'Date'},inplace=True)
    
except FileNotFoundError:
    st.error("Data file not found for Dashboard 2. Please check the path.")
    st.stop()
    
# Load data for Dashboard 3
try:
    df3 = pd.read_csv('cc_sample_nov.csv')  # Replace with your actual path
    df3.rename(columns={
    'score_sup': 'Support Score',
    'score_activity': 'Communication Score',
    'score_usage': 'Usage Score',
    'score_contract': 'Contract Score'
    }, inplace=True)
    df3.rename(columns={'FOM':'Date'},inplace=True)
    df3['Date'] = pd.to_datetime(df3['Date'])
except FileNotFoundError:
    st.error("Data file not found for Dashboard 3. Please check the path.")
    st.stop()
    


# Convert 'Month' column to datetime objects
stats_df['Month'] = pd.to_datetime(stats_df['Month'])

# Create IsForecast flag
stats_df['IsForecast'] = stats_df['Month'] > pd.to_datetime('2024-11-01')

# Initialize session state for the selected dashboard
if 'selected_dashboard' not in st.session_state:
    st.session_state.selected_dashboard = "Executive Dashboard"  # Default dashboard
    

# Create tabs (or a similar navigation)
dashboard_options = ["Executive Dashboard", "Usage Dashboard","Customer Overview" ]
selected_dashboard = st.selectbox("Select Dashboard", dashboard_options)

# Update session state when a tab is selected
if selected_dashboard!= st.session_state.selected_dashboard:
    st.session_state.selected_dashboard = selected_dashboard

if st.session_state.selected_dashboard == "Executive Dashboard":
    st.title("Executive Dashboard")
    # Year and Month selection
    years = stats_df['Month'].dt.year.unique()
    selected_year = st.selectbox("Select Year", years, index=list(years).index(2024)) # default year 2024

    months = stats_df[stats_df['Month'].dt.year == selected_year]['Month'].dt.month.unique()
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    default_months = [month_names[m] for m in months if month_names[m] == 'Nov'] # default month Nov
    selected_months = st.multiselect("Select Months", [month_names[m] for m in months], default=default_months)


    # Filter the DataFrame based on selected year and months
    filtered_df = stats_df[
        (stats_df['Month'].dt.year == selected_year) &
        (stats_df['Month'].dt.month.isin([m for m, name in month_names.items() if name in selected_months]))
    ]

    if not filtered_df.empty:
        # Display Counts
        col_names_count = ['New Count', 'Renew Count', 'Upsell Count', 'Churn Count']
        cols_count = st.columns(len(col_names_count))
        for i, col_name in enumerate(col_names_count):
            with cols_count[i]:
                value = filtered_df[col_name].sum()
                st.markdown(f"""
                    <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f0f0f0; text-align: center;">
                        <span style="font-weight: bold; display: block;">{col_name}</span>
                        <span>{value}</span>
                    </div>
                """, unsafe_allow_html=True)

        # Display ACVs
        col_names_acv = ['New ACV', 'Renew ACV', 'Upsell ACV', 'Churn ACV']
        cols_acv = st.columns(len(col_names_acv))
        for i, col_name in enumerate(col_names_acv):
            with cols_acv[i]:
                # Convert the column to numeric (handling commas)
                filtered_df[col_name] = filtered_df[col_name].astype(str).str.replace(',', '')
                filtered_df[col_name] = pd.to_numeric(filtered_df[col_name])

                value = filtered_df[col_name].sum().round()
                st.markdown(f"""
                    <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f0f0f0; text-align: center;">
                        <span style="font-weight: bold; display: block;">{col_name}</span>
                        <span>{value}</span>
                    </div>
                """, unsafe_allow_html=True)

        # Create IsForecast flag
        stats_df['IsForecast'] = stats_df['Month'] > pd.to_datetime('2024-11-01')

        # Filter data for the chart (actual data only)
        chart_data = stats_df[stats_df['IsForecast'] == False].melt(id_vars=['Month'], value_vars=['Cumulative Churn Count', 'Cumulative Customer Count', 'New Count', 'Active Count'],
                                                                  var_name='Count Type', value_name='Count')

        # Create the line chart for actual data
        fig = px.line(chart_data, x='Month', y='Count', color='Count Type', title='')

        
        # Update legend name for actual data (removing "solid")
        for trace in fig.data:
            if trace.type == 'scatter':  # Only update traces of type 'scatter'
                trace.update(name=f"{trace.name}")  # Update the legend name to match the count type
                trace.update(mode='lines')  # Ensure it's a line trace (remove markers)
                trace.update(line=dict(color=trace.line.color, width=2))  # Add line style without "solid"

        # Add forecasted data with dashed line and tooltip
        forecast_data = stats_df[stats_df['IsForecast'] == True]

        # Simulation type selection
        simulation_types = forecast_data['simulation'].unique()
        selected_simulation = st.selectbox('Select Simulation Type', simulation_types)

        # Filter forecasted data based on selected simulation
        selected_forecast_data = forecast_data[forecast_data['simulation'] == selected_simulation].melt(
            id_vars=['Month', 'simulation'],  # Add 'simulation' to id_vars
            value_vars=['Cumulative Churn Count', 'Cumulative Customer Count', 'New Count', 'Active Count'],
            var_name='Count Type',
            value_name='Count'
        )

        # Add forecasted data to the chart without line_dash
        forecast_fig = px.line(selected_forecast_data, x='Month', y='Count', color='Count Type', hover_data=['simulation'])


        # Extract the trace from the forecasted figure and add it to the main figure with black dots
        # Add forecasted data as black dots (no line)
        for count_type in selected_forecast_data['Count Type'].unique():
            count_data = selected_forecast_data[selected_forecast_data['Count Type'] == count_type]

            # Create a scatter trace for the forecasted data (black dots)
            trace = go.Scatter(
                x=count_data['Month'],
                y=count_data['Count'],
                mode='markers',  # Only show markers (dots), no lines
                name=count_type,
                marker=dict(color='black', symbol='circle', size=4),
                showlegend=False)  # Black dots with circle markers
      
            fig.add_trace(trace)
            
        # Display the figure
        st.plotly_chart(fig)
        
        # Forecasted values for the table
        forecasted_values = {
            'Metric': ['Churn Rate', 'Total ACV', 'New Business ACV'],
            'Month 1': [
                forecast_data[forecast_data['simulation'] == selected_simulation]['Churn ACV Rate'].values[0],  # Churn ACV Rate for Month 1
                forecast_data[forecast_data['simulation'] == selected_simulation]['Cumulative Customer ACV'].values[0],  # Cumulative Customer ACV for Month 1
                forecast_data[forecast_data['simulation'] == selected_simulation]['New ACV'].values[0]  # New ACV for Month 1
            ],
            'Month 2': [
                forecast_data[forecast_data['simulation'] == selected_simulation]['Churn ACV Rate'].values[1],  # Churn ACV Rate for Month 2
                forecast_data[forecast_data['simulation'] == selected_simulation]['Cumulative Customer ACV'].values[1],  # Cumulative Customer ACV for Month 2
                forecast_data[forecast_data['simulation'] == selected_simulation]['New ACV'].values[1]  # New ACV for Month 2
            ],
            'Month 3': [
                forecast_data[forecast_data['simulation'] == selected_simulation]['Churn ACV Rate'].values[2],  # Churn ACV Rate for Month 3
                forecast_data[forecast_data['simulation'] == selected_simulation]['Cumulative Customer ACV'].values[2],  # Cumulative Customer ACV for Month 3
                forecast_data[forecast_data['simulation'] == selected_simulation]['New ACV'].values[2]  # New ACV for Month 3
            ]
        }

        # Convert the dictionary to a DataFrame
        forecast_df = pd.DataFrame(forecasted_values)

        # Formatting numbers for better display
        forecast_df['Month 1'] = forecast_df['Month 1'].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)
        forecast_df['Month 2'] = forecast_df['Month 2'].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)
        forecast_df['Month 3'] = forecast_df['Month 3'].apply(lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else x)

        # Display the table under the graph
        st.markdown("### Forecasted Metrics for the Next 3 Months")
        st.dataframe(forecast_df, use_container_width=True)

    else:
        st.write("Please select at least one month.")

    # Hide the raw data (DataFrame)
    st.write("")  # Add empty string to hide the data frame. You can also use st.dataframe(df.head(0)) to hide it.
    
    

elif st.session_state.selected_dashboard == "Usage Dashboard":
    st.title("Usage Dashboard")

    if 'Date' not in df2.columns:  # Check for the "Date" column
        st.error("The DataFrame for Dashboard 2 must have a 'Date' column.")
        st.stop()

    if df2['Date'].dtype!= 'datetime64[ns]':
        df2['Date'] = pd.to_datetime(df2['Date'])  # Convert to datetime if needed
        
        
    # Rename labels
    labels = [col for col in df2.columns if col.endswith('_label')]
    labels.remove('acv_label')
    label_mapping = {
        "raim_abm__num_active_users_label": "active users",
        "num_product1_1_label": "product_1",
        "amount_product1_2_label": "product_2",
        "total_product1_3_created_label": "product_3",
        "product1_3_used_in_any_activation_label": "activation"
    }
    df2.rename(columns=label_mapping, inplace=True)
    labels = [label_mapping[l] for l in labels]
    
    # Extract year and month directly
    df2['year'] = df2['Date'].dt.year
    df2['month'] = df2['Date'].dt.month

    if not labels:
        st.warning("No label columns found in Dashboard 2 data.")

    # Year and Month selection
    years = df2['Date'].dt.year.unique()
    selected_year = st.selectbox("Select Year", years, index=list(years).index(2024) if 2024 in years else 0)  # Default year 2024
    
    months = df2[df2['Date'].dt.year == selected_year]['Date'].dt.month.unique()
    month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                  7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    default_months = ['Nov']  # Default month November

    selected_months = st.multiselect("Select Months", [month_names[m] for m in months], default=default_months)

    # Filter the data based on the selected year and months
    filtered_df2 = df2[
        (df2['Date'].dt.year == selected_year) &
        (df2['Date'].dt.month.isin([m for m, name in month_names.items() if name in selected_months]))
    ]
    
    
    if not filtered_df2.empty:
        # Calculate monthly stats for all labels and categories
        all_monthly_stats = []
        for label in labels:
            # Extract categories from the label column
            categories = filtered_df2[label].unique()

            for category in categories:
                # Use the extracted year and month columns in groupby
                monthly_stats = filtered_df2[filtered_df2[label] == category].groupby(['year', 'month'], as_index=False)[label].count().rename(columns={label: 'Account Count'})
                monthly_stats = monthly_stats.reset_index()
                monthly_stats['Date'] = pd.to_datetime(monthly_stats[['year', 'month']].assign(day=1))
                monthly_stats['Label'] = label  # Add a 'Label' column to identify the label
                monthly_stats['Category'] = category  # Add a 'Category' column
                all_monthly_stats.append(monthly_stats)

        # Combine all monthly stats into a single DataFrame
        all_monthly_stats = pd.concat(all_monthly_stats)

        if not all_monthly_stats.empty:
            # Actionable Insights
            st.subheader("Actionable Insights")
            st.write("- Increasing the number of active users to 4 or above is expected to reduce the likelihood of churn by 28%")
            st.write("- Increasing the activation to 12 or above is expected to reduce the likelihood of churn by 15%")
            st.write("- Reducing the percentage of unused credit to 30% or lower is expected to reduce the likelihood of churn by 8%")
        
            # Display the labels and combined boxes with proper grouping
            for i, label in enumerate(labels):
                st.write(f"<div style='font-weight: bold;'>{label}</div>", unsafe_allow_html=True)

                # Calculate total_accounts for each label separately
                total_accounts = all_monthly_stats[all_monthly_stats['Label'] == label]['Account Count'].sum()

                # Display the combined colored boxes for each category
                filtered_stats = all_monthly_stats[all_monthly_stats['Label'] == label]
                for category, color in [("healthy", "green"), ("normal", "yellow"), ("risky", "red")]:
                    category_stats = filtered_stats[filtered_stats['Category'] == category]
                    st.markdown(f"""
                        <div style="border: 1px solid #ccc; padding: 10px; border-radius: 5px; background-color: {color}; text-align: center; font-size: 14px; display: flex; justify-content: space-between;">
                            <span style="font-weight: bold;">{category} Count: {category_stats['Account Count'].sum()}</span>
                            <span style="font-weight: bold;">{category} Percentage: {category_stats['Account Count'].sum() / total_accounts * 100:.2f}%</span>
                        </div>
                    """, unsafe_allow_html=True)

                # Add spacing between labels
                st.write("")
        
    else:
        st.write("No data available for the selected year and months.")


elif st.session_state.selected_dashboard == "Customer Overview":
    st.title("Customer Overview")

    # Calculate category counts and percentages
    category_counts = df3['predicted_category'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Count']
    category_counts['Percentage'] = (category_counts['Count'] / category_counts['Count'].sum()) * 100

    # Create the bar chart
    color_map = {'risky': 'red', 'adoption': 'orange', 'renewal': 'yellow', 'expansion': 'green'}
    fig = px.bar(category_counts, x='Category', y='Count', color='Category',
                 color_discrete_map=color_map,
                 hover_data=['Percentage'],
                 title="Predicted Category Distribution")

    # Display the chart
    st.plotly_chart(fig, use_container_width=True, key="category_chart")

    # Selection box for category instead of click event
    selected_category = st.selectbox("Select a Category", category_counts['Category'].tolist())

    # Filter the table based on the selected category
    filtered_df3 = df3[df3['predicted_category'] == selected_category]

    # Create the table
    st.subheader("Account Details")
    table_data = filtered_df3[['account_name_s_x', 'Support Score', 'Communication Score', 'Usage Score', 'Contract Score']].copy()
    table_data.rename(columns={'account_name_s_x': 'Account Name'}, inplace=True)

    # Apply conditional formatting to the score columns (excluding Final Score)
    def apply_conditional_formatting(df):
        def style_score(val):
            if val == 'healthy':  # For 'healthy' (green)
                return 'background-color: green; color: white'
            elif val == 'normal':  # For 'normal' (yellow)
                return 'background-color: yellow; color: black'
            elif val == 'risky':  # For 'risky' (red)
                return 'background-color: red; color: white'
            else:
                return ''  # No styling for other values

        # Apply conditional formatting only to the score columns (no color for Final Score)
        score_columns = ['Support Score', 'Communication Score', 'Usage Score', 'Contract Score']
        return df.style.applymap(style_score, subset=score_columns)

    # Apply conditional formatting
    styled_table = apply_conditional_formatting(table_data)

    # Add an empty 'Recommendation' column
    table_data['Recommendation'] = ''

    # Display the formatted table
    st.dataframe(styled_table, use_container_width=True)