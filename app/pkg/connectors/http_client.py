import hashlib
import hmac
import json

import httpx

from .base import BaseConnector
from .error import NoConnectorError


class HttpClient(BaseConnector):
    def __init__(self,
                 timeout: float = 40,
                 base_url: str = "",

                 ):

        self.__client = httpx.AsyncClient(
            timeout=timeout,
            base_url=base_url,
        )

    async def get_connect(self):
        if self.__client is None:
            raise NoConnectorError("http_client", self)
        async with self.__client as client:
            yield client

    def get_dsn(self) -> str:
        pass

    async def make_request(self, request: httpx.Request) -> httpx.Response:
        return await self.__client.send(
            request=request
        )


def make_signature(private_key: str, data: dict) -> str:
    return hmac.new(
        private_key.encode("utf-8"),
        json.dumps(data).encode("utf-8"),
        hashlib.sha512,
    ).hexdigest()
