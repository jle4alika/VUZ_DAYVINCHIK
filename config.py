import datetime
from dotenv import find_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Объявление переменных окружения
    """

    TOKEN: str
    SQLALCHEMY_URL: str

    SHORT_NAME: str
    API_ID: int
    API_HASH: str

    class Config:
        """
        Настройки конфигурации Pydantic
        """

        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"


settings: Settings = Settings()
