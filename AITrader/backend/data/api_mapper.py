"""
api_mapper.py
-------------
Handles connection and translation between exchange APIs and internal data structures.
Supports multiple exchanges using unified format.
"""

import os
import ccxt
import pandas as pd

SUPPORTED_EXCHANGES = {
    "HTX": "htx",
    "CoinEx": "coinex"
}

class ExchangeAPIMapper:
    """
    A unified interface to pull OHLCV and ticker data from supported exchanges.
    """

    def __init__(self, exchange_name: str = 'htx'):
        if exchange_name not in ccxt.exchanges:
            raise ValueError(f"Exchange '{exchange_name}' not supported by ccxt.")

        self.exchange = getattr(ccxt, exchange_name)({
            'apiKey': os.getenv("API_KEY"),
            'secret': os.getenv("API_SECRET")
        })

    def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', limit: int = 500) -> pd.DataFrame:
        """
        Fetches historical OHLCV data.

        :param symbol: Market pair (e.g. 'BTC/USDT')
        :param timeframe: OHLCV timeframe (e.g. '1m', '5m', '1h')
        :param limit: Number of candles to fetch
        :return: DataFrame with standardized OHLCV columns
        """
        raw = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(raw, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def fetch_ticker(self, symbol: str) -> dict:
        """
        Fetches current ticker info.

        :param symbol: Market pair
        :return: Ticker dictionary
        """
        return self.exchange.fetch_ticker(symbol)

    def list_markets(self) -> list:
        """
        Lists all available markets for the current exchange.

        :return: List of market symbols
        """
        markets = self.exchange.load_markets()
        return list(markets.keys())
