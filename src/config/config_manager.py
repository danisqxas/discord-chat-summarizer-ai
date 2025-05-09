# Configuration management module
import json
from pathlib import Path

# Configuration keys
API_KEY_CONFIG = "summarizer_api_key"
MODEL_CONFIG = "summarizer_model"
DEBUG_CONFIG = "summarizer_debug"
SUMMARY_CONFIG = "summarizer_summary"
CHANNEL_CONFIG = "summarizer_channel"
MEMORY_LIMIT_CONFIG = "summarizer_memory_limit"
MESSAGE_LIMIT_CONFIG = "summarizer_message_limit"

# Default configuration
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"
DEFAULT_MEMORY_LIMIT = 10
DEFAULT_MESSAGE_LIMIT = 250

# Path to configuration file
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
