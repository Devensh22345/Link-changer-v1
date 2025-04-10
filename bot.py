from pyrogram import Client, filters
from pyrogram.types import ChatInviteLink
from configs import cfg
from database import (
    add_active_channel, get_active_channels,
    save_logged_message, get_logged_messages,
    update_logged_message
)
from datetime import datetime, timedelta, timezone  # ✅ Add timezone
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
                    text=f"🔗 Updated Invite Link for Channel `{channel_id}`:\n{invite_link}"
                )
            except Exception as e:
                print(f"Edit failed: {e}")
                msg = await app.send_message(
                    LOG_CHANNEL,
                    f"🔗 New Invite Link for Channel `{channel_id}`:\n{invite_link}"
                )
                logged_messages[channel_id] = msg.id  # ✅ updated
                update_logged_message(channel_id, msg.id)
        else:
            msg = await app.send_message(
                LOG_CHANNEL,
                f"🔗 Invite Link for Channel `{channel_id}`:\n{invite_link}"
            )
            logged_messages[channel_id] = msg.id  # ✅ updated
            save_logged_message(channel_id, msg.id)
    except Exception as e:
        print(f"Log/update error: {e}")

# Background task to rotate invite link every 15 minutes
async def rotate_invite_link(channel_id: int):
    while True:
        try:
            # ✅ timezone-aware datetime
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=15)
            invite: ChatInviteLink = await app.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=expire_time,
                member_limit=0,
                name="15min-invite"
            )
            await send_or_update_invite_link(channel_id, invite.invite_link)
            await asyncio.sleep(900)
        except Exception as e:
            await log_to_channel(f"❌ Error rotating link for {channel_id}: {e}")
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

# Start the bot
print("Bot Running...")
app.run()
