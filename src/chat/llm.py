import json
from openai import OpenAI
from tools import TOOLS, TOOL_HANDLERS


SYSTEM_PROMPT = """
You are a friendly birthday reminder assistant. You help the user manage birthdays of their friends and family.

You can:
- Add new birthdays (ask for the person's name and birthday date)
- List all stored birthdays
- Look up a specific person's birthday
- Delete a birthday

When adding birthdays, always confirm the date format. If the user gives a date like "March 12" without a year, ask for it.
Keep responses concise and friendly. Use emojis occasionally to keep things fun 🎂"""


def chat_with_tools(openai_api_key: str, mongodb_uri: str, user_message: str) -> str:
    """
    Send a user message to OpenAI with tool definitions,
    handle any tool calls, and return the final response.
    """
    client = OpenAI(api_key=openai_api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # First call — may include tool calls
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=TOOLS,
    )

    assistant_message = response.choices[0].message

    # If no tool calls, return the response directly
    if not assistant_message.tool_calls:
        return assistant_message.content

    # Process tool calls
    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Execute the tool
        handler = TOOL_HANDLERS.get(function_name)
        if handler:
            result = handler(mongodb_uri, arguments)
        else:
            result = json.dumps({"error": f"Unknown tool: {function_name}"})

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

    # Second call — LLM generates a natural language response from tool results
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    return final_response.choices[0].message.content
