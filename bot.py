from pyrogram import Client
from pyrogram.types import ChatInviteLink
from configs import cfg
from database import (
    add_active_channel, get_active_channels,
    save_logged_message, get_logged_messages,
    update_logged_message,
    get_invite_log, set_invite_log,
    remove_active_channel, remove_logged_message
)
from datetime import datetime, timedelta, timezone
import asyncio
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


# 🔁 Log or update invite link message in log channel
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
                logged_messages[channel_id] = msg.id
                update_logged_message(channel_id, msg.id)
        else:
            msg = await app.send_message(
                LOG_CHANNEL,
                f"🔗 Invite Link for Channel `{channel_id}`:\n{invite_link}"
            )
            logged_messages[channel_id] = msg.id
            save_logged_message(channel_id, msg.id)
    except Exception as e:
        print(f"Log/update error: {e}")


# 🔄 Create and rotate invite link every 15 mins
async def rotate_invite_link(channel_id: int):
    while channel_id in active_channels:
        try:
            expire_time = datetime.now(timezone.utc) + timedelta(minutes=2)
            invite: ChatInviteLink = await app.create_chat_invite_link(
                chat_id=channel_id,
                expire_date=expire_time,
                member_limit=0,
                name="15min-invite"
            )
            await send_or_update_invite_link(channel_id, invite.invite_link)
            set_invite_log(channel_id, invite.invite_link, expire_time)
            await asyncio.sleep(120)
        except Exception as e:
            await log_to_channel(f"❌ Error rotating link for {channel_id}: {e}")
            break


# 📩 Send log message to log channel
async def log_to_channel(text: str):
    try:
        await app.send_message(LOG_CHANNEL, text)
    except Exception as e:
        print(f"Log error: {e}")


# 🧹 Clean up when bot is removed from a channel
def cleanup_channel(channel_id: int):
    active_channels.discard(channel_id)
    remove_active_channel(channel_id)
    remove_logged_message(channel_id)


# 👮 Handle bot being added or removed as admin
@app.on_chat_member_updated()
async def handle_chat_member_update(client, update):
    me = await app.get_me()
    channel_id = update.chat.id

    # Bot added as admin
    if update.new_chat_member and update.new_chat_member.user.id == me.id:
        if update.new_chat_member.status in ("administrator", "creator"):
            if channel_id not in active_channels:
                active_channels.add(channel_id)
                add_active_channel(channel_id)
                await log_to_channel(f"✅ Bot added as admin in channel: `{update.chat.title}` (`{channel_id}`)")
                asyncio.create_task(rotate_invite_link(channel_id))

    # Bot removed or lost admin rights
    if update.old_chat_member and update.old_chat_member.user.id == me.id:
        if update.old_chat_member.status in ("administrator", "creator") and update.new_chat_member.status not in ("administrator", "creator"):
            if channel_id in active_channels:
                cleanup_channel(channel_id)
                await log_to_channel(f"❌ Bot removed or lost admin rights in channel: `{update.chat.title}` (`{channel_id}`)")


# 🔁 Start invite rotation on startup
async def auto_start_rotation():
    print("🔁 Checking invite links...")
    for channel_id in list(active_channels):
        data = get_invite_log(channel_id)
        if data and 'invite_link' in data and 'expires_at' in data:
            expires_at = data['expires_at']
            if isinstance(expires_at, datetime):
                if expires_at.tzinfo is None:
                    expires_at = expires_at.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                if expires_at > now:
                    remaining = (expires_at - now).total_seconds()
                    print(f"⏳ Reusing link for {channel_id}, expires in {int(remaining)}s")
                    asyncio.create_task(sleep_then_rotate(channel_id, remaining))
                    continue
        # Expired or no data
        print(f"🔄 Generating new link for {channel_id}")
        asyncio.create_task(rotate_invite_link(channel_id))


# ⏳ Wait till current link expires then rotate
async def sleep_then_rotate(channel_id: int, sleep_time: float):
    await asyncio.sleep(sleep_time)
    await rotate_invite_link(channel_id)


# ✅ Start everything
async def main():
    await app.start()
    await auto_start_rotation()
    print("✅ Bot Running...")
    from pyrogram import idle
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
