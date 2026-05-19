import json
from db.mongo import update_birthday


UPDATE_BIRTHDAY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "update_birthday",
        "description": "Update an existing person's birthday. Use this when the user wants to change the month or day of someone's birthday.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The person's name to update",
                },
                "month": {
                    "type": "integer",
                    "description": "The new birthday month (1-12)",
                },
                "day": {
                    "type": "integer",
                    "description": "The new birthday day of the month (1-31)",
                },
            },
            "required": ["name", "month", "day"],
        },
    },
}


def tool_update_birthday(mongodb_uri: str, arguments: dict) -> str:
    """Execute the update_birthday tool."""
    name = arguments["name"]
    month = arguments["month"]
    day = arguments["day"]

    success = update_birthday(mongodb_uri, name, month, day)
    if success:
        return json.dumps({"message": f"Updated {name}'s birthday to {month}/{day}."})
    return json.dumps({"message": f"No birthday found for '{name}'."})
