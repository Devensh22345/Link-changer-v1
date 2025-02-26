from os import getenv

class Config:
    API_ID = int(getenv("API_ID", "22207976"))  
    API_HASH = getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")  
    BOT_TOKEN = getenv("BOT_TOKEN", "8017555909:AAHkb7UMF8GNzYZcrO9shconqPwlfE73qe0")  
    SESSION_STRING = getenv("SESSION_STRING", "")  
    SUDO = list(map(int, getenv("SUDO", "6872968794").split()))  
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  

cfg = Config()
