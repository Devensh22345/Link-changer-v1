from pymongo import MongoClient
from configs import cfg
from datetime import datetime

# Initialize MongoDB client
client = MongoClient(cfg.MONGO_URI)

# Database and collections
db = client['main']
channels = db['channels']
temp_channels = db['temp_channels']

# Add a created channel to the database
def add_created_channel(channel_id: int, old_username: str = None, new_username: str = None) -> None:
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({
            "channel_id": channel_id,
            "old_username": old_username,
            "new_username": new_username,
            "created_at": datetime.utcnow()
        })

# Get all created channels
def get_all_created_channels() -> list:
    return [channel['channel_id'] for channel in channels.find({})]

# Add a temporary channel to the database
def add_temp_channel(channel_id: int, old_username: str, delete_at: datetime) -> None:
    temp_channels.insert_one({
        "channel_id": channel_id,
        "old_username": old_username,
        "delete_at": delete_at,
        "created_at": datetime.utcnow()
    })

# Get all temporary channels scheduled for deletion
def get_temp_channels_to_delete(current_time: datetime) -> list:
    return list(temp_channels.find({"delete_at": {"$lte": current_time}}))

# Remove a temporary channel from the database
def remove_temp_channel(channel_id: int) -> None:
    temp_channels.delete_one({"channel_id": channel_id})
