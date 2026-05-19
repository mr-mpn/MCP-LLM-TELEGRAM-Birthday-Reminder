import json
from db.mongo import get_birthday


GET_BIRTHDAY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_birthday",
        "description": "Get a specific person's birthday by their name. Use this when the user asks about a specific person's birthday.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The person's name to look up",
                },
            },
            "required": ["name"],
        },
    },
}


def tool_get_birthday(mongodb_uri: str, arguments: dict) -> str:
    """Execute the get_birthday tool."""
    name = arguments["name"]
    result = get_birthday(mongodb_uri, name)
    if result is None:
        return json.dumps({"message": f"No birthday found for '{name}'."})
    return json.dumps(result)
