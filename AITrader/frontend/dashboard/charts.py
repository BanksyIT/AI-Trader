# Placeholder for charts.py
"""
charts.py
---------
Provides visualizations for market data and signals using Streamlit + Matplotlib.
"""

import matplotlib.pyplot as plt
import streamlit as st

def plot_price_with_signals(df):
    """
    Plots close price over time with buy/sell signals overlaid.
    """
    if df is None or df.empty:
        st.warning("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['timestamp'], df['close'], label='Close Price', linewidth=2)

    if 'signal' in df.columns:
        buys = df[df['signal'] == 1]
        sells = df[df['signal'] == -1]
        ax.scatter(buys['timestamp'], buys['close'], color='green', label='Buy Signal', marker='^')
        ax.scatter(sells['timestamp'], sells['close'], color='red', label='Sell Signal', marker='v')

    ax.set_title("Price Chart with Trading Signals")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
