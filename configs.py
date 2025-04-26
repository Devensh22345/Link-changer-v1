import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8186305026:AAHRhmjQxBON6QfkmGOYN5WMJtyl1Vpyk9A")
    
    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://GUNJI:GUNJI@cluster0.tbsqu96.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL_1", "-1002571702527"))
    
    LINK_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002067586560"))  # Default is a placeholder

cfg = Config()
