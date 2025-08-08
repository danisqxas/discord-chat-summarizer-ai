"""Serverless entrypoint for Vercel.

This module defines a ``handler`` class compatible with Vercel's Python
Runtime.  When deployed, Vercel will instantiate this class to handle incoming
HTTP requests.  The ``do_GET`` method returns a simple JSON body indicating the
API is alive.

The implementation avoids external dependencies so that cold starts remain
fast and the function is unlikely to crash at runtime.
"""

from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    """Vercel entrypoint returning a basic health message."""

    def do_GET(self):  # noqa: N802 (required name by BaseHTTPRequestHandler)
        body = json.dumps({"message": "Discord Chat Summarizer API is running"})
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())
