# --- Chat Handler Lambda ---

data "archive_file" "chat_lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/../dist/chat_lambda.zip"
}

resource "aws_lambda_function" "chat_handler" {
  function_name    = "${var.project_name}-chat-handler"
  role             = aws_iam_role.lambda_role.arn
  handler          = "chat.handler.lambda_handler"
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

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.chat_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.telegram_webhook.execution_arn}/*/*"
}

# --- Dependencies Layer ---

resource "aws_lambda_layer_version" "dependencies" {
  layer_name          = "${var.project_name}-dependencies"
  filename            = "${path.module}/../dist/dependencies_layer.zip"
  compatible_runtimes = ["python3.12"]
  description         = "Python dependencies for birthday bot"
}
