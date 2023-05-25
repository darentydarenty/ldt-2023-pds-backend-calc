import asyncio
import datetime
import logging

__all__ = ["App"]

import time

import fastapi
from asgiref.sync import async_to_sync
from fastapi import APIRouter, FastAPI

from app import config
from app.pkg import connectors
from app.pkg.logger import Logger
from app.pkg.encrypt import fernet

from app.internal.constant import ConstantRepository, ConstantUseCase, ConstantHandler
from app.internal.calculations import CalculationsHandler, CalculationsRepository, CalculationsUseCase

from pydantic import BaseModel


class HealthCheckModel(BaseModel):
    status: str = "OK"
    request_duration: float | None


router = APIRouter(prefix="/base", tags=["Basic"])


fastapi_app: FastAPI


@router.get("/health")
async def health_check():
    start = datetime.datetime.now()
    response = HealthCheckModel()
    end = datetime.datetime.now()
    response.request_duration = end.microsecond - start.microsecond

    return response


class App:
    __settings: config.Settings
    __fernet_encryptor: fernet.FernetEncryptor

    _logger: Logger
    _postgresql: connectors.Postgresql
    _http_client: connectors.HttpClient

    _constant_repo: ConstantRepository
    _constant_uc: ConstantUseCase

    __app: fastapi.FastAPI

    def __init__(self):
        print("really did this shit")

    @classmethod
    async def build(cls):
        global fastapi_app

        self = cls()
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

        self._logger.log(f"init app with docs_url: {self.__settings.DOCS_URL}", logging.INFO)

        self.__app = fastapi.FastAPI(
            title=self.__settings.SERVICE_NAME,
            description="put your description here",
            version="0.1.0",
            docs_url=self.__settings.DOCS_URL,
            openapi_url=self.__settings.OPENAPI_URL,
        )

        self.__fernet_encryptor = fernet.FernetEncryptor(
            self.__settings.FERNET_KEY.get_secret_value()
        )

        self._constant_repo = ConstantRepository(
            postgresql=self._postgresql
        )
        self._constant_uc = ConstantUseCase(
            const_repo=self._constant_repo
        )
        await self._constant_uc.load()

        self._constant_handler = ConstantHandler(const_uc=self._constant_uc)

        self._calc_repo = CalculationsRepository(postgresql=self._postgresql)
        md = self._constant_uc.get_data()
        print(md)
        self._calc_uc = CalculationsUseCase(
            calc_repo=self._calc_repo,
            model_data=md,
        )
        self._calc_handler = CalculationsHandler(calc_uc=self._calc_uc)

        self.__app.include_router(router)
        self.__app.include_router(self._constant_handler.router)
        self.__app.include_router(self._calc_handler.router)

        fastapi_app = self.__app

    def get_app(self) -> fastapi.FastAPI:
        return self.__app

    async def a_get_app(self) -> fastapi.FastAPI:
        return self.__app


__all__ = ['App']
