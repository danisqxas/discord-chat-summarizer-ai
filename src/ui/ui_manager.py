# UI management module
import os


def open_router_keys():
    """Open the OpenRouter keys page in the default browser."""
    try:
        os.startfile("https://openrouter.ai/keys")
        print("Opening OpenRouter API keys page in your browser.")
    except OSError as e:
        print(f"Error opening browser: {e}")


def open_router_models():
    """Open the OpenRouter models page in the default browser."""
    try:
        os.startfile("https://openrouter.ai/models")
        print("Opening OpenRouter models page in your browser.")
    except OSError as e:
        print(f"Error opening browser: {e}")
