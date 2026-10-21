# Set 4 - Log Archive

**Scenario.** Application logs land in CloudWatch Logs. A subscription filter ships them to Lambda, which gunzips/decodes the payload and writes NDJSON under `archive/` in a private S3 bucket that expires those objects after 30 days.

## Part A names
| Resource | Name |
|---|---|
| App log group | `/h3-<id>/app` |
| Lambda / ECR / role | `h3-<id>-archive` (+ `-role`) |
| Bucket | `h3-<id>-archive` (BPA all true, lifecycle `archive/` → expire 30 days) |
| Permission | `logs.amazonaws.com` may invoke the function |

**Live:** put a log event into `/h3-<id>/app`; an object appears under `archive/` within ~2 minutes; lifecycle rule exists.

Same Dockerfile / IMMUTABLE ECR / OIDC CI rules as other sets.

## Part B / C / Submit
Six `crack-files/` fixes + `FINDINGS.md` + submit. No destroy.
