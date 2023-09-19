import sys

from loguru import logger
from pydantic import ValidationError, BaseSettings


class Settings(BaseSettings):
    """Model for service settings."""
    
    service_name: str
    service_version: str
    structured_logs: bool = False

    api_token: str

    class Config:  # NOQA
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Envs validation.

    @return [Settings]: Settings model
    """
    try:
        Settings()
    except ValidationError:
        logger.critical("Envs were set incorrectly !")
        sys.exit(0)
    logger.info("Envs are correct !")
    logger.info(f"Received envs {Settings()}")
    return Settings()

service_settings = get_settings()
