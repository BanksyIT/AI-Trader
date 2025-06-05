# Placeholder for database.py
"""
database.py
-----------
Handles persistent storage of market data, signals, trades, and metadata using SQLite or PostgreSQL.
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.getenv("DB_PATH", "cache/market_data.db")

class DatabaseClient:
    """
    Basic SQLite client for storing and retrieving market data and signals.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        """Creates required tables if they do not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ohlcv (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                timestamp TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                timeframe TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                timestamp TEXT,
                signal INTEGER,
                strategy TEXT
            )
        ''')
        self.conn.commit()

    def insert_ohlcv(self, df: pd.DataFrame, symbol: str, timeframe: str):
        """Inserts OHLCV records into the database."""
        records = [
            (symbol, str(row['timestamp']), row['open'], row['high'], row['low'], row['close'], row['volume'], timeframe)
            for _, row in df.iterrows()
        ]
        self.cursor.executemany('''
            INSERT INTO ohlcv (symbol, timestamp, open, high, low, close, volume, timeframe)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', records)
        self.conn.commit()

    def insert_signals(self, df: pd.DataFrame, symbol: str, strategy: str):
        """Inserts strategy signals into the database."""
        records = [
            (symbol, str(row['timestamp']), row['signal'], strategy)
            for _, row in df.iterrows()
            if 'signal' in row and row['signal'] != 0
        ]
        self.cursor.executemany('''
            INSERT INTO signals (symbol, timestamp, signal, strategy)
            VALUES (?, ?, ?, ?)
        ''', records)
        self.conn.commit()

    def close(self):
        self.conn.close()
