from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import cfg
from database import add_created_channel
import random
import string
import asyncio
import pyrogram.utils
from pyrogram.errors import FloodWait, UsernameOccupied, RPCError
from typing import List
import os

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
    if session_name not in user_apps:
        user_apps[session_name] = Client(session_name, api_id=cfg.API_ID, api_hash=cfg.API_HASH, session_string=session_string)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Variable to control the infinite loop
changeall_running = False
current_session = None

# Load loop state from file
def load_loop_state():
    try:
        with open("loop_state.txt", "r") as f:
            return f.read().strip() == "1"
    except FileNotFoundError:
        return False

# Save loop state to file
def save_loop_state(state: bool):
    with open("loop_state.txt", "w") as f:
        f.write("1" if state else "0")

# Function to log messages in the log channel
async def log_to_channel(text: str):
    await asyncio.sleep(2)
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
@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can create channels.")
        await log_to_channel(f"❌ Unauthorized attempt to create a channel by {message.from_user.mention} (ID: {message.from_user.id})")
        return

    try:
        if current_session not in user_apps:
            await message.reply_text("⚠️ No session is currently selected.")
            return

        user = user_apps[current_session]
        channel = await user.create_channel(
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

# /changeall command — show session buttons and "All"
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
    buttons.append([InlineKeyboardButton(text="🔁 All", callback_data="select_session_all")])

    await message.reply_text(
        "Select a session or click 🔁 All to start changing usernames in all accounts:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Session or "All" handler
@app.on_callback_query(filters.regex(r"^select_session_"))
async def on_select_session(client, callback_query):
    global current_session, changeall_running
    changeall_running = True
    save_loop_state(True)

    session_name = callback_query.data.split("_")[2]

    if session_name == "all":
        await callback_query.answer("🔁 All sessions selected.")
        await callback_query.message.edit_text("✅ Started username changing loop for ALL sessions.")
        await log_to_channel("🔁 Started changing usernames for all sessions.")

        tasks = []
        for session_key in user_apps.keys():
            tasks.append(asyncio.create_task(process_username_loop(session_key)))

        await asyncio.gather(*tasks, return_exceptions=True)
        await log_to_channel("✅ Finished processing all sessions.")
    else:
        current_session = session_name
        await callback_query.answer(f"Session {session_name} selected.")
        await callback_query.message.edit_text(f"✅ Session '{session_name}' selected. Starting username change loop...")
        await log_to_channel(f"🔁 Started change loop for session: {session_name}")
        await process_username_loop(session_name)

    changeall_running = False
    save_loop_state(False)
    await log_to_channel("🛑 Change loop stopped.")

# Reusable function for the loop
async def process_username_loop(session_name):
    try:
        user = user_apps[session_name]
        channels = []

        async for dialog in user.get_dialogs():
            if dialog.chat.username:
                channels.append(dialog.chat)

        if not channels:
            await log_to_channel(f"❌ No channels with usernames in session {session_name}.")
            return

        for channel in channels:
            if not changeall_running:
                break

            old_username = channel.username
            new_suffix = generate_random_string()
            new_username = f"{old_username[:-2]}{new_suffix}"

            try:
                await user.set_chat_username(channel.id, new_username)
                await log_to_channel(f"✅ [{session_name}] Changed: https://t.me/{old_username} → https://t.me/{new_username}")

            except UsernameOccupied:
                retry_suffix = generate_random_string()
                retry_username = f"{old_username[:-2]}{retry_suffix}"
                try:
                    await user.set_chat_username(channel.id, retry_username)
                    await log_to_channel(f"✅ [{session_name}] Retry: https://t.me/{old_username} → https://t.me/{retry_username}")
                except Exception as e:
                    await log_to_channel(f"❌ [{session_name}] Retry failed: {e}")

            except FloodWait as e:
                await log_to_channel(f"❌ [{session_name}] FloodWait: sleeping {e.value}s")
                await asyncio.sleep(e.value)

            except RPCError as e:
                await log_to_channel(f"❌ [{session_name}] RPCError: {e}")

            await asyncio.sleep(60)

    except Exception as e:
        await log_to_channel(f"❌ [{session_name}] Loop error: {e}")
        await asyncio.sleep(2)

# Change the channel link for channels with a username
@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    sudo_users = cfg.SUDO
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can change channel links.")
        await log_to_channel(f"❌ Unauthorized attempt to change channel link by {message.from_user.mention} (ID: {message.from_user.id})")
        return

    if current_session not in user_apps:
        await message.reply_text("⚠️ No session is currently selected.")
        return

    try:
        channels = []
        user = user_apps[current_session]

        async for dialog in user.get_dialogs():
            await log_to_channel(f"Found chat: {dialog.chat.title} | Type: {dialog.chat.type} | Username: @{dialog.chat.username if dialog.chat.username else 'No Username'}")
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

        if current_session not in user_apps:
            await callback_query.answer("⚠️ No session is currently selected.", show_alert=True)
            return

        user = user_apps[current_session]
        channel = await user.get_chat(channel_id)

        if not channel.username:
            await callback_query.answer("❌ This channel does not have a username!", show_alert=True)
            return

        old_username = channel.username
        new_suffix = generate_random_string()
        new_username = f"{old_username[:-3]}{new_suffix}"

        await user.set_chat_username(channel_id, new_username)

        await callback_query.message.reply_text(f"✅ Channel link changed to: https://t.me/{new_username}")
        await log_to_channel(
            f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username} "
            f"by {callback_query.from_user.mention} (ID: {callback_query.from_user.id})"
        )

    except Exception as e:
        error_msg = f"❌ Error while changing link: {e}"
        await callback_query.message.reply_text(error_msg)
        await log_to_channel(error_msg)

# Stop the change all process gracefully
@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global changeall_running
    changeall_running = False
    save_loop_state(False)
    await message.reply_text("🛑 Stopped the /changeall process.")
    await log_to_channel("🛑 The /changeall process was stopped.")

# Start both clients
print("Bot & User Sessions Running...")
for session_name, session_string in cfg.SESSIONS.items():
    try:
        add_user_session(session_name, session_string)
        user_apps[session_name].start()
        print(f"✅ Started session: {session_name}")
    except Exception as e:
        print(f"❌ Failed to start session {session_name}: {e}")

# Resume loop if it was active before restart
changeall_running = load_loop_state()
if changeall_running:
    print("🔁 Resuming username changing loop after restart...")
    for session_key in user_apps.keys():
        asyncio.create_task(process_username_loop(session_key))

app.run()
