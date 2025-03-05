import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7430337602:AAHes470_Jry8lghlL4_bo49SKZ5W-stBYo")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFl9_kAagtNFawC2ym0B6bR_8Moll7RqysuGVoogDk3weX-GkoPJyRabNa8qEvrUPYzZW9BRx3lPOYVSHHSArBShKELoD-NpCurpNPheAaQlFxPB7ELXO5ybKPmswjxYpsGtPsDK7NqlH1herD8se5yQmhm0tEmko5aUnO5B86bcLurCgkjgPczXRQ1gq2MhuMC4OUxUb7L-w32pB46uNvETJt2gM5A7ic3ZFD-hrFA_wUdt7khlE1wOvYw-S0v5zHkYCsORn6iTAgFtejUyvjyYxlsKvA2vgtdtvBn2KfHpmy0f-E09YIusjGJ4Yg-j2GzQUvKA4wGaC_3fQpTHtJU2bxDtwAAAAHkzOnhAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
