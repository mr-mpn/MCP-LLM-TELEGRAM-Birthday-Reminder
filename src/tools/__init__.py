from tools.add_birthday import tool_add_birthday, ADD_BIRTHDAY_SCHEMA
from tools.list_birthdays import tool_list_birthdays, LIST_BIRTHDAYS_SCHEMA
from tools.get_birthday import tool_get_birthday, GET_BIRTHDAY_SCHEMA
from tools.delete_birthday import tool_delete_birthday, DELETE_BIRTHDAY_SCHEMA
from tools.update_birthday import tool_update_birthday, UPDATE_BIRTHDAY_SCHEMA
from tools.convert_shamsi_to_miladi import tool_convert_shamsi_to_miladi, CONVERT_SHAMSI_TO_MILADI_SCHEMA

# All available tools for OpenAI function calling
TOOLS = [
    ADD_BIRTHDAY_SCHEMA,
    LIST_BIRTHDAYS_SCHEMA,
    GET_BIRTHDAY_SCHEMA,
    DELETE_BIRTHDAY_SCHEMA,
    UPDATE_BIRTHDAY_SCHEMA,
    CONVERT_SHAMSI_TO_MILADI_SCHEMA,
]

TOOL_HANDLERS = {
    "add_birthday": tool_add_birthday,
    "list_birthdays": tool_list_birthdays,
    "get_birthday": tool_get_birthday,
    "delete_birthday": tool_delete_birthday,
    "update_birthday": tool_update_birthday,
    "convert_shamsi_to_miladi": tool_convert_shamsi_to_miladi,
}
