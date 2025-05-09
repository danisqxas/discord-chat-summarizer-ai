# History management module
import json
from pathlib import Path
from src.config.config_manager import get_config_data

# Configuration keys
MEMORY_LIMIT_CONFIG = "summarizer_memory_limit"
DEFAULT_MEMORY_LIMIT = 10

# Path to history file
BASE_DIR = Path("json")
HISTORY_FILE = BASE_DIR / "summarizer_history.json"


def ensure_dir():
    """Ensure the directory for JSON files exists."""
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def load_history():
    """Load chat history from the JSON file."""
    ensure_dir()
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
            return history
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_history(history_list):
    """Save chat history to the JSON file, respecting the memory limit."""
    ensure_dir()
    memory_limit = get_config_data().get(MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT)
    message_limit = memory_limit * 2

    if len(history_list) > message_limit:
        to_remove = len(history_list) - message_limit
        if to_remove % 2 != 0:
            to_remove += 1
        history_list = history_list[to_remove:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history_list, f, indent=4)


def reset_history():
    """Reset the chat history."""
    save_history([])
