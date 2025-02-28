from pyrogram import Client, filters
import re
import asyncio
import logging
from configs import cfg

# Set up logging to see debug output in your logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**[@DK_ANIMES](https://t.me/DK_ANIMES)**"  # Bold and clickable username

# /start command to check if the bot is online
@app.on_message(filters.command("start") & filters.private)
async def start_message(_, message):
    logging.info(f"Received /start command from {message.chat.id}")
    await message.reply_text("✅ Bot is online and working!")

# This handler processes only video messages in channels
@app.on_message(filters.channel & filters.video)
async def edit_caption(_, message):
    logging.info(f"Received video message in chat: {message.chat.id}")
    logging.info(f"Original caption: {message.caption}")
    if message.caption:
        new_caption = re.sub(r"@[\w_]+", replacement_username, message.caption)
        logging.info(f"New caption: {new_caption}")
        try:
            await message.edit_caption(new_caption, parse_mode="Markdown")
            logging.info(f"Edited caption in chat: {message.chat.id}")
        except Exception as e:
            logging.error(f"Failed to edit caption in chat {message.chat.id}: {e}")

async def main():
    try:
        await app.start()
        logging.info("Bot has started and is running.")
    except Exception as e:
        logging.error("Error starting the bot. Check BOT_TOKEN, API_ID, and API_HASH. Error: %s", e)
        return  # Stop execution if credentials are wrong
    await asyncio.Event().wait()  # Keeps the bot running

if __name__ == "__main__":
    logging.info("I'm Alive Now!")
    asyncio.run(main())
