from pyrogram import Client, filters
import re
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from configs import cfg

# Initialize MongoDB Client
mongo_client = AsyncIOMotorClient(cfg.MONGO_URL)
db = mongo_client["autoposter_db"]
channels_collection = db["channels"]

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**@DK_ANIMES**"  # Bold username in Markdown

@app.on_message(filters.channel & (filters.photo | filters.video | filters.animation | filters.document))
async def edit_caption(_, message):
    """Detect media posts (image, video, GIF, document) in a channel and edit only the caption."""
    if message.caption:  # Only modify if there's a caption
        new_caption = re.sub(r"@([\w_]+)", lambda m: replacement_username, message.caption)

        try:
            await message.edit_caption(new_caption, parse_mode="Markdown")  # Edit caption with Markdown format
        except Exception as e:
            print(f"Failed to edit caption in {message.chat.id}: {e}")

async def main():
    await app.start()
    print("hello")  # Print when the bot starts
    await asyncio.Event().wait()  # Keep the bot running

print("I'm Alive Now!")

# Correct way to run the bot
asyncio.run(main())  # Runs the async main function properly
