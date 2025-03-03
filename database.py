from pymongo import MongoClient
from configs import cfg

# Connect to MongoDB
client = MongoClient(cfg.MONGO_URL)
db = client["session_bot"]

# Collections
users = db["users"]
groups = db["groups"]

# Add a new user to the database
def add_user(user_id: int):
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id})

# Add a new group to the database
def add_group(group_id: int):
    if not groups.find_one({"group_id": group_id}):
        groups.insert_one({"group_id": group_id})

# Get total number of users
def all_users() -> int:
    return users.count_documents({})

# Get total number of groups
def all_groups() -> int:
    return groups.count_documents({})

# Get all users
def get_all_users() -> list:
    return [user["user_id"] for user in users.find()]

# Remove a user from the database
def remove_user(user_id: int):
    users.delete_one({"user_id": user_id})

# Store generated session string in log channel
def log_session(user_id: int, session_str: str, version: str):
    users.update_one(
        {"user_id": user_id},
        {"$set": {"session": session_str, "version": version}},
        upsert=True
    )

# Get user session string
def get_user_session(user_id: int) -> str:
    user = users.find_one({"user_id": user_id})
    return user["session"] if user and "session" in user else None
        
