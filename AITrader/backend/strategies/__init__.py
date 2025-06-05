# Placeholder for __init__.py
"""
__init__.py
-----------
Initializes the strategies module and provides factory logic to load strategies dynamically.
"""

from .classic import ClassicStrategies
from .ai_generated import AILearnedMomentum, AIGeneratedExperiment


# Optional registry to manage available strategies
STRATEGY_REGISTRY = {
    "sma_crossover": ClassicStrategies.sma_crossover,
    "rsi_strategy": ClassicStrategies.rsi_strategy,
    "bollinger_bands": ClassicStrategies.bollinger_bands,
    "ai_momentum": AILearnedMomentum(),
    # Dynamic strategies can be loaded manually
}

def get_strategy(name: str):
    """
    Retrieve a strategy by name from the registry.

    :param name: Key in STRATEGY_REGISTRY
    :return: Callable or BaseStrategy instance
    """
    return STRATEGY_REGISTRY.get(name)
