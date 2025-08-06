# Discord Chat Summarizer AI

Utilities and example interfaces for summarising chat conversations. The
project includes a lightweight extractive summariser, a small Tkinter
GUI and helper scripts for managing configuration and history files.

## Features

- **Word-frequency summariser** implemented in `src.utils.summarize_text`.
- **Demo GUI** (`src/ui.py`) for manually pasting text and seeing the
  summary.
- **Command line script** (`chat_summarizer_v3_optimized.py`) that reads
  stored history and prints a summary.

## Usage

Summarise stored history for a channel:

```bash
python chat_summarizer_v3_optimized.py --channel default
```

Launch the demo GUI:

```bash
python -m src.ui
```

## Development

Run the tests with:

```bash
pytest -q
```
