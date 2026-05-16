import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.data_fetcher import DataFetcher
from src.indicators import TechnicalIndicators
from src.strategy_generator import StrategyGenerator
from src.backtester import Backtester

st.set_page_config(page_title="QuantAI Strategy Optimizer", layout="wide")
st.title("📊 QuantAI Strategy Optimizer")
st.markdown("Backtest multiple technical trading strategies on stocks & crypto.")

# Sidebar inputs
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Symbol", value="AAPL", help="e.g., AAPL, MSFT, BTC-USD")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))
compare_all = st.sidebar.checkbox("Compare all strategies", value=True)

# Strategy selection if not compare all
available_strategies = [s["name"] for s in StrategyGenerator.generate_all_strategies()]
if not compare_all:
    selected_strategy = st.sidebar.selectbox("Strategy", available_strategies)
else:
    selected_strategy = None

# Run button
if st.sidebar.button("Run Backtest"):
    with st.spinner("Fetching data..."):
        fetcher = DataFetcher()
        data = fetcher.get_historical_data(
            symbol,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        )
        data = TechnicalIndicators.add_all_indicators(data)

    strategies = StrategyGenerator.generate_all_strategies()
    if not compare_all:
        strategies = [s for s in strategies if s["name"] == selected_strategy]

    with st.spinner("Backtesting..."):
        backtester = Backtester(data, initial_capital=10000)
        results = backtester.test_strategies(strategies)

    # Metrics table
    st.subheader("📈 Performance Metrics")
    metrics_list = [r["metrics"] for r in results]
    df_metrics = pd.DataFrame(metrics_list).set_index("strategy")
    st.dataframe(df_metrics.style.format({
        "total_return": "{:.2%}",
        "win_rate": "{:.2%}",
        "max_drawdown": "{:.2%}",
        "sharpe_ratio": "{:.2f}"
    }))

    # Equity curves chart
    st.subheader("💰 Equity Curves")
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    for r in results:
        ax1.plot(r["equity_curve"], label=r["strategy"])
    ax1.set_title("Equity Curves")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Performance comparison (only if multiple strategies)
    if len(results) > 1:
        st.subheader("⚖️ Performance Comparison")
        fig2, axes = plt.subplots(2, 2, figsize=(14, 10))
        df_comp = df_metrics.copy()
        df_comp["total_return"].plot(kind="bar", ax=axes[0,0], title="Total Return", color="skyblue")
        df_comp["win_rate"].plot(kind="bar", ax=axes[0,1], title="Win Rate", color="lightgreen")
        df_comp["max_drawdown"].plot(kind="bar", ax=axes[1,0], title="Max Drawdown", color="salmon")
        df_comp["sharpe_ratio"].plot(kind="bar", ax=axes[1,1], title="Sharpe Ratio", color="gold")
        plt.tight_layout()
        st.pyplot(fig2)

    # Trades count
    st.subheader("📊 Number of Trades")
    trades_data = {"Strategy": [r["strategy"] for r in results], "Trades": [r["trades"] for r in results]}
    st.dataframe(pd.DataFrame(trades_data))

    st.success("Backtest complete!")