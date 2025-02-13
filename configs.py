from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = getenv("BOT_TOKEN", "7365852964:AAHZHUP0UGLyU2hco5AruU7XlTcW3ktwmwo")
    FSUB = getenv("FSUB", "DK_ANIMES")
    CHID = int(getenv("CHID", "-1002154311129"))
    SUDO = list(map(int, getenv("SUDO").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Autofilterbot:Autofilterbot@cluster0.1oipdqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    
cfg = Config()
