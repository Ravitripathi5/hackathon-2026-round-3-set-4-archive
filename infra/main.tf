# Set 4 - Log Archive.
#
# TODO Log group /${local.prefix}/app
# TODO Subscription filter -> Lambda ${local.prefix}-archive
# TODO aws_lambda_permission for logs.amazonaws.com
# TODO S3 ${local.prefix}-archive with lifecycle expire prefix archive/ after 30 days
# TODO ECR/Lambda/role + BPA + retention 14 on Lambda log group
