from pyrogram import Client, filters, errors
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo
from pymongo import MongoClient
import asyncio
from configs import cfg  

# Connect to MongoDB
mongo_client = MongoClient(cfg.MONGO_URI)
db = mongo_client["EditBotDB"]
edited_messages = db["edited_messages"]
users = db["users"]

# Initialize Bot Client
app = Client(
    "bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Initialize User Client (for editing messages)
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.SESSION_STRING
)

# Define new content
NEW_MEDIA = "https://example.com/new_media.jpg"
NEW_CAPTION = "**🔄 This media has been updated! 🔄**"
NEW_TEXT = "**🔄 This message has been updated! 🔄**"

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Use /editall to edit all previous messages.")

@app.on_message(filters.command("editall"))
async def edit_all_messages(client: Client, message: Message):
    chat_id = message.chat.id

    # Check if the message is sent from a channel admin
    if message.sender_chat and str(chat_id).startswith("-100"):
        sender_chat_id = message.sender_chat.id  # The channel ID
    else:
        await message.reply_text("❌ This command can only be used in a channel by an admin.")
        return

    msg_count = 0
    await message.reply_text("🔄 Editing all previous messages...")

    try:
    async for msg in user_app.get_chat_history(chat_id, limit=1000):
        try:
            if msg.photo:
                await user_app.edit_message_media(chat_id, msg.id, media=InputMediaPhoto(NEW_MEDIA, caption=NEW_CAPTION))
            elif msg.video:
                await user_app.edit_message_media(chat_id, msg.id, media=InputMediaVideo(NEW_MEDIA, caption=NEW_CAPTION))
            elif msg.document:
                await user_app.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
            elif msg.caption:
                await user_app.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
            else:
                await user_app.edit_message_text(chat_id, msg.id, NEW_TEXT)

            edited_messages.insert_one({
                "chat_id": chat_id,
                "message_id": msg.id,
                "new_content": NEW_TEXT if not msg.caption else NEW_CAPTION,
                "edited_by": message.from_user.id
            })

            msg_count += 1
            await asyncio.sleep(1)  

        except errors.MessageNotModified:
            continue
        except errors.MessageEditTimeExpired:
            continue
        except Exception as e:
            print(f"Error editing message {msg.id}: {e}")

    await message.reply_text(f"✅ Successfully edited {msg_count} messages.")
except Exception as e:  # ✅ Add this block
    await message.reply_text(f"❌ Error: {e}")
    print(e)




        


@app.on_message(filters.command("edithistory") & filters.user(cfg.SUDO))
async def edit_history(client: Client, message: Message):
    chat_id = message.chat.id
    history = edited_messages.find({"chat_id": chat_id})
    response = "**📝 Edit History:**\n"
    for doc in history:
        response += f"📌 Message ID: {doc['message_id']} | Edited by: {doc['edited_by']}\n"
    if response == "**📝 Edit History:**\n":
        response += "No edits found."
    await message.reply_text(response)

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

# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
