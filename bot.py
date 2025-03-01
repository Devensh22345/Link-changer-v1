from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired, PeerIdInvalid, FloodWait
from configs import cfg
from database import is_sudo_user, add_sudo_user, get_all_sudo_users, add_created_channel
import asyncio

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Client (for creating channels)
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.SESSION_STRING
)

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Use /create to create a private channel.")

@app.on_message(filters.command("addsudo"))
async def add_sudo(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a user to make them sudo!")
        return
    
    user_id = message.reply_to_message.from_user.id
    add_sudo_user(user_id)
    await message.reply_text(f"✅ User {user_id} added as sudo.")

@app.on_message(filters.command("create"))
async def create_channel(client: Client, message: Message):
    sudo_users = get_all_sudo_users()
    if message.from_user.id not in sudo_users:
        await message.reply_text("❌ Only sudo users can create channels.")
        return
    
    try:
        channel = await user_app.create_channel(
            title="hi",
            description="A private channel created by the bot."
        )
        add_created_channel(channel.id)
        await message.reply_text(f"✅ Private channel created: {channel.title}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
