import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8017555909:AAHkb7UMF8GNzYZcrO9shconqPwlfE73qe0")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFP5NMAb8Grng6oPBGtvmy3oAwgFL8hxIlxK8ehWE-oFnTwtr29EvsVCyY_W-c5uaCVcORW2ccH39YHyFK__ghhHAdyM2cCTqcnn19BEchjROJ9HGIRSZMJ8ZOMsTUBWEVFV9NonW_eljo8b3g-x4SEmYRnmXmjqWNG15N1CguBMfnFRpkez5dg-eSsgEQLq9Rqj2Pf7YUqlxmhR_BQZKOmBrsDPIl85XSY5wGcX4_PYPvT8bfcuzCYZ_m1hjs67KS0-SYkC78eVRs_GAA6cCKUvKAkiIrpHZSJQjwrTReJjpRbPUkp-Hkj1IUroOr1q1pdboPwtSh-DUGJGwzs3ZHqKagj9AAAAAHObFO5AA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002392460433"))  # Default is a placeholder

cfg = Config()
