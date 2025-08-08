# Discord Chat Summarizer AI

This project is a lightweight foundation for a future Discord chat summarizer.
It currently offers a small set of utility helpers and a basic deployment target.

## Features
- Vercel serverless function that renders a friendly HTML status page with a centered card on a gradient background.
- Utility helpers for common tasks such as logging and directory creation.
- Basic test suite executed with `pytest`.

## Deployment
Deploying the repository on [Vercel](https://vercel.com) will expose the status page.
The serverless function in `api/index.py` returns a styled HTML page that confirms
the deployment is working and links back to the source code.

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

