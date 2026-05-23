import json
from openai import OpenAI
from tools import TOOLS, TOOL_HANDLERS


SYSTEM_PROMPT = """You are a birthday reminder assistant. You help the user manage birthdays of their friends and family.

You can:
- Add new birthdays
- List all stored birthdays in Miladi (Gregorian)
- Look up a specific person's birthday
- Update a birthday
- Delete a birthday
- Convert Shamsi (Jalali/Persian) dates to Miladi (Gregorian) using tools

IMPORTANT RULES:
- Act immediately. Do NOT ask for confirmation. Just do what the user asks.
- We do NOT store chat history, so never ask follow-up questions. If the user provides enough info, execute the action right away.
- If the user says "add Sarah March 12" — just add it. Do not ask "are you sure?" or "shall I proceed?".
- If the user says "delete John" — just delete it.
- If the user says "change Sarah to April 5" — just update it.
- You do NOT need the year. Only the month and day matter.
- We store dates in MILADI (Gregorian) calendar.
- If the user gives a date in SHAMSI (Jalali/Persian) like "1 Ordibehesht", first convert it to Miladi using the convert_shamsi_to_miladi tool, then add it with the Miladi month/day.
- If the user gives a date in Miladi (like "March 12" or "12 January"), just add it directly.
- Keep responses short and confirm what you did.

Use emojis occasionally to keep things fun 🎂"""


def chat_with_tools(openai_api_key: str, mongodb_uri: str, user_message: str) -> str:
    """
    Send a user message to OpenAI with tool definitions,
    handle any tool calls, and return the final response.
    Supports multiple rounds of tool calls (e.g., convert then add).
    """
    client = OpenAI(api_key=openai_api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    # Loop until the LLM gives a final text response (max 5 rounds to prevent infinite loops)
    for _ in range(5):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=TOOLS,
        )

        assistant_message = response.choices[0].message

        # If no tool calls, we're done — return the text response
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

    # Fallback if we hit the loop limit
    return assistant_message.content or "Done!"
