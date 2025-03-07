import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7686232626:AAFb8LoDG_Ioy-r3pGA9gfJejRm4I60HCnA")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQGwgsYAEiQJm6BHhAJHrNGVG2cbdS-H13UMhHX_OquKRwrUyfLKT-n4w8UJQXKcovSeZiGlwlNzoVAPt_5siZ71VwnTTvVwq8sbgGOD_dmP-0XLpZCFZPdp-0KzTc3T77XLx2NVpQn0qZL0-mGjHM9yKancIycwsYuZG4GV3SYitU0nfhWrJS_mnN_yjinYrLPrYlAShGw-aObsPXhE-cGX6Uc7ZVVv_xI5_nEPPJP8_QOv_jtwuBItioa36rMsHyTSiSwbTVwWBZAYK1X3SlV5lnhrjOPazUgsLkkoJivEfTC4pidUNakHyNwDNeawrHP5Y31X5U-VCWo_EeCLOP05H3taOAAAAAHTrS0mAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
