import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv, load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
env_file_path = os.path.join(BASE_DIR, ".env")

load_dotenv(find_dotenv(env_file_path))

class EnvConfig(BaseSettings):
    POSTGRES_USER:str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST:str
    POSTGRES_PORT:int = 5433
    POSTGRES_DB:str
    DEBUG:bool
    model_config = SettingsConfigDict(case_sensitive=True)

ENVS = EnvConfig()
