from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7567832185:AAGV60L-Tfw6AZBn1lfYr6_YZDrBSiRgbl4")
    FSUB = getenv("FSUB", "Bot")
    CHID = int(getenv("CHID", "-1002413846440"))
    SUDO = list(map(int, getenv("SUDO", "6872968794").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Auto1:Auto1@cluster0.umt5z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LOG_CHANNEL = "-1002413846440"  # Replace with your log channel ID

cfg = Config()
