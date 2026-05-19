import json
from src.db.mongo import delete_birthday


DELETE_BIRTHDAY_SCHEMA = {
    "type": "function",
    "function": {
        "name": "delete_birthday",
        "description": "Delete a person's birthday from the database. Use this when the user wants to remove someone's birthday.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The person's name to delete",
                },
            },
            "required": ["name"],
        },
    },
}


def tool_delete_birthday(mongodb_uri: str, arguments: dict) -> str:
    """Execute the delete_birthday tool."""
    name = arguments["name"]
    success = delete_birthday(mongodb_uri, name)
    if success:
        return json.dumps({"message": f"Deleted birthday for '{name}'."})
    return json.dumps({"message": f"No birthday found for '{name}'."})
