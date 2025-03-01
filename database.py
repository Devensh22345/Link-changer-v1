from pymongo import MongoClient
from configs import cfg

# MongoDB Connection
client = MongoClient(cfg.MONGO_URI)
db = client['main']

# Collections
users = db['users']
channels = db['channels']

# Check if user is a sudo user
def is_sudo_user(user_id: int) -> bool:
    return users.find_one({"user_id": user_id}) is not None

# Add a sudo user
def add_sudo_user(user_id: int) -> None:
    if not is_sudo_user(user_id):
        users.insert_one({"user_id": user_id})

# Get all sudo users
def get_all_sudo_users() -> list:
    return [user['user_id'] for user in users.find()]

# Add created channel to the database
def add_created_channel(channel_id: int) -> None:
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({"channel_id": channel_id})

# Get all created channels
def get_all_channels() -> list:
    return [channel['channel_id'] for channel in channels.find()]
