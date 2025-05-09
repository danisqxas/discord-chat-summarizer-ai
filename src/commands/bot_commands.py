# Bot commands module


async def summarize_command(ctx, args):
    """Main command for managing chat summarization."""
    await ctx.message.delete()

    if not args:
        # Generate a summary of the last messages
        await generate_summary(ctx.channel.id)
        return

    # Handle other subcommands (e.g., status, reset, chat)
    # ...existing logic for subcommands...


async def generate_summary(channel_id):
    """Generate a summary of the last messages in the specified channel."""
    # Logic for generating a summary
    # ...existing logic for summary generation...
