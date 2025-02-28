import re
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient

# Bot Configuration
API_ID = "29308061"
API_HASH = "462de3dfc98fd938ef9c6ee31a72d099"
BOT_TOKEN = "6963634345:AAEcvFr_rg3133R5BVZOiD35Kz09fNfYkfk"
MONGO_URI = "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
REPLACEMENT_CHANNEL = "@DK_ANIME"

# Initialize Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Pyrogram Client
bot = Client("CaptionEditorBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize MongoDB
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["telegram_bot"]
channels_collection = db["channels"]

async def add_channel(channel_id):
    """ Add channel to MongoDB if not exists """
    existing = await channels_collection.find_one({"channel_id": channel_id})
    if not existing:
        await channels_collection.insert_one({"channel_id": channel_id})
        logger.info(f"Added new channel to DB: {channel_id}")

@bot.on_message(filters.chat([]) & (filters.video | filters.document))
async def edit_caption(client: Client, message: Message):
    """ Edit captions to replace any channel mentions with @DK_ANIME """
    chat_id = message.chat.id

    # Ensure bot is tracking the channel
    await add_channel(chat_id)

    if message.caption:
        updated_caption = re.sub(r"@[\w_]+|t\.me/[\w_]+", REPLACEMENT_CHANNEL, message.caption)

        if updated_caption != message.caption:
            try:
                await message.edit_caption(updated_caption)
                logger.info(f"Edited caption in {chat_id}: {updated_caption}")
            except Exception as e:
                logger.error(f"Failed to edit caption in {chat_id}: {e}")

@bot.on_chat_member_updated
async def track_channels(client: Client, event):
    """ Track when the bot is added to a new channel """
    if event.new_chat_member and event.new_chat_member.user.id == bot.me.id:
        await add_channel(event.chat.id)
        logger.info(f"Bot added to channel: {event.chat.id}")

@bot.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    """ Send a start message """
    await message.reply("Hello! I'm a bot that automatically edits captions in channels.")

# Run the bot
bot.run()
