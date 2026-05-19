def is_authorized(user_id: int, allowed_ids: list[int]) -> bool:
    """Check if a Telegram user is authorized to use the bot."""
    return user_id in allowed_ids
