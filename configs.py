import os

class Config:
    # Basic Telegram Bot & User Client Configurations
    API_ID = int(os.getenv("API_ID", "22207976"))
    API_HASH = os.getenv("API_HASH", "5c0ad7c48a86afac87630ba28b42560d")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7686232626:AAFb8LoDG_Ioy-r3pGA9gfJejRm4I60HCnA")
    SESSION_STRING_1 = os.getenv("SESSION_STRING_1", "BQGofiMAE-6C5Fa73QyvAw7oiLskI59RpgP1fEXijpWofwc39WV71-PzHd1mFGr7uWeDFaajV-eHIDIA48DvIdb4aZjym8bw3PTcHGXVCMAy4oTubpnC8DBzINo_xtpvEZhRUourv59mupimDuIJUX6fwAc-rRVDDsWKxLDTAz1-3D0cXL39CVScpSOUoURx-s9J3tJtsma0H3TYVX_ArNVfj0jfzZt40O-YC85eO6SXyDbdz2rQNfu2utoRAqeDPwJNvb1UbAqDEWUFRqoAuhPSAxUwiRuITR-yJ7veJs1-qnuST67i-OEicHWSA4c3zDxlDWT2HmkFSBZzX7QowIDM4IV1QQAAAAHLm2QHAA")
    SESSION_STRING_2 = os.getenv("SESSION_STRING_2", "BQF3Z0oARxpI6HZNBMuijHW5JNYH466X3LDWLvq-oI5lgctud69UcCKQhKLbKmsPN6i1hKZClliMI7FCzCQn_oBxpnDqgQpxCqRfzBhsTbUYLOGuOMHdmFREFuG_r_8GUos6-z_56SRKENbGWbtXrNDsTOduecx4RrD2lBE3OyJwkTyfzNkfjNyxy6fXl_McztnQpW0o-r-Jl-klG3KmOm22hUXSyrskGS7FvfFF_AV7ynE7d7CCAvt_K5HCbBksjGz8MxpZ0StR0BzLcUPG2SjVDR3rb6t4DZdlahawpwrvqoGS6Pg5hsHSl58QvS4IY48mD72dsQXnsCrRC4ABMnapb68unwAAAAHjPESeAA")

    # Sudo Users (Admins)
    SUDO = list(map(int, os.getenv("SUDO", "6872968794").split()))

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://Test:Test@cluster0.pcpx5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "Test")
    # Log Channel (Add your log channel ID here)
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1002372592189"))  # Default is a placeholder

cfg = Config()
