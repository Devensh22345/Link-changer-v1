import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7611358375:AAET1Zs1DSNhuSeXhJfDvc6GFhOZn5YgC5Q")
    
    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL_1", "-1002604101366"))
    
    LINK_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001917588179"))  # Default is a placeholder

cfg = Config()
