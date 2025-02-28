from pyrogram import Client, filters
import re
from motor.motor_asyncio import AsyncIOMotorClient
from configs import cfg

# Initialize MongoDB Client
mongo_client = AsyncIOMotorClient(cfg.MONGO_URL)
db = mongo_client["autoposter_db"]
channels_collection = db["channels"]

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

replacement_username = "**DK_ANIMES**"  # Set your replacement username

@app.on_message(filters.chat & (filters.photo | filters.video | filters.document))
async def edit_caption(_, message):
    """Detect media posts in a channel and edit only the caption."""
    chat_id = message.chat.id

    # Check if the bot is an admin before proceeding
    bot_member = await app.get_chat_member(chat_id, (await app.get_me()).id)
    if bot_member.status not in ["administrator", "creator"]:
        return

    if message.caption:  # Only modify if there's a caption
        new_caption = re.sub(r"@([\w_]+)", lambda m: f"@{replacement_username}", message.caption)

        try:
            await message.edit_caption(new_caption)  # Edit the caption instead of reposting
        except Exception as e:
            print(f"Failed to edit caption in {chat_id}: {e}")

async def main():
    await app.start()
    print("hello")
    await asyncio.Event().wait()

print("I'm Alive Now!")
app.run(main)
