# Discord Chat Summarizer AI

This project is a lightweight foundation for a future Discord chat summarizer.
It offers a basic summarization endpoint and utility helpers that keep the code
simple and deployment friendly.

## Features
- Vercel serverless function that renders a friendly HTML status page with a
  textarea to experiment with the summarizer.
- JSON API at `/summarize` that performs a small extractive summary of the
  posted text using word-frequency scoring.
- Utility helpers for common tasks such as logging and directory creation.
- Basic test suite executed with `pytest`.

## Deployment
Deploying the repository on [Vercel](https://vercel.com) will expose the status
page and summarization API. The serverless function in `api/index.py` returns a
styled HTML page confirming the deployment is working and includes a simple form
that calls the summarizer.

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
