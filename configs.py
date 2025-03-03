import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7749301298:AAE_E6Rtza_Gi564Lu42N0YzCa4P5wxVrGQ")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFP5NMAPdIxyCoAjUyNwKUU6Mhzrs-qpzP94WAcNzkwyobumflu4J2KJTZ0PliYMmQEAiaO1fiGUzMuf4jdnOsUZBOwDqKGWX1MDNEhK6mcAkKzk0jq0ONSs08Y-IDylN698soccrLcjiYKNKB4NA4MDWWcr0iOaKY3reXftW5xjZrv2t2EHbsqLfVE4-c1Ohzwnbil5ttvSSEH9qWMmDgmTGW9q_3HWpITBLDWGee4RGz-6CaH7eA1dq9ittriUQS0TTHPU-pFo3n_D-KsW9fxEhl__29kRftUjRQMmvNCNhJ4vL90fWE8etoCFq3a4G7RGp5g0UZU26ZpIt8jFW_jr6GV6AAAAAHObFO5AA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002392460433"))  # Default is a placeholder

cfg = Config()
