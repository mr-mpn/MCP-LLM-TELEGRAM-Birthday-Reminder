import os


def load_config() -> dict:
    """Load configuration from environment variables."""
    config = {
        "telegram_bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
        "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
        "mongodb_uri": os.environ.get("MONGODB_URI", ""),
        "allowed_telegram_ids": [],
        "reminder_days_ahead": int(os.environ.get("REMINDER_DAYS_AHEAD", "3")),
    }

    # Parse allowed Telegram IDs
    ids_str = os.environ.get("ALLOWED_TELEGRAM_IDS", "")
    if ids_str:
        config["allowed_telegram_ids"] = [
            int(id.strip()) for id in ids_str.split(",") if id.strip()
        ]

    return config
