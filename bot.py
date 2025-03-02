from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database import (
    add_user, remove_user, add_group, all_users, all_groups, 
    add_sudo_user, remove_sudo_user, is_sudo_user, get_sudo_users, 
    authorize_user, unauthorize_user, is_authorized_user
)
from configs import cfg
import asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Start Command
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    user = m.from_user
    await app.send_message(LOG_CHANNEL, f"📢 **User Started Bot:** {user.first_name} (`{user.id}`)")
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Click Here", url="https://t.me/yourbot?start=start")]]
    )

    await m.reply_text(
        "Hello! I am your bot.",
        reply_markup=keyboard
    )
    add_user(user.id)

# Add Sudo User
@app.on_message(filters.command("addsudo") & filters.user(cfg.OWNER_ID))
async def add_sudo(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a user to add as sudo.")
        return
    
    sudo_id = m.reply_to_message.from_user.id
    add_sudo_user(sudo_id)
    await m.reply_text(f"User `{sudo_id}` added as sudo.")
    await app.send_message(LOG_CHANNEL, f"✅ **Sudo User Added:** `{sudo_id}`")

# Remove Sudo User
@app.on_message(filters.command("rsudo") & filters.user(cfg.OWNER_ID))
async def remove_sudo(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a user to remove from sudo.")
        return
    
    sudo_id = m.reply_to_message.from_user.id
    remove_sudo_user(sudo_id)
    await m.reply_text(f"User `{sudo_id}` removed from sudo.")
    await app.send_message(LOG_CHANNEL, f"❌ **Sudo User Removed:** `{sudo_id}`")

# List Sudo Users
@app.on_message(filters.command("sudo") & filters.user(cfg.OWNER_ID))
async def list_sudo(_, m: Message):
    sudo_list = get_sudo_users()
    if sudo_list:
        msg = "👑 **Sudo Users:**\n" + "\n".join([f"`{user}`" for user in sudo_list])
    else:
        msg = "No sudo users found."
    
    await m.reply_text(msg)
    await app.send_message(LOG_CHANNEL, f"📋 **Sudo Users Listed:**\n{msg}")

# Authorize User
@app.on_message(filters.command("auth") & (filters.user(cfg.OWNER_ID) | filters.user(get_sudo_users())))
async def authorize(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a user to authorize them.")
        return
    
    user_id = m.reply_to_message.from_user.id
    authorize_user(user_id)
    await m.reply_text(f"User `{user_id}` authorized.")
    await app.send_message(LOG_CHANNEL, f"🔑 **User Authorized:** `{user_id}`")

# Unauthorize User
@app.on_message(filters.command("unauth") & (filters.user(cfg.OWNER_ID) | filters.user(get_sudo_users())))
async def unauthorize(_, m: Message):
    if not m.reply_to_message:
        await m.reply_text("Reply to a user to unauthorize them.")
        return
    
    user_id = m.reply_to_message.from_user.id
    unauthorize_user(user_id)
    await m.reply_text(f"User `{user_id}` unauthorized.")
    await app.send_message(LOG_CHANNEL, f"🚫 **User Unauthorized:** `{user_id}`")

# List Authorized Users
@app.on_message(filters.command("auths") & (filters.user(cfg.OWNER_ID) | filters.user(get_sudo_users())))
async def list_auths(_, m: Message):
    group_members = await app.get_chat_members(m.chat.id)
    auth_list = [member.user.id for member in group_members if is_authorized_user(member.user.id)]

    if auth_list:
        msg = "✅ **Authorized Users:**\n" + "\n".join([f"`{user}`" for user in auth_list])
    else:
        msg = "No authorized users found in this group."
    
    await m.reply_text(msg)
    await app.send_message(LOG_CHANNEL, f"📋 **Authorized Users Listed:**\n{msg}")

# Broadcast to All Users
@app.on_message(filters.command("ucast") & filters.user(cfg.OWNER_ID))
async def ucast(_, m: Message):
    allusers = [user["user_id"] for user in users.find()]
    success, failed = 0, 0
    
    for user_id in allusers:
        try:
            await m.reply_to_message.copy(int(user_id))
            success += 1
        except Exception:
            failed += 1
    
    await m.reply_text(f"✅ Success: {success}\n❌ Failed: {failed}")
    await app.send_message(LOG_CHANNEL, f"📢 **Ucast:** Success `{success}`, Failed `{failed}`")

# Broadcast to All Groups
@app.on_message(filters.command("gcast") & filters.user(cfg.OWNER_ID))
async def gcast(_, m: Message):
    allgroups = [group["chat_id"] for group in groups.find()]
    success, failed = 0, 0
    
    for chat_id in allgroups:
        try:
            await m.reply_to_message.copy(int(chat_id))
            success += 1
        except Exception:
            failed += 1
    
    await m.reply_text(f"✅ Success: {success}\n❌ Failed: {failed}")
    await app.send_message(LOG_CHANNEL, f"📢 **Gcast:** Success `{success}`, Failed `{failed}`")

# User & Group Stats
@app.on_message(filters.command("users"))
async def users_stats(_, m: Message):
    user_count = all_users()
    group_count = all_groups()
    total = user_count + group_count

    msg = f"""
    📊 **Bot Stats:**
    👤 **Users:** `{user_count}`
    👥 **Groups:** `{group_count}`
    🌐 **Total:** `{total}`
    """
    await m.reply_text(msg)
    await app.send_message(LOG_CHANNEL, f"📈 **Stats Command Used:**\n{msg}")

# Delete Edited Messages
@app.on_edited_message(filters.group)
async def handle_edited_message(client, message):
    user_id = m.from_user.id
    if is_authorized_user(user_id) or is_sudo_user(user_id) or user_id == cfg.OWNER_ID:
        return
    
    old_message = m.text or "Media Message"
    await m.delete()
    msg = f"[{m.from_user.mention}] your message '{old_message}' was deleted due to editing."
    await m.chat.send_message(msg)
    await app.send_message(LOG_CHANNEL, f"🗑 **Message Deleted:**\nUser: `{user_id}`\nMessage: `{old_message}`")

# Bot Running
print("🤖 Bot is running...")
app.run()
