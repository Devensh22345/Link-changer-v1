from pyrogram import Client, filters
import re
import asyncio
from configs import cfg

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**[@DK_ANIMES](https://t.me/DK_ANIMES)**"  # Bold and clickable username

@app.on_message(filters.channel & filters.video)  # Only for video posts
async def edit_caption(_, message):
    """Edit video captions if posted by an admin in the channel."""
    chat_id = message.chat.id

    try:
        # Fetch list of admins
        admins = [admin.user.id async for admin in app.get_chat_members(chat_id, filter="administrators")]

        # If the message has a caption and was posted by an admin
        if message.caption and message.sender_chat:
            new_caption = re.sub(r"@[\w_]+", replacement_username, message.caption)

            await message.edit_caption(new_caption, parse_mode="Markdown")
            print(f"Edited caption in {chat_id}")
    except Exception as e:
        print(f"Failed to edit caption in {chat_id}: {e}")

async def main():
    await app.start()
    print("hello")  # Print when the bot starts
    await asyncio.Event().wait()  # Keep the bot running

print("I'm Alive Now!")

# Correct way to run the bot
asyncio.run(main())  # Runs the async main function properly
