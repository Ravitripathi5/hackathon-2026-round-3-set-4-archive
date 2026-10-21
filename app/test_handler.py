import base64
import gzip
import json
import os
import unittest
from unittest import mock

os.environ["ARCHIVE_BUCKET"] = "h3-p01-archive"
os.environ["APP_VERSION"] = "v1"

import handler  # noqa: E402


def encode(payload):
    return base64.b64encode(gzip.compress(json.dumps(payload).encode("utf-8"))).decode("ascii")


class ArchiveTests(unittest.TestCase):
    def test_writes_ndjson(self):
        payload = {
            "logGroup": "/h3-p01/app",
            "logStream": "s1",
            "logEvents": [{"id": "1", "timestamp": 1, "message": "hello"}],
        }
        event = {"awslogs": {"data": encode(payload)}}
        with mock.patch.object(handler, "s3") as s3:
            res = handler.lambda_handler(event, None)
        self.assertTrue(res["ok"])
        kwargs = s3.return_value.put_object.call_args.kwargs
        self.assertTrue(kwargs["Key"].startswith("archive/"))
        self.assertIn("hello", kwargs["Body"].decode("utf-8"))

    def test_missing_data(self):
        with self.assertRaises(ValueError):
            handler.lambda_handler({}, None)


if __name__ == "__main__":
    unittest.main()
