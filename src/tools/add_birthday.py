import json
from db.mongo import add_birthday


ADD_BIRTHDAY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_birthday",
        "description": "Add a person's birthday to the database. Only call this when you have BOTH the person's name AND their birthday (month and day).",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The person's name",
                },
                "month": {
                    "type": "integer",
                    "description": "The birthday month (1-12)",
                },
                "day": {
                    "type": "integer",
                    "description": "The birthday day of the month (1-31)",
                },
            },
            "required": ["name", "month", "day"],
        },
    },
}


def tool_add_birthday(mongodb_uri: str, arguments: dict) -> str:
    """Execute the add_birthday tool."""
    name = arguments["name"]
    month = arguments["month"]
    day = arguments["day"]

    result = add_birthday(mongodb_uri, name, month, day)
    return json.dumps(result)
