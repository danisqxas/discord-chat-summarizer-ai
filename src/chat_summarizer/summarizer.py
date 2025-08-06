"""Core summarisation utilities for the chat summariser package."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import logging
import re
from typing import Iterable, List, Sequence, Set

# Configure a module level logger. Applications embedding the library
# can configure logging as desired; by default nothing is output.
logger = logging.getLogger(__name__)

# Basic Spanish and English stopwords to filter uninformative terms.
DEFAULT_STOPWORDS: Set[str] = {
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

# Alias maintained for backwards compatibility
STOPWORDS = DEFAULT_STOPWORDS


def debug_log(message: str) -> None:
    """Log ``message`` at debug level.

    Abstracted behind a function so tests or applications can easily mock or
    redirect the logging behaviour without altering callers.
    """

    logger.debug(message)


def _tokenise(text: str, stopwords: Set[str]) -> Iterable[str]:
    """Yield lowercase tokens for ``text`` without stopwords."""

    for token in re.findall(r"\w+", text.lower()):
        if token not in stopwords:
            yield token


@dataclass(order=True)
class Sentence:
    """Container used for ranking sentences by score and position."""

    score: float
    index: int
    text: str


def summarize_text(
    text: str,
    max_sentences: int = 3,
    stopwords: Sequence[str] | None = None,
) -> str:
    """Return an extractive summary of ``text``.

    Sentences are ranked by the frequency of their significant words.  The
    highest scoring ``max_sentences`` sentences are returned in their original
    order.  The approach is intentionally simple yet effective for short
    snippets of text.
    """

    sentences: List[str] = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    if not sentences or max_sentences <= 0:
        return ""

    stopwords_set = set(stopwords) if stopwords is not None else STOPWORDS
    word_frequencies = Counter()
    for sentence in sentences:
        word_frequencies.update(_tokenise(sentence, stopwords_set))

    if not word_frequencies:
        return sentences[0]

    scored_sentences: List[Sentence] = []
    for idx, sentence in enumerate(sentences):
        tokens = list(_tokenise(sentence, stopwords_set))
        score = sum(word_frequencies[t] for t in tokens) / len(tokens) if tokens else 0
        scored_sentences.append(Sentence(score, idx, sentence))

    top_sentences = sorted(scored_sentences, key=lambda s: (-s.score, s.index))[:max_sentences]
    ordered = [s.text for s in sorted(top_sentences, key=lambda s: s.index)]
    return " ".join(ordered)


__all__ = ["debug_log", "summarize_text", "STOPWORDS"]
