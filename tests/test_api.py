"""Tests for the Vercel serverless entrypoint."""

import sys
from io import BytesIO
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.index import handler


class DummyHandler:
    """Minimal stand-in for ``BaseHTTPRequestHandler``.

    Only the methods accessed by :func:`handler.do_GET` are implemented.
    ``wfile`` captures the written response so assertions can be made on it.
    """

    def __init__(self):
        self.wfile = BytesIO()

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
    assert "Discord Chat Summarizer API" in body

