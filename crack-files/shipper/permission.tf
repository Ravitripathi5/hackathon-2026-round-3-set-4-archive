resource "aws_lambda_permission" "logs" {
  statement_id  = "AllowLogsInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "log-shipper"
  principal     = "logs.amazonaws.com"
}
