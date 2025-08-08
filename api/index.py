"""Serverless entrypoint for Vercel.

This module defines a ``handler`` class compatible with Vercel's Python
Runtime.  It serves a small HTML page on ``GET /`` and exposes a JSON
summarization endpoint on ``POST /summarize``.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from textwrap import dedent

from src.summarizer import summarize


class handler(BaseHTTPRequestHandler):
    """Vercel entrypoint providing a simple summarization API."""

    def do_GET(self):  # noqa: N802 (required name by BaseHTTPRequestHandler)
        if self.path != "/":
            self.send_error(404, "Not found")
            return

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
                  max-width: 480px;
                  width: 100%;
                }
                h1 {
                  color: var(--brand);
                  margin: 0 0 1rem 0;
                }
                textarea {
                  width: 100%;
                  height: 120px;
                }
                button {
                  margin-top: 0.5rem;
                  background: var(--brand);
                  color: #fff;
                  border: none;
                  padding: 0.5rem 1rem;
                  border-radius: 4px;
                  cursor: pointer;
                }
                pre {
                  text-align: left;
                  white-space: pre-wrap;
                }
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
                <p>Service is running. Paste text below to see a naive summary.</p>
                <form id="form">
                  <textarea name="text" required></textarea><br/>
                  <button type="submit">Summarize</button>
                </form>
                <pre id="result"></pre>
                <p><a href="https://github.com/danisqxas/discord-chat-summarizer-ai">View source on GitHub</a></p>
              </main>
              <script>
                const form = document.getElementById('form');
                form.addEventListener('submit', async (e) => {
                  e.preventDefault();
                  const text = form.text.value;
                  const res = await fetch('/summarize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                  });
                  const data = await res.json();
                  document.getElementById('result').textContent = data.summary;
                });
              </script>
            </body>
            </html>
            """
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_POST(self):  # noqa: N802
        if self.path != "/summarize":
            self.send_error(404, "Not found")
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
            text = payload["text"]
        except Exception:  # noqa: BLE001 - we want a generic 400
            self.send_error(400, "Invalid JSON body")
            return

        summary = summarize(text)
        resp = json.dumps({"summary": summary}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)
