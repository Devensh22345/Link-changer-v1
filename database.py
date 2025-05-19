from pymongo import MongoClient
from configs import cfg
from datetime import datetime

# Connect to MongoDB
client = MongoClient(cfg.MONGO_URI)
db = client[cfg.MONGO_DB_NAME]

# Collections
created_channels = db['created_channels']
channel_logs = db['channel_logs']
old_usernames = db['old_usernames']  # NEW COLLECTION

# Add a created channel to the database
def add_created_channel(channel_id: int, channel_name: str = None, created_by: str = None, username: str = None):
    created_channels.insert_one({
        'channel_id': channel_id,
        'channel_name': channel_name,
        'created_by': created_by,
        'username': username,
        'created_at': datetime.utcnow()
    })

# Get all created channels from the database
def get_created_channels():
    return list(created_channels.find())

# Delete a created channel from the database
def delete_created_channel(channel_id: int):
    created_channels.delete_one({'channel_id': channel_id})

# Check if a channel exists in the database
def channel_exists(channel_id: int) -> bool:
    return created_channels.find_one({'channel_id': channel_id}) is not None

# Store old and new usernames when the channel username changes
def log_channel_username_change(old_username: str, new_username: str, changed_by: str):
    channel_logs.insert_one({
        'old_username': old_username,
        'new_username': new_username,
        'changed_by': changed_by,
        'changed_at': datetime.utcnow()
    })

# Add temporary channel details to the database, including username
def add_temporary_channel(channel_id: int, old_username: str, created_by: str):
    created_channels.insert_one({
        'channel_id': channel_id,
        'temporary': True,
        'old_username': old_username,
        'created_by': created_by,
        'created_at': datetime.utcnow()
    })

# Get all temporary channels
def get_temporary_channels():
    return list(created_channels.find({'temporary': True}))

# Delete a temporary channel from the database
def delete_temporary_channel(channel_id: int):
    created_channels.delete_one({'channel_id': channel_id})

# Log creation of a new channel with a specific username
def log_new_channel_creation(channel_id: int, old_username: str, created_by: str):
    channel_logs.insert_one({
        'channel_id': channel_id,
        'username': old_username,
        'created_by': created_by,
        'created_at': datetime.utcnow()
    })

# ✅ NEW: Save old username for a channel (for /private -> /public use case)
def save_old_username(channel_id: int, username: str):
    old_usernames.update_one(
        {"channel_id": channel_id},
        {"$set": {"username": username}},
        upsert=True
    )

# ✅ NEW: Get previously saved old username
def get_old_username(channel_id: int):
    data = old_usernames.find_one({"channel_id": channel_id})
    return data["username"] if data else None

# ✅ NEW: Get all saved usernames (for restoring public usernames)
def get_all_saved_usernames():
    return list(old_usernames.find())
