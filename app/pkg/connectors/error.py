from .base import BaseConnector


class NoConnectorError(Exception):
    def __init__(self, message: str, connector: BaseConnector):
        super().__init__(f"There's no connector inside {message}|{connector}")

