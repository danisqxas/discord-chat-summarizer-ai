# Discord Chat Summarizer AI

This project provides tools for summarizing conversations, targeting Discord chat logs.
It includes a JSON API endpoint with an extractive summarisation engine and a very
lightweight web interface for experimenting with the feature.

## Features
- HTTP API (`/api/index`) that accepts chat text and returns a condensed summary.
- Extractive summariser implemented with `nltk` for deterministic results.
- Simple HTML/JS front-end served from `index.html` for manual testing.
- Utility helpers for common tasks such as logging and directory creation.
- Basic test suite executed with `pytest`.

## Deployment
Deploying the repository on [Vercel](https://vercel.com) will expose the static
front-end at the root URL and the API under `/api/index`.
The serverless function lives in `api/index.py` and returns a health message as
well as handling chat summarisation requests.

## Installation
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests
Execute the test suite from the repository root:
```bash
pytest -q
```

## License
This project is provided as-is for educational purposes.

