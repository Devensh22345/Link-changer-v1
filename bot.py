import asyncio
import random
import string
from pyrogram import Client, filters
from config import LOG_CHANNEL, API_ID, API_HASH
from plugins.database import db
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

LOG_TEXT = """<b>#NewUser

ID - <code>{}</code>

Name - {}</b>
"""

changeall_running = False

# Start Command
@Client.on_message(filters.command('start'))
async def start_message(c, m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id, m.from_user.first_name)
        await c.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
    await m.reply("Hello")

# Create Channel Command
@Client.on_message(filters.command("create"))
async def create_channel(bot: Client, message: Message):
    user_id = message.from_user.id
    sessions = await db.get_sessions(user_id)

    if not sessions:
        await message.reply("You need to /login first.")
        return

    buttons = [
        [InlineKeyboardButton(label, callback_data=f"create_{label}")]
        for label in sessions.keys()
    ]
    await message.reply(
        "Select an assistant account to create the channel:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^create_(.+)"))
async def handle_account_selection(bot: Client, query):
    user_id = query.from_user.id
    label = query.data.split("_", 1)[1]
    sessions = await db.get_sessions(user_id)

    if label not in sessions:
        await query.message.edit("Invalid selection. Please try again.")
        return

    await query.message.edit("Enter the name for the new private channel:")

    try:
        name_msg = await bot.listen(user_id, timeout=60)
        channel_name = name_msg.text.strip()
        if not channel_name:
            await query.message.reply("Invalid channel name. Please try again.")
            return
    except asyncio.TimeoutError:
        await query.message.reply("Time out. Please try again.")
        return

    session_string = sessions[label]
    try:
        client = Client(":memory:", session_string=session_string, api_id=API_ID, api_hash=API_HASH)
        await client.start()
        new_channel = await client.create_channel(channel_name, "")
        await query.message.reply(
            f"Private channel '{channel_name}' created successfully!\nChannel ID: `{new_channel.id}`"
        )
        await client.stop()
    except Exception as e:
        await query.message.reply(f"Failed to create the channel: {str(e)}")

# Start the Automatic Username Change Process
@Client.on_message(filters.command("change_all"))
async def change_all_channel_links(bot: Client, message: Message):
    global changeall_running

    if changeall_running:
        await message.reply("❌ The /change_all process is already running.")
        return

    user_id = message.from_user.id
    sessions = await db.get_sessions(user_id)

    if not sessions:
        await message.reply("You need to /login first.")
        return

    buttons = [
        [InlineKeyboardButton(label, callback_data=f"changeall_{label}")]
        for label in sessions.keys()
    ]
    await message.reply(
        "Select an assistant account for automatic username changing:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@Client.on_callback_query(filters.regex(r"^changeall_(.+)"))
async def handle_changeall_selection(bot: Client, query):
    global changeall_running

    user_id = query.from_user.id
    label = query.data.split("_", 1)[1]
    sessions = await db.get_sessions(user_id)

    if label not in sessions:
        await query.message.edit("Invalid selection. Please try again.")
        return

    if changeall_running:
        await query.message.edit("❌ The /change_all process is already running.")
        return

    session_string = sessions[label]
    await query.message.edit("✅ Started changing all channel usernames in an infinite loop.")
    
    changeall_running = True
    asyncio.create_task(change_all_usernames(bot, session_string, user_id))

async def change_all_usernames(bot: Client, session_string: str, user_id: int):
    global changeall_running
    try:
        client = Client(":memory:", session_string=session_string, api_id=API_ID, api_hash=API_HASH)
        await client.start()

        while changeall_running:
            channels = []
            async for dialog in client.get_dialogs():
                if dialog.chat.username:
                    channels.append(dialog.chat)

            if not channels:
                await bot.send_message(user_id, "❌ No channels with a username found in the session account.")
                break

            for channel in channels:
                if not changeall_running:
                    break

                try:
                    old_username = channel.username
                    new_username = generate_username(old_username)
                    await client.set_chat_username(channel.id, new_username)
                    await bot.send_message(
                        user_id,
                        f"✅ Channel link changed from https://t.me/{old_username} to https://t.me/{new_username}"
                    )
                    await asyncio.sleep(3600)  # Wait for 1 hour
                except Exception as e:
                    await bot.send_message(user_id, f"❌ Failed to change username for {channel.title}: {str(e)}")
                    await asyncio.sleep(1800)  # Wait for 30 minutes on failure

        await client.stop()

    except Exception as e:
        await bot.send_message(user_id, f"❌ An error occurred: {str(e)}")

    finally:
        changeall_running = False
        await bot.send_message(user_id, "🛑 The /change_all process was stopped.")

# Stop the Automatic Username Change Process
@Client.on_message(filters.command("stopchangeall"))
async def stop_change_all(bot: Client, message: Message):
    global changeall_running
    if not changeall_running:
        await message.reply("❌ No active /change_all process found.")
        return

    changeall_running = False
    await message.reply("🛑 Stopped the /change_all process.")

# Generate a New Username
def generate_username(old_username: str) -> str:
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=2))
    return old_username[:-2] + suffix
