# Set 4 - Log Archive

**Scenario.** Application logs land in CloudWatch Logs. A subscription filter ships them to Lambda, which gunzips/decodes the payload and writes NDJSON under `archive/` in a private S3 bucket that expires those objects after 30 days.

## Part A - Build and deploy (50 points)

| What | Exact name or setting |
|---|---|
| ECR | `h3-<id>-archive`, scan on push **on**, **IMMUTABLE**; image `:v1` |
| App log group | `/h3-<id>/app`, retention 14 |
| Bucket | `h3-<id>-archive-<account-id>` using `local.account_id`; all BPA flags true |
| Lifecycle | Enabled rule: exact prefix `archive/`, expire after 30 days |
| Role | `h3-<id>-archive-role` with the supplied permissions boundary |
| Lambda | `h3-<id>-archive`, Image `:v1`, arm64, env `ARCHIVE_BUCKET`, `APP_VERSION` |
| Lambda logs | `/aws/lambda/h3-<id>-archive`, retention 14 |
| Permission | `logs.amazonaws.com`, scoped to app log-group ARN and source account |
| Subscription | App log group to the archive Lambda |

**Live:** put a log event into `/h3-<id>/app`; an object appears under `archive/` within ~2 minutes; lifecycle rule exists.

Root Dockerfile: Lambda Python 3.12, `handler.lambda_handler`, and `APP_VERSION`. Root `deploy.yml`: tests, OIDC, ECR build/push, Terraform fmt/validate/plan, and no static AWS keys. Terraform must pass fmt/validate and contain no hardcoded account ID or credentials.

Run `python3 tools/check_build.py --id <id>` after deployment.

## Part B / C / Submit
Six `crack-files/` fixes + `FINDINGS.md` + submit. No destroy.
