# Discord Chat Summarizer AI

Utilities and example interfaces for summarising chat conversations. The
project exposes a lightweight extractive summariser, a small Tkinter GUI
and a simple command line interface packaged under `chat_summarizer`.

## Features

- **Word-frequency summariser** (`chat_summarizer.summarize_text`).
- **Demo GUI** (`chat_summarizer.ui`) for manually pasting text and
  viewing the summary.
- **Command line interface** (`python -m chat_summarizer`) that reads
  stored history and prints a summary.

## Usage

Summarise stored history for a channel:

```bash
python -m chat_summarizer --channel default
```

Launch the demo GUI:

```bash
python -m chat_summarizer.ui
```

## Development

Run the tests with:

```bash
pytest -q
```
