from pyrogram import Client, filters
from pyrogram.types import Message
from configs import cfg
from database import add_created_channel
import asyncio
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647
# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Client (for creating channels)
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.SESSION_STRING
)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Function to log messages in the log channel
async def log_to_channel(text: str):
    await app.send_message(LOG_CHANNEL, text)

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Use /create to create a private channel.")
    await log_to_channel(f"👋 Bot started by {message.from_user.mention} (ID: {message.from_user.id})")

@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can create channels.")
        await log_to_channel(f"❌ Unauthorized attempt to create a channel by {message.from_user.mention} (ID: {message.from_user.id})")
        return
    
    try:
        channel = await user_app.create_channel(
            title="hi",
            description="A private channel created by the bot."
        )
        add_created_channel(channel.id)
        await message.reply_text(f"✅ Private channel created: {channel.title}")
        await log_to_channel(f"✅ Channel '{channel.title}' created by {message.from_user.mention} (ID: {message.from_user.id})")
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        await message.reply_text(error_msg)
        await log_to_channel(error_msg)

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
