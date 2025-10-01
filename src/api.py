"""API integration module for the Discord Chat Summarizer.

Historically this module was intended to call an external summarisation
service (e.g. OpenRouter or another hosted model). For the purposes of
this project we avoid external dependencies and instead delegate to the
local summariser implemented in :mod:`src.helpers.utils`. If you wish to
integrate with a remote API in the future, you can extend this module to
handle authentication, request construction and response parsing.
"""

from __future__ import annotations

from typing import Iterable, Optional

from src.helpers.utils import summarize_messages


def fetch_summary(api_key: Optional[str], data: Iterable[str]) -> str:
    """Generate a summary for the provided messages.

    Parameters
    ----------
    api_key : str or None
        An optional API key. It is currently ignored because summarisation
        happens locally. This parameter is retained for API compatibility.
    data : Iterable[str]
        A collection of message strings to be summarised.

    Returns
    -------
    str
        The summary of the messages produced by the local summariser.
    """
    # For now, ignore api_key and use the built‑in summariser
    return summarize_messages(list(data))
