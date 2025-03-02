from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from configs import cfg
from database import (
    add_user, add_group, all_users, all_groups, 
    add_auth, remove_auth, get_auth, 
    add_sudo, remove_sudo, get_sudo
)

app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

LOG_CHANNEL = cfg.LOG_CHANNEL

# Start Command
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    add_user(message.from_user.id)
    buttons = [[InlineKeyboardButton("Help", callback_data="help")]]
    await message.reply_text(
        "Hello!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await app.send_message(LOG_CHANNEL, f"User started bot: {message.from_user.mention} (ID: {message.from_user.id})")

# Add Group to Database
@app.on_message(filters.group)
async def group_handler(client, message):
    add_group(message.chat.id)
    await app.send_message(LOG_CHANNEL, f"Bot added to group: {message.chat.title} (ID: {message.chat.id})")

# Broadcast to Groups (/gcast)
@app.on_message(filters.command("gcast") & filters.user(cfg.OWNER_ID))
async def gcast(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast in groups.")
        return

    msg = message.reply_to_message
    sent = 0
    for group_id in await all_groups():
        try:
            await msg.copy(group_id['chat_id'])
            sent += 1
        except Exception as e:
            print(f"Failed to send in group {group_id['chat_id']}: {e}")
    await message.reply_text(f"Message sent to {sent} groups.")
    await app.send_message(LOG_CHANNEL, f"Broadcast to {sent} groups by {message.from_user.mention}")

# Broadcast to Users (/ucast)
@app.on_message(filters.command("ucast") & filters.user(cfg.OWNER_ID))
async def ucast(client, message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to broadcast to users.")
        return

    msg = message.reply_to_message
    sent = 0
    for user_id in await all_users():
        try:
            await msg.copy(user_id['user_id'])
            sent += 1
        except Exception as e:
            print(f"Failed to send to user {user_id['user_id']}: {e}")
    await message.reply_text(f"Message sent to {sent} users.")
    await app.send_message(LOG_CHANNEL, f"Broadcast to {sent} users by {message.from_user.mention}")

# Command to see total groups and users (/users)
@app.on_message(filters.command("users") & filters.user(cfg.OWNER_ID))
async def users_command(client, message):
    total_users = all_users()
    total_groups = all_groups()
    await message.reply_text(f"Total Users: {total_users}\nTotal Groups: {total_groups}")
    await app.send_message(LOG_CHANNEL, f"Checked total users and groups: {message.from_user.mention}")

# Add Sudo User (/addsudo)
@app.on_message(filters.command("addsudo") & filters.user(cfg.OWNER_ID))
async def add_sudo_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /addsudo <user_id>")
        return

    user_id = message.command[1]
    add_sudo(user_id)
    await message.reply_text(f"Added {user_id} as sudo user.")
    await app.send_message(LOG_CHANNEL, f"Added sudo user: {user_id} by {message.from_user.mention}")

# Remove Sudo User (/rsudo)
@app.on_message(filters.command("rsudo") & filters.user(cfg.OWNER_ID))
async def remove_sudo_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /rsudo <user_id>")
        return

    user_id = message.command[1]
    remove_sudo(user_id)
    await message.reply_text(f"Removed {user_id} from sudo users.")
    await app.send_message(LOG_CHANNEL, f"Removed sudo user: {user_id} by {message.from_user.mention}")

# Show Sudo Users (/sudo)
@app.on_message(filters.command("sudo") & filters.user(cfg.OWNER_ID))
async def sudo_command(client, message):
    sudo_users = get_sudo()
    await message.reply_text(f"Sudo Users: {', '.join(sudo_users) if sudo_users else 'No sudo users'}")

# Authorize User in Group (/auth)
@app.on_message(filters.command("auth") & filters.group)
async def auth_command(client, message):
    if message.from_user.id not in get_sudo() and message.from_user.id != cfg.OWNER_ID:
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: /auth <user_id>")
        return

    user_id = message.command[1]
    add_auth(message.chat.id, user_id)
    await message.reply_text(f"Authorized {user_id} in this group.")
    await app.send_message(LOG_CHANNEL, f"Authorized {user_id} in group {message.chat.title}")

# Unauthorize User in Group (/unauth)
@app.on_message(filters.command("unauth") & filters.group)
async def unauth_command(client, message):
    if message.from_user.id not in get_sudo() and message.from_user.id != cfg.OWNER_ID:
        return

    if len(message.command) < 2:
        await message.reply_text("Usage: /unauth <user_id>")
        return

    user_id = message.command[1]
    remove_auth(message.chat.id, user_id)
    await message.reply_text(f"Unauthorized {user_id} in this group.")
    await app.send_message(LOG_CHANNEL, f"Unauthorized {user_id} in group {message.chat.title}")

# Show Auth Users in Group (/auths)
@app.on_message(filters.command("auths") & filters.group)
async def auths_command(client, message):
    auth_users = get_auth(message.chat.id)
    await message.reply_text(f"Authorized Users: {', '.join(auth_users) if auth_users else 'No authorized users'}")

# Handle Edited Messages
@app.on_message(filters.group & filters.update.edited_message)
async def handle_edited_message(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if user_id == cfg.OWNER_ID or user_id in get_sudo() or str(user_id) in get_auth(chat_id):
        return

    original_text = message.text or message.caption or ""
    await message.delete()
    await message.reply_text(f"[{message.from_user.mention}] Your message '{original_text}' was deleted.")
    await app.send_message(LOG_CHANNEL, f"Deleted edited message in {message.chat.title} by {message.from_user.mention}")

# Error Handling
@app.on_errors()
async def error_handler(client, error):
    await app.send_message(LOG_CHANNEL, f"Error occurred: {str(error)}")

print("Bot is running...")
app.run()
