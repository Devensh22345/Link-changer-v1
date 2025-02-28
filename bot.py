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

@app.on_message(filters.channel & filters.video)  # Only for videos
async def edit_caption(_, message):
    """Edit video captions if posted by another admin."""
    chat_id = message.chat.id
    sender_id = message.from_user.id if message.from_user else None

    # Get bot's own ID
    bot_id = (await app.get_me()).id  

    if sender_id and sender_id != bot_id:
        try:
            # Fetch admin list
            admins = [admin.user.id async for admin in app.get_chat_members(chat_id, filter="administrators")]

            if sender_id in admins:  # If the sender is an admin (but not the bot)
                if message.caption:
                    new_caption = re.sub(r"@[\w_]+", replacement_username, message.caption)
                    await message.edit_caption(new_caption, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to edit caption in {message.chat.id}: {e}")

async def main():
    await app.start()
    print("hello")  # Print when the bot starts
    await asyncio.Event().wait()  # Keep the bot running

print("I'm Alive Now!")

# Correct way to run the bot
asyncio.run(main())  # Runs the async main function properly
