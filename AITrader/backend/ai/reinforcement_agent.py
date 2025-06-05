# Placeholder for reinforcement_agent.py
"""
reinforcement_agent.py
----------------------
Defines a simplified reinforcement learning (RL) agent that learns to trade based on market state-reward feedback.
"""

import numpy as np
import pandas as pd

class ReinforcementTradingAgent:
    """
    A simple tabular Q-learning agent for trading environments.
    Not optimized for production — serves as an educational prototype.
    """

    def __init__(self, actions=None, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.actions = actions or ['BUY', 'SELL', 'HOLD']
        self.alpha = alpha    # learning rate
        self.gamma = gamma    # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}     # state -> action -> value

    def _get_state_key(self, row: pd.Series) -> str:
        """Extracts a simple state representation from row."""
        return f"{int(row['close'] > row['open'])}-{int(row['volume'] > 0)}"

    def _choose_action(self, state_key: str) -> str:
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        q_values = self.q_table.get(state_key, {})
        return max(q_values, key=q_values.get, default='HOLD')

    def train(self, df: pd.DataFrame):
        """
        Trains the agent on historical market data.
        """
        df = df.copy()
        df['action'] = 'HOLD'
        df['reward'] = 0

        for i in range(1, len(df)):
            prev_row, row = df.iloc[i - 1], df.iloc[i]
            state_key = self._get_state_key(prev_row)
            next_state_key = self._get_state_key(row)
            action = self._choose_action(state_key)

            reward = row['close'] - prev_row['close'] if action == 'BUY' else prev_row['close'] - row['close']

            df.at[i, 'action'] = action
            df.at[i, 'reward'] = reward

            # Q-learning update
            if state_key not in self.q_table:
                self.q_table[state_key] = {a: 0.0 for a in self.actions}

            next_max_q = max(self.q_table.get(next_state_key, {}).values(), default=0.0)
            old_q = self.q_table[state_key][action]
            new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
            self.q_table[state_key][action] = new_q

        return df[['action', 'reward']]
