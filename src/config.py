import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:" \
                   f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:" \
                   f"{POSTGRES_PORT}/{POSTGRES_DATABASE}"
setting = Settings()

print(setting.__dict__,"Seeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")