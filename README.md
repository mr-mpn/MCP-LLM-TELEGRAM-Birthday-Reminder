# Birthday Reminder Bot

A Telegram bot powered by OpenAI that helps you manage and get reminded about upcoming birthdays.

## Architecture

- **Telegram Bot** — Chat interface for managing birthdays + receiving reminders
- **AWS Lambda (Chat)** — Handles Telegram webhook, calls OpenAI with tool definitions
- **AWS Lambda (Reminder)** — Daily cron that checks upcoming birthdays and sends alerts
- **OpenAI API** — LLM for natural language understanding and tool calling
- **MongoDB** — Stores people and their birthdays
- **Terraform** — Infrastructure as code for all AWS resources

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
