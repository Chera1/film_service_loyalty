import os
from logging import config as logging_config

from src.core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    """Конфиг сервиса"""

    project_name: str = Field('', env="PROJECT_NAME")

    redis_host: str = Field('127.0.0.1', env="REDIS_HOST")
    redis_port: int = Field('6379', env="REDIS_PORT")

    default_page_size: int = 50
    default_page_number: int = 1

    FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут

    class Config:
        env_file = "src/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
