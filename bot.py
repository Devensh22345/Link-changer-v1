from pyrogram import Client, filters, errors, enums
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo
import asyncio
from configs import cfg  # Importing config

# Bot Config
app = Client(
    "editor_bot",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# New media and caption (Replace with your content)
NEW_MEDIA = "https://example.com/new_media.jpg"  # Replace with your image/video URL
NEW_CAPTION = "**🔄 This media has been updated! 🔄**"  # New caption
NEW_TEXT = "**🔄 This message has been updated! 🔄**"  # New text for text-only messages

# Start command
@app.on_message(filters.command("start"))
async def start_message(client: Client, message: Message):
    await message.reply_text("Hello")  # Replies with "Hello" when the bot is started

# Edit all messages in a chat
@app.on_message(filters.command("editall") & filters.user(cfg.SUDO))  # Only sudo users can trigger
async def edit_all_messages(client: Client, message: Message):
    chat_id = message.chat.id  # Uses the chat where the command is sent
    msg_count = 0

    try:
        async for msg in client.get_chat_history(chat_id, limit=1000):  # Adjust limit if needed
            try:
                if msg.photo:  # If the message contains a photo
                    await client.edit_message_media(
                        chat_id,
                        msg.id,
                        media=InputMediaPhoto(NEW_MEDIA, caption=NEW_CAPTION)
                    )
                elif msg.video:  # If the message contains a video
                    await client.edit_message_media(
                        chat_id,
                        msg.id,
                        media=InputMediaVideo(NEW_MEDIA, caption=NEW_CAPTION)
                    )
                elif msg.document:  # If the message contains a document
                    await client.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
                elif msg.caption:  # If the message has a caption but no media
                    await client.edit_message_caption(chat_id, msg.id, NEW_CAPTION)
                else:  # If it's a text message
                    await client.edit_message_text(chat_id, msg.id, NEW_TEXT)

                msg_count += 1
                await asyncio.sleep(1)  # Delay to prevent floodwait errors

            except errors.MessageNotModified:
                continue  # Skip if already updated
            except errors.MessageEditTimeExpired:
                continue  # Skip if message is too old to edit
            except Exception as e:
                print(f"Error editing message {msg.id}: {e}")

        await message.reply_text(f"✅ Successfully edited {msg_count} messages in this chat.")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
        print(e)

print("Bot is running...")
app.run()
