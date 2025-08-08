# Discord Chat Summarizer AI

This project provides tools for summarizing conversations, targeting Discord chat logs.  
It includes a minimal API endpoint, utility helpers, and an early user interface scaffold.

## Features
- Simple HTTP API for receiving chat messages and returning a placeholder summary.
- Utility helpers for common tasks such as logging and directory creation.
- Basic test suite executed with `pytest`.

## Deployment
Deploying the repository on [Vercel](https://vercel.com) will expose the API at the root URL.
The serverless function lives in `api/index.py` and returns a minimal HTML page
to confirm the deployment is working.

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

