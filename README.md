# Birthday Reminder Bot

A Telegram bot powered by OpenAI that helps you manage and get reminded about upcoming birthdays.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          TELEGRAM                                    │
│                                                                     │
│   ┌──────────┐         ┌──────────────┐                            │
│   │   User   │◄───────►│ Telegram Bot │                            │
│   └──────────┘         └──────┬───────┘                            │
│                               │                                     │
└───────────────────────────────┼─────────────────────────────────────┘
                                │ Webhook (HTTPS)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                            AWS                                       │
│                                                                     │
│   ┌───────────────┐    ┌──────────────────┐    ┌────────────────┐  │
│   │ API Gateway   │───►│ Lambda (Chat)    │───►│ OpenAI API     │  │
│   │ POST /webhook │    │                  │◄───│ (gpt-4o-mini)  │  │
│   └───────────────┘    │  ┌────────────┐  │    └────────────────┘  │
│                         │  │ Tools:     │  │                        │
│                         │  │ • add      │  │    ┌────────────────┐  │
│                         │  │ • list     │  │───►│ MongoDB Atlas  │  │
│                         │  │ • get      │  │◄───│ (birthdays)    │  │
│                         │  │ • update   │  │    └────────────────┘  │
│                         │  │ • delete   │  │                        │
│                         │  │ • convert  │  │                        │
│                         │  └────────────┘  │                        │
│                         └──────────────────┘                        │
│                                                                     │
│   ┌───────────────┐    ┌──────────────────┐                        │
│   │ EventBridge   │───►│ Lambda (Reminder)│──► Telegram Bot API    │
│   │ (daily cron)  │    │                  │───► MongoDB Atlas       │
│   └───────────────┘    └──────────────────┘                        │
│                                                                     │
│   Infrastructure managed by Terraform                               │
└─────────────────────────────────────────────────────────────────────┘
```

### Flow: Chat

1. User sends a message in Telegram (e.g. "Add Ali, 1 Ordibehesht")
2. Telegram forwards it to API Gateway via webhook
3. Chat Lambda receives the message, validates the user ID
4. Message is sent to OpenAI with tool definitions
5. OpenAI decides which tools to call (e.g. convert Shamsi → Miladi, then add)
6. Lambda executes the tools against MongoDB
7. OpenAI generates a human-friendly response
8. Lambda sends the response back via Telegram Bot API

### Flow: Daily Reminder

1. EventBridge triggers the Reminder Lambda every day at 8:00 AM UTC
2. Lambda queries MongoDB for birthdays in the next N days
3. Formats a reminder message and sends it to the user via Telegram

## Project Structure

```
├── terraform/          # AWS infrastructure (Lambda, API Gateway, EventBridge, etc.)
├── src/
│   ├── chat/           # Telegram webhook Lambda (message handling, LLM, auth)
│   ├── reminder/       # Daily reminder Lambda
│   ├── tools/          # MCP tools (add, list, get, delete birthdays)
│   ├── db/             # MongoDB connection and queries
│   └── shared/         # Shared config and utilities
├── tests/              # Unit tests
└── requirements.txt    # Python dependencies
```

## Setup

1. Create a Telegram bot via @BotFather
2. Get your OpenAI API key
3. Set up a MongoDB instance (Atlas free tier works)
4. Configure Terraform variables
5. Deploy with `terraform apply`
6. Set the Telegram webhook to your API Gateway URL

## Environment Variables

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `OPENAI_API_KEY` | OpenAI API key |
| `MONGODB_URI` | MongoDB connection string |
| `ALLOWED_TELEGRAM_IDS` | Comma-separated list of allowed user IDs |
| `REMINDER_DAYS_AHEAD` | How many days before a birthday to remind (default: 3) |
