# Placeholder for orchestrator.py
"""
orchestrator.py
----------------
The brain of the bot — coordinates data ingestion, strategy evaluation, signal processing, and storage.
"""

from backend.data import MarketDataIngestor, DatabaseClient
from backend.services import TradingService, SignalProcessor

class TradingOrchestrator:
    """
    Master orchestrator to run the entire trading loop.
    """

    def __init__(self, exchange='htx', symbol='BTC/USDT', timeframe='1m', strategy_name='sma_crossover'):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy_name = strategy_name

        self.ingestor = MarketDataIngestor(exchange, symbol, timeframe)
        self.database = DatabaseClient()
        self.trader = TradingService(strategy_name)
        self.signal_processor = SignalProcessor()

    def run_once(self):
        """
        Executes one full cycle: ingest, evaluate, process, store.
        """
        # Step 1: Fetch market data
        df = self.ingestor.fetch_and_store(to_csv=False)

        # Step 2: Generate signals
        df = self.trader.evaluate(df)

        # Step 3: Process signals into trade actions
        actions = self.signal_processor.process_signals(df)
        df = df.iloc[1:]  # Align with actions (signals are delayed by one step)
        df['action'] = actions

        # Step 4: Store signals and OHLCV
        self.database.insert_ohlcv(df, symbol=self.symbol, timeframe=self.timeframe)
        self.database.insert_signals(df, symbol=self.symbol, strategy=self.strategy_name)

        return df

    def shutdown(self):
        """Closes database connections, cleans up resources."""
        self.database.close()
