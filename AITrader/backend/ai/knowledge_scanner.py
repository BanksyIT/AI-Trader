"""
knowledge_scanner.py
---------------------
Scans the internet for trading-related content and extracts strategy ideas.
"""

import requests
import logging
from bs4 import BeautifulSoup
from backend.core import CONFIG

log = logging.getLogger("Scanner")

CRYPTO_PANIC_URL = f"https://cryptopanic.com/api/v1/posts/?auth_token={CONFIG['CRYPTOPANIC_API_KEY']}&currencies=BTC,ETH&filter=rising"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (AI Trading Bot)'  # Anti-bot bypass
}

def fetch_trading_articles(limit=5):
    try:
        response = requests.get(CRYPTO_PANIC_URL, headers=HEADERS, timeout=10)
        data = response.json()
        articles = data.get("results", [])[:limit]
        return [article['title'] + " — " + article['url'] for article in articles]
    except Exception as e:
        log.error(f"[Scanner] ❌ Failed to fetch articles: {e}")
        return []

def summarize_article(url: str) -> str:
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs[:5])
        return text.strip()[:1000]
    except Exception as e:
        log.error(f"[Scanner] ❌ Could not summarize article: {e}")
        return ""

def scan_for_strategy_ideas():
    log.info("[Scanner] 🌐 Searching for trading wisdom...")
    articles = fetch_trading_articles()
    summaries = [summarize_article(url.split(" — ")[-1]) for url in articles]
    return summaries
