from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

# Databases and Collections
db = client['main']
users = db['users']
groups = db['groups']
sudo_users = db['sudo_users']
authorized_users = db['authorized_users']

# Check if User Exists in DB
def already_db(user_id):
    return users.find_one({"user_id": str(user_id)}) is not None

# Check if Group Exists in DB
def already_dbg(chat_id):
    return groups.find_one({"chat_id": str(chat_id)}) is not None

# Add User to DB
def add_user(user_id):
    if not already_db(user_id):
        users.insert_one({"user_id": str(user_id)})

# Remove User from DB
def remove_user(user_id):
    if already_db(user_id):
        users.delete_one({"user_id": str(user_id)})

# Add Group to DB
def add_group(chat_id):
    if not already_dbg(chat_id):
        groups.insert_one({"chat_id": str(chat_id)})

# Get Total Number of Users
def all_users():
    return len(list(users.find({})))

# Get Total Number of Groups
def all_groups():
    return len(list(groups.find({})))

# Add Sudo User
def add_sudo_user(user_id):
    if not is_sudo_user(user_id):
        sudo_users.insert_one({"user_id": str(user_id)})

# Remove Sudo User
def remove_sudo_user(user_id):
    if is_sudo_user(user_id):
        sudo_users.delete_one({"user_id": str(user_id)})

# Check if User is a Sudo User
def is_sudo_user(user_id):
    return sudo_users.find_one({"user_id": str(user_id)}) is not None

# Get All Sudo Users
def get_sudo_users():
    return [int(user['user_id']) for user in sudo_users.find()]

# Authorize User to Avoid Deletion
def authorize_user(user_id):
    if not is_authorized_user(user_id):
        authorized_users.insert_one({"user_id": str(user_id)})

# Unauthorize User to Revoke Permission
def unauthorize_user(user_id):
    if is_authorized_user(user_id):
        authorized_users.delete_one({"user_id": str(user_id)})

# Check if User is Authorized
def is_authorized_user(user_id):
    return authorized_users.find_one({"user_id": str(user_id)}) is not None
