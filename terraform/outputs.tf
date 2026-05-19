output "api_gateway_url" {
  description = "The URL for the Telegram webhook"
  value       = "${aws_apigatewayv2_stage.default.invoke_url}/webhook"
}

output "chat_lambda_name" {
  description = "Name of the chat handler Lambda function"
  value       = aws_lambda_function.chat_handler.function_name
}

output "reminder_lambda_name" {
  description = "Name of the reminder Lambda function"
  value       = aws_lambda_function.reminder.function_name
}

output "webhook_setup_command" {
  description = "Run this command to set the Telegram webhook"
  value       = "curl -X POST 'https://api.telegram.org/bot${var.telegram_bot_token}/setWebhook?url=${aws_apigatewayv2_stage.default.invoke_url}/webhook'"
  sensitive   = true
}
