
import logging

__all__ = ["App"]

import fastapi

from app import config
from app.pkg import connectors
from app.pkg.logger import Logger


class App:
    __settings: config.Settings

    _logger: logging.Logger
    _postgresql: connectors.Postgresql
    _http_client: connectors.HttpClient

    __app: fastapi.FastAPI

    def __init__(self):
        self.__settings = config.parse_settings()

        self._logger = Logger(
            username=self.__settings.LOGGER_LOKI_USERNAME,
            password=self.__settings.LOGGER_LOKI_PASSWORD,
            url=self.__settings.LOGGER_LOKI_URL,
            service_name=self.__settings.SERVICE_NAME,
            logger_path=str(self.__settings.LOGGER_FILE_PATH.absolute()),
        )

        self._postgresql = connectors.Postgresql(
            username=self.__settings.POSTGRES_USER,
            password=self.__settings.POSTGRES_PASSWORD,
            host=self.__settings.POSTGRES_HOST,
            port=self.__settings.POSTGRES_PORT,
            database_name=self.__settings.POSTGRES_DATABASE_NAME,
        )

        self._http_client = connectors.HttpClient(
            timeout=float(self.__settings.HTTP_CLIENT_TIMEOUT),
        )

        self.__app = fastapi.FastAPI(
            title=self.__settings.SERVICE_NAME,
            description="put your description here",
            version="0.1.0",
            openapi_url=self.__settings.OPENAPI_URL,
            docs_url=self.__settings.DOCS_URL,
        )

    def get_app(self) -> fastapi.FastAPI:
        return self.__app
