import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7611358375:AAG3Ky6DLfch9jDd7tXhQchDmXgbeiErg1s")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQE2UfoAMvfkYk49GCsudtFID4728i_QkbyXQ4-DdK4a8qRL5Lx32hX26KiTYAPSvY-rBU1WkwzmQ1SNkBP_ZeuIdesjzg0g5n5MJNTmoBukoBRHMhpp9wxBWv8JtBTpFr4DRl19ST_PNSFjXsHT4GCWlR_bfg5jIqP-WXaozZ82dp9ZGhvpfxrlKdYebimLy9lh57gOZlhHO03toEjjC39PBhp0D-7vxP5bAtibdYRKE3uI0lKE7TbqtHVlPfNMO5DvuSfYcMAign22UtYEKeRfW7rkOnWXmBftycFVZTWR-KOO3jNbiy-PEzI7JfyI9U0aIRe7Q-6PFsxr3a_-3n5LDXtXsAAAAAHQQQwQAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
