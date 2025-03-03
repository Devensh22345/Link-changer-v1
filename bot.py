from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import cfg
from database import add_created_channel
import random
import string
import asyncio
import time
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

# Variable to control the infinite loop
changeall_running = False

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
    await message.reply_text(
        "Hello! Use /create to create a private channel.\n"
        "Use /change1 to change a channel link.\n"
        "Use /changeall to change all channel usernames in a loop.\n"
        "Use /stopchangeall to stop the change all process."
    )
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
            await log_to_channel(f"Found chat: {dialog.chat.title} | Type: {dialog.chat.type} | Username: @{dialog.chat.username if dialog.chat.username else 'No Username'}")

            # Check if the chat has a valid username
            if dialog.chat.username:
                channels.append(dialog.chat)
        
        if not channels:
            await message.reply_text("❌ No channels with a username found in the session account.")
            await log_to_channel("❌ No channels with a username found in the session account.")
            return

        # Display available channels as inline buttons
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

        # Update the channel username
        await user_app.set_chat_username(channel_id, new_username)        
        await callback_query.message.reply_text(f"✅ Channel link changed to: https://t.me/{new_username}")
        
        await log_to_channel(
            f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username} "
            f"by {callback_query.from_user.mention} (ID: {callback_query.from_user.id})"
        )

    except Exception as e:
        error_msg = f"❌ Error while changing link: {e}"
        await callback_query.message.reply_text(error_msg)
        await log_to_channel(error_msg)

async def show_countdown(seconds: int):
    message = await log_to_channel(f"⏳ Next channel link change in {seconds // 3600} hours, {(seconds % 3600) // 60} minutes...")
    while seconds > 0:
        await asyncio.sleep(30)  # Wait for 30 seconds
        seconds -= 30
        try:
            await message.edit_text(f"⏳ Next channel link change in {seconds // 3600} hours, {(seconds % 3600) // 60} minutes...")
        except Exception as e:
            print(f"Failed to edit message: {e}")

# Change all channels in a sequential loop
@app.on_message(filters.command("changeall"))
async def change_all_channel_links(client: Client, message: Message):
    global changeall_running
    sudo_users = cfg.SUDO

    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can change all channel links.")
        return

    if changeall_running:
        await message.reply_text("❌ The /changeall process is already running.")
        return

    changeall_running = True
    await message.reply_text("✅ Started changing all channel usernames in an infinite loop.")
    await log_to_channel("✅ Started /changeall process.")

    while changeall_running:
        try:
            channels = []
            async for dialog in user_app.get_dialogs():
                if dialog.chat.username:
                    channels.append(dialog.chat)

            if not channels:
                await log_to_channel("❌ No channels with a username found in the session account.")
                break

            for channel in channels:
                if not changeall_running:
                    break

                old_username = channel.username
                new_suffix = generate_random_string()
                new_username = f"{old_username[:-3]}{new_suffix}"

                # Change the channel username
                await user_app.set_chat_username(channel.id, new_username)
                await asyncio.sleep(2)
                await log_to_channel(
                    f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username}"
                )

                await asyncio.sleep(60)  # Wait 1 minutes before creating a temporary channel

                # Create a temporary channel with the old username
                try:
                    new_channel = await user_app.create_channel(
                        title=old_username, 
                        description=f"Temporary channel for @{old_username}"
                    )
                    await user_app.set_chat_username(new_channel.id, old_username)

                    add_created_channel(new_channel.id)
                    await asyncio.sleep(2)
                    await log_to_channel(f"✅ Temporary channel created with username @{old_username}")
                    await show_countdown(4 * 60 * 60)
                    # Schedule deletion after 4 hours
                    asyncio.create_task(delete_temp_channel_after_delay(new_channel.id, old_username))

                except Exception as e:
                    await log_to_channel(f"❌ Error creating temporary channel: {e}")

                # Show countdown for the next change (1 hour 20 min)
                await show_countdown(60 * 80)

                # Wait for 1 hour 20 min before changing the next channel
                await asyncio.sleep(60 * 80)

        except Exception as e:
            await log_to_channel(f"❌ Error while changing links in loop: {e}")
            await asyncio.sleep(60 * 80)

    await log_to_channel("🛑 The /changeall process was stopped.")

# Delete temporary channel after a delay
async def delete_temp_channel_after_delay(channel_id: int, username: str):
    await asyncio.sleep(4 * 60 * 60)  # Wait for 4 hours
    try:
        await user_app.delete_channel(channel_id)
        await asyncio.sleep(2)
        await log_to_channel(f"🗑️ Temporary channel @{username} deleted after 4 hours")
    except Exception as e:
        await log_to_channel(f"❌ Error deleting temporary channel @{username}: {e}")

# Stop the change all process
@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global changeall_running
    changeall_running = False
    await asyncio.sleep(2)
    await message.reply_text("🛑 Stopped the /changeall process.")
    await log_to_channel("🛑 The /changeall process was stopped.")

# Start both clients
print("Bot & User Session Running...")
user_app.start()
app.run()

