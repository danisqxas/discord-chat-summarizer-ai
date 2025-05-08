@aerthexscript(
    name="Chat Summarizer v2.7",
    author="thedorekaczynski",
    description="Chat with and summarize the last 250 messages using OpenRouter API with chat history support and UI",
    usage="""<p>summarize - Generate a summary of the last 250 messages in the current channel
<p>summarize --channel <channel_id> - Generate a summary of the last 250 messages in the specified channel
<p>summarize chat <message> - Chat with the full logs of the last 250 messages (requires a summary to be generated first)
<p>summarize status - Show current configuration
<p>summarize reset - Reset the chat history
""",
)
def chat_summarizer_script():
    """
    CHAT SUMMARIZER SCRIPT
    ---------------------

    This script allows you to generate a summary of the last 250 messages in a channel
    and then chat with the full logs using the OpenRouter API.

    SETUP:
    1. You must set your OpenRouter API key using the UI tab
    2. Get your API key at: https://openrouter.ai/keys

    COMMANDS:
    <p>summarize - Generate a summary of the last 250 messages in the current channel
    <p>summarize --channel <channel_id> - Generate a summary of the last 250 messages in the specified channel
    <p>summarize chat <message> - Chat with the full logs of the last 250 messages (requires a summary to be generated first)
    <p>summarize status - Show current configuration
    <p>summarize reset - Reset the chat history

    EXAMPLES:
    <p>summarize - Generate a summary of the last 250 messages
    <p>summarize --channel 1234567890 - Generate a summary for channel with ID 1234567890
    <p>summarize chat What were the main topics discussed? - Ask a question about the conversation
    <p>summarize reset - Clear chat history

    NOTES:
    - The script fetches the last 250 messages from the current or specified channel
    - It generates a summary of these messages using the OpenRouter API
    - A summary must be generated first to establish the channel context
    - The script maintains a history of your chat messages for context
    - The summary is regenerated each time you use the <p>summarize command
    - When using <p>summarize chat in a different channel, it uses the most recent channel context
    """
    import aiohttp
    import json
    from pathlib import Path
    import asyncio
    import re
    from datetime import datetime
    import os  # Added for startfile functionality

    # Available free models from OpenRouter
    FREE_MODELS = [
        # Deepseek models
        "deepseek/deepseek-chat-v3-0324:free",
        "deepseek/deepseek-chat:free",
        "tngtech/deepseek-r1t-chimera:free",
        # Meta-Llama models
        "meta-llama/llama-4-scout:free",
        "meta-llama/llama-3.1-405b:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "meta-llama/llama-4-maverick:free",
        # Mistral models
        "mistralai/mistral-7b-instruct:free",
        "mistralai/mistral-small-3.1-24b-instruct:free",
        # Google models
        "google/gemini-2.0-flash-exp:free",
        "google/gemma-3-27b-it:free",
        # Qwen models
        "qwen/qwen-2.5-72b-instruct:free",
        "qwen/qwen3-32b:free",
        "qwen/qwen3-235b-a22b:free",
    ]

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

    # Initialize configuration with defaults if not set
    if getConfigData().get(API_KEY_CONFIG) is None:
        updateConfigData(API_KEY_CONFIG, "")
    if getConfigData().get(MODEL_CONFIG) is None:
        updateConfigData(MODEL_CONFIG, DEFAULT_MODEL)
    if getConfigData().get(DEBUG_CONFIG) is None:
        updateConfigData(DEBUG_CONFIG, False)
    if getConfigData().get(SUMMARY_CONFIG) is None:
        updateConfigData(SUMMARY_CONFIG, "")
    if getConfigData().get(CHANNEL_CONFIG) is None:
        updateConfigData(CHANNEL_CONFIG, "")
    if getConfigData().get(MEMORY_LIMIT_CONFIG) is None:
        updateConfigData(MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT)
    if getConfigData().get(MESSAGE_LIMIT_CONFIG) is None:
        updateConfigData(MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT)

    def debug_log(message):
        """Log debug messages if debug mode is enabled"""
        if getConfigData().get(DEBUG_CONFIG, False):
            print(f"[Chat Summarizer Debug] {message}", type_="DEBUG")

    # Set up chat history storage
    BASE_DIR = Path(getScriptsPath()) / "json"
    HISTORY_FILE = BASE_DIR / "summarizer_history.json"

    def ensure_dir():
        """Ensure the directory for JSON files exists"""
        BASE_DIR.mkdir(parents=True, exist_ok=True)

    def load_history():
        """Load chat history from the JSON file"""
        ensure_dir()
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)

                # Check if history is in the old format (just array of strings)
                # Convert to new format if needed
                if history and isinstance(history[0], str):
                    debug_log("Converting old history format to new format")
                    new_history = []
                    for message in history:
                        new_history.append({"role": "user", "content": message})
                    return new_history
                return history
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(history_list):
        """Save chat history to the JSON file, respecting the memory limit"""
        ensure_dir()
        # Get the memory limit - this is the number of conversation turns (user+assistant)
        memory_limit = getConfigData().get(MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT)

        # Since each conversation turn is 2 messages (user+assistant), we multiply by 2
        # But first check that we have proper pairing
        message_limit = memory_limit * 2

        # If we have more messages than the limit, remove oldest pairs
        if len(history_list) > message_limit:
            # Keep only the most recent messages up to the limit
            # Make sure we remove complete pairs by cutting off at an even number
            to_remove = len(history_list) - message_limit
            if to_remove % 2 != 0:
                to_remove += 1

            history_list = history_list[to_remove:]
            debug_log(
                f"Trimmed history to {len(history_list)} messages ({len(history_list)//2} conversation turns)"
            )

        with open(HISTORY_FILE, "w") as f:
            json.dump(history_list, f, indent=4)

    def reset_history():
        """Reset the chat history"""
        save_history([])

    def get_system_prompt():
        """Get the system prompt for the summarizer"""
        return """Summarize this Discord chat concisely but completely. Include:
- Main topics and discussions
- Key decisions or conclusions
- Important questions raised
- Action items mentioned

Organize your summary clearly. Focus on meaningful content, not individual messages."""

    def get_chat_system_prompt(summary):
        """Get the system prompt for chatting with the summary"""
        return f"""You are a helpful Discord chat assistant. Answer questions based only on this conversation summary:

{summary}

If information isn't in the summary, say so."""

    def get_full_logs_system_prompt(conversation):
        """Get the system prompt for chatting with the full logs"""
        return f"""You are a helpful Discord chat assistant. Answer questions based on this conversation log from Discord:

{conversation}

Focus on the messages and their content. If the information isn't in the logs, say so. Be direct and concise."""

    # UI SETUP
    try:
        # Create a tab prefix to avoid conflicts with other UI scripts
        TAB_PREFIX = "summarizer_"

        # Create a new tab
        summarizer_tab = Tab(
            name=f"Chat Summarizer", icon="message", title="Chat Summarizer"
        )

        # Create a wrapper container with columns layout
        wrapper_container = summarizer_tab.create_container(type="columns")

        # Create left container with rows layout
        left_container = wrapper_container.create_container(type="rows")

        # TOP CARD - INSTRUCTIONS
        top_card = left_container.create_card(gap=4)

        # Create a button group for the API key link
        api_key_group = top_card.create_group(
            type="columns", gap=2, vertical_align="center"
        )

        # Add button to open OpenRouter keys page
        open_router_button = api_key_group.create_ui_element(
            UI.Button, label="Get OpenRouter API Key", variant="solid", size="sm"
        )

        # Function to open the OpenRouter keys page
        def open_router_keys():
            try:
                os.startfile("https://openrouter.ai/keys")
                summarizer_tab.toast(
                    title="Opening Website",
                    description="Opening OpenRouter API keys page in your browser.",
                    type="INFO",
                )
            except Exception as e:
                print(f"Error opening browser: {e}", type_="ERROR")
                summarizer_tab.toast(
                    title="Error",
                    description=f"Failed to open browser: {e}",
                    type="ERROR",
                )

        # Attach event handler to the button
        open_router_button.onClick = open_router_keys

        top_card.create_ui_element(
            UI.Text,
            content=f"""How to use Chat Summarizer:

1. Set your OpenRouter API key in the settings panel to the right
2. Select an AI model from the dropdown menu
3. Use {bot.command_prefix}summarize to generate a summary of messages in the current channel
4. Use {bot.command_prefix}summarize --channel <channel_id> to summarize a specific channel
5. Use {bot.command_prefix}summarize chat <message> to chat with the full logs of the conversation

All settings are configured here in the UI""",
            size="tiny",
        )

        # BOTTOM CARD - STATUS PANEL
        bottom_card = left_container.create_card(gap=4)

        # Create a group for the model status
        model_status_group = bottom_card.create_group(
            type="columns", gap=2, vertical_align="center"
        )
        model_status_text = model_status_group.create_ui_element(
            UI.Text,
            content=f"Current Model: {getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)}",
            size="base",
        )

        # Get channel name if possible
        channel_id = getConfigData().get(CHANNEL_CONFIG, "")
        channel_name = "None"
        if channel_id:
            try:
                # Try to get the channel from the client's cache
                channel = bot.get_channel(int(channel_id))
                if channel:
                    server_name = (
                        channel.guild.name
                        if hasattr(channel, "guild") and channel.guild
                        else "Unknown"
                    )
                    channel_name = f"#{channel.name} in {server_name}"
                else:
                    channel_name = f"<#{channel_id}>"
            except:
                channel_name = f"<#{channel_id}>"

        # Create a group for the channel status
        channel_status_group = bottom_card.create_group(
            type="columns", gap=2, vertical_align="center"
        )
        channel_status_text = channel_status_group.create_ui_element(
            UI.Text, content=f"Active Channel: {channel_name}", size="base"
        )

        # Create a group for the chat history status
        history_status_group = bottom_card.create_group(
            type="columns", gap=2, vertical_align="center"
        )

        # Count messages in history
        current_history = load_history()
        history_count = len(current_history)
        memory_limit = getConfigData().get(MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT)

        history_status_text = history_status_group.create_ui_element(
            UI.Text,
            content=f"Chat History: {history_count // 2} conversations (limit: {memory_limit})",
            size="base",
        )

        # RIGHT CONTAINER - CONFIGURATION
        right_container = wrapper_container.create_container(type="columns")
        right_card = right_container.create_card(gap=2)

        # Add descriptive text
        right_card.create_ui_element(UI.Text, content="Configuration", size="lg")

        # Add API key input
        api_key_input = right_card.create_ui_element(
            UI.Input,
            label="OpenRouter API Key",
            placeholder="Enter your OpenRouter API key",
            value=getConfigData().get(API_KEY_CONFIG, ""),
            description="Your OpenRouter API key is stored securely in Nighty's configuration",
        )

        # Prepare model options for the dropdown
        current_model = getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)
        model_options = []

        # Define model icons
        MODEL_ICONS = {
            "qwen": "https://cdn-avatars.huggingface.co/v1/production/uploads/620760a26e3b7210c2ff1943/-s1gyJfvbE1RgO5iBeNOi.png",
            "meta-llama": "https://cdn-avatars.huggingface.co/v1/production/uploads/646cf8084eefb026fb8fd8bc/oCTqufkdTkjyGodsx1vo1.png",
            "mistralai": "https://cdn-avatars.huggingface.co/v1/production/uploads/62dac1c7a8ead43d20e3e17a/wrLf5yaGC6ng4XME70w6Z.png",
            "google": "https://cdn-avatars.huggingface.co/v1/production/uploads/5dd96eb166059660ed1ee413/WtA3YYitedOr9n02eHfJe.png",
            "anthropic": "https://cdn-avatars.huggingface.co/v1/production/uploads/1670531762351-6200d0a443eb0913fa2df7cc.png",
            "deepseek": "https://cdn-avatars.huggingface.co/v1/production/uploads/6538815d1bdb3c40db94fbfa/xMBly9PUMphrFVMxLX4kq.png",
            "tngtech": "https://cdn-avatars.huggingface.co/v1/production/uploads/6538815d1bdb3c40db94fbfa/xMBly9PUMphrFVMxLX4kq.png",
        }

        # Define custom model option
        CUSTOM_MODEL_ID = "custom_model_option"
        model_options.append({"id": CUSTOM_MODEL_ID, "title": "Use custom model"})

        # Add the current model to options if it's not in FREE_MODELS and not the custom option
        if current_model not in FREE_MODELS and current_model != CUSTOM_MODEL_ID:
            icon_url = None
            for prefix, url in MODEL_ICONS.items():
                if current_model.startswith(prefix):
                    icon_url = url
                    break

            if icon_url:
                model_options.append(
                    {
                        "id": current_model,
                        "title": f"Current: {current_model}",
                        "iconUrl": icon_url,
                    }
                )
            else:
                model_options.append(
                    {"id": current_model, "title": f"Current: {current_model}"}
                )

        # Add all free models to options with icons
        for model in FREE_MODELS:
            model_option = {"id": model, "title": model}

            # Add icon URL if available for this model
            for prefix, url in MODEL_ICONS.items():
                if model.startswith(prefix):
                    model_option["iconUrl"] = url
                    break

            model_options.append(model_option)

        # Add model dropdown
        model_select = right_card.create_ui_element(
            UI.Select,
            label="AI Model",
            items=model_options,
            selected_items=[
                current_model if current_model != CUSTOM_MODEL_ID else CUSTOM_MODEL_ID
            ],
            description="Select an AI model to use for summarization and chat",
            full_width=True,
        )

        # Add custom model input field (initially hidden if not using custom model)
        custom_model_group = right_card.create_group(
            type="columns", gap=4, vertical_align="center"
        )
        custom_model_input = custom_model_group.create_ui_element(
            UI.Input,
            label="Custom Model Identifier",
            placeholder="e.g. anthropic/claude-3-opus",
            value=(
                current_model
                if current_model not in FREE_MODELS and current_model != CUSTOM_MODEL_ID
                else ""
            ),
            description="Enter a specific model identifier for OpenRouter API",
            visible=current_model not in FREE_MODELS
            and current_model != CUSTOM_MODEL_ID,
        )

        # Add button to open OpenRouter models page (visible only when custom model input is visible)
        models_button = custom_model_group.create_ui_element(
            UI.Button,
            label="OpenRouter Models",
            variant="solid",
            size="sm",
            visible=current_model not in FREE_MODELS
            and current_model != CUSTOM_MODEL_ID,
        )

        # Function to open the OpenRouter models page
        def open_router_models():
            try:
                os.startfile("https://openrouter.ai/models")
                summarizer_tab.toast(
                    title="Opening Website",
                    description="Opening OpenRouter models page in your browser.",
                    type="INFO",
                )
            except Exception as e:
                print(f"Error opening browser: {e}", type_="ERROR")
                summarizer_tab.toast(
                    title="Error",
                    description=f"Failed to open browser: {e}",
                    type="ERROR",
                )

        # Attach event handler to the button
        models_button.onClick = open_router_models

        # Create a group for the limit inputs
        limits_group = right_card.create_group(
            type="columns", gap=4, vertical_align="center"
        )

        # Add memory limit input
        memory_limit_input = limits_group.create_ui_element(
            UI.Input,
            label="Chat Memory Limit",
            placeholder="10",
            value=str(getConfigData().get(MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT)),
            description="Conversation turns to save",
            full_width=False,
        )

        # Add message limit input
        message_limit_input = limits_group.create_ui_element(
            UI.Input,
            label="Messages to Summarize",
            placeholder="250",
            value=str(getConfigData().get(MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT)),
            description="Messages to fetch (10-300)",
            full_width=False,
        )

        # Create a button group with save and reset buttons
        button_group = right_card.create_group(type="columns", gap=4)

        # Add save button
        save_button = button_group.create_ui_element(
            UI.Button, label="Save Settings", variant="cta"
        )

        # Add reset history button
        reset_button = button_group.create_ui_element(
            UI.Button, label="Reset Chat History", variant="bordered", color="danger"
        )

        # Helper function to update status texts (no toast)
        def update_status_texts(show_toast=True):
            # Update model status
            model_status_text.content = (
                f"Current Model: {getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)}"
            )

            # Update channel status
            channel_id = getConfigData().get(CHANNEL_CONFIG, "")
            channel_name = "None"
            if channel_id:
                try:
                    # Try to get the channel from the client's cache
                    channel = bot.get_channel(int(channel_id))
                    if channel:
                        server_name = (
                            channel.guild.name
                            if hasattr(channel, "guild") and channel.guild
                            else "Unknown"
                        )
                        channel_name = f"#{channel.name} in {server_name}"
                    else:
                        channel_name = f"<#{channel_id}>"
                except:
                    channel_name = f"<#{channel_id}>"

            channel_status_text.content = f"Active Channel: {channel_name}"

            # Update history status
            current_history = load_history()
            history_count = len(current_history)
            memory_limit = getConfigData().get(
                MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT
            )
            history_status_text.content = f"Chat History: {history_count // 2} conversations (limit: {memory_limit})"

            # Show success toast only if requested
            if show_toast:
                summarizer_tab.toast(
                    title="Status Updated",
                    description="Status panel has been refreshed with the latest information.",
                    type="INFO",
                )

        # Event handlers
        def save_settings_handler():
            try:
                # Get values from inputs
                api_key = api_key_input.value.strip()
                memory_limit = memory_limit_input.value.strip()
                message_limit = message_limit_input.value.strip()
                changes_made = False

                # Get selected model from dropdown
                selected_models = model_select.selected_items
                if selected_models and len(selected_models) > 0:
                    model = selected_models[0]

                    # Handle custom model case
                    if model == CUSTOM_MODEL_ID:
                        custom_model = custom_model_input.value.strip()
                        if custom_model:
                            model = custom_model
                        else:
                            # If custom model field is empty, show error
                            print(
                                "Custom model field cannot be empty when 'Use custom model' is selected",
                                type_="ERROR",
                            )
                            summarizer_tab.toast(
                                title="Error",
                                description="Custom model field cannot be empty",
                                type="ERROR",
                            )
                            return

                    if model and model != getConfigData().get(
                        MODEL_CONFIG, DEFAULT_MODEL
                    ):
                        updateConfigData(MODEL_CONFIG, model)
                        print(f"Model updated to: {model} via UI", type_="INFO")
                        changes_made = True

                # Validate and save API key
                current_api_key = getConfigData().get(API_KEY_CONFIG, "")
                if api_key and api_key != current_api_key:
                    updateConfigData(API_KEY_CONFIG, api_key)
                    print("OpenRouter API key updated via UI", type_="INFO")
                    changes_made = True

                # Validate and save memory limit
                if memory_limit:
                    try:
                        memory_limit_int = int(memory_limit)
                        current_memory_limit = getConfigData().get(
                            MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT
                        )

                        if memory_limit_int < 1:
                            raise ValueError("Memory limit must be at least 1")

                        if memory_limit_int != current_memory_limit:
                            updateConfigData(MEMORY_LIMIT_CONFIG, memory_limit_int)
                            print(
                                f"Memory limit updated to: {memory_limit_int} via UI",
                                type_="INFO",
                            )
                            changes_made = True

                            # Trim history if needed
                            current_history = load_history()
                            if (
                                len(current_history) > memory_limit_int * 2
                            ):  # Multiply by 2 for user+assistant messages
                                save_history(
                                    current_history
                                )  # This will trim automatically
                    except ValueError as e:
                        print(f"Invalid memory limit value: {e}", type_="ERROR")
                        summarizer_tab.toast(
                            title="Error",
                            description=f"Invalid memory limit: {e}",
                            type="ERROR",
                        )
                        return  # Exit early on error

                # Validate and save message limit
                if message_limit:
                    try:
                        message_limit_int = int(message_limit)
                        current_message_limit = getConfigData().get(
                            MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT
                        )

                        # Enforce minimum and maximum values
                        if message_limit_int < 10:
                            raise ValueError("Message limit must be at least 10")
                        if message_limit_int > 300:
                            raise ValueError("Message limit cannot exceed 300")

                        if message_limit_int != current_message_limit:
                            updateConfigData(MESSAGE_LIMIT_CONFIG, message_limit_int)
                            print(
                                f"Message limit updated to: {message_limit_int} via UI",
                                type_="INFO",
                            )
                            changes_made = True
                    except ValueError as e:
                        print(f"Invalid message limit value: {e}", type_="ERROR")
                        summarizer_tab.toast(
                            title="Error",
                            description=f"Invalid message limit: {e}",
                            type="ERROR",
                        )
                        return  # Exit early on error

                # Update status texts silently (without toast)
                update_status_texts(show_toast=False)

                # Show toast based on whether changes were made
                if changes_made:
                    summarizer_tab.toast(
                        title="Settings Saved",
                        description="Chat Summarizer settings updated successfully!",
                        type="SUCCESS",
                    )
                else:
                    summarizer_tab.toast(
                        title="No Changes",
                        description="No settings were changed.",
                        type="INFO",
                    )
            except Exception as e:
                print(f"Error saving settings: {e}", type_="ERROR")
                summarizer_tab.toast(
                    title="Error",
                    description=f"Failed to save settings: {e}",
                    type="ERROR",
                )

        def reset_history_handler():
            try:
                reset_history()
                print("Chat history reset via UI", type_="INFO")

                # Update status texts
                update_status_texts(show_toast=False)

                # Show success toast
                summarizer_tab.toast(
                    title="History Reset",
                    description="Chat history has been reset successfully!",
                    type="SUCCESS",
                )
            except Exception as e:
                print(f"Error resetting history: {e}", type_="ERROR")
                summarizer_tab.toast(
                    title="Error",
                    description=f"Failed to reset history: {e}",
                    type="ERROR",
                )

        # Function to handle model selection change
        def handle_model_selection(selected_items):
            if selected_items and selected_items[0] == CUSTOM_MODEL_ID:
                # Show custom model input when custom option is selected
                custom_model_input.visible = True
                models_button.visible = True
            else:
                # Hide custom model input for predefined models
                custom_model_input.visible = False
                models_button.visible = False

        # Attach event handlers
        save_button.onClick = save_settings_handler
        reset_button.onClick = reset_history_handler
        model_select.onChange = handle_model_selection

        # Render the tab
        summarizer_tab.render()
    except Exception as e:
        print(f"Error initializing Chat Summarizer UI: {e}", type_="ERROR")
        import traceback

        print(traceback.format_exc(), type_="ERROR")

    @bot.command(
        name="summarize",
        description="Generate a summary of the last 250 messages and chat with it",
    )
    async def summarize_command(ctx, *, args: str = ""):
        """Main command for managing chat summarization"""
        await ctx.message.delete()

        try:
            args = args.strip()

            if not args:
                # Generate a summary of the last messages
                await generate_summary(ctx, ctx.channel.id)
                return

            # Check for --channel flag
            channel_match = re.match(r"--channel\s+(\d+)(?:\s+(.*))?", args)
            if channel_match:
                channel_id = channel_match.group(1)
                remaining_args = channel_match.group(2) or ""

                # If there are additional arguments after channel ID, process them separately
                if remaining_args:
                    await ctx.send(
                        "❌ Invalid command format. Please use `<p>summarize --channel <channel_id>` without additional arguments."
                    )
                    return

                # Generate summary for the specified channel
                await generate_summary(ctx, channel_id)
                return

            # Split command into subcommand and arguments
            cmd_parts = args.split(" ", 1)
            subcommand = cmd_parts[0].lower()
            subargs = cmd_parts[1] if len(cmd_parts) > 1 else ""

            if subcommand == "status":
                model = getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)
                debug_enabled = getConfigData().get(DEBUG_CONFIG, False)
                summary = getConfigData().get(SUMMARY_CONFIG, "")
                summary_length = len(summary) if summary else 0
                channel_id = getConfigData().get(CHANNEL_CONFIG, "")

                # Try to get the channel name if possible
                channel_name = "None"
                if channel_id:
                    try:
                        # Try to get the channel from the client's cache
                        channel = bot.get_channel(int(channel_id))
                        if channel:
                            server_name = (
                                channel.guild.name
                                if hasattr(channel, "guild") and channel.guild
                                else "Unknown"
                            )
                            channel_name = f"#{channel.name} in {server_name}"
                        else:
                            channel_name = f"<#{channel_id}>"
                    except:
                        channel_name = f"<#{channel_id}>"

                memory_limit = getConfigData().get(
                    MEMORY_LIMIT_CONFIG, DEFAULT_MEMORY_LIMIT
                )
                message_limit = getConfigData().get(
                    MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT
                )
                current_history = load_history()

                # Save current private setting and disable private mode for forwarding embed
                current_private = getConfigData().get("private")
                updateConfigData("private", False)

                # Format configuration as markdown
                config_content = (
                    "## Chat Summarizer Configuration\n\n"
                    f"**Model:** {model}\n"
                    f"**Debug Mode:** {'Enabled' if debug_enabled else 'Disabled'}\n"
                    f"**Summary Length:** {summary_length} characters\n"
                    f"**Current Channel:** {channel_name}\n"
                    f"**Memory Limit:** {memory_limit} conversation turns\n"
                    f"**Messages to Summarize:** {message_limit} messages\n"
                    f"**Current History:** {len(current_history)} messages\n"
                )

                # Send configuration as embed
                await forwardEmbedMethod(
                    channel_id=ctx.channel.id,
                    content=config_content,
                    title="Chat Summarizer Status",
                    image=None,
                )

                # Restore original private setting
                updateConfigData("private", current_private)
                return

            elif subcommand == "reset":
                reset_history()

                # Update UI status
                try:
                    update_status_texts(show_toast=False)
                except Exception as e:
                    debug_log(f"Error updating UI after reset: {e}")

                # Send temporary message that will delete after 10 seconds
                temp_msg = await ctx.send("✅ Chat history has been reset.")
                # Schedule deletion after 10 seconds
                await asyncio.sleep(10)
                try:
                    await temp_msg.delete()
                except:
                    pass  # Ignore errors if message already deleted
                return

            elif subcommand == "chat":
                if not subargs:
                    await ctx.send(
                        "❌ Please provide a message to chat with the conversation"
                    )
                    return

                # Check if we have a summary (used to establish channel context)
                summary = getConfigData().get(SUMMARY_CONFIG, "")

                # If we don't have a summary, prompt user to generate one first
                if not summary:
                    await ctx.send(
                        "❌ No channel context found. Please generate a summary first using `<p>summarize` or `<p>summarize --channel <channel_id>`"
                    )
                    return

                # Chat with the full logs
                await chat_with_full_logs(ctx, subargs, summary)
                return

            else:
                # Send temporary message that will delete after 10 seconds
                temp_msg = await ctx.send(
                    "❌ Unknown subcommand. Use `<p>summarize` to generate a summary or `<p>summarize chat <message>` to chat with the conversation."
                )
                # Schedule deletion after 10 seconds
                await asyncio.sleep(10)
                try:
                    await temp_msg.delete()
                except:
                    pass  # Ignore errors if message already deleted
                return

        except Exception as e:
            print(f"Error in summarize command: {str(e)}", type_="ERROR")
            await ctx.send(f"❌ Error: {str(e)}")

    async def generate_summary(ctx, channel_id):
        """Generate a summary of the last messages in the specified channel"""
        # Check if API key is set
        api_key = getConfigData().get(API_KEY_CONFIG, "")
        if not api_key:
            await ctx.send(
                "❌ OpenRouter API key not set. Please configure it in the Summarizer tab in the Nighty UI."
            )
            return

        # Get the message limit from configuration
        message_limit = getConfigData().get(MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT)

        # Show typing indicator using Discord's channel mention format
        try:
            msg = await ctx.send(
                f"Generating summary of the last {message_limit} messages from <#{channel_id}>..."
            )
        except Exception as send_error:
            print(f"Error sending initial message: {send_error}", type_="ERROR")
            try:
                # Try to send a message without channel mention which might be causing issues
                msg = await ctx.send(
                    f"Generating summary of the last {message_limit} messages..."
                )
            except Exception as retry_error:
                print(
                    f"Failed to send even simple message: {retry_error}", type_="ERROR"
                )
                return

        try:
            # Get the target channel
            target_channel = None

            # Try to get the channel from the client's cache
            try:
                target_channel = bot.get_channel(int(channel_id))
            except ValueError:
                await msg.delete()
                await ctx.send(f"❌ Invalid channel ID: {channel_id}")
                return

            # If channel not found in cache, try to fetch it
            if not target_channel:
                try:
                    target_channel = await bot.fetch_channel(int(channel_id))
                except Exception as e:
                    await msg.delete()
                    await ctx.send(
                        f"❌ Couldn't find channel with ID {channel_id}: {str(e)}"
                    )
                    return

            # Fetch the last messages based on the limit in configuration
            messages = []
            try:
                async for message in target_channel.history(limit=message_limit):
                    # Skip bot messages and commands
                    if message.author.bot or message.content.startswith("<p>"):
                        continue

                    # Format the message
                    timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    author = message.author.display_name
                    content = message.content

                    # Add to messages list
                    messages.append(f"[{timestamp}] {author}: {content}")
            except Exception as fetch_error:
                print(f"Error fetching messages: {fetch_error}", type_="ERROR")
                await msg.delete()
                await ctx.send(f"❌ Error fetching messages: {str(fetch_error)}")
                return

            # Reverse the messages to get them in chronological order
            messages.reverse()

            # Join the messages with newlines
            conversation = "\n".join(messages)

            # If no messages were found
            if not conversation:
                await msg.delete()
                await ctx.send(f"❌ No messages found in channel <#{channel_id}>.")
                return

            # Prepare the API request
            model = getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)
            system_prompt = get_system_prompt()

            # Prepare messages array
            api_messages = [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"Please summarize the following Discord conversation:\n\n{conversation}",
                },
            ]

            # Debug log the messages being sent
            debug_log(
                f"Sending messages to OpenRouter for summarization:\n{json.dumps(api_messages, indent=2)}"
            )

            # Prepare API request
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nighty.one",  # Required by OpenRouter
                "X-Title": "Nighty Selfbot",  # Required by OpenRouter
            }

            payload = {"model": model, "messages": api_messages}

            # Debug log the full request
            # Create a copy of headers with masked API key for logging
            log_headers = headers.copy()
            if "Authorization" in log_headers:
                log_headers["Authorization"] = "Bearer [REDACTED]"

            debug_log(
                f"Full request to OpenRouter:\nURL: {api_url}\nHeaders: {json.dumps(log_headers, indent=2)}\nPayload: {json.dumps(payload, indent=2)}"
            )

            # Make the API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url, headers=headers, json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Debug log the response
                        debug_log(f"OpenRouter response:\n{json.dumps(data, indent=2)}")

                        # Check for error in response
                        if "error" in data:
                            error_data = data["error"]
                            error_code = error_data.get("code")
                            error_message = error_data.get("message")
                            provider_name = error_data.get("metadata", {}).get(
                                "provider_name", "Unknown"
                            )

                            try:
                                await msg.delete()
                            except Exception as delete_error:
                                print(
                                    f"Error deleting status message: {delete_error}",
                                    type_="ERROR",
                                )
                                # Continue even if message deletion fails

                            # Send error message that will delete after 15 seconds
                            error_msg = await ctx.send(
                                f"❌ Error from {provider_name}: {error_message}"
                            )
                            # Schedule deletion after 15 seconds
                            asyncio.create_task(self_delete_message(error_msg, 15))
                            return

                        # Handle different response formats
                        if "choices" in data and len(data["choices"]) > 0:
                            summary = data["choices"][0]["message"]["content"]
                        elif "text" in data:
                            summary = data["text"]
                        elif "response" in data:
                            summary = data["response"]
                        elif "content" in data:
                            summary = data["content"]
                        else:
                            # If we can't find the response in any known format, show the full response for debugging
                            summary = f"Unexpected response format. Full response:\n{json.dumps(data, indent=2)}"

                        model_used = data.get("model", model)

                        # Save the summary and channel ID
                        updateConfigData(SUMMARY_CONFIG, summary)
                        updateConfigData(CHANNEL_CONFIG, str(channel_id))

                        # Reset history when generating a new summary
                        reset_history()

                        # Delete the "Generating summary..." message
                        await msg.delete()

                        # Save current private setting and disable private mode for forwarding embed
                        current_private = getConfigData().get("private")
                        updateConfigData("private", False)

                        # Format the content for the embed
                        formatted_content = f"## Conversation Summary for <#{channel_id}>\n\n{summary}\n\n## Instructions\nYou can now chat with this summary using `<p>summarize chat <your question>`"

                        # Send the response as an embed
                        await forwardEmbedMethod(
                            channel_id=ctx.channel.id,
                            content=formatted_content,
                            title=f"Chat Summarizer - {model_used}",
                            image=None,
                        )

                        # Restore original private setting
                        updateConfigData("private", current_private)

                        # Update UI status
                        try:
                            update_status_texts(show_toast=False)
                        except Exception as e:
                            debug_log(f"Error updating UI after summary: {e}")
                    else:
                        error_msg = await response.text()
                        debug_log(
                            f"OpenRouter error response:\nStatus: {response.status}\nError: {error_msg}"
                        )
                        try:
                            await msg.delete()
                        except Exception as delete_error:
                            print(
                                f"Error deleting status message: {delete_error}",
                                type_="ERROR",
                            )
                            # Continue even if message deletion fails

                        # Send error message that will delete after 15 seconds
                        error_msg = await ctx.send(
                            f"❌ Error: {response.status}\n{error_msg}"
                        )
                        # Schedule deletion after 15 seconds
                        asyncio.create_task(self_delete_message(error_msg, 15))

        except Exception as e:
            print(f"Error generating summary: {str(e)}", type_="ERROR")
            try:
                await msg.delete()
            except Exception as delete_error:
                print(f"Error deleting status message: {delete_error}", type_="ERROR")
                # Continue even if message deletion fails

            # Send error message that will delete after 15 seconds
            error_msg = await ctx.send(f"❌ Error occurred: {str(e)}")
            # Schedule deletion after 15 seconds
            asyncio.create_task(self_delete_message(error_msg, 15))

    async def chat_with_full_logs(ctx, message, summary):
        """Chat with the full logs instead of the summary"""
        # Check if API key is set
        api_key = getConfigData().get(API_KEY_CONFIG, "")
        if not api_key:
            await ctx.send(
                "❌ OpenRouter API key not set. Please configure it in the Summarizer tab in the Nighty UI."
            )
            return

        # Show typing indicator
        try:
            msg = await ctx.send("Thinking...")
        except Exception as send_error:
            print(f"Error sending initial message: {send_error}", type_="ERROR")
            try:
                # Try again with a different message that might work
                msg = await ctx.send("Processing...")
            except Exception as retry_error:
                print(
                    f"Failed to send even simple message: {retry_error}", type_="ERROR"
                )
                return

        try:
            # Get the channel ID
            channel_id = getConfigData().get(CHANNEL_CONFIG, "")

            if not channel_id:
                try:
                    await msg.delete()
                except Exception as delete_error:
                    print(f"Error deleting message: {delete_error}", type_="ERROR")
                await ctx.send("❌ Cannot find the channel for the last summary.")
                return

            # Get the target channel
            try:
                target_channel = bot.get_channel(int(channel_id))
                if not target_channel:
                    target_channel = await bot.fetch_channel(int(channel_id))
            except Exception as e:
                try:
                    await msg.delete()
                except Exception as delete_error:
                    print(f"Error deleting message: {delete_error}", type_="ERROR")
                await ctx.send(
                    f"❌ Couldn't find channel with ID {channel_id}: {str(e)}"
                )
                return

            # Get the message limit from configuration
            message_limit = getConfigData().get(
                MESSAGE_LIMIT_CONFIG, DEFAULT_MESSAGE_LIMIT
            )

            # Fetch the last messages based on the limit in configuration
            messages = []
            try:
                async for discord_msg in target_channel.history(limit=message_limit):
                    # Skip bot messages and commands
                    if discord_msg.author.bot or discord_msg.content.startswith("<p>"):
                        continue

                    # Format the message
                    timestamp = discord_msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    author = discord_msg.author.display_name
                    content = discord_msg.content

                    # Add to messages list
                    messages.append(f"[{timestamp}] {author}: {content}")
            except Exception as fetch_error:
                print(f"Error fetching messages: {fetch_error}", type_="ERROR")
                try:
                    await msg.delete()
                except Exception as delete_error:
                    print(f"Error deleting message: {delete_error}", type_="ERROR")
                await ctx.send(f"❌ Error fetching messages: {str(fetch_error)}")
                return

            # Reverse the messages to get them in chronological order
            messages.reverse()

            # Join the messages with newlines
            conversation = "\n".join(messages)

            # If no messages were found
            if not conversation:
                await msg.delete()
                await ctx.send(f"❌ No messages found in channel <#{channel_id}>.")
                return

            # Prepare the API request
            model = getConfigData().get(MODEL_CONFIG, DEFAULT_MODEL)
            system_prompt = get_full_logs_system_prompt(conversation)

            # Load chat history
            history = load_history()

            # Prepare messages array
            api_messages = [{"role": "system", "content": system_prompt}]

            # Add chat history if available
            for msg_history in history:
                api_messages.append(msg_history)

            # Add the current message
            api_messages.append({"role": "user", "content": message})

            # Debug log the messages being sent
            debug_log(
                f"Sending messages to OpenRouter for chat:\n{json.dumps(api_messages, indent=2)}"
            )

            # Prepare API request
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://nighty.one",  # Required by OpenRouter
                "X-Title": "Nighty Selfbot",  # Required by OpenRouter
            }

            payload = {"model": model, "messages": api_messages}

            # Debug log the full request
            # Create a copy of headers with masked API key for logging
            log_headers = headers.copy()
            if "Authorization" in log_headers:
                log_headers["Authorization"] = "Bearer [REDACTED]"

            debug_log(
                f"Full request to OpenRouter:\nURL: {api_url}\nHeaders: {json.dumps(log_headers, indent=2)}\nPayload: {json.dumps(payload, indent=2)}"
            )

            # Make the API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    api_url, headers=headers, json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Debug log the response
                        debug_log(f"OpenRouter response:\n{json.dumps(data, indent=2)}")

                        # Check for error in response
                        if "error" in data:
                            error_data = data["error"]
                            error_code = error_data.get("code")
                            error_message = error_data.get("message")
                            provider_name = error_data.get("metadata", {}).get(
                                "provider_name", "Unknown"
                            )

                            try:
                                await msg.delete()
                            except Exception as delete_error:
                                print(
                                    f"Error deleting status message: {delete_error}",
                                    type_="ERROR",
                                )
                                # Continue even if message deletion fails

                            # Send error message that will delete after 15 seconds
                            error_msg = await ctx.send(
                                f"❌ Error from {provider_name}: {error_message}"
                            )
                            # Schedule deletion after 15 seconds
                            asyncio.create_task(self_delete_message(error_msg, 15))
                            return

                        # Handle different response formats
                        if "choices" in data and len(data["choices"]) > 0:
                            ai_response = data["choices"][0]["message"]["content"]
                        elif "text" in data:
                            ai_response = data["text"]
                        elif "response" in data:
                            ai_response = data["response"]
                        elif "content" in data:
                            ai_response = data["content"]
                        else:
                            # If we can't find the response in any known format, show the full response for debugging
                            ai_response = f"Unexpected response format. Full response:\n{json.dumps(data, indent=2)}"

                        model_used = data.get("model", model)

                        # Update chat history with proper user/assistant format
                        history.append({"role": "user", "content": message})

                        history.append({"role": "assistant", "content": ai_response})

                        save_history(history)

                        # Delete the "Thinking..." message
                        try:
                            await msg.delete()
                        except Exception as delete_error:
                            print(
                                f"Error deleting status message: {delete_error}",
                                type_="ERROR",
                            )
                            # Continue even if message deletion fails

                        # Save current private setting and disable private mode for forwarding embed
                        current_private = getConfigData().get("private")
                        updateConfigData("private", False)

                        # Format the content for the embed with User and AI sections
                        formatted_content = f"## User Question\n{message}\n\n## {model_used} Response\n{ai_response}"

                        # Send the response as an embed
                        await forwardEmbedMethod(
                            channel_id=ctx.channel.id,
                            content=formatted_content,
                            title=f"Chat Summarizer - {model_used}",
                            image=None,
                        )

                        # Restore original private setting
                        updateConfigData("private", current_private)

                        # Update UI status
                        try:
                            update_status_texts(show_toast=False)
                        except Exception as e:
                            debug_log(f"Error updating UI after chat: {e}")
                    else:
                        error_msg = await response.text()
                        debug_log(
                            f"OpenRouter error response:\nStatus: {response.status}\nError: {error_msg}"
                        )
                        try:
                            await msg.delete()
                        except Exception as delete_error:
                            print(
                                f"Error deleting status message: {delete_error}",
                                type_="ERROR",
                            )
                            # Continue even if message deletion fails

                        # Send error message that will delete after 15 seconds
                        error_msg = await ctx.send(
                            f"❌ Error: {response.status}\n{error_msg}"
                        )
                        # Schedule deletion after 15 seconds
                        asyncio.create_task(self_delete_message(error_msg, 15))

        except Exception as e:
            print(f"Error in chat request: {str(e)}", type_="ERROR")
            try:
                await msg.delete()
            except Exception as delete_error:
                print(f"Error deleting status message: {delete_error}", type_="ERROR")
                # Continue even if message deletion fails

            # Send error message that will delete after 15 seconds
            error_msg = await ctx.send(f"❌ Error occurred: {str(e)}")
            # Schedule deletion after 15 seconds
            asyncio.create_task(self_delete_message(error_msg, 15))

    async def self_delete_message(message, delay_seconds):
        """Helper function to delete a message after a specified delay"""
        try:
            await asyncio.sleep(delay_seconds)
            await message.delete()
        except Exception as e:
            # Silently fail - the message may have been deleted already
            debug_log(f"Error auto-deleting message: {e}")


# Call the function to initialize the script
chat_summarizer_script()
