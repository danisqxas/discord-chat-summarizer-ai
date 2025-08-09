import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.index import handler


class DummyRequest:
    def __init__(self, method="GET", body=""):
        self.method = method
        self.body = body


def test_handler_returns_health_message():
    response = handler(DummyRequest())
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"].startswith("Discord Chat Summarizer API")


def test_handler_summarizes_text():
    text = "Sentence one. Sentence two about cats. Sentence three about cats and dogs."
    request = DummyRequest(method="POST", body=json.dumps({"text": text}))
    response = handler(request)
    assert response["statusCode"] == 200
    data = json.loads(response["body"])
    assert "summary" in data
    assert len(data["summary"]) < len(text)
