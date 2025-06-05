# Placeholder for __init__.py
"""
__init__.py
-----------
Initializes the data module and exposes key ingestion and storage components.
"""

from .api_mapper import ExchangeAPIMapper, SUPPORTED_EXCHANGES
from .ingestor import MarketDataIngestor
from .database import DatabaseClient
