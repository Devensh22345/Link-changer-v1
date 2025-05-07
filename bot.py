from pyrogram import Client, filters
from pyrogram.types import ChatInviteLink, Message
from configs import cfg
from database import (
    add_active_channel, get_active_channels,
    save_logged_message, get_logged_messages,
    update_logged_message, remove_channel_from_db,
    save_invite_info, get_invite_info,
    save_channel_link_mapping, get_channel_link_mapping
)
from datetime import datetime, timedelta, timezone
import traceback
from pyrogram.errors import FloodWait, ChatAdminRequired, ChannelPrivate
import asyncio
import time
from pyrogram.types import Message
from pyrogram import filters
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


# ✅ Send or update invite message to the linked LINK_CHANNEL (per rotation channel)
async def send_or_update_invite_link(channel_id: int, invite_link: str):
    try:
        LINK_CHANNEL = get_channel_link_mapping(channel_id)
        if not LINK_CHANNEL:
            await log_to_channel(f"⚠️ No link channel found for {channel_id}")
            return

        if channel_id in logged_messages:
            message_id = logged_messages[channel_id]
            try:
                await app.edit_message_text(
                    chat_id=LINK_CHANNEL,
                    message_id=message_id,
                    text=f"<b>♨️ 𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 𝐀𝐍𝐈𝐌𝐄 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</b> ♨️\n<blockquote><b>\n{invite_link}\n" * 6 + "</b></blockquote>"
                )
            except Exception as e:
                print(f"Edit failed: {e}")
                del logged_messages[channel_id]
                update_logged_message(channel_id, None)
                msg = await app.send_message(
                    LINK_CHANNEL,
                    f"<b>♨️ 𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 𝐀𝐍𝐈𝐌𝐄 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</b> ♨️\n<blockquote><b>\n{invite_link}\n" * 6 + "</b></blockquote>"
                )
                logged_messages[channel_id] = msg.id
                update_logged_message(channel_id, msg.id)
        else:
            msg = await app.send_message(
                LINK_CHANNEL,
                f"<b>♨️  𝐉𝐨𝐢𝐧 𝐨𝐮𝐫 𝐀𝐍𝐈𝐌𝐄 𝐂𝐡𝐚𝐧𝐧𝐞𝐥</b> ♨️\n<blockquote><b>\n{invite_link}\n" * 6 + "</b></blockquote>"
            )
            logged_messages[channel_id] = msg.id
            save_logged_message(channel_id, msg.id)
    except Exception as e:
        await log_to_channel(f"Log/update error: {e}")


# ✅ Invite rotation logic
async def rotate_invite_link(channel_id: int):
    while True:
        try:
            invite_info = get_invite_info(channel_id)
            now = datetime.now(timezone.utc)

            if invite_info:
                expires_at = invite_info["expires_at"]
                if isinstance(expires_at, str):
                    expires_at = datetime.fromisoformat(expires_at)
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)

                if expires_at > now:
                    await log_to_channel(f"⏳ Invite for {channel_id} valid until {expires_at.isoformat()}")
                    await asyncio.sleep((expires_at - now).total_seconds())
                    continue

            expire_time = now + timedelta(minutes=10)
            invite: ChatInviteLink = await app.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=expire_time,
                member_limit=0,
                name="15min-invite",
                creates_join_request=True
            )

            await send_or_update_invite_link(channel_id, invite.invite_link)

            log_message_id = logged_messages.get(channel_id)
            if log_message_id:
                save_invite_info(channel_id, invite.invite_link, expire_time, log_message_id)
            else:
                await log_to_channel(f"⚠️ No log_message_id found for {channel_id}")

            await asyncio.sleep(570)

        except FloodWait as e:
            await log_to_channel(f"⏳ FloodWait for {e.value} seconds in {channel_id}")
            await asyncio.sleep(e.value)

        except Exception as e:
            await log_to_channel(f"❌ Error rotating link for {channel_id}: {e}")
            active_channels.discard(channel_id)
            try:
                remove_channel_from_db(channel_id)
            except Exception as cleanup_error:
                await log_to_channel(f"⚠️ Failed to remove {channel_id}: {cleanup_error}")
            break


# ✅ Command to set rotation + link channel and start rotation

@app.on_message(filters.command("addrotation"))
async def add_rotation_channel(client, message: Message):
    # Ensure command is sent in a channel (not private chat)
    if message.chat.type != "channel":
        return await message.reply("❌ Please use this command in a Telegram channel.")

    try:
        # Get channel IDs directly from the message
        rotation_channel = int(message.text.split()[1])

        link_channel_id = message.chat.id  # Message must be sent *from* the link channel
        save_channel_link_mapping(rotation_channel, link_channel_id)
        add_active_channel(rotation_channel)
        active_channels.add(rotation_channel)

        await message.reply(
            f"✅ Added rotation channel `{rotation_channel}`.\n🔁 Starting invite rotation with this channel (`{link_channel_id}`) as the link display."
        )
        asyncio.create_task(rotate_invite_link(rotation_channel))

    except IndexError:
        await message.reply("Usage: /addrotation <rotation_channel_id>")
    except Exception as e:
        await message.reply(f"❌ Failed: {e}")


# ✅ Logging utility
async def log_to_channel(text: str):
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Log error: {e}")


# ✅ Detect if bot added manually (won't auto start rotation)
@app.on_chat_member_updated()
async def bot_added_to_channel(client, chat_member_updated):
    if chat_member_updated.new_chat_member and chat_member_updated.new_chat_member.user.id == (await app.get_me()).id:
        channel_id = chat_member_updated.chat.id
        if channel_id not in active_channels:
            active_channels.add(channel_id)
            add_active_channel(channel_id)
            await log_to_channel(f"✅ Bot added as admin in channel: `{chat_member_updated.chat.title}` (`{channel_id}`)")
            # ❌ Do NOT auto-start rotation


# ✅ Restart rotation for existing active channels on startup
async def main():
    async with app:
        for channel_id in active_channels:
            asyncio.create_task(rotate_invite_link(channel_id))
        print("Bot Running...")
        await asyncio.Event().wait()

app.run(main())
