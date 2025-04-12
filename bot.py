from pyrogram import Client, filters
from pyrogram.types import ChatInviteLink
from configs import cfg
from database import (
    add_active_channel, get_active_channels,
    save_logged_message, get_logged_messages,
    update_logged_message, remove_channel_from_db, save_invite_info, get_invite_info
)
from datetime import datetime, timedelta, timezone  # ✅ Add timezone
import traceback
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.errors import ChannelPrivate
import asyncio
import time
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

LOG_CHANNEL = cfg.LOG_CHANNEL
active_channels = set(get_active_channels())
logged_messages = get_logged_messages()  # {channel_id: message_id}


# Function to log or edit invite link in the log channel
async def send_or_update_invite_link(channel_id: int, invite_link: str):
    try:
        if channel_id in logged_messages:
            message_id = logged_messages[channel_id]
            try:
                await app.edit_message_text(
                    chat_id=LOG_CHANNEL,
                    message_id=message_id,
                    text=f"<b>𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐄𝐩𝐢𝐬𝐨𝐝𝐞 𝐥𝐢𝐧𝐤 👉👉\n{invite_link}\n{invite_link}</b>"
                )
            except Exception as e:
                print(f"Edit failed: {e}")
                # Delete old ID and fall back to sending new message
                del logged_messages[channel_id]
                update_logged_message(channel_id, None)
                msg = await app.send_message(
                    LOG_CHANNEL,
                    f"<b>𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐄𝐩𝐢𝐬𝐨𝐝𝐞 𝐥𝐢𝐧𝐤 👉👉\n{invite_link}\n{invite_link}</b>"
                )
                logged_messages[channel_id] = msg.id
                update_logged_message(channel_id, msg.id)
        else:
            msg = await app.send_message(
                LOG_CHANNEL,
                f"<b>𝐇𝐞𝐫𝐞 𝐢𝐬 𝐲𝐨𝐮𝐫 𝐄𝐩𝐢𝐬𝐨𝐝𝐞 𝐥𝐢𝐧𝐤 👉👉\n{invite_link}\n{invite_link}</b>"
            )
            logged_messages[channel_id] = msg.id
            save_logged_message(channel_id, msg.id)
    except Exception as e:
        print(f"Log/update error: {e}")


# Background task to rotate invite link every 15 minutes

async def rotate_invite_link(channel_id: int):
    while True:
        try:
            invite_info = get_invite_info(channel_id)
            now = datetime.now(timezone.utc)

            if invite_info:
               expires_at = invite_info["expires_at"]
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                if expires_at > now:

                    # Still valid, reuse it
                    await send_or_update_invite_link(channel_id, invite_info["invite_link"])
                    await asyncio.sleep((expires_at - now).total_seconds())
                    continue  # Skip creating new link

            # Otherwise, create a new one
            expire_time = now + timedelta(minutes=2)
            invite: ChatInviteLink = await app.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=expire_time,
                member_limit=0,
                name="15min-invite",
                creates_join_request=True
            )

            # Log or update the invite
            await send_or_update_invite_link(channel_id, invite.invite_link)

            # Save to DB
            save_invite_info(channel_id, invite.invite_link, expire_time, logged_messages[channel_id])

            # Sleep 2 minutes
            await asyncio.sleep(120)

        except FloodWait as e:
            await log_to_channel(f"⏳ FloodWait for {e.value} seconds in {channel_id}")
            await asyncio.sleep(e.value)

        except Exception as e:
            await log_to_channel(f"❌ Error rotating link for {channel_id}: {e}")
            active_channels.discard(channel_id)
            try:
                remove_channel_from_db(channel_id)
            except Exception as cleanup_error:
                await log_to_channel(f"⚠️ Failed to remove {channel_id} from DB: {cleanup_error}")
            break

            break




# Function to log messages
async def log_to_channel(text: str):
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Log error: {e}")

# Detect when bot added to channel
@app.on_chat_member_updated()
async def bot_added_to_channel(client, chat_member_updated):
    if chat_member_updated.new_chat_member and chat_member_updated.new_chat_member.user.id == (await app.get_me()).id:
        channel_id = chat_member_updated.chat.id
        if channel_id not in active_channels:
            active_channels.add(channel_id)
            add_active_channel(channel_id)
            await log_to_channel(f"✅ Bot added as admin in channel: `{chat_member_updated.chat.title}` (`{channel_id}`)")
            asyncio.create_task(rotate_invite_link(channel_id))

# ✅ Startup tasks: restart rotation for existing active channels
# ✅ Startup tasks: restart rotation for existing active channels
async def main():
    async with app:
        for channel_id in active_channels:
            asyncio.create_task(rotate_invite_link(channel_id))
        print("Bot Running...")
        await asyncio.Event().wait()  # ✅ Keeps the bot alive

# Start the bot
app.run(main())
