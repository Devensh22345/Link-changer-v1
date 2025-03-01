from pymongo import MongoClient
from configs import cfg

# Initialize MongoDB Client
client = MongoClient(cfg.MONGO_URI)

# Database and Collections
db = client['main']
users = db['users']  # Sudo users
channels = db['channels']  # Created channels

# SUDO USER FUNCTIONS

def is_sudo_user(user_id: int) -> bool:
    """Check if a user is a sudo user."""
    return users.find_one({"user_id": user_id}) is not None

def add_sudo_user(user_id: int) -> None:
    """Add a user to the sudo user list."""
    if not is_sudo_user(user_id):
        users.insert_one({"user_id": user_id})

def remove_sudo_user(user_id: int) -> None:
    """Remove a user from the sudo user list."""
    users.delete_one({"user_id": user_id})

def get_all_sudo_users() -> list:
    """Return a list of all sudo user IDs."""
    return [user["user_id"] for user in users.find()]

def total_sudo_users() -> int:
    """Return the total count of sudo users."""
    return users.count_documents({})

# CHANNEL FUNCTIONS

def add_channel(channel_id: int, channel_name: str, created_by: int) -> None:
    """Add a created channel to the database."""
    if not channels.find_one({"channel_id": channel_id}):
        channels.insert_one({
            "channel_id": channel_id,
            "channel_name": channel_name,
            "created_by": created_by
        })

def is_channel_in_db(channel_id: int) -> bool:
    """Check if a channel exists in the database."""
    return channels.find_one({"channel_id": channel_id}) is not None

def get_all_channels() -> list:
    """Return a list of all created channels."""
    return list(channels.find({}))

def total_channels() -> int:
    """Return the total count of created channels."""
    return channels.count_documents({})
