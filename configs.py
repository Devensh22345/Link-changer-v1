import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7430337602:AAHes470_Jry8lghlL4_bo49SKZ5W-stBYo")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQGWsKgAOUCvuMygQHNNYKWp9QqCX_M_fv7mxyvX-zJO_bLiras4g1YMZaqowebr2pz_czND0z0Hr5jAlGf5Q5Jj6ocWuy0WCMuqh1hk89Yub3cB8marX2n21FsNAWWTz4exbZkQBVOlSBao-atMuxQ46mFsoj8Edk3xteNAABME1uxUeQmemWDDvREP_4xdFkorRHQwU5dwGRqq9VTmS5QLdK0mTcdxT0BDrP2VwpdHV5v-Bhc7mGnLumB8bQDPiednuKvdOmEHKJdXiew7Y8XsittCwSvryjvS7fBebostHNFYzAunXEB7qVQmF-XqgIe6VWMjxtiTJSzm34as_e1oUP84AQAAAAGh6PtbAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
