# Placeholder for bot_handler.py
"""
bot_handler.py
--------------
Initializes and runs the Telegram bot interface for remote control of the trading system.
"""

import os
from telegram.ext import Updater, CommandHandler
from backend.core import CONFIG, get_logger
from backend.core.orchestrator import TradingOrchestrator

logger = get_logger("TelegramBot")


def start(update, context):
    update.message.reply_text("👋 Welcome to the AI Trading Bot! Type /run to execute a strategy.")


def run(update, context):
    update.message.reply_text("⏳ Running trading strategy...")
    try:
        orchestrator = TradingOrchestrator(
            exchange=CONFIG["DEFAULT_EXCHANGE"],
            symbol=CONFIG["DEFAULT_SYMBOL"],
            timeframe=CONFIG["DEFAULT_TIMEFRAME"],
            strategy_name=CONFIG["DEFAULT_STRATEGY"]
        )
        df = orchestrator.run_once()
        update.message.reply_text(f"✅ Done! {len(df)} records processed.")
    except Exception as e:
        logger.error(f"Telegram error: {e}")
        update.message.reply_text(f"❌ Error: {e}")
    finally:
        orchestrator.shutdown()


def init_bot():
    updater = Updater(token=os.getenv("TELEGRAM_TOKEN"), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("run", run))

    logger.info("🤖 Telegram bot started.")
    updater.start_polling()
    updater.idle()
