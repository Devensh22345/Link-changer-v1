import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7523630639:AAEKX-h5rGwGzCIn-8fcsCJW-CKcWuu640U")
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFP5NMAnuCnUZEXyZOTW_iPBNvBVkacf-VJ2Y2ZL0uo44um8_qZSkHb5itc0ddI8XUnihqhkGyMtkP9Hafx5g8V6KZSPCaxhPDJxdwMDiZATy5Zd-ur4romPpjlELbBV6UNGEoRj3pdzyx-w9Y_q8mRNWWOJr1L5FqNo_tH9ycfYGVzP1K5tVO8veM9iZMAg2D5DBLeeAbxraVpuT1TOW07rNwLdKfrx3jQgz8l3arCiNp1JajYl-P2RkUO6wFcsE3NAeZqyvg_70CgtmzSXVxn_Gyd5sZtLXiVyc2SiM3NYsm1cEDfs0WLz3MbGV49ap17pZwnDpXwRteNua95lhZK-tCmkQAAAAHObFO5AA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
