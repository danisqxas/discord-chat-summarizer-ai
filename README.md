# Discord Chat Summarizer AI

Utilities and example interfaces for summarising chat conversations. The
project includes a lightweight extractive summariser, a small Tkinter
GUI and a simple command line interface.

## Features

- **Word-frequency summariser** implemented in `src.utils.summarize_text`.
- **Demo GUI** (`src/ui.py`) for manually pasting text and seeing the
  summary.
- **Command line script** (`summarize.py`) that reads stored history and prints a summary.

## Usage

Summarise stored history for a channel:

```bash
python summarize.py --channel default
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
