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

replacement_username = "DK_ANIMES"  # Set your replacement username

@app.on_message(filters.channel & (filters.photo | filters.video | filters.document))
async def edit_caption(_, message):
    """Detect media posts in a channel and edit only the caption."""
    if message.caption:  # Only modify if there's a caption
        new_caption = re.sub(r"@([\w_]+)", lambda m: f"<b>@{replacement_username}</b>", message.caption)

        try:
            await message.edit_caption(new_caption)  # Edit the caption instead of reposting
        except Exception as e:
            print(f"Failed to edit caption in {message.chat.id}: {e}")

async def main():
    await app.start()
    print("hello")
    await asyncio.Event().wait()

print("I'm Alive Now!")
app.run(main)
