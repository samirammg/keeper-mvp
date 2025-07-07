import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Growth Behaviors", layout="wide")

st.title("📊 Classic System Dynamics Growth Behaviors")

# Parameters
months = 100
initial_active = 100
carrying_capacity = 3000

# Timeline
time = np.arange(months)

# Simulations

def simulate_exponential():
    active = np.zeros(months)
    active[0] = initial_active
    for t in range(1, months):
        new = 0.045 * active[t-1] + 4
        active[t] = active[t-1] + new
    return active

def simulate_s_shaped():
    active = np.zeros(months)
    active[0] = initial_active
    for t in range(1, months):
        growth = 0.06 * active[t-1] * (1 - active[t-1] / carrying_capacity)
        active[t] = active[t-1] + growth
    return active

def simulate_overshoot_collapse():
    active = np.zeros(months)
    active[0] = initial_active
    for t in range(1, months):
        if t < 50:
            growth = 0.07 * active[t-1] * (1 - active[t-1] / carrying_capacity)
            churn = 0
        else:
            growth = 0.01 * active[t-1]  # minimal continued growth
            churn = 0.10 * (active[t-1] - carrying_capacity * 0.5)  # ramped-up churn once past midpoint
            churn = max(churn, 0)
        active[t] = max(active[t-1] + growth - churn, 0)
    return active

# Scenarios
scenarios = {
    "Exponential Growth": simulate_exponential(),
    "S-Shaped Growth": simulate_s_shaped(),
    "Overshoot & Collapse": simulate_overshoot_collapse()
}

# Select and plot
selected = st.selectbox("Select Growth Behavior", list(scenarios.keys()))

st.subheader(f"📈 {selected}")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(time, scenarios[selected], label=selected, linewidth=2)
ax.set_xlabel("Time")
ax.set_ylabel("Active Accounts")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Interpretations
st.subheader("🧠 Insight")
if selected == "Exponential Growth":
    st.markdown("A smooth, accelerating increase in accounts with no constraints — typical of early-stage momentum.")
elif selected == "S-Shaped Growth":
    st.markdown("Growth starts strong and then decelerates as it approaches a natural limit — like saturation or internal bottlenecks.")
elif selected == "Overshoot & Collapse":
    st.markdown("Growth overshoots sustainable limits and then steadily collapses in a smooth bell-shaped pattern under mounting churn pressure.")