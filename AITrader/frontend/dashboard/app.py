import streamlit as st
st.set_page_config(page_title="AI Trading Bot", layout="wide")

from backend.core import CONFIG
from backend.core.orchestrator import TradingOrchestrator
from backend.core.scheduler import StrategyScheduler
from backend.performance_metrics import evaluate_strategy
from frontend.dashboard.controls import strategy_controls
from frontend.dashboard.charts import plot_price_with_signals
from frontend.dashboard.performance import show_performance_summary
from frontend.dashboard.backtest_controls import backtest_controls

st.title("🤖 AI Trading Bot Dashboard")

# Load user-selected config from sidebar
user_config = strategy_controls()
backtest_config = backtest_controls()

# Refresh orchestrator if inputs change
if ("orchestrator" not in st.session_state or
    st.session_state.get("config") != user_config):

    st.session_state.orchestrator = TradingOrchestrator(
        exchange=user_config["exchange"],
        symbol=user_config["symbol"],
        timeframe=user_config["timeframe"],
        strategy_name=user_config["strategy"]
    )
    st.session_state.config = user_config
    st.session_state.scheduler = StrategyScheduler(
        orchestrator=st.session_state.orchestrator,
        interval_minutes=5
    )

st.markdown("---")

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("▶ Run Strategy"):
        with st.spinner("Running strategy..."):
            df = st.session_state.orchestrator.run_once()
            st.success(f"Strategy executed. {len(df)} rows processed.")
            plot_price_with_signals(df)
            show_performance_summary(evaluate_strategy(df))
            st.dataframe(df.tail(20))

    if st.button("🧪 Run Backtest"):
        with st.spinner("Running backtest..."):
            df_bt = st.session_state.orchestrator.run_backtest(
                start_date=backtest_config["start"],
                end_date=backtest_config["end"],
                custom_tf=backtest_config["timeframe"]
            )
            st.success(f"Backtest complete. {len(df_bt)} rows processed.")
            plot_price_with_signals(df_bt)
            show_performance_summary(evaluate_strategy(df_bt))
            st.dataframe(df_bt.tail(20))

with col2:
    if st.toggle("Auto Run (5m)", value=False):
        if not st.session_state.scheduler._running:
            st.session_state.scheduler.start()
    else:
        if st.session_state.scheduler._running:
            st.session_state.scheduler.stop()

st.markdown("---")
st.subheader("Configuration Snapshot")
st.json(user_config)
