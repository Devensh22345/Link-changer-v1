import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8017555909:AAHkb7UMF8GNzYZcrO9shconqPwlfE73qe0")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")

    # Log Channel (for storing logs and session data)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002392460433"))

    # Default Values for Creating Channels and Temporary Channels
    TEMP_CHANNEL_PREFIX = os.getenv("TEMP_CHANNEL_PREFIX", "Temp-")
    CHANNEL_CREATION_TIMEOUT = int(os.getenv("CHANNEL_CREATION_TIMEOUT", "18000"))  # 5 hours (in seconds)
    USERNAME_CHANGE_INTERVAL = int(os.getenv("USERNAME_CHANGE_INTERVAL", "3600"))  # 1 hour (in seconds)

cfg = Config()
