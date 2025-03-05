import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7749301298:AAE_E6Rtza_Gi564Lu42N0YzCa4P5wxVrGQ")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQG6pK4ANMnmYMIDfnkV-TDaaWLgAoLTEH8pnESRVRnZKL8IooKYybV0pdP1Vr3_Rwk_nb_xdnHZWZn_tbGvBB9GPLj6ILowvMX0ucLByzweMhkBsb1x2Ej4Iz5UoDXVnbKphC26GGlm5Mq_pNBB50MDth22_0xsRHdC2qITQbJLi-AKm7jm61RQJslksKCZbIR8vF1erLnDh4ocObkxk_DnaLAVplvzP7KvCFXkjG3A6ZWSiI7vTS7GOkvedbRFurwvhNMb82MLo1CBxU4G2C_NrkR-is6596OEnkRt88Yz2ffcGuyzIuadnWP5Eu4fPfS-8bY2mJqT5mQ3Og1NRZhlVZAhKgAAAAG_F4DBAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
