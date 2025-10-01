"""Utility functions for the Discord Chat Summarizer.

This module contains reusable helpers that power the core functionality of
the Discord Chat Summarizer. In addition to any generic utility routines,
it also implements a simple extractive summarisation algorithm that can be
used independently of the rest of the project. The summariser does not rely
on any external machine‑learning models or third‑party APIs, making it
portable and easy to deploy in constrained environments.

Functions
---------
summarize_text(text: str, max_sentences: int) -> str
    Produce a concise summary of the given free‑form text using a
    frequency‑based algorithm.

summarize_messages(messages: list[str], max_sentences: int) -> str
    Join a list of messages into a single corpus and summarise it.

clean_word(word: str) -> str
    Normalise a token by stripping punctuation and converting to lower
    case.

split_sentences(text: str) -> list[str]
    Split a text into sentences using simple punctuation cues. This is not
    language aware but works reasonably well for short chat messages.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Iterable, List


# A small set of stop words to ignore when scoring sentences. This list is
# intentionally limited to common English and Spanish stop words to keep the
# summariser lightweight. Additional stop words can be added as needed.
STOP_WORDS: set[str] = {
    "", "the", "and", "a", "an", "in", "on", "at", "for", "to", "of", "is",
    "it", "this", "that", "with", "as", "i", "you", "he", "she", "we", "they",
    "me", "my", "your", "su", "tú", "yo", "él", "ella", "nosotros", "ustedes",
    "de", "la", "el", "los", "las", "y", "en", "un", "una", "por", "que",
    "como", "para", "es", "son", "con", "se", "del", "al", "lo", "sus", "mi"
}

def clean_word(word: str) -> str:
    """Normalise a token by removing punctuation and converting to lower case.

    Parameters
    ----------
    word : str
        The raw token extracted from the input text.

    Returns
    -------
    str
        A cleaned token with punctuation stripped and lowercased.
    """
    return re.sub(r"[^\wáéíóúÁÉÍÓÚñÑ]", "", word).lower()


def split_sentences(text: str) -> List[str]:
    """Split a text into sentences based on punctuation markers.

    The function uses periods, question marks and exclamation marks to
    approximate sentence boundaries. Consecutive whitespace is collapsed.

    Parameters
    ----------
    text : str
        The full body of text to segment.

    Returns
    -------
    list[str]
        A list of sentence strings with leading and trailing whitespace
        removed. Sentences shorter than two characters are discarded.
    """
    # Normalise whitespace
    cleaned = re.sub(r"\s+", " ", text.strip())
    # Split on sentence terminators
    raw_sentences = re.split(r"(?<=[.!?])\s", cleaned)
    return [s.strip() for s in raw_sentences if len(s.strip()) > 1]


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Generate a short extractive summary from a single string of text.

    The summariser works by scoring each sentence according to the
    frequencies of the words it contains. Stop words are ignored and
    punctuation is removed. The highest scoring sentences are returned in
    their original order up to the requested limit.

    Parameters
    ----------
    text : str
        The text to summarise.
    max_sentences : int, optional
        The maximum number of sentences to include in the summary, by
        default 3.

    Returns
    -------
    str
        A summary consisting of the selected sentences joined by a space.
        If the input is too short, the original text is returned.
    """
    sentences = split_sentences(text)
    if not sentences or len(sentences) <= max_sentences:
        return text.strip()

    # Compute word frequencies across all sentences
    freq: Counter[str] = Counter()
    for sentence in sentences:
        words = [clean_word(w) for w in sentence.split()]
        freq.update(w for w in words if w not in STOP_WORDS and w.isalpha())

    if not freq:
        # If no valid words, return the first few sentences as summary
        return " ".join(sentences[:max_sentences])

    # Score sentences by summing word frequencies
    scores: defaultdict[int, float] = defaultdict(float)
    for idx, sentence in enumerate(sentences):
        for word in [clean_word(w) for w in sentence.split()]:
            if word in freq:
                scores[idx] += freq[word]

    # Select top indices
    top_indices = sorted(scores, key=scores.get, reverse=True)[:max_sentences]
    # Preserve original order
    selected = sorted(top_indices)
    return " ".join(sentences[i] for i in selected)


def summarize_messages(messages: Iterable[str], max_sentences: int = 3) -> str:
    """Summarise a list of chat messages into a concise digest.

    Parameters
    ----------
    messages : Iterable[str]
        An iterable of message strings (e.g., chat logs) to summarise.
    max_sentences : int, optional
        The maximum number of sentences in the summary, by default 3.

    Returns
    -------
    str
        A single string representing the summary of the provided messages.
    """
    # Join messages into a single paragraph. Insert periods if missing to
    # ensure proper sentence segmentation.
    joined = ". ".join(msg.strip().rstrip(".?!") for msg in messages) + "."
    return summarize_text(joined, max_sentences=max_sentences)
