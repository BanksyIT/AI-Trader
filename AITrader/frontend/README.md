# Placeholder for README.md
# AI Trading Bot — Frontend

This module contains the user-facing interfaces to control and monitor the AI Trading Bot system.

## 🧠 Interfaces

### ✅ Telegram Bot
- Command-based interaction
- Supports `/start`, `/run`, `/help`, and future custom commands
- Built using `python-telegram-bot`

### 📊 Streamlit Dashboard
- One-click strategy execution
- Live strategy configuration (exchange, pair, timeframe, strategy)
- Visual signal overlays on price charts

## 🔧 Running Frontend

### Start Telegram Bot
```bash
python -m frontend.telegram.bot_handler
```

### Launch Streamlit Dashboard
```bash
streamlit run frontend/dashboard/app.py
```

## 📁 Structure
```
frontend/
├── telegram/
│   ├── __init__.py
│   ├── bot_handler.py
│   └── commands.py
├── dashboard/
│   ├── __init__.py
│   ├── app.py
│   ├── charts.py
│   └── controls.py
└── README.md
```

---
Designed for modular control of the backend AI trading system.
