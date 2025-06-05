# Placeholder for ingestor.py
"""
ingestor.py
-----------
Fetches, processes, and stores historical or live market data from supported exchanges.
Can be scheduled or triggered manually.
"""

import os
import pandas as pd
from backend.data.api_mapper import ExchangeAPIMapper

DATA_PATH = os.getenv("DATA_PATH", "cache/market_data")
os.makedirs(DATA_PATH, exist_ok=True)

class MarketDataIngestor:
    """
    Ingests market data from exchange APIs and optionally stores it locally.
    """

    def __init__(self, exchange: str = 'htx', symbol: str = 'BTC/USDT', timeframe: str = '1m'):
        self.mapper = ExchangeAPIMapper(exchange)
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch_and_store(self, limit: int = 500, to_csv: bool = True) -> pd.DataFrame:
        """
        Downloads and optionally saves OHLCV data.

        :param limit: Number of candles to fetch
        :param to_csv: Whether to store as CSV
        :return: Fetched DataFrame
        """
        df = self.mapper.fetch_ohlcv(symbol=self.symbol, timeframe=self.timeframe, limit=limit)

        if to_csv:
            filename = f"{self.symbol.replace('/', '_')}_{self.timeframe}.csv"
            path = os.path.join(DATA_PATH, filename)
            df.to_csv(path, index=False)

        return df

    def get_markets(self) -> list:
        """
        Lists all tradable symbols on the configured exchange.
        """
        return self.mapper.list_markets()
