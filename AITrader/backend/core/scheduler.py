"""
scheduler.py
-------------
Auto-run strategy orchestrator on a timed interval (e.g., every N minutes).
"""

import threading
import time
import logging

log = logging.getLogger("Scheduler")

class StrategyScheduler:
    def __init__(self, orchestrator, interval_minutes=5):
        self.orchestrator = orchestrator
        self.interval = interval_minutes * 60  # in seconds
        self._running = False
        self._thread = None

    def _run_loop(self):
        while self._running:
            try:
                log.info("[Scheduler] ⏱ Running scheduled strategy...")
                self.orchestrator.run_once()
            except Exception as e:
                log.error(f"[Scheduler] ❌ Error during run: {e}")
            time.sleep(self.interval)

    def start(self):
        if not self._running:
            log.info("[Scheduler] ✅ Scheduler started")
            self._running = True
            self._thread = threading.Thread(target=self._run_loop, daemon=True)
            self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
            log.info("[Scheduler] 🛑 Scheduler stopped")
