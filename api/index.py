"""Serverless entrypoint for Vercel.

This module defines a ``handler`` class compatible with Vercel's Python
Runtime.  When deployed, Vercel will instantiate this class to handle incoming
HTTP requests.  The ``do_GET`` method returns a simple HTML page indicating the
API is alive.

The implementation avoids external dependencies so that cold starts remain
fast and the function is unlikely to crash at runtime.
"""

from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    """Vercel entrypoint returning a basic health page."""

    def do_GET(self):  # noqa: N802 (required name by BaseHTTPRequestHandler)
        body = (
            "<html><body><h1>Discord Chat Summarizer API</h1>"
            "<p>Service is running.</p></body></html>"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
