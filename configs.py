from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "8112564584:AAFTqWtQ4L1uezP6-SDAG5YE27pdQO4w2iI")
    FSUB = getenv("FSUB", "Bot")
    CHID = int(getenv("CHID", "-1002413846440"))
    SUDO = list(map(int, getenv("SUDO").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Auto1:Auto1@cluster0.umt5z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    LOG_CHANNEL = "-1002413846440"  # Replace with your log channel ID

cfg = Config()
