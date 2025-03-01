from pymongo import MongoClient
from configs import cfg

# Initialize MongoDB client
client = MongoClient(cfg.MONGO_URI)

# Database and collections
db = client['main']
channels = db['channels']

# Add a created channel to the database
def add_created_channel(channel_id: int) -> None:
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({"channel_id": channel_id})

# Get all created channels
def get_all_created_channels() -> list:
    return [channel['channel_id'] for channel in channels.find({})]
