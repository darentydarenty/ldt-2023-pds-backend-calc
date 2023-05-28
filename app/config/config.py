import os
import pathlib

from functools import lru_cache

from pydantic import BaseModel, PositiveInt, SecretStr, StrictStr


class Settings(BaseModel):

    SERVICE_NAME: str

    POSTGRES_HOST: str
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DATABASE_NAME: str

    LOGGER_LEVEL: StrictStr
    LOGGER_FILE_PATH: pathlib.Path
    LOGGER_LOKI_USERNAME: str
    LOGGER_LOKI_PASSWORD: SecretStr
    LOGGER_LOKI_URL: str

    FERNET_KEY: SecretStr

    HTTP_CLIENT_TIMEOUT: PositiveInt

    OPENAPI_URL: str
    DOCS_URL: str

    TEMPLATE_PATH: str
    OUTPUT_PATH: str

    class Config:
        """Configuration of settings."""

        #: str: env file encoding.
        env_file_encoding = "utf-8"
        #: str: allow custom fields in model.
        arbitrary_types_allowed = True


@lru_cache()
def parse_settings() -> Settings:
    return Settings(**os.environ)
