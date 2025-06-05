# Placeholder for commands.py
"""
commands.py
-----------
Command definitions and utilities for Telegram bot interactions.
"""

AVAILABLE_COMMANDS = {
    "/start": "Greet the user and describe the bot.",
    "/run": "Run the default trading strategy once.",
    "/status": "Check if the bot is active and responsive.",
    "/help": "List available commands and descriptions."
}

def get_help_message() -> str:
    """
    Generates a help message with available commands.
    """
    help_lines = ["🤖 *Available Commands:*\n"]
    for cmd, desc in AVAILABLE_COMMANDS.items():
        help_lines.append(f"{cmd} — {desc}")
    return "\n".join(help_lines)


def is_authorized(user_id: int, authorized_id: int) -> bool:
    """
    Simple authorization check (useful for production bots).
    """
    return user_id == authorized_id
