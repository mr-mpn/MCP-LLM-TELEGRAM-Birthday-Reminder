import requests
from typing import Optional


def parse_update(event: dict) -> Optional[dict]:
    """
    Parse a Telegram webhook update and extract the message info.

    Returns a dict with user_id, chat_id, and text, or None if not a text message.
    """
    import json

    body = json.loads(event.get("body", "{}"))

    message = body.get("message")
    if not message:
        return None

    text = message.get("text")
    if not text:
        return None

    return {
        "user_id": message["from"]["id"],
        "chat_id": message["chat"]["id"],
        "text": text,
        "first_name": message["from"].get("first_name", ""),
    }


def send_message(bot_token: str, chat_id: int, text: str) -> dict:
    """Send a message via the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload, timeout=10)
    return response.json()
