# Placeholder for classic.py
"""
classic.py
------------
Contains a collection of time-tested, rule-based trading strategies
implemented with clarity, precision, and extendability in mind.
These act as a base reference for benchmarking AI-generated techniques.
"""

import pandas as pd

class ClassicStrategies:
    @staticmethod
    def sma_crossover(df: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
        """
        Simple Moving Average Crossover strategy.
        Generates buy/sell signals based on SMA crossovers.

        :param df: DataFrame with 'close' price.
        :param short_window: Window size for short-term SMA.
        :param long_window: Window size for long-term SMA.
        :return: DataFrame with 'signal' column.
        """
        df = df.copy()
        df['sma_short'] = df['close'].rolling(window=short_window, min_periods=1).mean()
        df['sma_long'] = df['close'].rolling(window=long_window, min_periods=1).mean()

        df['signal'] = 0
        df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1
        df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1
        return df

    @staticmethod
    def rsi_strategy(df: pd.DataFrame, period: int = 14, lower: float = 30, upper: float = 70) -> pd.DataFrame:
        """
        RSI overbought/oversold strategy.

        :param df: DataFrame with 'close' price.
        :param period: RSI calculation period.
        :param lower: Oversold threshold.
        :param upper: Overbought threshold.
        :return: DataFrame with 'rsi' and 'signal' columns.
        """
        df = df.copy()
        delta = df['close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        df['rsi'] = 100 - (100 / (1 + rs))

        df['signal'] = 0
        df.loc[df['rsi'] < lower, 'signal'] = 1  # Buy
        df.loc[df['rsi'] > upper, 'signal'] = -1  # Sell
        return df

    @staticmethod
    def bollinger_bands(df: pd.DataFrame, window: int = 20, num_std_dev: float = 2) -> pd.DataFrame:
        """
        Bollinger Bands breakout strategy.

        :param df: DataFrame with 'close' price.
        :param window: Rolling window.
        :param num_std_dev: Number of standard deviations for the band.
        :return: DataFrame with bands and 'signal'.
        """
        df = df.copy()
        df['ma'] = df['close'].rolling(window=window).mean()
        df['std'] = df['close'].rolling(window=window).std()
        df['upper_band'] = df['ma'] + num_std_dev * df['std']
        df['lower_band'] = df['ma'] - num_std_dev * df['std']

        df['signal'] = 0
        df.loc[df['close'] < df['lower_band'], 'signal'] = 1  # Buy
        df.loc[df['close'] > df['upper_band'], 'signal'] = -1  # Sell
        return df
