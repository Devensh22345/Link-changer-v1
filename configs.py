import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7686232626:AAFb8LoDG_Ioy-r3pGA9gfJejRm4I60HCnA")
    SESSION_STRING_1 = os.getenv("SESSION_STRING_1", "BQG6pK4AatAzI2WWOxijL_pFOJwbm2WcSCdQmkI5OMev9sGhcMZ-hpUstwxhGhZ1j3dMcreGcymKZfMrNVLN9mH8O2cr2rQJGdl2kwYZ2kbJ991jFUXbRR49ZUUERCPN4QgZz9eUCZWtn2iSUo8TRNIjmiqJ9UPnlNBtBxnOzl2awyxytYiGpsiiGx4pLmZwM5JB6qjsXlYsHDNf33iJbWokE85vgJ3fbeF039KZRuGoxzIT9XoihcCUxnO6c0O-y67qpnAoJ4xQeKqu7c-Wq0csIKhnEVjXC3c4yWMczJ2KPTmTwtrXeSSatMbisIDgdRnHU7E3lxSukxgw0tmVN0cxnaHMuwAAAAG_F4DBAA")
    #SESSION_STRING_2 = os.getenv("SESSION_STRING_2", "BQE2UfoANOeG6AAhWvcYMBJnzemxCQ81VK7dvm9QA0jCiYRXFgzdQwD4ZiGAAxcCrzspUiKtG6zsvjCNUXNQhinXVJUS6n4-9ca6DDlus1kTuAbkC8kWzcKWC_UTdQfTw-RjBQrDD2u6Pc4BWxaXC6lT6DnKHO-vdhXYMkf1opOP3tgREL6GOppliaPF2sCDsfP0VRx4Aoq78HJjjPK_9IWtOGgqXqlNwj08KG6VPfVHvmaNXq-fw5HHq9r4YCDUufJxUIxzJ14I8yLj5K_zUp3uWWb7d7RUcV3JNxJzzYHmzBu7WV3lOu05CvBMXyFmi0-HjQnbWCHKdyfkrMbbzP5KBblYfAAAAAHQQQwQAA")
    #SESSION_STRING_24 = os.getenv("SESSION_STRING_24", "")
    #SESSION_STRING_25 = os.getenv("SESSION_STRING_25", "")
    #SESSION_STRING_26 = os.getenv("SESSION_STRING_26", "")
    #SESSION_STRING_27 = os.getenv("SESSION_STRING_27", "")
    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
