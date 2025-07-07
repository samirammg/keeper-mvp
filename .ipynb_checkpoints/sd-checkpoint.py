import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Customer Growth Dynamics", layout="wide")

st.title("📈 Customer Growth Dynamics Simulation")
st.markdown("""
Simulate and visualize customer growth over time, transitioning through:
- **Exponential Growth**
- **Saturation (S-Shaped Growth)**
- **Overshoot and Collapse**

Adjust the parameters to see how early interventions can alter the trajectory.
""")

# Sidebar for user inputs
st.sidebar.header("Simulation Parameters")

# Simulation parameters
initial_customers = st.sidebar.number_input("Initial Customers", min_value=1, value=100)
growth_rate = st.sidebar.slider("Growth Rate (%)", min_value=1, max_value=100, value=20)
carrying_capacity = st.sidebar.number_input("Carrying Capacity", min_value=100, value=1000)
churn_rate = st.sidebar.slider("Churn Rate (%)", min_value=0, max_value=100, value=5)
simulation_steps = st.sidebar.slider("Simulation Steps", min_value=10, max_value=200, value=100)

# Convert percentages to decimals
growth_rate /= 100
churn_rate /= 100

# Initialize arrays
customers = [initial_customers]

# Simulation loop
for t in range(1, simulation_steps):
    current_customers = customers[-1]
    # Logistic growth
    growth = growth_rate * current_customers * (1 - current_customers / carrying_capacity)
    # Apply churn
    churn = churn_rate * current_customers
    # Update customer count
    new_customers = current_customers + growth - churn
    customers.append(new_customers)

# Create a DataFrame for plotting
df = pd.DataFrame({
    'Time': range(simulation_steps),
    'Active Customers': customers
})

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Time'], df['Active Customers'], label='Active Customers', color='blue')
ax.axhline(y=carrying_capacity, color='red', linestyle='--', label='Carrying Capacity')
ax.set_xlabel('Time')
ax.set_ylabel('Number of Customers')
ax.set_title('Customer Growth Over Time')
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Interpretation
st.subheader("📊 Interpretation")
if customers[-1] < carrying_capacity * 0.9:
    st.success("The customer base is growing sustainably within the carrying capacity.")
elif customers[-1] >= carrying_capacity * 0.9 and customers[-1] <= carrying_capacity:
    st.warning("The customer base is approaching the carrying capacity. Consider strategies to manage growth.")
else:
    st.error("The customer base has exceeded the carrying capacity, leading to potential collapse. Immediate intervention is required.")
