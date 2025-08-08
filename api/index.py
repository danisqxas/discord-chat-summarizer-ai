"""Serverless entrypoint for Vercel.

This module defines a ``handler`` class compatible with Vercel's Python
Runtime.  When deployed, Vercel will instantiate this class to handle incoming
HTTP requests.  The ``do_GET`` method returns a simple HTML page indicating the
API is alive.

The implementation avoids external dependencies so that cold starts remain
fast and the function is unlikely to crash at runtime.
"""

from http.server import BaseHTTPRequestHandler
from textwrap import dedent


class handler(BaseHTTPRequestHandler):
    """Vercel entrypoint returning a styled status page."""

    def do_GET(self):  # noqa: N802 (required name by BaseHTTPRequestHandler)
        body = dedent(
            """
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="utf-8"/>
              <title>Discord Chat Summarizer API</title>
              <style>
                :root {
                  --brand: #5865F2;
                  --bg: #23272a;
                  --card-bg: #ffffff;
                }
                body {
                  font-family: system-ui, sans-serif;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                  min-height: 100vh;
                  margin: 0;
                  background: linear-gradient(135deg, var(--brand), var(--bg));
                }
                .card {
                  background: var(--card-bg);
                  padding: 2rem 3rem;
                  border-radius: 12px;
                  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
                  text-align: center;
                }
                h1 {
                  color: var(--brand);
                  margin: 0;
                }
                p { margin-top: 0.5rem; }
                a {
                  color: var(--brand);
                  text-decoration: none;
                }
                a:hover { text-decoration: underline; }
              </style>
            </head>
            <body>
              <main class="card">
                <h1>Discord Chat Summarizer API</h1>
                <p>Service is running.</p>
                <p><a href="https://github.com/danisqxas/discord-chat-summarizer-ai">View source on GitHub</a></p>
              </main>
            </body>
            </html>
            """
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
