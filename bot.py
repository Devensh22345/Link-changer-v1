from pyrogram import Client, filters, errors
from pyrogram.types import Message
from pymongo import MongoClient
from configs import cfg  

# Connect to MongoDB
mongo_client = MongoClient(cfg.MONGO_URI)
db = mongo_client["EditBotDB"]
users = db["users"]

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Client
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.SESSION_STRING
)

# Start message
@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Bot is running.")

# Add a user as a sudo
@app.on_message(filters.command("addsudo") & filters.user(cfg.SUDO))
async def add_sudo(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("❌ Reply to a user to make them sudo!")
        return
    
    user_id = message.reply_to_message.from_user.id
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id})
        await message.reply_text("✅ User added as sudo.")
    else:
        await message.reply_text("✅ User is already a sudo user.")

# Create a private channel named "hi" (Only for sudo users)
@app.on_message(filters.command("create"))
async def create_private_channel(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if the user is a sudo user
    is_sudo = user_id == cfg.SUDO or users.find_one({"user_id": user_id})

    if not is_sudo:
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    try:
        chat = await user_app.create_channel(
            title="hi",
            description="This is a private channel.",
        )
        await message.reply_text(f"✅ Private channel created: {chat.title}\nChannel ID: `{chat.id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
