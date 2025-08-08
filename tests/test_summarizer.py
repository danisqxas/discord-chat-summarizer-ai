"""Tests for the simple summarizer utility."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.summarizer import summarize


def test_summarize_picks_relevant_sentences():
    text = (
        "Cats are smart. Dogs are loyal. Cats and dogs are common pets. Birds fly high."
    )
    expected = "Cats are smart. Cats and dogs are common pets."
    assert summarize(text, max_sentences=2) == expected


def test_summarize_rejects_non_positive():
    try:
        summarize("text", max_sentences=0)
    except ValueError:
        assert True
    else:
        assert False
