import json
from src.db.mongo import list_birthdays


LIST_BIRTHDAYS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "list_birthdays",
        "description": "List all stored birthdays. Use this when the user wants to see all the birthdays they have saved.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}


def tool_list_birthdays(mongodb_uri: str, arguments: dict) -> str:
    """Execute the list_birthdays tool."""
    result = list_birthdays(mongodb_uri)
    if not result:
        return json.dumps({"message": "No birthdays stored yet."})
    return json.dumps(result)
