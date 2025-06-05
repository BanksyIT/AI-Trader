"""
backtest_controls.py
---------------------
Streamlit sidebar inputs for backtesting configuration.
"""

import streamlit as st
import datetime

def backtest_controls():
    st.sidebar.subheader("🧪 Backtest Settings")

    start_date = st.sidebar.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=7))
    end_date = st.sidebar.date_input("End Date", value=datetime.date.today())

    custom_timeframe = st.sidebar.selectbox("Backtest Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=2)

    if start_date > end_date:
        st.sidebar.warning("Start date must be before end date.")

    return {
        "start": start_date,
        "end": end_date,
        "timeframe": custom_timeframe
    }
