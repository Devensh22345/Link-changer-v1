import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7833128310:AAEoF3shK5Z3EFNsin1gr5BpQyjzLyzyc5A")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQGrkk0AYZvLlO4pTcTNov0UBvh2sxfeXzsiUHS1q8P_ZQtavJM4DiO94nCkrt50cFhZqESdUKeJL16OKJul3BuOAfeFbEP6QJ5YvWB-5l43OldjFt3yIMuR7_ApX8zaecgh-luecmPeLPNZj61WnxTbEqJoNo0rv8SFc-F9yPecH6gD4xN49SasPRfRFh1IB0HnrUDuZrOWxO-3C6nYml9i2PZ1faXHpURI6D8VNZpnFJCZ1HOCnIRgwel6zTzsILT3AvXTAGL3-RtSd6_64mTvpf__62cI2XqMPbsgTZXerGLHoahl1tztz-xmVPSszxFczUC6T_5LBBsFVab7HngDLhkEmAAAAAG69JBgAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
