variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "birthday-bot"
}

variable "telegram_bot_token" {
  description = "Telegram bot token from @BotFather"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}

variable "mongodb_uri" {
  description = "MongoDB connection string"
  type        = string
  sensitive   = true
}

variable "allowed_telegram_ids" {
  description = "Comma-separated list of allowed Telegram user IDs"
  type        = string
}

variable "reminder_days_ahead" {
  description = "How many days before a birthday to send a reminder"
  type        = number
  default     = 3
}

variable "reminder_schedule" {
  description = "Cron expression for the reminder schedule (UTC)"
  type        = string
  default     = "cron(0 8 * * ? *)" # Every day at 8:00 AM UTC
}
