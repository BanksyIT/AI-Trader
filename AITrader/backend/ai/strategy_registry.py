"""
strategy_registry.py
--------------------
Registers and manages dynamically generated trading strategies (LLM-based).
"""

from backend.strategies.classic import sma_crossover
from backend.strategies.ai_generated import ai_rsi_boost

STRATEGY_REGISTRY = {
    "sma_crossover": sma_crossover,
    "ai_rsi_boost": ai_rsi_boost
}

def register_strategy(name: str, func) -> None:
    """Registers a new strategy by name."""
    STRATEGY_REGISTRY[name] = func

def get_strategy(name: str):
    """Returns the strategy function for a given name."""
    return STRATEGY_REGISTRY.get(name)

def list_strategies():
    return list(STRATEGY_REGISTRY.keys())
