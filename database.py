from pymongo import MongoClient, ASCENDING
from configs import cfg
from datetime import datetime

# Connect to MongoDB
client = MongoClient(cfg.MONGO_URI)
db = client[cfg.MONGO_DB_NAME]

# Collections for storing created channels, logs, and user sessions
created_channels = db['created_channels']
channel_logs = db['channel_logs']
user_sessions = db['user_sessions']

# Ensure indexes for faster queries and unique constraints
created_channels.create_index([('channel_id', ASCENDING)], unique=True)
channel_logs.create_index([('channel_id', ASCENDING)])
user_sessions.create_index([('user_id', ASCENDING)], unique=True)

# Add a created channel to the database
def add_created_channel(channel_id: int, channel_name: str = None, created_by: str = None, username: str = None, temporary: bool = False):
    created_channels.update_one(
        {'channel_id': channel_id},
        {
            '$set': {
                'channel_name': channel_name,
                'created_by': created_by,
                'username': username,
                'temporary': temporary,
                'created_at': datetime.utcnow()
            }
        },
        upsert=True
    )

# Get all created channels from the database
def get_created_channels(temporary: bool = False):
    return list(created_channels.find({'temporary': temporary}))

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
    add_created_channel(
        channel_id=channel_id,
        username=old_username,
        created_by=created_by,
        temporary=True
    )

# Get all temporary channels
def get_temporary_channels():
    return get_created_channels(temporary=True)

# Delete a temporary channel from the database
def delete_temporary_channel(channel_id: int):
    delete_created_channel(channel_id)

# Log creation of a new channel with a specific username
def log_new_channel_creation(channel_id: int, old_username: str, created_by: str):
    channel_logs.insert_one({
        'channel_id': channel_id,
        'username': old_username,
        'created_by': created_by,
        'created_at': datetime.utcnow()
    })

# Add or update a user session in the database
def set_session(user_id: int, session: str = None):
    user_sessions.update_one(
        {'user_id': user_id},
        {'$set': {'session': session, 'updated_at': datetime.utcnow()}},
        upsert=True
    )

# Retrieve a user session from the database
def get_session(user_id: int) -> str:
    user_data = user_sessions.find_one({'user_id': user_id})
    return user_data.get('session') if user_data else None

# Delete a user session (logout)
def delete_session(user_id: int):
    user_sessions.delete_one({'user_id': user_id})

# Check if a session exists for the user
def session_exists(user_id: int) -> bool:
    return user_sessions.find_one({'user_id': user_id}) is not None
