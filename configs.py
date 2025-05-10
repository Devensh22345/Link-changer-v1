import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7854395979:AAHh64HzOBiWaqzA_lxw8lCpGuQvldSqd5Q")
    SESSION_STRING_1 = os.getenv("SESSION_STRING_1", "BQEzMd4Au1th1lduQ7mLgosYc4fg8kbaY09VuHkR7eSPoOg2nfQKLz0epSOClyC5JLjfYPJlLtV4v46J7FWN-7L_pMmbb5MNMO6vc0dRSUiIAjwRrzI-KBcIyUnFX8Ouic88UQI4UE62zsorm8eH1vzjzD4PMpevaHPCPFc84pmPRH01NCzn8Y-sRllijlwN8vPJh2ZayFaNSuDqPKyaObNyTJTgbZdIEKyXL1CHxT-lr0BUCV1Zgjb-azEYdHqH572ZqfvEO14vyaM0XvrGu92PZd6JmKcYkVX7gNC_hRkESN2XB2-k84nsQUMwE5LKYYKopoLHxNlTQ4Okz376LyNzOsyWWAAAAAG9nYW3AA")
    SESSION_STRING_2 = os.getenv("SESSION_STRING_2", "BQFDKyMAs-qzw9Baeqa_-v8Pfo1aoKrLziftnRoWFLkyte-F_teOruVaRqGVvCQllY4v6GcW2lZAudEJeBY8gICZIi3rvkfLytp-UOiRuK41LNXsP8Q6gffcih94PILOk5sScvtsfQuhMbdVOoi3Y_u_2Z-mns5zXrWXXC8PWq35t6a4jar6uYpZGG_Ekc8uTfTI5EJLysPBAY4BHb78tJnOgEEINi9W07EPj0ssDFS9mk7IxPt6mdviMEA2Xxb63It6aKbraApCADigWBsq2J6j7P6TfjMA-1HrR54FchDhXyd5pIbhpoE_ENLumsgw-RlQJMxGxDCqyqHx4EpBQ2ybCEfuaQAAAAHjhKGMAA")
    SESSION_STRING_3 = os.getenv("SESSION_STRING_3", "BQFDZXoAKu0SS4tBmjoJ3Zw-uG0EEx8OeNZf2pMBNz2V86_weHALnllkFUvAq5LYfc8NWWZbHcqZ5vIZQHMF7Kk9SAydZ4Q0hvKuODKYuvfxrE4I-0rpB8vvwOiuzTZRPYGSLuRtpCMJ3gyYqbRK_BAMNhWGC239wjNmMn4L1GpkenGtDyV3ThaxMKTXINQMK-lN6NsEgo9kpnS1f6She-eDpGMuTlHvv_h5IMG51jt5G749_IcXuac4kHgH0N209-3RpUHjoZBt-tsH7__wHg4MlcdB2tOgMPcAiMZZURl6mxJ9M_n9ZDwj_NGpvrdV5YxnbbM21fuLz3UEFLC480Vxd14EjwAAAAHhkoCOAA")
    #SESSION_STRING_17 = os.getenv("SESSION_STRING_17", "")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "5687700734").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://gun:gun@cluster0.9xemgey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002680234737"))  # Default is a placeholder

cfg = Config()
