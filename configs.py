import os

class Config:
    API_ID = int(getenv("API_ID", "22207976"))  
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")  
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8017555909:AAHkb7UMF8GNzYZcrO9shconqPwlfE73qe0")  
    SESSION_STRING = os.getenv("SESSION_STRING", "BQFBTREAe1JW2Q0rmgGLPLiY7VA9lWMZqzN17_6HDuurf3k2LxkSEfBpAOlwhMtLtKn31fCcz_WfKhUyLHh6H8Qf1y5M_2v0K0PHxFsWLm-KXzkWt5w-7T355FGAEDe_UqrnyfIpegSZdgZHwDoculI_CT6BXkYqMnl4SUfh73tdMf1qmrxuZui0O9Xn5cg8K_kdf5KzcI8JcAfIC7R0nyxo9AxZHRyOUUmvFH2-AE_Ti9CkMu5sy_j-4xve7PATYj0H8iov6oeJ_ckIlI3B4xNg3nvwaEWaeVe0S_P5k-hnYjjZ7MB7LFR50vm6xhGfN7Ln52hecskrfF6gP2Fry88AVMH7SAAAAAGSmGh2AA")  
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))  
    MONGO_URI = int(os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  

cfg = Config()
