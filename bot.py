from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import cfg
from database import add_created_channel
import random
import string
import asyncio
import pyrogram.utils
from pyrogram.errors import FloodWait, UsernameOccupied
from typing import List

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Clients for multiple sessions
user_apps = {}

# Add a session to the bot
def add_user_session(session_name: str, session_string: str):
    user_apps[session_name] = Client(session_name, api_id=cfg.API_ID, api_hash=cfg.API_HASH, session_string=session_string)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Variable to control the infinite loop
changeall_running = False
current_session = None

# Function to log messages in the log channel
async def log_to_channel(text: str):
    await asyncio.sleep(2)  # Delay log sending by 2 seconds
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Failed to log message: {e}")

# Function to generate a random string of 2 characters (mix of letters and digits)
def generate_random_string():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=2))

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
# /changeall command — show session buttons
@app.on_message(filters.command("changeall"))
async def change_all_channel_links(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can change all channel links.")
        return

    if changeall_running:
        await message.reply_text("❌ The /changeall process is already running.")
        return

    buttons = [
        [InlineKeyboardButton(text=session_name, callback_data=f"select_session_{session_name}")]
        for session_name in user_apps.keys()
    ]

    await message.reply_text(
        "Select a session to start changing usernames:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Handle session selection and immediately start loop
@app.on_callback_query(filters.regex(r"^select_session_"))
async def on_select_session(client, callback_query):
    global current_session, changeall_running

    session_name = callback_query.data.split("_")[2]
    current_session = session_name
    changeall_running = True

    await callback_query.answer(f"Session {session_name} selected.")
    await callback_query.message.edit_text(f"✅ Session '{session_name}' selected. Starting username change loop...")

    await log_to_channel(f"🔁 Started change loop for session: {session_name}")

    while changeall_running:
        try:
            channels = []
            async for dialog in user_apps[current_session].get_dialogs():
                if dialog.chat.username:
                    channels.append(dialog.chat)

            if not channels:
                await log_to_channel("❌ No channels with a username found.")
                break

            for channel in channels:
                if not changeall_running:
                    break

                old_username = channel.username
                new_suffix = generate_random_string()
                new_username = f"{old_username[:-2]}{new_suffix}"

                try:
                    await user_apps[current_session].set_chat_username(channel.id, new_username)
                    await log_to_channel(
                        f"✅ Changed: https://t.me/{old_username} → https://t.me/{new_username}"
                    )
                except UsernameOccupied:
                    retry_suffix = generate_random_string()
                    retry_username = f"{old_username[:-2]}{retry_suffix}"
                    try:
                        await user_apps[current_session].set_chat_username(channel.id, retry_username)
                        await log_to_channel(
                            f"✅ Changed (retry): https://t.me/{old_username} → https://t.me/{retry_username}"
                        )
                    except Exception as e:
                        await log_to_channel(f"❌ Retry failed: {e}")
                except FloodWait as e:
                    await log_to_channel(f"❌ FloodWait: sleeping {e.value}s")
                    await asyncio.sleep(e.value)

                await asyncio.sleep(60)  # 1 min delay

        except Exception as e:
            await log_to_channel(f"❌ Loop error: {e}")
            await asyncio.sleep(2)

    await log_to_channel("🛑 Change loop stopped.")

# Stop the change all process gracefully
@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global changeall_running
    changeall_running = False
    await message.reply_text("🛑 Stopped the /changeall process.")
    await log_to_channel("🛑 The /changeall process was stopped.")

# Start both clients
print("Bot & User Sessions Running...")
# Load and start all user sessions from config
for session_name, session_string in cfg.SESSIONS.items():
    add_user_session(session_name, session_string)
    user_apps[session_name].start()
    print(f"✅ Started session: {session_name}")
app.run()

