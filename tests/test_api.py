import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.index import handler


class DummyRequest:
    def __init__(self):
        self.method = "GET"


def test_handler_returns_health_message():
    response = handler(DummyRequest())
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"].startswith("Discord Chat Summarizer API")
