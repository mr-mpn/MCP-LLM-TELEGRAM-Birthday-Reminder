# --- Reminder Lambda ---

resource "aws_lambda_function" "reminder" {
  function_name    = "${var.project_name}-reminder"
  role             = aws_iam_role.lambda_role.arn
  handler          = "reminder.handler.lambda_handler"
  runtime          = "python3.12"
  timeout          = 30
  memory_size      = 256
  filename         = data.archive_file.chat_lambda_zip.output_path
  source_code_hash = data.archive_file.chat_lambda_zip.output_base64sha256

  layers = [aws_lambda_layer_version.dependencies.arn]

  environment {
    variables = {
      TELEGRAM_BOT_TOKEN   = var.telegram_bot_token
      OPENAI_API_KEY       = var.openai_api_key
      MONGODB_URI          = var.mongodb_uri
      ALLOWED_TELEGRAM_IDS = var.allowed_telegram_ids
      REMINDER_DAYS_AHEAD  = tostring(var.reminder_days_ahead)
    }
  }
}

# --- EventBridge Rule (Daily Cron) ---

resource "aws_cloudwatch_event_rule" "daily_reminder" {
  name                = "${var.project_name}-daily-reminder"
  description         = "Triggers the birthday reminder Lambda daily"
  schedule_expression = var.reminder_schedule
}

resource "aws_cloudwatch_event_target" "reminder_target" {
  rule      = aws_cloudwatch_event_rule.daily_reminder.name
  target_id = "reminder-lambda"
  arn       = aws_lambda_function.reminder.arn
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reminder.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_reminder.arn
}
