import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7749301298:AAE_E6Rtza_Gi564Lu42N0YzCa4P5wxVrGQ")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQG6pK4AZbYpWA6ctsAL4-Sr73Q0Yn9BLLSfB6SRUYq9izFVwBvfcZgLw6gs-MUtjUCuIU-S6fgu80U8HOZ0l8uJkpDw4mJf53yra7rg1ExtYg4Jg-7iXeCf5-LsISflel_SfjVAnxz9E9bXF5R44eAOfIGe7ileDiJJF5gO0i7p150LFC4tiWEjXZGyVzhjsdk5T5DLJ-5loa2SdyEqqvnotHqdkFZCTAS6gbkMCIGQ5oOTiGzyiUbBO_EAgq2X32sAfY6m51a8-3iTJYDw-JZ4TvZYU5KzSwEgEKNP2tKuBGpZrAQ5102_4XOzf35aG9ScqBeTRSf4FZ23RO5EEzYE8mezagAAAAG_F4DBAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002392460433"))  # Default is a placeholder

cfg = Config()
