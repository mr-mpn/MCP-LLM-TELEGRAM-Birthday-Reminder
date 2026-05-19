from src.tools.add_birthday import tool_add_birthday, ADD_BIRTHDAY_SCHEMA
from src.tools.list_birthdays import tool_list_birthdays, LIST_BIRTHDAYS_SCHEMA
from src.tools.get_birthday import tool_get_birthday, GET_BIRTHDAY_SCHEMA
from src.tools.delete_birthday import tool_delete_birthday, DELETE_BIRTHDAY_SCHEMA

# All available tools for OpenAI function calling
TOOLS = [
    ADD_BIRTHDAY_SCHEMA,
    LIST_BIRTHDAYS_SCHEMA,
    GET_BIRTHDAY_SCHEMA,
    DELETE_BIRTHDAY_SCHEMA,
]

TOOL_HANDLERS = {
    "add_birthday": tool_add_birthday,
    "list_birthdays": tool_list_birthdays,
    "get_birthday": tool_get_birthday,
    "delete_birthday": tool_delete_birthday,
}
