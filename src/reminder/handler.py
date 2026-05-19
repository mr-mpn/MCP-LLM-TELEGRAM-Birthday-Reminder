from shared.config import load_config
from db.mongo import get_upcoming_birthdays
from chat.telegram import send_message


def lambda_handler(event, context):
    """
    AWS Lambda handler for the daily birthday reminder.
    Triggered by EventBridge on a cron schedule.
    Checks for upcoming birthdays and sends Telegram notifications.
    """
    config = load_config()
    days_ahead = config["reminder_days_ahead"]

    # Get upcoming birthdays
    upcoming = get_upcoming_birthdays(config["mongodb_uri"], days_ahead)

    if not upcoming:
        return {"statusCode": 200, "body": "No upcoming birthdays."}

    # Build the reminder message
    message = format_reminder_message(upcoming)

    # Send to all allowed users
    for user_id in config["allowed_telegram_ids"]:
        send_message(config["telegram_bot_token"], user_id, message)

    return {
        "statusCode": 200,
        "body": f"Sent reminders for {len(upcoming)} upcoming birthday(s).",
    }


def format_reminder_message(upcoming: list) -> str:
    """Format the upcoming birthdays into a friendly Telegram message."""
    lines = ["🎂 *Birthday Reminder* 🎂\n"]

    for entry in upcoming:
        name = entry["name"]
        days = entry["days_until"]

        if days == 0:
            lines.append(f"🎉 *{name}*'s birthday is TODAY!")
        elif days == 1:
            lines.append(f"⏰ *{name}*'s birthday is TOMORROW!")
        else:
            lines.append(f"📅 *{name}*'s birthday is in *{days} days*")

    return "\n".join(lines)
