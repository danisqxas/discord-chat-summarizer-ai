# Consolidated Chat Summarizer Script
import argparse
import json
import webbrowser
from pathlib import Path

from src.utils import summarize_text

# Configuration management
API_KEY_CONFIG = "summarizer_api_key"
MODEL_CONFIG = "summarizer_model"
CONFIG_FILE = Path("config.json")


# Ensure configuration file exists
def ensure_config_file():
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


# Load configuration
def get_config_data():
    ensure_config_file()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# Update configuration
def update_config_data(key, value):
    config = get_config_data()
    config[key] = value
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


# History management
BASE_DIR = Path("json")
HISTORY_FILE = BASE_DIR / "summarizer_history.json"


def ensure_dir():
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def load_history():
    ensure_dir()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history_list):
    ensure_dir()
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=4)


def reset_history():
    save_history([])


# Mock API interactions
def send_request_to_openrouter(api_url, headers, payload):
    print(f"Mock API call to {api_url} with headers {headers} and payload {payload}")
    return {"status": "success", "data": "This is a mock response."}


# Bot commands
def summarize_command(ctx, args):
    print(f"Summarizing with args: {args}")
    if not args:
        generate_summary(ctx.channel.id)
        return


def generate_summary(channel_id):
    """Generate and print a summary for the provided ``channel_id``.

    Messages are loaded from the history file and summarized using
    :func:`src.utils.summarize_text`.  Each history item can either be a
    plain string or a mapping containing a ``content`` field.
    """

    history = load_history()
    if not history:
        print("No history available to summarise.")
        return

    messages = [
        item["content"] if isinstance(item, dict) and "content" in item else str(item)
        for item in history
    ]
    summary = summarize_text(" ".join(messages))
    print(f"Summary for channel {channel_id}:\n{summary}")


# UI management
def open_router_keys():
    try:
        webbrowser.open("https://openrouter.ai/keys")
    except webbrowser.Error as e:
        print(f"Error opening browser: {e}")


def open_router_models():
    try:
        webbrowser.open("https://openrouter.ai/models")
    except webbrowser.Error as e:
        print(f"Error opening browser: {e}")


# Main script logic
def chat_summarizer_script():
    parser = argparse.ArgumentParser(description="Summarise stored chat history")
    parser.add_argument(
        "--channel", type=str, default="default", help="Channel identifier for the history"
    )
    args = parser.parse_args()

    try:
        print("Chat Summarizer initialized.")
        config = get_config_data()
        print("Loaded config:", config)
        generate_summary(args.channel)
    except ValueError as e:
        print(f"Error: {e}")


# Run the script
if __name__ == "__main__":
    chat_summarizer_script()
