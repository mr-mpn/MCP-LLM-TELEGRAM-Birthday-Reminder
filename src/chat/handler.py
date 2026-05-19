import json
from src.shared.config import load_config
from src.chat.auth import is_authorized
from src.chat.telegram import parse_update, send_message
from src.chat.llm import chat_with_tools


def lambda_handler(event, context):
    """
    AWS Lambda handler for Telegram webhook.
    Receives messages from Telegram, processes them through OpenAI, and responds.
    """
    config = load_config()

    # Parse the incoming Telegram update
    update = parse_update(event)
    if not update:
        return {"statusCode": 200, "body": "OK"}

    user_id = update["user_id"]
    chat_id = update["chat_id"]
    text = update["text"]

    # Check authorization
    if not is_authorized(user_id, config["allowed_telegram_ids"]):
        return {"statusCode": 200, "body": "OK"}

    # Process the message through the LLM with tools
    try:
        response_text = chat_with_tools(
            openai_api_key=config["openai_api_key"],
            mongodb_uri=config["mongodb_uri"],
            user_message=text,
        )
    except Exception as e:
        response_text = f"Sorry, something went wrong: {str(e)}"

    # Send the response back via Telegram
    send_message(config["telegram_bot_token"], chat_id, response_text)

    return {"statusCode": 200, "body": "OK"}
