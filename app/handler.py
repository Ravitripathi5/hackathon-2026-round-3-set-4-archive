"""Log Archive - decode CloudWatch Logs subscription payload, write NDJSON to S3."""
import base64
import gzip
import json
import os
import time

BUCKET = os.environ.get("ARCHIVE_BUCKET", "")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_client = None


def s3():
    global _client
    if _client is None:
        import boto3
        _client = boto3.client("s3")
    return _client


def decode_awslogs(event):
    raw = event.get("awslogs", {}).get("data")
    if not raw:
        raise ValueError("missing awslogs.data")
    payload = gzip.decompress(base64.b64decode(raw))
    return json.loads(payload.decode("utf-8"))


def lambda_handler(event, context):
    data = decode_awslogs(event)
    lines = []
    for item in data.get("logEvents") or []:
        lines.append(json.dumps({
            "id": item.get("id"),
            "timestamp": item.get("timestamp"),
            "message": item.get("message"),
            "logGroup": data.get("logGroup"),
            "logStream": data.get("logStream"),
            "version": APP_VERSION,
        }, separators=(",", ":")))
    body = "\n".join(lines) + ("\n" if lines else "")
    key = "archive/{0}-{1}.ndjson".format(int(time.time()), data.get("logStream", "stream"))
    s3().put_object(Bucket=BUCKET, Key=key, Body=body.encode("utf-8"), ContentType="application/x-ndjson")
    return {"ok": True, "key": key, "count": len(lines)}
