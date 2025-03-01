from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import cfg
from database import (
    add_created_channel, 
    get_created_channels, 
    delete_created_channel, 
    add_temporary_channel, 
    delete_temporary_channel, 
    log_channel_username_change, 
    log_new_channel_creation
)
import random
import string
import pyrogram.utils
import asyncio

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
change_all_active = False

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
    await message.reply_text("Hello! Use /create to create a private channel.\nUse /change1 to change a channel link.\nUse /changeall to change all channel usernames.")
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

# Change the channel link for channels with a username
@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can change channel links.")
        await log_to_channel(f"❌ Unauthorized attempt to change channel link by {message.from_user.mention} (ID: {message.from_user.id})")
        return

    try:
        channels = []
        async for dialog in user_app.get_dialogs():
            if dialog.chat.username:
                channels.append(dialog.chat)
        
        if not channels:
            await message.reply_text("❌ No channels with a username found in the session account.")
            await log_to_channel("❌ No channels with a username found in the session account.")
            return

        buttons = [
            [InlineKeyboardButton(text=channel.title, callback_data=f"change_{channel.id}")]
            for channel in channels
        ]
        await message.reply_text(
            "Select a channel to change its link:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except Exception as e:
        error_msg = f"❌ Error while fetching channels: {e}"
        await message.reply_text(error_msg)
        await log_to_channel(error_msg)

# Handle the button press and change the link
@app.on_callback_query(filters.regex(r"^change_"))
async def on_callback_query(client, callback_query):
    try:
        channel_id = int(callback_query.data.split("_")[1])
        channel = await user_app.get_chat(channel_id)

        if not channel.username:
            await callback_query.answer("❌ This channel does not have a username!", show_alert=True)
            return

        old_username = channel.username
        new_suffix = generate_random_string()
        new_username = f"{old_username[:-3]}{new_suffix}"

        await user_app.set_chat_username(channel_id, new_username)

        await callback_query.message.reply_text(f"✅ Channel link changed to: https://t.me/{new_username}")
        
        await log_to_channel(
            f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username} "
            f"by {callback_query.from_user.mention} (ID: {callback_query.from_user.id})"
        )

        log_channel_username_change(old_username, new_username, callback_query.from_user.mention)

    except Exception as e:
        error_msg = f"❌ Error while changing link: {e}"
        await callback_query.message.reply_text(error_msg)
        await log_to_channel(error_msg)

# Change all channel usernames in an infinite loop
@app.on_message(filters.command("changeall"))
async def change_all_usernames(client: Client, message: Message):
    global change_all_active
    change_all_active = True
    await message.reply_text("🔁 Starting infinite loop to change all channel usernames every hour.")
    await log_to_channel("🔁 Started infinite loop to change all channel usernames every hour.")

    while change_all_active:
        async for dialog in user_app.get_dialogs():
            if not change_all_active:
                break
            if dialog.chat.username:
                try:
                    old_username = dialog.chat.username
                    new_suffix = generate_random_string()
                    new_username = f"{old_username[:-3]}{new_suffix}"

                    await user_app.set_chat_username(dialog.chat.id, new_username)

                    await log_to_channel(
                        f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username}"
                    )

                    log_channel_username_change(old_username, new_username, message.from_user.mention)

                    # Create a new temporary channel with the old username
                    new_channel = await user_app.create_channel(
                        title="Temporary Channel",
                        description="Temporary channel for old username reuse"
                    )
                    await user_app.set_chat_username(new_channel.id, old_username)

                    add_temporary_channel(new_channel.id, old_username, message.from_user.mention)
                    log_new_channel_creation(new_channel.id, old_username, message.from_user.mention)
                    
                    await log_to_channel(f"✅ Created temporary channel with username: https://t.me/{old_username}")

                    await asyncio.sleep(10800)  # Wait 3 hours before deleting the channel
                    await user_app.delete_channel(new_channel.id)
                    delete_temporary_channel(new_channel.id)
                    await log_to_channel(f"🗑️ Deleted temporary channel with ID: {new_channel.id}")

                except Exception as e:
                    await log_to_channel(f"❌ Error: {e}")

            await asyncio.sleep(3600)  # Wait 1 hour before changing the next channel

# Stop the infinite loop of changeall command
@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global change_all_active
    change_all_active = False
    await message.reply_text("⏹️ Stopped changing all channel usernames.")
    await log_to_channel("⏹️ Stopped the infinite loop for changing all channel usernames.")

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
