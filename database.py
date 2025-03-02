from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']
auths = client['main']['auths']
sudos = client['main']['sudos']

# Check if user exists in the database
def already_db(user_id):
    return bool(users.find_one({"user_id": str(user_id)}))

# Check if group exists in the database
def already_dbg(chat_id):
    return bool(groups.find_one({"chat_id": str(chat_id)}))

# Add a new user to the database
def add_user(user_id):
    if not already_db(user_id):
        users.insert_one({"user_id": str(user_id)})

# Remove a user from the database
def remove_user(user_id):
    if already_db(user_id):
        users.delete_one({"user_id": str(user_id)})

# Add a new group to the database
def add_group(chat_id):
    if not already_dbg(chat_id):
        groups.insert_one({"chat_id": str(chat_id)})

# Get the total number of users
def all_users():
    return users.count_documents({})

# Get the total number of groups
def all_groups():
    return groups.count_documents({})

# Get all authorized users in a group
def get_auth(chat_id):
    auth_data = auths.find_one({"chat_id": str(chat_id)})
    return auth_data['auth_users'] if auth_data else []

# Add an authorized user to a group
def add_auth(chat_id, user_id):
    auth_data = auths.find_one({"chat_id": str(chat_id)})
    if auth_data:
        if str(user_id) not in auth_data['auth_users']:
            auth_data['auth_users'].append(str(user_id))
            auths.update_one({"chat_id": str(chat_id)}, {"$set": {"auth_users": auth_data['auth_users']}})
    else:
        auths.insert_one({"chat_id": str(chat_id), "auth_users": [str(user_id)]})

# Remove an authorized user from a group
def remove_auth(chat_id, user_id):
    auth_data = auths.find_one({"chat_id": str(chat_id)})
    if auth_data and str(user_id) in auth_data['auth_users']:
        auth_data['auth_users'].remove(str(user_id))
        auths.update_one({"chat_id": str(chat_id)}, {"$set": {"auth_users": auth_data['auth_users']}})

# Get all sudo users
def get_sudo():
    sudo_data = sudos.find_one({"sudo": "users"})
    return sudo_data['sudo_users'] if sudo_data else []

# Add a sudo user
def add_sudo(user_id):
    sudo_data = sudos.find_one({"sudo": "users"})
    if sudo_data:
        if str(user_id) not in sudo_data['sudo_users']:
            sudo_data['sudo_users'].append(str(user_id))
            sudos.update_one({"sudo": "users"}, {"$set": {"sudo_users": sudo_data['sudo_users']}})
    else:
        sudos.insert_one({"sudo": "users", "sudo_users": [str(user_id)]})

# Remove a sudo user
def remove_sudo(user_id):
    sudo_data = sudos.find_one({"sudo": "users"})
    if sudo_data and str(user_id) in sudo_data['sudo_users']:
        sudo_data['sudo_users'].remove(str(user_id))
        sudos.update_one({"sudo": "users"}, {"$set": {"sudo_users": sudo_data['sudo_users']}})
