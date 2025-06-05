"""
main.py
--------
Entrypoint for AI trading bot. Runs orchestrator, self-learning, evaluation, Streamlit, and scheduler.
"""

import logging
import threading
import time
import streamlit.web.bootstrap
from backend.core.logger import configure_logging
from backend.core.config import CONFIG
from backend.ai.strategy_synthesizer import auto_generate_strategies
from backend.core.orchestrator import TradingOrchestrator
from backend.core.scheduler import StrategyScheduler
from backend.performance_metrics import evaluate_strategy
from backend.ai.strategy_registry import strategy_registry

log = logging.getLogger("Main")

BEST_STRATEGY_FILE = "cache/best_strategy.txt"


def run_streamlit():
    log.info("🖥️ Launching Streamlit dashboard...")
    streamlit.web.bootstrap.run(
        "frontend/dashboard/app.py",
        f"streamlit run frontend/dashboard/app.py",
        [],
        {}  # No special args
    )


def evaluate_all_strategies(orchestrator: TradingOrchestrator):
    log.info("🧪 Evaluating all available strategies...")
    scores = []
    for name in strategy_registry:
        orchestrator.strategy_name = name
        try:
            df = orchestrator.run_once()

            # Futures-oriented: convert buy/sell → long/short
            if "signal" in df.columns:
                df["signal"] = df["signal"].map({"buy": "long", "sell": "short"}).fillna(df["signal"])

            metrics = evaluate_strategy(df)
            scores.append((name, metrics.get("total_return", 0)))
            log.info(f"🔍 {name}: return={metrics.get('total_return')}")
        except Exception as e:
            log.warning(f"⚠ Failed to evaluate {name}: {e}")
    if scores:
        best = max(scores, key=lambda x: x[1])
        log.info(f"🏆 Best strategy: {best[0]} (return={best[1]})")
        with open(BEST_STRATEGY_FILE, "w") as f:
            f.write(best[0])


def main():
    configure_logging()
    log.info("🚀 Starting AI Trading Bot")

    try:
        threading.Thread(target=run_streamlit, daemon=True).start()

        auto_generate_strategies()

        orchestrator = TradingOrchestrator(
            exchange=CONFIG["DEFAULT_EXCHANGE"],
            symbol=CONFIG["DEFAULT_SYMBOL"],
            timeframe=CONFIG["DEFAULT_TIMEFRAME"],
            strategy_name=CONFIG["DEFAULT_STRATEGY"]
        )

        evaluate_all_strategies(orchestrator)

        scheduler = StrategyScheduler(orchestrator=orchestrator, interval_minutes=60)
        scheduler.start()

        while True:
            time.sleep(10)

    except Exception as e:
        log.error(f"❌ Error in trading bot: {e}")

    log.info("🛑 Shutdown complete.")


if __name__ == "__main__":
    main()
