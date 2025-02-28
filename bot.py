from pyrogram import Client, filters
import asyncio
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from configs import cfg

# Initialize MongoDB Client
mongo_client = AsyncIOMotorClient(cfg.MONGO_URL)  # Use your MongoDB connection string
db = mongo_client["autoposter_db"]
channels_collection = db["channels"]

app = Client(
    "autoposter",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

image_url = "https://envs.sh/E-7.jpg"  # Replace with your image URL

async def post_message(chat_id):
    """Send an image with a caption to a given channel."""
    caption = f"🦊 **Automatic Post!**\n\n📅 Date: {datetime.datetime.now().strftime('%Y-%m-%d')}\n🕒 Time: {datetime.datetime.now().strftime('%H:%M:%S')}\n\nJoin us: @DK_ANIMES"
    try:
        await app.send_photo(chat_id, image_url, caption=caption)
    except Exception as e:
        print(f"Failed to send image in {chat_id}: {e}")

async def auto_post():
    """Post an image every hour in all registered channels."""
    while True:
        try:
            channels = await channels_collection.find().to_list(length=None)  # Fetch all stored channels
            for channel in channels:
                await post_message(channel["chat_id"])
            await asyncio.sleep(3600)  # Wait for 1 hour
        except Exception as e:
            print(f"Auto post error: {e}")

@app.on_chat_member_updated(filters.group | filters.channel)
async def new_channel_added(_, m):
    """Detect when the bot is added to a channel and post immediately."""
    if m.new_chat_member and m.new_chat_member.user.id == (await app.get_me()).id:
        chat_id = m.chat.id
        # Check if the channel is already stored
        existing_channel = await channels_collection.find_one({"chat_id": chat_id})
        if not existing_channel:
            await channels_collection.insert_one({"chat_id": chat_id})  # Store new channel
        await post_message(chat_id)  # Post instantly after being added

async def main():
    await app.start()
    print("hello")  # Print "hello" when the bot starts
    asyncio.create_task(auto_post())  # Start the auto-posting task
    await app.idle()  # Keep the bot running

print("I'm Alive Now!")
app.run(main())
