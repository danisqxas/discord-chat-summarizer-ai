"""Simple text summarization helper.

The ``summarize`` function takes a block of text and returns the first few
sentences.  It intentionally avoids heavy NLP dependencies to keep the
project lightweight and suitable for serverless environments.
"""
from __future__ import annotations

import re


def summarize(text: str, max_sentences: int = 2) -> str:
    """Return the first ``max_sentences`` sentences from ``text``.

    Sentences are naively split on punctuation (``.?!``) followed by a space.
    ``max_sentences`` controls how many sentences are returned.
    """
    if max_sentences < 1:
        raise ValueError("max_sentences must be positive")

    sentences = re.split(r"(?<=[.!?]) +", text.strip())
    summary = " ".join(sentences[:max_sentences]).strip()
    return summary
