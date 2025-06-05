# Placeholder for config.py
"""
config.py
---------
Handles environment configuration and default settings.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file if available
load_dotenv()

DEFAULT_EXCHANGE = os.getenv("DEFAULT_EXCHANGE", "htx")

# Conditional resolution of credentials
if DEFAULT_EXCHANGE == "htx":
    API_KEY = os.getenv("HTX_API_KEY")
    API_SECRET = os.getenv("HTX_SECRET_KEY")
elif DEFAULT_EXCHANGE == "coinex":
    API_KEY = os.getenv("COINEX_API_KEY")
    API_SECRET = os.getenv("COINEX_SECRET_KEY")
else:
    API_KEY = None
    API_SECRET = None

CONFIG = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "CHAT_ID": os.getenv("CHAT_ID"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "LOG_FILE": os.getenv("LOG_FILE", "cache/trading_bot.log"),
    "DB_PATH": os.getenv("DB_PATH", "cache/market_data.db"),
    "DATA_PATH": os.getenv("DATA_PATH", "cache/market_data"),
    "DEFAULT_EXCHANGE": DEFAULT_EXCHANGE,
    "DEFAULT_SYMBOL": os.getenv("DEFAULT_SYMBOL", "BTC/USDT"),
    "DEFAULT_TIMEFRAME": os.getenv("DEFAULT_TIMEFRAME", "1m"),
    "DEFAULT_STRATEGY": os.getenv("DEFAULT_STRATEGY", "sma_crossover")
}
