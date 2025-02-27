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
NEW_MEDIA = "https://envs.sh/eZL.jpg"
NEW_CAPTION = "**JOIN FOR ANIME IN HINDI - [@DK_ANIMES]**"
NEW_TEXT = "**JOIN FOR ANIME IN HINDI - [@DK_ANIMES]**"

@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello! Use /editall to edit all previous messages.")

@app.on_message(filters.command("editall"))
async def edit_all_messages(client: Client, message: Message):
    chat_id = message.chat.id

    if not message.sender_chat or not str(chat_id).startswith("-100"):
        await message.reply_text("❌ This command can only be used in a channel by an admin.")
        return

    msg_count = 0
    await message.reply_text("🔄 Editing all previous messages...")

    try:
        async for msg in user_app.get_chat_history(chat_id, limit=1000):
            try:
                if msg.photo or msg.video:  # Replace both video & photo with a new photo
                    await user_app.edit_message_media(chat_id, msg.id, media=InputMediaPhoto(NEW_MEDIA, caption=NEW_CAPTION))
                elif msg.document:
                    await user_app.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
                elif msg.caption:
                    await user_app.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
                else:
                    await user_app.edit_message_text(chat_id, msg.id, NEW_TEXT)

                edited_messages.insert_one({
                    "chat_id": chat_id,
                    "message_id": msg.id,
                    "new_content": NEW_CAPTION,
                    "edited_by": message.from_user.id
                })

                msg_count += 1
                await asyncio.sleep(1)  

            except errors.MessageNotModified:
                continue
            except errors.MessageEditTimeExpired:
                continue
            except errors.ChatAdminRequired:
                await message.reply_text("❌ The bot needs admin permissions to edit messages in this channel.")
                return
            except Exception as e:
                print(f"Error editing message {msg.id}: {e}")

        await message.reply_text(f"✅ Successfully edited {msg_count} messages.")
    except Exception as e:
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
        
@app.on_message(filters.command("checkchat"))
async def check_chat(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        chat = await user_app.get_chat(chat_id)
        await message.reply_text(f"✅ User session recognizes the channel: {chat.title}")
    except errors.PeerIdInvalid:
        await message.reply_text("❌ Peer ID Invalid: The user session doesn't recognize this channel.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("checklastmsg"))
async def check_last_msg(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        async for msg in user_app.get_chat_history(chat_id, limit=1):
            await message.reply_text(f"✅ Last message found: {msg.text}")
            return
        await message.reply_text("❌ No messages found.")
    except errors.PeerIdInvalid:
        await message.reply_text("❌ Peer ID Invalid: The user session doesn't recognize this channel.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        


        

@app.on_message(filters.command("fetchmessages"))
async def fetch_messages(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        async for msg in user_app.get_chat_history(chat_id, limit=5):
            await message.reply_text(f"📩 Found Message ID: {msg.id}")
        await message.reply_text("✅ Successfully fetched messages!")
    except errors.PeerIdInvalid:
        await message.reply_text("❌ Peer ID Invalid")
async def join_channel(client, message: Message):
    chat_id = message.chat.id
    try:
        # Have the assistant join the channel
        await assistant.join_chat(chat_id)
        await asyncio.sleep(2)  # Give time for the join to process

        # Confirm the join by fetching the chat details with the assistant
        chat = await assistant.get_chat(chat_id)
        await message.reply_text(f"✅ Assistant joined the channel: {chat.title}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
 The user session doesn't recognize this channel.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("checksession"))
async def check_session(client: Client, message: Message):
    try:
        chat = await user_app.get_chat(message.chat.id)
        await message.reply_text(f"✅ User session is in the chat: {chat.title}")
    except errors.PeerIdInvalid:
        await message.reply_text("❌ Peer ID Invalid: The user session does not recognize this chat.")
    except errors.ChatAdminRequired:
        await message.reply_text("❌ Bot needs to be an admin to perform this action.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        
@app.on_message(filters.command("join"))
async def join_channel(client, message: Message):
    chat_id = message.chat.id
    try:
        # Have the assistant join the channel
        await assistant.join_chat(chat_id)
        await asyncio.sleep(2)  # Give time for the join to process

        # Confirm the join by fetching the chat details with the assistant
        chat = await assistant.get_chat(chat_id)
        await message.reply_text(f"✅ Assistant joined the channel: {chat.title}")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        

@app.on_message(filters.command("rejoinchannel"))
async def rejoin_channel(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await user_app.leave_chat(chat_id)  # Leave the channel
        await asyncio.sleep(2)  # Wait before rejoining
        await user_app.join_chat(chat_id)  # Rejoin the channel
        await message.reply_text("✅ Left and rejoined the channel. Try again!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("testedit"))
async def test_edit(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        async for msg in user_app.get_chat_history(chat_id, limit=1):
            await user_app.edit_message_text(chat_id, msg.id, "✅ Test edit successful!")
            await message.reply_text("✅ Successfully edited a message.")
            return
        await message.reply_text("❌ No messages found to edit.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")



# Start both clients
print("Bot & User Session Running...")
user_app.start()  
app.run()
