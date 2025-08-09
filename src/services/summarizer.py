"""Text summarisation utilities.

This module exposes a small extractive summariser based on word frequency using
:mod:`nltk`.  It is intentionally lightweight yet provides deterministic
summaries suitable for quick previews on the front-end.
"""

from __future__ import annotations

import heapq
import re
from typing import List

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure required tokenizer models are available at runtime.
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


def _clean_words(words: List[str]) -> List[str]:
    """Return alphanumeric tokens in lower case."""
    return [re.sub(r"[^a-zA-Z0-9]", "", w).lower() for w in words if w.isalnum()]


def summarize_text(text: str, max_sentences: int = 2) -> str:
    """Return an extractive summary of ``text``.

    Parameters
    ----------
    text:
        Text to summarise.
    max_sentences:
        Maximum number of sentences to return in the summary.
    """

    sentences = sent_tokenize(text)
    if not sentences:
        return ""
    if len(sentences) <= max_sentences:
        return text.strip()

    words = _clean_words(word_tokenize(text))
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    sentence_scores = {}
    for idx, sentence in enumerate(sentences):
        for word in _clean_words(word_tokenize(sentence)):
            if word in freq:
                sentence_scores[idx] = sentence_scores.get(idx, 0) + freq[word]

    # Choose the highest scoring sentences and preserve their original order.
    top_indices = sorted(
        heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    )
    summary = " ".join(sentences[i] for i in top_indices)
    return summary.strip()
