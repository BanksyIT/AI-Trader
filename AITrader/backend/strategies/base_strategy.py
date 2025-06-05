# Placeholder for base_strategy.py
"""
base_strategy.py
----------------
Defines the abstract base class for all trading strategies.
This ensures standardization across classic, AI-generated, and RL-based strategies.
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    Enforces structure for signal generation and strategy metadata.
    """

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Core method every strategy must implement.
        It takes historical price data and returns a DataFrame with signals.

        :param df: Historical market data (candlestick format)
        :return: DataFrame with at least a 'signal' column
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable name of the strategy.
        """
        pass

    @property
    def description(self) -> str:
        """
        Optional description of the strategy.
        """
        return "No description provided."

    @property
    def author(self) -> str:
        """
        Optional author or origin of the strategy.
        """
        return "Unknown"
