"""
orchestrator.py
----------------
Manages the trading logic: data ingestion, strategy execution, and (now) backtesting + futures execution.
"""

from backend.data.database import MarketDatabase
from backend.data.api_mapper import ExchangeAPIMapper
from backend.services.trading_service import TradingService
from backend.strategies import classic, ai_generated
from backend.ai.strategy_registry import get_strategy
import pandas as pd
import logging

log = logging.getLogger("Orchestrator")

class TradingOrchestrator:
    def __init__(self, exchange: str, symbol: str, timeframe: str, strategy_name: str,
                 trade_enabled=True, amount=1.0, leverage=5, trade_pct=None,
                 stop_loss=None, trailing_stop=None):
        self.exchange = exchange
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy_name = strategy_name
        self.trade_enabled = trade_enabled
        self.amount = amount
        self.leverage = leverage
        self.trade_pct = trade_pct  # Use percent of balance if defined
        self.stop_loss = stop_loss
        self.trailing_stop = trailing_stop

        self.database = MarketDatabase()
        self.api = ExchangeAPIMapper(exchange)
        self.trader = TradingService(exchange)

    def run_once(self) -> pd.DataFrame:
        df = self.api.fetch_ohlcv(self.symbol, self.timeframe)
        self.database.insert_ohlcv(df, symbol=self.symbol, timeframe=self.timeframe)
        strat = get_strategy(self.strategy_name)
        if not strat:
            raise Exception(f"Strategy not found: {self.strategy_name}")

        df = strat(df)

        if self.trade_enabled and "signal" in df.columns and not df.empty:
            last_signal = df.iloc[-1]["signal"]
            if last_signal in ["long", "short"]:
                log.info(f"⚡ Signal detected: {last_signal} — executing futures trade")
                self.trader.place_futures_order(
                    symbol=self.symbol,
                    side=last_signal,
                    amount=self.amount,
                    leverage=self.leverage,
                    use_pct=self.trade_pct,
                    stop_loss=self.stop_loss,
                    trailing_stop=self.trailing_stop
                )

        return df

    def run_backtest(self, start_date, end_date, custom_tf) -> pd.DataFrame:
        log.info(f"[Backtest] Running from {start_date} to {end_date} at {custom_tf}")
        df = self.database.fetch_ohlcv_range(
            symbol=self.symbol,
            timeframe=custom_tf,
            start=start_date,
            end=end_date
        )
        strat = get_strategy(self.strategy_name)
        if not strat:
            raise Exception(f"Strategy not found: {self.strategy_name}")
        return strat(df)
