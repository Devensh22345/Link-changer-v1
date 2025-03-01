from pyrogram import Client, filters
from pyrogram.types import Message
from configs import cfg
from database import add_created_channel
import random
import string
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Client (for managing channels)
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.SESSION_STRING
)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Function to log messages in the log channel
async def log_to_channel(text: str):
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Failed to log message: {e}")

# Function to generate a random string of 3 characters (mix of letters and digits)
def generate_random_string():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=3))

# Start message
@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Use /create to create a private channel.\nUse /change1 to change a public channel link.")
    await log_to_channel(f"👋 Bot started by {message.from_user.mention} (ID: {message.from_user.id})")

# Create a private channel
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

# Change the last 3 characters of the public channel link
@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can change channel links.")
        await log_to_channel(f"❌ Unauthorized attempt to change channel link by {message.from_user.mention} (ID: {message.from_user.id})")
        return

    try:
        # Fetch all public channels using get_dialogs() method
        channels = []
        async for dialog in user_app.get_dialogs():
            if dialog.chat.type == "channel" and dialog.chat.username:
                channels.append(dialog.chat)
                await log_to_channel(f"✅ Found public channel: {dialog.chat.title} (Username: @{dialog.chat.username})")

        if not channels:
            await message.reply_text("❌ No public channels found in the session account.")
            await log_to_channel("❌ No public channels found in the session account.")
            return
        
        # Select the top-most public channel
        channel = channels[0]
        old_username = channel.username
        new_suffix = generate_random_string()
        new_username = f"{old_username[:-3]}{new_suffix}"

        # Update the channel username (link)
        await user_app.update_chat_username(channel.id, new_username)
        await message.reply_text(f"✅ Channel link changed to: https://t.me/{new_username}")
        await log_to_channel(f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username} by {message.from_user.mention} (ID: {message.from_user.id})")
    
    except Exception as e:
        error_msg = f"❌ Error while changing link: {e}"
        await message.reply_text(error_msg)
        await log_to_channel(error_msg)

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
