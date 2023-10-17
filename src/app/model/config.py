from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    timezone: int = 8


@lru_cache()
def get_settings():
    return Settings()
