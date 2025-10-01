"""Service layer for handling API logic.

This module abstracts the details of summarisation and health endpoints from
higher‑level controllers. If in the future you wish to integrate with
external services, this is the place to centralise those interactions. For
now it simply delegates to the local summariser defined in :mod:`src.api`.
"""

from __future__ import annotations

from typing import Iterable

from src import api


async def summarize_messages_async(messages: Iterable[str]) -> dict[str, str]:
    """Asynchronously summarise a collection of messages.

    Although the underlying summarisation is synchronous, this function is
    declared as asynchronous to allow seamless integration with async web
    frameworks (e.g. aiohttp, FastAPI). It simply wraps the synchronous
    call in an awaitable context.

    Parameters
    ----------
    messages : Iterable[str]
        The chat messages to summarise.

    Returns
    -------
    dict[str, str]
        A dictionary containing the generated summary under the ``summary``
        key.
    """
    summary = api.fetch_summary(None, messages)
    return {"summary": summary}


async def health_async() -> dict[str, str]:
    """Return a simple health message.

    This endpoint can be used by monitoring systems to verify the
    application is running.

    Returns
    -------
    dict[str, str]
        A dictionary with a static health message.
    """
    return {"message": "Discord Chat Summarizer API is running"}
