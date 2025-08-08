import json

def handler(request):
    """Vercel entrypoint returning a basic health message."""
    body = {"message": "Discord Chat Summarizer API is running"}
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
