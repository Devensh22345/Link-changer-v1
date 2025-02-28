from pyrogram import Client, filters
import re
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from configs import cfg

# Set up logging to help with debugging and monitoring
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize MongoDB connection using Motor
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

# Replacement: Bold and clickable username for your channel.
replacement_username = "**[@DK_ANIMES](https://t.me/DK_ANIMES)**"
# Plain version (for comparisons) – set to your channel's username in lowercase.
my_channel_username = "dk_animes"

def replace_username(match):
    username = match.group(1)
    # If the found username is not your channel, replace it.
    if username.lower() != my_channel_username:
        return replacement_username
    else:
        return match.group(0)

# /start command to check if the bot is online (in private chat)
@app.on_message(filters.command("start") & filters.private)
async def start_message(_, message):
    logging.info(f"Received /start command from {message.chat.id}")
    await message.reply_text("✅ Bot is online and working!")

# Sample /sudo command (only accessible to sudo users defined in cfg.SUDO_USERS)
@app.on_message(filters.command("sudo") & filters.private)
async def sudo_command(_, message):
    if message.from_user and message.from_user.id in cfg.SUDO_USERS:
        await message.reply_text("✅ You are a sudo user.")
    else:
        await message.reply_text("❌ You are not authorized to use this command.")

# Handler to edit captions on messages in channels that are either video or document (file)
@app.on_message(filters.channel & (filters.video | filters.document))
async def edit_caption(_, message):
    chat_id = message.chat.id
    logging.info(f"Received message in channel {chat_id}")

    # Save the channel to MongoDB if it is not already stored.
    existing = await channels_collection.find_one({"chat_id": chat_id})
    if not existing:
        await channels_collection.insert_one({"chat_id": chat_id})
        logging.info(f"Stored new channel {chat_id} in MongoDB.")

    if message.caption:
        original_caption = message.caption
        # Replace any occurrence of @username with the replacement (unless it’s your channel)
        new_caption = re.sub(r"@([\w_]+)", replace_username, original_caption)
        logging.info(f"Original caption: {original_caption}")
        logging.info(f"New caption: {new_caption}")
        try:
            await message.edit_caption(new_caption, parse_mode="Markdown")
            logging.info(f"Edited caption in channel {chat_id}.")
        except Exception as e:
            logging.error(f"Failed to edit caption in channel {chat_id}: {e}")

async def main():
    try:
        await app.start()
        logging.info("Bot has started and is running.")
    except Exception as e:
        logging.error("Error starting the bot. Check BOT_TOKEN, API_ID, and API_HASH. Error: %s", e)
        return  # Stop execution if credentials are wrong
    await asyncio.Event().wait()  # Keeps the bot running indefinitely

if __name__ == "__main__":
    logging.info("I'm Alive Now!")
    asyncio.run(main())
