"""
trading_service.py
------------------
Manages the end-to-end execution of trading strategies.
Executes futures trades via HTX and CoinEx APIs.
"""

import pandas as pd
import ccxt
import logging
import os

log = logging.getLogger("Trader")

EXCHANGE_KEYS = {
    "htx": {
        "apiKey": os.getenv("HTX_API_KEY"),
        "secret": os.getenv("HTX_SECRET_KEY")
    },
    "coinex": {
        "apiKey": os.getenv("COINEX_API_KEY"),
        "secret": os.getenv("COINEX_SECRET_KEY")
    }
}

class TradingService:
    def __init__(self, exchange: str):
        self.exchange_id = exchange.lower()
        if self.exchange_id not in EXCHANGE_KEYS:
            raise ValueError(f"Unsupported exchange: {exchange}")

        self.exchange = getattr(ccxt, self.exchange_id)({
            "apiKey": EXCHANGE_KEYS[self.exchange_id]["apiKey"],
            "secret": EXCHANGE_KEYS[self.exchange_id]["secret"],
            "enableRateLimit": True,
            "options": {"defaultType": "future"}  # Critical for futures
        })

    def place_futures_order(self, symbol: str, side: str, amount: float, leverage: int = 1,
                             use_pct: float = None, stop_loss: float = None, trailing_stop: float = None):
        try:
            market = self.exchange.market(symbol)
            self.exchange.set_leverage(leverage, symbol)

            balance = self.exchange.fetch_balance({"type": "future"})
            usdt_bal = balance["total"].get("USDT", 0)
            if use_pct:
                amount = round((usdt_bal * use_pct / 100) / market["info"].get("contract_size", 1), 2)

            side_map = {
                "long": "buy",
                "short": "sell"
            }
            order_side = side_map.get(side)
            if order_side is None:
                raise ValueError("Invalid trade signal: must be 'long' or 'short'")

            params = {"reduceOnly": False}
            if stop_loss:
                params["stopPrice"] = stop_loss
            if trailing_stop:
                params["trailingPercent"] = trailing_stop

            log.info(f"📈 Placing {side.upper()} futures order on {symbol}: amt={amount} lev={leverage}")

            order = self.exchange.create_market_order(
                symbol=symbol,
                side=order_side,
                amount=amount,
                params=params
            )
            log.info(f"✅ Order executed: {order['id']}")
        except Exception as e:
            log.error(f"❌ Trade failed: {e}")
