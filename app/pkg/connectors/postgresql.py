"""Postgresql connector."""
import asyncio
import functools
from contextlib import asynccontextmanager

import aiopg
from aiopg.connection import Cursor
import pydantic
from aiopg import Connection
from psycopg2.extras import RealDictCursor

from .base import BaseConnector

__all__ = ["Postgresql", "get_connection", "NoResultsException"]


class NoResultsException(Exception):
    ...


class Postgresql(BaseConnector):
    def __init__(
            self,
            username: str,
            password: pydantic.SecretStr,
            host: str,
            port: pydantic.PositiveInt,
            database_name: str,
    ):
        """Settings for create postgresql dsn.

        Args:
            username: database username.
            password: database password.
            host: the host where the database is located.
            port: the port of database server.
            database_name: database name.
        """
        self.pool = aiopg.create_pool(dsn=self.get_dsn())
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

    def get_dsn(self):
        """Description of ``BaseConnector.get_dsn``."""
        return (
            f"postgresql://"
            f"{self.username}:"
            f"{self.password.get_secret_value()}@"
            f"{self.host}:{self.port}/"
            f"{self.database_name}"
        )

    @asynccontextmanager
    async def get_connect(self) -> Connection:
        """Create pool of connectors to a Postgres database.

        Yields:
            ``aiopg.Connection instance`` in asynchronous context manager.
        """
        if self.pool is None:
            self.pool = aiopg.create_pool(dsn=self.get_dsn())

        async with self.pool as pool:
            async with pool.acquire() as conn:
                yield conn


@asynccontextmanager
async def get_connection(
        postgresql: Postgresql
) -> Cursor:
    async with postgresql.get_connect() as connection:
        async with (await connection.cursor(cursor_factory=RealDictCursor)) as cur:
            yield cur



