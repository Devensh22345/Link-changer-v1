from pymongo import MongoClient
from configs import cfg
from datetime import datetime

# Connect to MongoDB
client = MongoClient(cfg.MONGO_URI)
db = client[cfg.MONGO_DB_NAME]

# Collections
created_channels = db['created_channels']
channel_logs = db['channel_logs']
channel_invites = db['channel_invites']

def add_created_channel(channel_id: int, channel_name: str = None, created_by: str = None, username: str = None):
    created_channels.insert_one({
        'channel_id': channel_id,
        'channel_name': channel_name,
        'created_by': created_by,
        'username': username,
        'created_at': datetime.utcnow()
    })


def channel_exists(channel_id: int) -> bool:
    return created_channels.find_one({'channel_id': channel_id}) is not None


# 🔄 Invite Link & Log Message Utils (MODIFIED)
# Set or update invite log for a channel
def set_invite_log(channel_id: int, invite_link: str, expires_at: datetime, message_id: int = None):
    update_data = {
        'invite_link': invite_link,
        'expires_at': expires_at,
        'last_updated': datetime.utcnow()
    }
    if message_id:
        update_data['message_id'] = message_id

    channel_invites.update_one(
        {'channel_id': channel_id},
        {'$set': update_data},
        upsert=True
    )


def get_invite_log(channel_id: int):
    return channel_invites.find_one({'channel_id': channel_id})

def delete_invite_log(channel_id: int):
    channel_invites.delete_one({'channel_id': channel_id})

def add_active_channel(channel_id: int):
    if not db['invite_rotation'].find_one({'channel_id': channel_id}):
        db['invite_rotation'].insert_one({
            'channel_id': channel_id,
            'joined_at': datetime.utcnow()
        })

def get_active_channels():
    return [doc['channel_id'] for doc in db['invite_rotation'].find()]

def save_logged_message(channel_id: int, message_id: int):
    db['invite_logs'].update_one(
        {'channel_id': channel_id},
        {'$set': {'message_id': message_id, 'updated_at': datetime.utcnow()}},
        upsert=True
    )

def update_logged_message(channel_id: int, message_id: int):
    db['invite_logs'].update_one(
        {'channel_id': channel_id},
        {'$set': {'message_id': message_id, 'updated_at': datetime.utcnow()}}
    )
# remove from active_channels


def remove_active_channel(channel_id: int):
    db['invite_rotation'].delete_one({"channel_id": channel_id})

def remove_logged_message(channel_id: int):
    db['invite_logs'].delete_one({"channel_id": channel_id})

def remove_channel_from_db(channel_id: int):
    remove_active_channel(channel_id)
    remove_logged_message(channel_id)
    delete_invite_log(channel_id)
    # Optionally:
    # created_channels.delete_one({'channel_id': channel_id})
    # channel_logs.delete_one({'channel_id': channel_id})



def get_logged_messages():
    return {
        doc['channel_id']: doc['message_id']
        for doc in db['invite_logs'].find()
        if 'message_id' in doc
    }
