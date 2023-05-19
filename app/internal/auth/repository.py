from .models import AuthServiceModel

from app.pkg.connectors.postgresql import Postgresql, get_connection, NoResultsException


class AuthRepository:
    def __init__(self, postgresql: Postgresql):
        self.__db = postgresql

    async def get_service_by_public_key(self, public_key: str) -> AuthServiceModel:
        query = """
                    SELECT * FROM service.auth WHERE public_key = $1;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, public_key)
            result = await cur.fetchone()

            if result is None:
                raise NoResultsException

            return AuthServiceModel(**result)

    async def get_service_by_name(self, name: str):
        query = """
                    SELECT * FROM service.auth WHERE name = $1;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, name)
            result = await cur.fetchone()

            if result is None:
                raise NoResultsException

            return AuthServiceModel(**result)
