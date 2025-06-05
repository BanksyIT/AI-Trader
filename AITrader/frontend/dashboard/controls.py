# Placeholder for controls.py
"""
controls.py
-----------
Reusable Streamlit UI controls for strategy, symbol, and timeframe selection.
"""

import streamlit as st
from backend.data import SUPPORTED_EXCHANGES
from backend.strategies import STRATEGY_REGISTRY

def strategy_controls():
    st.sidebar.header("⚙️ Strategy Configuration")

    exchange = st.sidebar.selectbox("Exchange", list(SUPPORTED_EXCHANGES.keys()))
    symbol = st.sidebar.text_input("Trading Pair", value="BTC/USDT")
    timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h"])
    strategy = st.sidebar.selectbox("Strategy", list(STRATEGY_REGISTRY.keys()))

    return {
        "exchange": SUPPORTED_EXCHANGES[exchange],
        "symbol": symbol,
        "timeframe": timeframe,
        "strategy": strategy
    }
