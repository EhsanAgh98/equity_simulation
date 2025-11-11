import streamlit as st
import numpy as np

# =======================
# 🎯 Streamlit Page Setup
# =======================
st.set_page_config(page_title="Trading Equity Curve Simulation", layout="centered")

st.title("📊 Trading Equity Curve Simulation")
st.caption("Monte Carlo simulation for trading strategy analysis")

# =======================
# 🔧 User Inputs
# =======================
with st.container():
    st.subheader("Simulation Parameters")

    col1, col2 = st.columns(2)
    with col1:
        win_rate = st.number_input("Win Rate (%)", min_value=0.0, max_value=100.0, value=45.0, step=0.5)
        risk_reward = st.number_input("Risk Reward Ratio (1:X)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
        risk_per_trade = st.number_input("Risk per Trade (%)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    with col2:
        n_trades = st.number_input("Number of Trades", min_value=1, max_value=1000, value=100, step=1)
        initial_capital = st.number_input("Initial Capital ($)", min_value=100.0, value=10000.0, step=100.0)

run_simulation = st.button("🚀 Run Simulation")

# =======================
# 📈 Simulation Logic
# =======================
if run_simulation:
    n_simulations = 1000
    results = []

    for _ in range(n_simulations):
        balance = initial_capital
        balances = [balance]
        for _ in range(int(n_trades)):
            if np.random.rand() < win_rate / 100:
                balance *= (1 + (risk_per_trade / 100) * risk_reward)
            else:
                balance *= (1 - (risk_per_trade / 100))
            balances.append(balance)
        results.append(balances)

    results = np.array(results)

    # =======================
    # 📊 Calculations
    # =======================
    best_result = results[-1].max()
    worst_result = results[-1].min()
    median_result = np.median(results[:, -1])

    best_return = (best_result / initial_capital - 1) * 100
    worst_return = (worst_result / initial_capital - 1) * 100
    median_return = (median_result / initial_capital - 1) * 100

    # Expectancy
    expectancy_r = ((win_rate / 100) * risk_reward) - ((1 - win_rate / 100) * 1)

    # Max drawdown (approximation)
    max_dds = []
    for sim in results:
        peak = sim[0]
        max_dd = 0
        for bal in sim:
            if bal > peak:
                peak = bal
            dd = (peak - bal) / peak
            max_dd = max(max_dd, dd)
        max_dds.append(max_dd)
    avg_drawdown = np.mean(max_dds) * 100

    # =======================
    # 🧾 Results
    # =======================
    st.subheader("Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Start Balance", f"${initial_capital:,.2f}")
        st.metric("Return (Compounded)", f"{median_return:.2f}%")
        st.metric("Expectancy (R)", f"{expectancy_r:.2f}R")

    with col2:
        st.metric("Most Probable End Balance", f"${median_result:,.2f}")
        st.metric("Best Case Return", f"{best_return:.2f}%")
        st.metric("Worst Case Return", f"{worst_return:.2f}%")

    with col3:
        st.metric("Avg Max Drawdown", f"{avg_drawdown:.2f}%")
        st.metric("Simulations Run", f"{n_simulations}")
        st.metric("Number of Trades", f"{int(n_trades)}")
