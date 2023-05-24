import logging

from logging.handlers import RotatingFileHandler
from pathlib import Path

import logging_loki
import logging_loki.emitter
import pydantic

MAIN_LOGGER = "main"


# Logger that prints to stdout and sends logs in loki
class Logger:

    LOG_LEVEL=logging.INFO

    __logger_path: str
    __log_format: str = (
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%("
        "funcName)s(%(lineno)d) - %(message)s "
    )

    __formatter: logging.Formatter
    _logger: logging.Logger

    __loki_handler: logging_loki.LokiHandler

    def __init__(self,
                 username: str,
                 password: pydantic.SecretStr,
                 url: str,
                 service_name: str,
                 logger_path: str):
        self.__loki_handler = logging_loki.LokiHandler(
            url=url,
            auth=(
                username, password.get_secret_value(),
            ),
            tags={
                "job": "app-logging",
                "sourse": service_name,
            }
        )

        self.__formatter = logging.Formatter(self.__log_format)

        self.__loki_handler.setFormatter(self.__formatter)

        self.__logger_path = logger_path
        logging.getLogger(MAIN_LOGGER)
        logging.basicConfig(
            format=self.__log_format,
            level=logging.INFO,
        )

        self._logger = self._get_logger()

    def get_stream_handler(self):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.__formatter)

        return stream_handler

    def _get_logger(self) -> logging.Logger:
        logger = logging.getLogger(MAIN_LOGGER)

        logger.addHandler(self.get_stream_handler())
        # logger.addHandler(self.__loki_handler)

        logger.setLevel(self.LOG_LEVEL)
        self._logger = logger
        return logger

    def log(self,
            message: str,
            level,
            add_tags: dict[str, object] = {}):
        self._logger.log(level, message, extra=add_tags)


