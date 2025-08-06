"""Command line interface for the chat summariser package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from .summarizer import summarize_text

HISTORY_FILE = Path("json/summarizer_history.json")


def load_history() -> list:
    """Return stored history entries if the file exists."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def generate_summary(channel_id: str, messages: Iterable[str]) -> str:
    """Summarise ``messages`` and return the resulting text."""
    summary = summarize_text(" ".join(messages))
    return f"Summary for channel {channel_id}:\n{summary}"


def main(argv: list[str] | None = None) -> None:
    """Entrypoint for the CLI."""
    parser = argparse.ArgumentParser(description="Summarise stored chat history")
    parser.add_argument(
        "--channel", type=str, default="default", help="Channel identifier for the history"
    )
    args = parser.parse_args(argv)

    history = load_history()
    if not history:
        print("No history available to summarise.")
        return

    messages = [
        item["content"] if isinstance(item, dict) and "content" in item else str(item)
        for item in history
    ]
    print(generate_summary(args.channel, messages))


__all__ = ["main", "load_history", "generate_summary"]
