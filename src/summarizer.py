"""Simple extractive text summarization helper.

The :func:`summarize` function scores sentences based on word frequency and
returns the top ``max_sentences``. It intentionally avoids heavy NLP
dependencies to keep the project lightweight and suitable for serverless
environments.
"""
from __future__ import annotations

import re
from collections import Counter

# Small set of stop words to ignore when scoring sentences. This keeps the
# implementation dependency‑free while offering slightly better summaries than
# returning the first lines verbatim.
STOPWORDS = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "are",
    "is",
    "to",
    "of",
    "in",
    "for",
    "on",
    "with",
    "this",
    "that",
    "it",
    "my",
}


def summarize(text: str, max_sentences: int = 2) -> str:
    """Return a short summary of ``text``.

    Sentences are scored by summing the frequencies of their non-stop-word
    tokens. The highest scoring ``max_sentences`` are returned in their original
    order.
    """
    if max_sentences < 1:
        raise ValueError("max_sentences must be positive")

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
    if not sentences:
        return ""

    words = re.findall(r"\w+", text.lower())
    freqs = Counter(w for w in words if w not in STOPWORDS)

    if not freqs:
        return " ".join(sentences[:max_sentences])

    scored = []
    for idx, sent in enumerate(sentences):
        tokens = re.findall(r"\w+", sent.lower())
        score = sum(freqs.get(tok, 0) for tok in tokens)
        scored.append((score, idx, sent))

    top = sorted(scored, key=lambda x: (-x[0], x[1]))[:max_sentences]
    top.sort(key=lambda x: x[1])
    summary = " ".join(s for _, _, s in top)
    return summary
