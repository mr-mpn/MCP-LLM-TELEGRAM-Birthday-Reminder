import json
from db.mongo import add_birthday


ADD_BIRTHDAY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "add_birthday",
        "description": "Add a person's birthday to the database. Use this when the user wants to remember someone's birthday.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The person's name",
                },
                "birthday": {
                    "type": "string",
                    "description": "The birthday in YYYY-MM-DD format",
                },
                "notes": {
                    "type": "string",
                    "description": "Optional notes about the person (e.g., relationship, gift ideas)",
                },
            },
            "required": ["name", "birthday"],
        },
    },
}


def tool_add_birthday(mongodb_uri: str, arguments: dict) -> str:
    """Execute the add_birthday tool."""
    name = arguments["name"]
    birthday = arguments["birthday"]
    notes = arguments.get("notes", "")

    result = add_birthday(mongodb_uri, name, birthday, notes)
    return json.dumps(result)
