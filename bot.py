from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import cfg
from database import add_created_channel, save_old_username, get_old_username, get_all_saved_usernames
import random
import string
import asyncio
import time
import pyrogram.utils
from pyrogram.errors import FloodWait, UsernameOccupied
import os
import logging  # Make sure logging is imported

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Dictionary to hold multiple user session clients
session_clients = {}

for i in range(1, 31):
    session_key = f"session{i}"
    session_string = getattr(cfg, f"SESSION_STRING_{i}", None)
    if session_string:
        session_clients[session_key] = Client(
            session_key,
            api_id=cfg.API_ID,
            api_hash=cfg.API_HASH,
            session_string=session_string
        )

# Start all session clients
async def start_all_sessions():
    for session_key, client in session_clients.items():
        try:
            await client.start()
            logging.info(f"Started {session_key}")
        except Exception as e:
            logging.error(f"Failed to start {session_key}: {e}")

LOG_CHANNEL = cfg.LOG_CHANNEL
changeall_running = False
channel_last_updated = {}

def generate_random_string():
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=2))

async def log_to_channel(text: str):
    await asyncio.sleep(2)
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Failed to log message: {e}")

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text(
        "Hello! Use /create, /change1, /changeall, /stopchangeall, /private, /public."
    )
    await log_to_channel(f"👋 Bot started by {message.from_user.mention} (ID: {message.from_user.id})")

@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        return await message.reply_text("❌ Only sudo users can create channels.")

    buttons = [
        [InlineKeyboardButton(f"Session {i}", callback_data=f"create_session{i}")]
        for i in range(1, 11) if f"session{i}" in session_clients
    ]
    await message.reply_text("Select session:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"^create_session(\d+)$"))
async def handle_create_callback(client, callback_query):
    session_number = callback_query.data.replace("create_session", "")
    session_key = f"session{session_number}"
    selected_client = session_clients[session_key]
    try:
        channel = await selected_client.create_channel(
            title="hi",
            description="A private channel created by the bot."
        )
        add_created_channel(channel.id)
        await callback_query.message.reply_text(f"✅ Channel created in {session_key}: {channel.title}")
    except Exception as e:
        await callback_query.message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        return await message.reply_text("❌ Only sudo users can change channel links.")

    buttons = [
        [InlineKeyboardButton(f"Session {i}", callback_data=f"change1_session{i}")]
        for i in range(1, 11) if f"session{i}" in session_clients
    ]
    await message.reply_text("Select a session:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"^change1_session(\d+)$"))
async def handle_change1_callback(client, callback_query):
    session_number = callback_query.data.replace("change1_session", "")
    session_key = f"session{session_number}"
    selected_client = session_clients[session_key]

    channels = [d.chat for d in await selected_client.get_dialogs() if d.chat.username]
    if not channels:
        return await callback_query.message.reply_text("❌ No channels with usernames found.")

    buttons = [
        [InlineKeyboardButton(channel.title, callback_data=f"change1_{session_key}_{channel.id}")]
        for channel in channels
    ]
    await callback_query.message.reply_text("Select a channel:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"^change1_session\d+_(-?\d+)$"))
async def on_channel_change_callback(client, callback_query):
    _, session_key, channel_id = callback_query.data.split("_")
    selected_client = session_clients[session_key]
    channel_id = int(channel_id)

    try:
        channel = await selected_client.get_chat(channel_id)
        old_username = channel.username
        new_suffix = generate_random_string()
        new_username = f"{old_username[:-3]}{new_suffix}"

        await selected_client.set_chat_username(channel.id, new_username)
        await callback_query.message.reply_text(f"✅ Changed to: https://t.me/{new_username}")
    except Exception as e:
        await callback_query.message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("changeall"))
async def changeall_command(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton(f"Session {i}", callback_data=f"changeall_session{i}")]
        for i in range(1, 31) if f"session{i}" in session_clients
    ]
    buttons.append([InlineKeyboardButton("All", callback_data="changeall_all")])
    await message.reply_text("Select a session:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"^changeall_session(\d+)$"))
async def handle_changeall_session(client: Client, callback_query):
    global changeall_running
    session_number = callback_query.data.replace("changeall_session", "")
    session_key = f"session{session_number}"
    selected_client = session_clients[session_key]
    changeall_running = True

    await callback_query.message.reply_text(f"✅ Started changing usernames for {session_key}.")

    async def process_session():
        global changeall_running
        async for dialog in selected_client.get_dialogs():
            if not changeall_running:
                break
            if not dialog.chat.username:
                continue

            old_username = dialog.chat.username
            new_suffix = generate_random_string()
            new_username = f"{old_username[:max(5, len(old_username) - 2)]}{new_suffix}"

            try:
                await selected_client.set_chat_username(dialog.chat.id, new_username)
                await log_to_channel(f"✅ {session_key}: @{old_username} → @{new_username}")
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except UsernameOccupied:
                continue
            except Exception as e:
                await log_to_channel(f"❌ {session_key} error: {e}")
                continue

            await asyncio.sleep(3600)

    asyncio.create_task(process_session())

@app.on_callback_query(filters.regex(r"^changeall_all$"))
async def handle_changeall_all_sessions(client: Client, callback_query):
    global changeall_running
    if changeall_running:
        return await callback_query.answer("⚠️ Already running.", show_alert=True)

    changeall_running = True
    await callback_query.message.reply_text("✅ Started changing usernames for ALL sessions.")

    async def process_session(session_key, selected_client):
        while changeall_running:
            try:
                channels = [d.chat for d in await selected_client.get_dialogs() if d.chat.username]
                for channel in channels:
                    if not changeall_running:
                        break
                    old_username = channel.username
                    new_suffix = generate_random_string()
                    new_username = f"{old_username[:max(5, len(old_username) - 2)]}{new_suffix}"
                    try:
                        await selected_client.set_chat_username(channel.id, new_username)
                        await log_to_channel(f"✅ {session_key}: @{old_username} → @{new_username}")
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    except UsernameOccupied:
                        continue
                    except Exception as e:
                        await log_to_channel(f"❌ {session_key} error: {e}")
                    await asyncio.sleep(5400)
            except Exception:
                await asyncio.sleep(5)

    for session_key, selected_client in session_clients.items():
        asyncio.create_task(process_session(session_key, selected_client))

@app.on_message(filters.command("stopchangeall"))
async def stop_changeall(client: Client, message: Message):
    global changeall_running
    if message.from_user.id not in cfg.SUDO:
        return await message.reply_text("❌ Only sudo users can stop changeall.")
    changeall_running = False
    await message.reply_text("🛑 changeall process stopped.")

@app.on_message(filters.command("private"))
async def make_channels_private(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        return await message.reply_text("❌ Only sudo users can use this command.")

    await message.reply_text("🔒 Making channels private...")
    for session_key, session_client in session_clients.items():
        async for dialog in session_client.get_dialogs():
            if dialog.chat.type != "channel" or not dialog.chat.username:
                continue
            try:
                save_old_username(dialog.chat.id, dialog.chat.username)
                await session_client.set_chat_username(dialog.chat.id, None)
                await log_to_channel(f"🔒 @{dialog.chat.username} made private.")
            except Exception as e:
                await log_to_channel(f"❌ Failed for @{dialog.chat.username}: {e}")
    await message.reply_text("✅ Done.")

@app.on_message(filters.command("public"))
async def make_channels_public(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        return await message.reply_text("❌ Only sudo users can use this command.")

    await message.reply_text("🌐 Making channels public again...")
    for entry in get_all_saved_usernames():
        channel_id = entry["channel_id"]
        old_username = entry["username"]
        for session_key, session_client in session_clients.items():
            try:
                await session_client.set_chat_username(channel_id, old_username)
                await log_to_channel(f"🌐 Restored @{old_username} on {session_key}")
                break
            except Exception:
                continue
    await message.reply_text("✅ Public restoration attempt complete.")

# Start all sessions on bot startup
async def main():
    await start_all_sessions()
    await app.start()
    print("Bot started!")
    try:
        # keep the program running
        await asyncio.Event().wait()
    finally:
        await app.stop()
