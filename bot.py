from pyrogram import Client, filters
import re
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from configs import cfg

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize MongoDB
mongo_client = AsyncIOMotorClient(cfg.MONGO_URL)
db = mongo_client["autoposter_db"]
channels_collection = db["channels"]

# Initialize Pyrogram Client
app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**[@DK_ANIMES](https://t.me/DK_ANIMES)**"  # Bold and clickable username

# /start command to check if the bot is online
@app.on_message(filters.command("start") & filters.private)
async def start_message(_, message):
    logging.info(f"Received /start command from {message.chat.id}")
    await message.reply_text("✅ Bot is online and working!")

# Video message handler in channels
@app.on_message(filters.channel & filters.video)
async def edit_caption(_, message):
    """Edit video captions in channels and store the channel in MongoDB."""
    chat_id = message.chat.id
    logging.info(f"Received video in chat: {chat_id}")

    # Store channel in MongoDB if not already present
    existing_channel = await channels_collection.find_one({"chat_id": chat_id})
    if not existing_channel:
        await channels_collection.insert_one({"chat_id": chat_id})
        logging.info(f"Stored new channel {chat_id} in MongoDB")

    # Edit the caption
    if message.caption:
        new_caption = re.sub(r"@[\w_]+", replacement_username, message.caption)
        logging.info(f"New caption: {new_caption}")
        try:
            await message.edit_caption(new_caption, parse_mode="Markdown")
            logging.info(f"Edited caption in chat: {chat_id}")
        except Exception as e:
            logging.error(f"Failed to edit caption in chat {chat_id}: {e}")

async def main():
    try:
        await app.start()
        logging.info("Bot has started and is running.")
    except Exception as e:
        logging.error("Error starting the bot. Check BOT_TOKEN, API_ID, and API_HASH. Error: %s", e)
        return  # Stop execution if credentials are wrong

    await asyncio.Event().wait()  # Keeps the bot running

if __name__ == "__main__":
    logging.info("I'm Alive Now!")
    asyncio.run(main())
