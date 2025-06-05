"""
performance.py
---------------
Streamlit module to visualize strategy performance.
"""

import streamlit as st
import matplotlib.pyplot as plt

def show_performance_summary(metrics: dict):
    st.subheader("📊 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PnL (%)", f"{metrics['pnl']}%")
    col2.metric("Win Rate", f"{metrics['win_rate']}%")
    col3.metric("Sharpe Ratio", metrics['sharpe'])
    col4.metric("Trades", metrics['trades'])

    # Optional pie chart for wins/losses
    fig, ax = plt.subplots()
    labels = ['Wins', 'Losses']
    sizes = [metrics['win_rate'], 100 - metrics['win_rate']]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)
