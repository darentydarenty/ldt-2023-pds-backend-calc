import asyncio
import functools

from asgiref.sync import async_to_sync

from app.pkg.connectors.postgresql import Postgresql, get_connection

from .models import *


class ConstantRepository:
    def __init__(self, postgresql: Postgresql):
        self.__db = postgresql

    async def get_data(self) -> list:
        queries = {
            """
            SELECT * FROM constant.county_prices;
            """: CountyPricesDAO,
            """
            SELECT * FROM constant.machine_prices;
            """: MachinePricesDAO,
            """
            SELECT * FROM constant.mean_salaries;
            """: MeanSalariesDAO,
            """
            SELECT * FROM constant.other_needs;
            """: OtherNeedsDAO,
            """
            SELECT * FROM constant.patent_prices;
            """: PatentPricesDAO
        }
        result = []
        async with get_connection(self.__db) as cur:
            for query, model in queries.items():
                await cur.execute(query)
                data = await cur.fetchall()
                result += [[model(**r) for r in data]]

        return result

    async def get_fields(self) -> dict[str, list[str]]:
        queries = {
            """
            SELECT machine_name FROM constant.machine_prices;
            """: ["machine_name", "machines"],
            """
            SELECT industry_name FROM constant.mean_salaries;
            """: ["industry_name", "industries"],
            """
            SELECT need_name FROM constant.other_needs;
            """: ["need_name", "needs"],
            """
            SELECT patent_name FROM constant.patent_prices;
            """: ["patent_name", "patents"],
        }
        result = {}
        async with get_connection(self.__db) as cur:
            for query, key in queries.items():
                await cur.execute(query)
                data = await cur.fetchall()
                result[key[1]] = [v[key[0]] for v in data]

            return result

    async def get_industries(self) -> list[str]:
        query = """
                SELECT industry_name FROM constant.mean_salaries;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            data = await cur.fetchall()

            return [r["industry_name"] for r in data]

    async def get_county_prices(self) -> list[CountyPricesDAO]:
        query = """
                SELECT * FROM constant.county_prices;
                """
        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            result = await cur.fetchall()

            return [CountyPricesDAO(**r) for r in result]

    async def get_machine_prices(self) -> list[MachinePricesDAO]:
        query = """
                SELECT * FROM constant.machine_prices;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            result = await cur.fetchall()

            return [MachinePricesDAO(**r) for r in result]

    async def get_mean_salaries(self) -> list[MeanSalariesDAO]:
        query = """
                SELECT * FROM constant.mean_salaries;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            result = await cur.fetchall()

            return [MeanSalariesDAO(**r) for r in result]

    async def get_other_needs(self) -> list[OtherNeedsDAO]:
        query = """
                                SELECT * FROM constant.other_needs;
                                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            result = await cur.fetchall()

            return [OtherNeedsDAO(**r) for r in result]

    async def get_patent_prices(self) -> list[PatentPricesDAO]:
        query = """
                                SELECT * FROM constant.patent_prices;
                                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            result = await cur.fetchall()

            return [PatentPricesDAO(**r) for r in result]
