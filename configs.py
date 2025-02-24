from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7586990531:AAFqwmiM6z88qAuNVyZ0nmCVzJQoXKhKGRg")
    FSUB = getenv("FSUB", "Bot")
    CHID = int(getenv("CHID", "-1002323780047"))
    SUDO = list(map(int, getenv("SUDO").split(7038407818,6872968794)))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Edit:Edit@cluster0.dzzd8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
cfg = Config()
