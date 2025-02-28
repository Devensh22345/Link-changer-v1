from pyrogram import Client, filters
import re
import asyncio
from configs import cfg

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**[@DK_ANIMES](https://t.me/DK_ANIMES)**"  # Bold and clickable username

# /start command to check if the bot is running
@app.on_message(filters.command("start") & filters.private)
async def start_message(_, message):
    await message.reply_text("✅ Bot is online and working!")

@app.on_message(filters.channel & filters.video)  # Only for videos in channels
async def edit_caption(_, message):
    """Edit video captions if posted by the channel itself (admin posts)."""
    if message.caption and message.sender_chat:  # Ensure message has a caption and is from the channel
        new_caption = re.sub(r"@[\w_]+", replacement_username, message.caption)
        
        try:
            await message.edit_caption(new_caption, parse_mode="Markdown")
            print(f"Edited caption in {message.chat.id}")
        except Exception as e:
            print(f"Failed to edit caption in {message.chat.id}: {e}")

async def main():
    await app.start()
    print("hello")  # Prints when the bot starts
    await asyncio.Event().wait()  # Keeps the bot running

print("I'm Alive Now!")

# Runs the bot correctly
asyncio.run(main())
