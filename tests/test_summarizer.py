"""Tests for the simple summarizer utility."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.summarizer import summarize


def test_summarize_returns_first_sentences():
    text = "One. Two. Three."
    assert summarize(text, max_sentences=2) == "One. Two."


def test_summarize_rejects_non_positive():
    try:
        summarize("text", max_sentences=0)
    except ValueError:
        assert True
    else:
        assert False
