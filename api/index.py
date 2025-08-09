"""Serverless entrypoint for Vercel.

This module exposes a ``handler`` function compatible with Vercel's Python
runtime.  Besides a basic health check it also exposes a minimal JSON API that
accepts ``POST`` requests containing a ``text`` field and returns a condensed
summary.  The implementation relies on :mod:`nltk` for an extractive
summarisation algorithm.
"""

from __future__ import annotations

import json
import os
import sys
from http import HTTPStatus

# Ensure the project root is on the import path when executed by Vercel.
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.summarizer import summarize_text


def _json_response(body: dict, status: HTTPStatus = HTTPStatus.OK) -> dict:
    """Return a JSON HTTP response understood by Vercel.

    Parameters
    ----------
    body:
        Dictionary that will be JSON serialised.
    status:
        HTTP status code for the response.
    """

    return {
        "statusCode": int(status),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }


def handler(request):  # pragma: no cover - exercised via tests
    """Entry point for Vercel.

    * ``GET`` requests return a simple health message.
    * ``POST`` requests expect a JSON body with a ``text`` field and return a
      generated summary.
    * ``OPTIONS`` requests are answered to satisfy CORS pre-flight checks.
    """

    method = getattr(request, "method", "GET").upper()

    if method == "OPTIONS":
        return _json_response({}, HTTPStatus.NO_CONTENT)

    if method == "POST":
        try:
            payload = json.loads(getattr(request, "body", "{}"))
        except json.JSONDecodeError:
            return _json_response({"error": "Invalid JSON payload"}, HTTPStatus.BAD_REQUEST)

        text = (payload.get("text") or "").strip()
        if not text:
            return _json_response({"error": "Missing 'text' field"}, HTTPStatus.BAD_REQUEST)

        summary = summarize_text(text)
        return _json_response({"summary": summary})

    # Default to health message for all other methods (e.g. GET)
    return _json_response({"message": "Discord Chat Summarizer API is running"})
