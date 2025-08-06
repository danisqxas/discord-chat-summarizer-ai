"""Utility helpers for the chat summarizer project.

This module centralises small helper routines used across the
codebase.  Besides providing a tiny ``debug_log`` helper it also
implements a lightweight extractive text summariser that does not rely
on heavy external dependencies.  The summariser ranks sentences based
on word frequency and returns the most relevant ones.
"""

from __future__ import annotations

from collections import Counter
import re
from typing import Iterable, List


# Basic Spanish and English stopwords to filter uninformative terms.
STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "are",
    "be",
    "de",
    "el",
    "en",
    "for",
    "in",
    "is",
    "it",
    "la",
    "of",
    "on",
    "que",
    "the",
    "to",
    "un",
    "una",
    "with",
    "y",
}


def debug_log(message: str) -> None:
    """Print a debug message.

    Parameters
    ----------
    message:
        Text to print with a ``DEBUG`` prefix.  Using a function makes it
        simple to extend with proper logging in the future.
    """

    print(f"DEBUG: {message}")


def _tokenise(text: str) -> Iterable[str]:
    """Yield lowercase tokens for ``text`` without stopwords."""

    for token in re.findall(r"\w+", text.lower()):
        if token not in STOPWORDS:
            yield token


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Return an extractive summary of ``text``.

    The algorithm scores sentences by the frequency of their significant
    words.  The highest scoring ``max_sentences`` sentences are returned
    in their original order.  The approach is intentionally simple yet
    surprisingly effective for short snippets of text.

    Parameters
    ----------
    text:
        Input text to summarise.
    max_sentences:
        Maximum number of sentences to return.
    """

    sentences: List[str] = re.split(r"(?<=[.!?])\s+", text.strip())
    if not sentences:
        return ""

    word_frequencies = Counter()
    for sentence in sentences:
        word_frequencies.update(_tokenise(sentence))

    if not word_frequencies:
        return sentences[0]

    scored_sentences = []
    for idx, sentence in enumerate(sentences):
        tokens = list(_tokenise(sentence))
        if not tokens:
            score = 0
        else:
            score = sum(word_frequencies[t] for t in tokens) / len(tokens)
        scored_sentences.append((score, idx, sentence))

    # Select top sentences by score and restore original order.
    top_sentences = sorted(scored_sentences, key=lambda s: s[0], reverse=True)[:max_sentences]
    ordered = [sent for _, _, sent in sorted(top_sentences, key=lambda s: s[1])]
    return " ".join(ordered)


__all__ = ["debug_log", "summarize_text"]
