# Placeholder for signal_processor.py
"""
signal_processor.py
--------------------
Processes raw strategy signals and converts them into actionable trading decisions
based on current position, risk management rules, and market context.
"""

import pandas as pd

class SignalProcessor:
    """
    Processes strategy signals and determines concrete trade actions.
    """

    def __init__(self, position: int = 0):
        """
        :param position: Current open position (+1 for long, -1 for short, 0 for flat)
        """
        self.position = position

    def process_signals(self, df: pd.DataFrame) -> list:
        """
        Analyzes signal transitions and generates trade instructions.

        :param df: DataFrame with 'signal' column
        :return: List of trade actions: ['BUY', 'SELL', 'HOLD']
        """
        actions = []

        for i in range(1, len(df)):
            prev_sig = df['signal'].iloc[i - 1]
            curr_sig = df['signal'].iloc[i]

            if curr_sig == 1 and self.position <= 0:
                actions.append('BUY')
                self.position = 1
            elif curr_sig == -1 and self.position >= 0:
                actions.append('SELL')
                self.position = -1
            else:
                actions.append('HOLD')

        return actions

    def reset(self):
        """
        Resets the internal position tracker.
        """
        self.position = 0
