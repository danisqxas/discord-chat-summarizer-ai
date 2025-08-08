"""Tests for the Vercel serverless entrypoint."""
import json
import sys
from io import BytesIO
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.index import handler


class DummyHandler:
    """Minimal stand-in for ``BaseHTTPRequestHandler``.

    Only the methods accessed by :class:`handler` are implemented. ``wfile``
    captures the written response so assertions can be made on it.
    """

    def __init__(self, path="/", body: bytes | None = None):
        self.path = path
        self.wfile = BytesIO()
        self.headers = {}
        if body is not None:
            self.rfile = BytesIO(body)
            self.headers["Content-Length"] = str(len(body))

    def send_response(self, code):
        self.code = code

    def send_header(self, *args, **kwargs):
        pass

    def end_headers(self):
        pass


def test_handler_returns_health_page():
    dummy = DummyHandler()
    handler.do_GET(dummy)
    dummy.wfile.seek(0)
    body = dummy.wfile.read().decode()
    assert dummy.code == 200
    assert "<title>Discord Chat Summarizer API</title>" in body
    assert "Service is running" in body
    assert "<form" in body


def test_handler_summarizes_text():
    payload = json.dumps({"text": "Hello world. Another sentence."}).encode()
    dummy = DummyHandler(path="/summarize", body=payload)
    handler.do_POST(dummy)
    dummy.wfile.seek(0)
    resp = json.loads(dummy.wfile.read().decode())
    assert dummy.code == 200
    assert resp["summary"] == "Hello world. Another sentence."
