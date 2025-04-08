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

app = Client("bot", api_id=cfg.API_ID, api_hash=cfg.API_HASH, bot_token=cfg.BOT_TOKEN)
user_app = Client("user_session", api_id=cfg.API_ID, api_hash=cfg.API_HASH, session_string=cfg.SESSION_STRING)

LOG_CHANNEL = cfg.LOG_CHANNEL
changeall_running = False


async def log_to_channel(text: str):
    await asyncio.sleep(2)
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Log error: {e}")


def generate_random_string(length=2):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text(
        "Hello! Use /create to create a private channel.\n"
        "Use /change1 to change a channel link.\n"
        "Use /changeall to change all channel usernames in a loop.\n"
        "Use /stopchangeall to stop the process."
    )
    await log_to_channel(f"Bot started by {message.from_user.mention} (ID: {message.from_user.id})")


@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        await message.reply_text("Only sudo users can create channels.")
        return

    try:
        channel = await user_app.create_channel(
            title="hi",
            description="A private channel created by the bot."
        )
        add_created_channel(channel.id)
        await message.reply_text(f"Private channel created: {channel.title}")
        await log_to_channel(f"Channel '{channel.title}' created by {message.from_user.mention}")
    except Exception as e:
        await message.reply_text(f"Error: {e}")
        await log_to_channel(f"Error creating channel: {e}")


@app.on_message(filters.command("change1"))
async def change_channel_link(client: Client, message: Message):
    if message.from_user.id not in cfg.SUDO:
        await message.reply_text("Only sudo users can change links.")
        return

    try:
        channels = [
            dialog.chat async for dialog in user_app.get_dialogs()
            if dialog.chat.username and dialog.chat.type == "channel"
        ]

        if not channels:
            await message.reply_text("No channels with usernames found.")
            return

        buttons = [[InlineKeyboardButton(text=channel.title, callback_data=f"change_{channel.id}")]
                   for channel in channels]

        await message.reply_text("Select a channel to change its link:", reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        await message.reply_text(f"Error: {e}")
        await log_to_channel(f"Error fetching channels: {e}")


@app.on_callback_query(filters.regex(r"^change_"))
async def on_callback_query(client, callback_query):
    try:
        channel_id = int(callback_query.data.split("_")[1])
        channel = await user_app.get_chat(channel_id)

        if not channel.username:
            await callback_query.answer("This channel has no username.", show_alert=True)
            return

        old_username = channel.username
        new_suffix = generate_random_string()
        new_username = f"{old_username[:-2]}{new_suffix}"

        await user_app.set_chat_username(channel.id, new_username)

        await callback_query.message.reply_text(f"Link changed to: https://t.me/{new_username}")
        await log_to_channel(
            f"Changed link from @{old_username} to @{new_username} by {callback_query.from_user.mention}"
        )

    except Exception as e:
        await callback_query.message.reply_text(f"Error: {e}")
        await log_to_channel(f"Error changing link: {e}")


@app.on_message(filters.command("changeall"))
async def change_all_channel_links(client: Client, message: Message):
    global changeall_running
    if message.from_user.id not in cfg.SUDO:
        await message.reply_text("Only sudo users can run this command.")
        return

    if changeall_running:
        await message.reply_text("Changeall is already running.")
        return

    changeall_running = True
    await message.reply_text("Started changing all channel usernames.")
    await log_to_channel("Started /changeall process.")

    while changeall_running:
        try:
            channels = [
                dialog.chat async for dialog in user_app.get_dialogs()
                if dialog.chat.username and dialog.chat.type == "channel"
            ]

            for channel in channels:
                if not changeall_running:
                    break

                old_username = channel.username
                new_username = f"{old_username[:-2]}{generate_random_string()}"

                try:
                    await user_app.set_chat_username(channel.id, new_username)
                    await log_to_channel(f"Changed @{old_username} to @{new_username}")
                except Exception as e:
                    await log_to_channel(f"Failed to change @{old_username}: {e}")
                    continue

                try:
                    temp_channel = await user_app.create_channel(title=old_username, description="Temp Channel")
                    await user_app.set_chat_username(temp_channel.id, old_username)
                    add_created_channel(temp_channel.id)
                    await log_to_channel(f"Temp channel @{old_username} created.")
                    asyncio.create_task(delete_temp_channel(temp_channel.id, old_username))
                except Exception as e:
                    await log_to_channel(f"Temp channel creation failed: {e}")

                await asyncio.sleep(60 * 60)  # 1 hour between changes

        except Exception as e:
            await log_to_channel(f"Loop error: {e}")
            await asyncio.sleep(60)

    await log_to_channel("Changeall process stopped.")


async def delete_temp_channel(channel_id: int, username: str):
    await asyncio.sleep(3 * 60 * 60)
    try:
        await user_app.delete_channel(channel_id)
        await log_to_channel(f"Deleted temp channel @{username}")
    except Exception as e:
        await log_to_channel(f"Failed to delete temp channel @{username}: {e}")


@app.on_message(filters.command("stopchangeall"))
async def stop_change_all(client: Client, message: Message):
    global changeall_running
    changeall_running = False
    await message.reply_text("Stopped the /changeall process.")
    await log_to_channel("Stopped /changeall process.")


print("Bot and user session starting...")
user_app.start()
app.run()
