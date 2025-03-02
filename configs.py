from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7294498798:AAGt-ecPtI2HuOTUq_Z7dTpcHO4rg70klQg")
    FSUB = getenv("FSUB", "Bot")
    CHID = int(getenv("CHID", "-1002413846440"))
    OWNER_ID = list(map(int, getenv("SUDO", "6872968794").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Edit:Edit@cluster0.dzzd8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LOG_CHANNEL = int(getenv("LOG_CHANNEL", "-1002403581455"))# Replace with your log channel ID

cfg = Config()
