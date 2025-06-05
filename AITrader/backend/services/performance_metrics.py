"""
performance_metrics.py
----------------------
Calculates strategy performance metrics: PnL, win rate, Sharpe ratio, etc.
"""

import pandas as pd
import numpy as np

def evaluate_strategy(df: pd.DataFrame) -> dict:
    """
    Evaluate strategy performance based on signal-generated trades.
    Assumes 'signal' and 'close' are available in df.
    """
    df = df.copy()
    df = df[df['signal'] != 0]  # only signal points

    if df.empty:
        return {"pnl": 0, "win_rate": 0, "sharpe": 0, "trades": 0}

    df['return'] = df['close'].pct_change().fillna(0)
    df['pnl'] = df['signal'].shift(1) * df['return']  # assume trade executes next candle

    cumulative_return = (df['pnl'] + 1).prod() - 1
    win_rate = (df['pnl'] > 0).sum() / len(df) if len(df) else 0
    sharpe = (df['pnl'].mean() / df['pnl'].std()) * np.sqrt(252) if df['pnl'].std() else 0

    return {
        "pnl": round(cumulative_return * 100, 2),
        "win_rate": round(win_rate * 100, 2),
        "sharpe": round(sharpe, 2),
        "trades": len(df)
    }
