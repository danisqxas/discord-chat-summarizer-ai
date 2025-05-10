# Standard library imports
"""
This script implements a comprehensive User Activity Tracker for Discord servers.
It includes functionality for tracking user activities, managing events, and providing analytics.
Modules and Classes:
--------------------
1. TrackerConfig:
    - Manages configuration settings and caching for users and guilds.
    - Provides methods for retrieving user data and managing cache.
2. ActivityStore:
    - Handles storage and management of activity events.
    - Provides methods for adding, retrieving, deleting, and exporting events.
    - Includes analytics functionality for summarizing user activity.
3. EventQueue:
    - Implements an asynchronous queue for processing events in batches.
    - Handles event processing and integration with the ActivityStore.
4. Tab:
    - Represents a UI tab in the application.
    - Provides methods for creating containers and cards for UI components.
5. UI Components:
    - Defines various UI elements such as input fields, buttons, tables, and charts.
    - Includes event handlers for user interactions.
6. Discord Bot:
    - Uses discord.py to interact with Discord servers.
    - Listens for events and integrates with the activity tracker.
Features:
---------
1. User Activity Tracking:
    - Tracks various user activities such as messages, reactions, voice events, and more.
    - Supports filtering and exporting activity data.
2. Analytics:
    - Provides detailed analytics for user activities.
    - Includes charts and metrics for visualizing activity trends.
3. Settings Management:
    - Allows customization of tracker settings such as cache duration, batch size, and event storage limits.
    - Supports auto-purging of old events.
4. UI Components:
    - Implements a graphical user interface using customtkinter.
    - Includes tabs for activity tracking, analytics, and settings.
5. Event Processing:
    - Processes events asynchronously in batches for efficiency.
    - Integrates with the Discord bot for real-time event tracking.
6. Export and Filtering:
    - Supports exporting activity data to CSV.
    - Provides filtering options for activity logs.
Usage:
------
- Run the script to start the User Activity Tracker application.
- Use the Discord bot to track user activities in servers.
- Interact with the UI to view activity logs, analytics, and manage settings.
Dependencies:
-------------
- customtkinter
- discord.py
- pyperclip
- Standard Python libraries (asyncio, csv, datetime, logging, etc.)
Note:
-----
- Ensure required dependencies are installed before running the script.
- Configure Discord bot intents appropriately for tracking message content and other events.
"""
import asyncio
import csv
import datetime
import io
import json
import logging
import os
import re
import time
import uuid
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union
# Third-party imports
import customtkinter as ctk
import discord
import pyperclip
from discord.ext import commands
    # Ensure pyperclip is installed: pip install pyperclip
    # Ensure discord.py is installed: pip install discord.py
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # ========== Config and Settings Management ==========
    class TrackerConfig:
        """Efficient caching system for user data to reduce API calls"""
        _users = {}
        _guilds = {}
        _last_cleanup = time.time()
        @staticmethod
        async def get_user(
        async def get_user(user_id: int, bot: commands.Bot) -> Union[discord.User, "PlaceholderUser"]:
            """Get user from cache or bot"""
            if user_id in TrackerConfig._users:
                return TrackerConfig._users[user_id]
            user = await bot.fetch_user(user_id)
            if user:
                TrackerConfig._users[user_id] = user
                return user
            return PlaceholderUser()
        """Placeholder for avatar URLs"""
        @property
        def url(self) -> str:
            return "https://cdn.discordapp.com/embed/avatars/0.png"
    # ========== Activity Event Storage and Management ==========
    class ActivityStore:
            """Add a new event to the store with timestamp and UUID"""
            event_id = str(uuid.uuid4())
            timestamp = datetime.now()
            # Create the event entry
            event = {
                "id": event_id,
                "timestamp": timestamp,
            @staticmethod
            def add_event(event_data: Dict) -> Dict:
                """Add a new event to the store with timestamp and UUID"""
                event_id = str(uuid.uuid4())
                timestamp = datetime.now()
                # Create the event entry
                event = {
                    "id": event_id,
                    "timestamp": timestamp,
                    "user_id": event_data["user_id"],
                    "event_type": event_data["event_type"],
                    "server_id": event_data.get("server_id", "unknown"),
                    "server_name": event_data.get("server_name", "unknown"),
                    "details": event_data.get("details", ""),
                    "extras": event_data.get("extras", {}),
                }
            ActivityStore._events.append(event)
            ActivityStore._event_index[event_id] = event
            # Trim if over max capacity
            max_events = TrackerConfig.get("max_events")
            if len(ActivityStore._events) > max_events:
                # Remove oldest events
                removed = ActivityStore._events[
                    : (len(ActivityStore._events) - max_events)
                ]
                ActivityStore._events = ActivityStore._events[
                    (len(ActivityStore._events) - max_events) :
                ]
                # Update index
                for r in removed:
                    ActivityStore._event_index.pop(r["id"], None)
            return event

        @staticmethod
        def get_event(filters=None):
            """Get events with optional filtering"""
            if not filters:
                return ActivityStore._events
            result = ActivityStore._events
            if "user_id" in filters:
                result = [
                    e for e in result if str(e["user_id"]) == str(filters["user_id"])
                ]
            if "event_type" in filters:
                result = [e for e in result if e["event_type"] == filters["event_type"]]
            if "server_id" in filters:
                result = [
                    e
                    for e in result
                    if str(e["server_id"]) == str(filters["server_id"])
                ]
            if "date_from" in filters:
                result = [e for e in result if e["timestamp"] >= filters["date_from"]]
            if "date_to" in filters:
                result = [e for e in result if e["timestamp"] <= filters["date_to"]]
            return result

        @staticmethod
        def delete_event(event_id):
            """Delete an event by its ID"""
            event = ActivityStore._event_index.pop(event_id, None)
            if event:
                ActivityStore._events.remove(event)
            return event
            # Filter out old events
            old_events = [
                e for e in ActivityStore._events if e["timestamp"] < cutoff_date
            ]
            ActivityStore._events = [
                e for e in ActivityStore._events if e["timestamp"] >= cutoff_date
            ]
            # Update index
            for event in old_events:
                ActivityStore._event_index.pop(event["id"], None)
            ActivityStore._last_purge = datetime.now()
            return len(old_events)
        @staticmethod
        def export_to_csv() -> Optional[str]:
        """Analytics engine for user activity data"""
        @staticmethod
        def get_user_activity_summary(user_id, days=7):
        """Queue for processing events asynchronously in batches"""
        _queue = []
            @staticmethod
            def get_user_activity_summary(user_id, days=7) -> Dict:
                """Analytics engine for user activity data"""
                cutoff_date = datetime.now() - timedelta(days=days)
                events = [
                    event for event in ActivityStore._events
                    if event["user_id"] == user_id and event["timestamp"] >= cutoff_date
                ]
                return Counter(event["event_type"] for event in events)

        class EventQueue:
            """Queue for processing events asynchronously in batches"""
            _queue = []
            _processing = False
            _max_batch_size = 10
            _process_interval = 1.0  # seconds

            @staticmethod
            def add(event_data: Dict):
                EventQueue._queue.append(event_data)
                if not EventQueue._processing:
                    asyncio.create_task(EventQueue.process())
                batch = EventQueue._queue[: EventQueue._max_batch_size]
                EventQueue._queue = EventQueue._queue[EventQueue._max_batch_size :]
                # Process each event in the batch
                processed_events = []
                for event_data in batch:
                    try:
                        # Fetch user info if needed
                        if "user" not in event_data:
                            event_data["user"] = await UserCache.get_user(
                                event_data["user_id"], EventQueue.bot
                            )
                        # Add to activity store
                        event = ActivityStore.add_event(
                            {
                                "user_id": event_data["user_id"],
                                "user_name": event_data["user"].display_name,
                                "event_type": event_data["event_type"],
                                "server_id": event_data.get("server_id", "unknown"),
                                "server_name": event_data["server_name"],
                                "details": event_data["details"],
                                "extras": event_data["extras"],
                            }
                        )
                        processed_events.append(event)
                    except Exception as e:
                        logging.error(f"Error processing event: {e}")
                print(f"Processed events: {processed_events}")
                update_activity_table(processed_events)
                if EventQueue._queue:
                    await asyncio.sleep(EventQueue._process_interval)
        finally:
            EventQueue._processing = False
    # Define UI tabs as frames
    class Tab(ctk.CTkFrame):
        def __init__(self, master, name, title, icon):
            super().__init__(master)
            self.name = name
            self.title = title
            self.icon = icon
        def create_container(self, type):
            return self
        def create_card(self, height, width, gap):
            return self
                            update_activity_table(processed_events)
                        # Short delay between batches
                        if EventQueue._queue:
                            await asyncio.sleep(EventQueue._process_interval)
            finally:
                EventQueue._processing = False
                        print(f"Processed events: {processed_events}")
                        update_activity_table(processed_events)
                    # Short delay between batches
                    if EventQueue._queue:
                        await asyncio.sleep(EventQueue._process_interval)
            finally:
                EventQueue._processing = False
    # ========== UI Components ==========
    # Define UI tabs
    ua_tab = Tab(name="Activity", title="User Activity Tracker", icon="activity")
    analytics_tab = Tab(
        name="Analytics", title="Activity Analytics", icon="bar-chart-2"
    )
    settings_tab = Tab(name="Settings", title="Tracker Settings", icon="settings")
    # Define event types with colors and icons
    events_select_list = [
        {
            "id": "message_sent",
            "title": "Message Sent",
            "color": "blue",
            "icon": "message-square",
        },
        {
            "id": "message_edited",
            "title": "Message Edited",
            "color": "yellow",
            "icon": "edit",
        },
        {
            "id": "message_deleted",
            "title": "Message Deleted",
            "color": "red",
            "icon": "trash-2",
        },
        {
            "id": "reaction_added",
            "title": "Reaction Added",
            "color": "purple",
            "icon": "plus-circle",
        },
        {
            "id": "reaction_removed",
            "title": "Reaction Removed",
            "color": "purple",
            "icon": "minus-circle",
        },
        {
            "id": "voice_joined",
            "title": "Voice Joined",
            "color": "green",
            "icon": "mic",
        },
        {
            "id": "voice_left",
            "title": "Voice Left",
            "color": "orange",
            "icon": "mic-off",
        },
        {
            "id": "voice_moved",
            "title": "Voice Moved",
            "color": "teal",
            "icon": "arrow-right",
        },
        {
            "id": "nickname_change",
            "title": "Nickname Change",
            "color": "pink",
            "icon": "user",
        },
        {
            "id": "role_update",
            "title": "Role Update",
            "color": "cyan",
            "icon": "shield",
        },
        {
            "id": "guild_join",
            "title": "Server Join",
            "color": "green",
            "icon": "log-in",
        },
        {
            "id": "guild_remove",
            "title": "Server Leave",
            "color": "red",
            "icon": "log-out",
        },
        {
            "id": "thread_created",
            "title": "Thread created",
            "color": "orange",
            "icon": "plus",
        },
        {
            "id": "thread_deleted",
            "title": "Thread deleted",
            "color": "red",
            "icon": "minus",
        },
    ]
    # Create event type lookup
    event_type_map = {event["id"]: event for event in events_select_list}
    # Create UI components
    def setup_ui_components():
        # Activity Tab Components
        ua_container = ua_tab.create_container(type="rows")
        ua_card = ua_container.create_card(height="full", width="full", gap=3)
        # Top controls
        ua_top_group = ua_card.create_group(type="columns", gap=3, full_width=True)
        ua_input = ua_top_group.create_ui_element(
            UI.Input,
            label="Enter User ID",
            full_width=True,
            show_clear_button=True,
            required=True,
        )
        ua_add_button = ua_top_group.create_ui_element(
            UI.Button,
            label="Add User",
            disabled=True,
            full_width=False,
            color="primary",
        )
        # Server selection for exclusion
        servers_select_list = [
            {"id": "select_server", "title": "Select server(s)", "disabled": True}
        ]
        excluded_servers = TrackerConfig.get("excluded_servers") or []
        for excluded_id in excluded_servers:
            if excluded_id.startswith("dm_"):
                user_id = excluded_id.split("_")[1]
                user = bot.get_user(int(user_id))
                if user:
                    servers_select_list.append(
                        {
                            "id": excluded_id,
                            "title": f"DM with {user.display_name}",
                            "iconUrl": str(user.display_avatar.url),
                        }
                    )
        for server in bot.guilds:
            servers_select_list.append(
                {
                    "id": str(server.id),
                    "title": server.name,
                    "iconUrl": (
                        str(server.icon.url)
                        if server.icon
                        else "https://cdn.discordapp.com/embed/avatars/0.png"
                    ),
                }
            )
        ua_server_select = ua_top_group.create_ui_element(
            UI.Select,
            label="Exclude Servers",
            items=servers_select_list,
            mode="multiple",
            disabled_items=["select_server"],
            selected_items=excluded_servers,
            onChange=lambda selected: TrackerConfig.update(
                "excluded_servers", selected
            ),
        )
        # Event type selection
        ua_events_select = ua_top_group.create_ui_element(
            UI.Select,
            label="Select Events",
            items=events_select_list,
            mode="multiple",
            selected_items=TrackerConfig.get("selected_events"),
            onChange=lambda selected: TrackerConfig.update("selected_events", selected),
        )
        # Export button
        ua_export_button = ua_top_group.create_ui_element(
            UI.Button,
            label="Export Data",
            variant="outline",
            color="default",
            onClick=export_activity_data,
        )
        ua_filter_input = ua_top_group.create_ui_element(
            UI.Input,
            label="Filter",
            placeholder="Filter by keyword...",
            show_clear_button=True,
            full_width=True,
            onChange=filter_activity_table,
        )
        # Delete selected logs button
        ua_delete_selected = ua_top_group.create_ui_element(
            UI.Button,
            variant="ghost",
            label="Delete selected logs",
            disabled=True,
            full_width=False,
            color="danger",
            onClick=delete_selected_logs,
        )
        # Table group
        ua_table_group = ua_card.create_group(
            type="columns", gap=6, full_width=True, horizontal_align="center"
        )
        # Users table
        ua_users_table = ua_table_group.create_ui_element(
            UI.Table,
            selectable=False,
            search=True,
            items_per_page=5,
            columns=[
                {"type": "text", "label": "User"},
                {"type": "text", "label": "User ID"},
                {
                    "type": "button",
                    "label": "Actions",
                    "buttons": [
                        {
                            "label": "View Analytics",
                            "color": "primary",
                            "onClick": view_user_analytics,
                        },
                        {
                            "label": "Remove",
                            "color": "danger",
                            "onClick": remove_tracked_user,
                        },
                    ],
                },
            ],
            rows=[],
        )
        # Activity table
        ua_activity_table = ua_table_group.create_ui_element(
            UI.Table,
            selectable=True,
            search=True,
            items_per_page=15,
            columns=[
                {"type": "tag", "label": "Type"},
                {"type": "text", "label": "User"},
                {"type": "text", "label": "Details"},
                {"type": "text", "label": "Time"},
                {
                    "type": "button",
                    "label": "Actions",
                    "buttons": [
                        {
                            "label": "Jump",
                            "color": "default",
                            "onClick": jump_to_message,
                        },
                        {
                            "label": "Disable server",
                            "color": "danger",
                            "onClick": disable_server,
                        },
                        {
                            "label": "Enable server",
                            "color": "default",
                            "onClick": enable_server,
                        },
                        {
                            "label": "Disable event",
                            "color": "danger",
                            "onClick": disable_event,
                        },
                        {
                            "label": "Copy to clipboard",
                            "color": "default",
                            "onClick": copy_to_clipboard,
                        },
                    ],
                },
            ],
            rows=[],
        )
        ua_activity_table.onSelectionChange = update_table_selection
        # Analytics Tab Components
        analytics_container = analytics_tab.create_container(type="rows")
        analytics_card = analytics_container.create_card(
            height="full", width="full", gap=3
        )
        # User selection dropdown
        tracked_users = TrackerConfig.get("tracked_users") or []
        user_select_items = [{"id": "none", "title": "Select User", "disabled": True}]
        for user_id in tracked_users:
            user = bot.get_user(int(user_id))
            if user:
                user_select_items.append(
                    {
                        "id": user_id,
                        "title": user.display_name,
                        "iconUrl": str(user.display_avatar.url),
                    }
                )
            else:
                user_select_items.append({"id": user_id, "title": f"User {user_id}"})
        analytics_top_group = analytics_card.create_group(
            type="columns", gap=3, full_width=True
        )
        analytics_user_select = analytics_top_group.create_ui_element(
            UI.Select,
            label="Select User",
            items=user_select_items,
            disabled_items=["none"],
            onChange=lambda selected: update_analytics_for_user(
                selected[0] if selected else None
            ),
        )
        analytics_period_select = analytics_top_group.create_ui_element(
            UI.Select,
            label="Time Period",
            items=[
                {"id": "1", "title": "Last 24 Hours"},
                {"id": "7", "title": "Last 7 Days"},
                {"id": "30", "title": "Last 30 Days"},
                {"id": "90", "title": "Last 90 Days"},
                {"id": "all", "title": "All Time"},
            ],
            selected_items=["7"],
            onChange=lambda selected: update_analytics_period(
                selected[0] if selected else "7"
            ),
        )
        # Analytics cards
        analytics_metrics_group = analytics_card.create_group(
            type="columns", gap=3, full_width=True
        )
        analytics_total_activity = analytics_metrics_group.create_ui_element(
            UI.Metric,
            title="Total Activity",
            value="0",
            description="Select a user to view stats",
        )
        analytics_most_active_server = analytics_metrics_group.create_ui_element(
            UI.Metric,
            title="Most Active Server",
            value="-",
            description="Server with most activity",
        )
        analytics_most_common_action = analytics_metrics_group.create_ui_element(
            UI.Metric,
            title="Most Common Action",
            value="-",
            description="Most frequent activity type",
        )
        analytics_charts_group = analytics_card.create_group(
            type="columns", gap=3, full_width=True
        )
        analytics_event_types_chart = analytics_charts_group.create_ui_element(
            UI.Chart,
            title="Activity by Event Type",
            type="pie",
            height=200,
            labels=[],
            datasets=[{"label": "Event Types", "data": []}],
        )
        analytics_daily_chart = analytics_charts_group.create_ui_element(
            UI.Chart,
            title="Daily Activity",
            type="bar",
            height=200,
            labels=[],
            datasets=[{"label": "Activity Count", "data": []}],
        )
        analytics_hourly_chart = analytics_charts_group.create_ui_element(
            UI.Chart,
            title="Activity by Hour",
            type="line",
            height=200,
            labels=list(range(24)),
            datasets=[{"label": "Activity Count", "data": [0] * 24}],
        )
        # Server distribution chart
        analytics_server_chart = analytics_card.create_ui_element(
            UI.Chart,
            title="Activity by Server",
            type="doughnut",
            height=200,
            labels=[],
            datasets=[{"label": "Server Activity", "data": []}],
        )
        # Settings Tab Components
        settings_container = settings_tab.create_container(type="rows")
        settings_card = settings_container.create_card(
            height="full", width="full", gap=3
        )
        settings_group = settings_card.create_group(type="rows", gap=3, full_width=True)
        # Cache settings
        cache_ttl_slider = settings_group.create_ui_element(
            UI.Slider,
            label="Cache Duration (minutes)",
            min=5,
            max=120,
            step=5,
            value=TrackerConfig.get("cache_ttl") // 60,
            onChange=lambda value: TrackerConfig.update("cache_ttl", value * 60),
        )
        # Batch processing settings
        batch_size_slider = settings_group.create_ui_element(
            UI.Slider,
            label="Event Batch Size",
            min=1,
            max=50,
            step=1,
            value=TrackerConfig.get("batch_size"),
            onChange=lambda value: TrackerConfig.update("batch_size", value),
        )
        # Storage settings
        max_events_slider = settings_group.create_ui_element(
            UI.Slider,
            label="Maximum Events to Store",
            min=100,
            max=10000,
            step=100,
            value=TrackerConfig.get("max_events"),
            onChange=lambda value: TrackerConfig.update("max_events", value),
        )
        # Purge toggle
        auto_purge_switch = settings_group.create_ui_element(
            UI.Switch,
            label="Auto-purge Old Events",
            checked=TrackerConfig.get("auto_purge"),
            onChange=lambda value: TrackerConfig.update("auto_purge", value),
        )
        # Purge days slider
        purge_days_slider = settings_group.create_ui_element(
            UI.Slider,
            label="Days to Keep Events",
            min=1,
            max=90,
            step=1,
            value=TrackerConfig.get("purge_days"),
            onChange=lambda value: TrackerConfig.update("purge_days", value),
        )
        # Analytics toggle
        analytics_switch = settings_group.create_ui_element(
            UI.Switch,
            label="Enable Analytics",
            checked=TrackerConfig.get("analytics_enabled"),
            onChange=lambda value: TrackerConfig.update("analytics_enabled", value),
        )
        # Manual purge button
        purge_button = settings_group.create_ui_element(
            UI.Button,
            label="Purge Old Events Now",
            color="danger",
            onClick=manual_purge_events,
        )
        # Reset settings button
        reset_button = settings_group.create_ui_element(
            UI.Button,
            label="Reset All Settings",
            color="danger",
            onClick=reset_settings,
        )
        # Return UI components dictionary
        return {
            "ua_input": ua_input,
            "ua_add_button": ua_add_button,
            "ua_server_select": ua_server_select,
            "ua_events_select": ua_events_select,
            "ua_users_table": ua_users_table,
            "ua_activity_table": ua_activity_table,
            "ua_delete_selected": ua_delete_selected,
            "ua_filter_input": ua_filter_input,
            "analytics_user_select": analytics_user_select,
            "analytics_period_select": analytics_period_select,
            "analytics_total_activity": analytics_total_activity,
            "analytics_most_active_server": analytics_most_active_server,
            "analytics_most_common_action": analytics_most_common_action,
            "analytics_event_types_chart": analytics_event_types_chart,
            "analytics_daily_chart": analytics_daily_chart,
            "analytics_hourly_chart": analytics_hourly_chart,
            "analytics_server_chart": analytics_server_chart,
        }
    # Global UI components reference
    ui = setup_ui_components()
    # Selected rows tracker
    selected_rows = []
    current_analytics_user = None
    global current_analytics_period
    current_analytics_period = 7
    # ========== UI Event Handlers ==========
    def update_table_selection(selection):
        """Delete selected activity logs"""
        for row in selected_rows:
            event_id = row.get("id")
            if event_id:
                ActivityStore.delete_event(event_id)
        ui["ua_activity_table"].rows = ActivityStore.get_events()
        selected_rows.clear()
        ui["ua_delete_selected"].disabled = True
    async def export_activity_data():
        """Placeholder for jump to message functionality"""
        # You can implement deep linking or logging here
        print(f"Jumping to message/event: {row.get('id')}")
    def disable_server(row):
        """Re-include server in tracking"""
        server_id = row.get("server_id")
        excluded = TrackerConfig.get("excluded_servers")
        if server_id in excluded:
            excluded.remove(server_id)
            TrackerConfig.update("excluded_servers", excluded)
            ui["ua_server_select"].selected_items = excluded
    def disable_event(row):
        """Copy event details to clipboard"""
        details = row.get("details", "")
        pyperclip.copy(details)
        print(f"Copied to clipboard: {details}")
    def update_activity_table(processed_events):
        # Placeholder function for updating the activity table in the UI.
        pass
    def copy_to_clipboard(row):
        """Apply filter to activity table"""
        keyword = value.lower() if value else ""
        filtered_rows = [
            event
            for event in ActivityStore.get_events()
            if keyword in event.get("details", "").lower()
        ]
        ui["ua_activity_table"].rows = filtered_rows
    def remove_tracked_user(row):
        """Generate and update analytics for a user"""
        user_id = row.get("User ID")
        if not user_id:
            return
        await update_analytics_for_user(user_id)
    async def update_analytics_for_user(user_id):
        """Manually purge old events"""
        removed = ActivityStore.purge_old_events()
        await ctx.send(f"Purged {removed} old events.")
        ui["ua_activity_table"].rows = ActivityStore.get_events()
    def start_application():
        try:
            # Initialize the main window
            root = ctk.CTk()
            root.title("User Activity Tracker")
            root.geometry("800x600")
            # Create tabs with the root window
            global ua_tab, analytics_tab, settings_tab
            ua_tab = Tab(root, name="Activity", title="User Activity Tracker", icon="activity")
            analytics_tab = Tab(root, name="Analytics", title="Activity Analytics", icon="bar-chart-2")
            settings_tab = Tab(root, name="Settings", title="Tracker Settings", icon="settings")
    intents = discord.Intents.default()
    intents.messages = True
    intents.guilds = True
    intents.message_content = True  # Enable message content intent

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")

    if __name__ == "__main__":
        # Assign the bot instance to EventQueue before starting the application
        EventQueue.bot = bot
