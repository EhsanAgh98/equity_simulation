import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# =======================
# 🎯 Streamlit Page Setup
# =======================
st.set_page_config(page_title="Trading Equity Curve Simulation", layout="centered")

st.markdown("<h1 style='text-align: center;'>📊 Trading Equity Curve Simulation</h1>", unsafe_allow_html=True)
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
    drawdowns = []
    consecutive_wins_list = []
    consecutive_losses_list = []

    for _ in range(n_simulations):
        balance = initial_capital
        balances = [balance]
        max_consec_win = 0
        max_consec_loss = 0
        current_win = 0
        current_loss = 0

        peak = balance
        max_dd = 0

        for _ in range(int(n_trades)):
            win = np.random.rand() < win_rate / 100
            if win:
                balance *= (1 + (risk_per_trade / 100) * risk_reward)
                current_win += 1
                max_consec_win = max(max_consec_win, current_win)
                current_loss = 0
            else:
                balance *= (1 - (risk_per_trade / 100))
                current_loss += 1
                max_consec_loss = max(max_consec_loss, current_loss)
                current_win = 0

            peak = max(peak, balance)
            dd = (peak - balance) / peak
            max_dd = max(max_dd, dd)

            balances.append(balance)

        results.append(balances)
        drawdowns.append(max_dd)
        consecutive_wins_list.append(max_consec_win)
        consecutive_losses_list.append(max_consec_loss)

    results = np.array(results)
    end_balances = results[:, -1]

    # =======================
    # 📊 Calculations
    # =======================
    best_result = np.max(end_balances)
    worst_result = np.min(end_balances)
    median_result = np.median(end_balances)

    best_path = results[np.argmax(end_balances)]
    worst_path = results[np.argmin(end_balances)]
    median_path = results[np.argsort(end_balances)[len(end_balances)//2]]

    best_return = (best_result / initial_capital - 1) * 100
    worst_return = (worst_result / initial_capital - 1) * 100
    median_return = (median_result / initial_capital - 1) * 100

    expectancy_r = ((win_rate / 100) * risk_reward) - ((1 - win_rate / 100) * 1)
    avg_drawdown = np.mean(drawdowns) * 100
    avg_max_win = int(np.mean(consecutive_wins_list))
    avg_max_loss = int(np.mean(consecutive_losses_list))

    # =======================
    # 🧾 Results Display
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
        st.metric("Max Consecutive Wins", f"{avg_max_win}")
        st.metric("Max Consecutive Losses", f"{avg_max_loss}")

    # =======================
    # 📉 Graph Display
    # =======================
    st.subheader("Trading Equity Graph Result")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(best_path, color='green', label='Best Case', linewidth=1.8)
    ax.plot(worst_path, color='red', label='Worst Case', linewidth=1.8)
    ax.plot(median_path, color='cyan', label='Most Probable', linewidth=2.5)

    ax.set_title("Trading Equity Curve", color='white', fontsize=13)
    ax.set_xlabel("Number of Trades")
    ax.set_ylabel("Account Balance ($)")
    ax.grid(alpha=0.2)
    ax.legend(facecolor='black', labelcolor='white')
    fig.patch.set_facecolor('#111')
    ax.set_facecolor('#111')
    plt.tick_params(colors='white')

    st.pyplot(fig)




    # =======================
    # 🌐 Clickable Image
    # =======================
    image_url = "https://i.postimg.cc/dVmcGc0j/ytchannel.jpg"
    link_url = "https://www.youtube.com/@zareii.Abbass/videos"

    st.markdown(
        f"""
        <a href="{link_url}" target="_blank">
            <img src="{image_url}" width="400" style="display:block; margin:auto;">
        </a>
        """,
        unsafe_allow_html=True
    )




