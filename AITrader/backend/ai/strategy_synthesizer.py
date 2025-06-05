"""
strategy_synthesizer.py
------------------------
Generates strategy code from ideas using LLM and registers it live.
"""

import openai
import logging
from backend.ai.strategy_registry import register_strategy
from backend.core import CONFIG
from backend.ai.knowledge_scanner import scan_for_strategy_ideas

log = logging.getLogger("Synthesizer")

openai.api_key = CONFIG.get("OPENAI_API_KEY", "")

SYSTEM_PROMPT = """
You are a quantitative trading assistant. Based on the given insight, generate a simple Python trading strategy function that takes a pandas DataFrame with OHLCV data and returns the same DataFrame with a new 'signal' column containing 'buy', 'sell', or None.
"""

def synthesize_strategy_from_text(text: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        log.error(f"[Synthesizer] ❌ LLM failed: {e}")
        return ""

def auto_generate_strategies():
    ideas = scan_for_strategy_ideas()
    for idx, idea in enumerate(ideas):
        code = synthesize_strategy_from_text(idea)
        name = f"llm_auto_{idx}"
        try:
            local_scope = {}
            exec(code, {}, local_scope)
            strategy_fn = next(v for v in local_scope.values() if callable(v))
            register_strategy(name, strategy_fn)
            log.info(f"[Synthesizer] ✅ Strategy registered: {name}")
        except Exception as e:
            log.warning(f"[Synthesizer] ⚠ Could not load strategy {name}: {e}")
