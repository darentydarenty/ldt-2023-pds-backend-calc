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

    async def update_constant(self, params: UpdateConstantUnit):
        queries = {
            "county_prices": """
            UPDATE constant.county_prices SET county_price = %s WHERE county_name = %s;
                    """,
            "machine_prices": """
            UPDATE constant.machine_prices SET machine_price = %s WHERE machine_name = %s;
                    """,
            "mean_salaries": """
            UPDATE constant.mean_salaries SET salary = %s WHERE industry_name = %s;
                    """,
            "other_needs": """
            UPDATE constant.other_needs SET need_coeff = %s WHERE need_name = %s;
                    """,
            "patent_prices": """
            UPDATE constant.patent_prices SET patent_price = %s WHERE patent_name = %s;
                    """
        }

        async with get_connection(self.__db) as cur:
            await cur.execute(queries[params.category], (params.value, params.name))

    async def insert_constant(self, params: UpdateConstantUnit):
        queries = {
            "county_prices": """
            INSERT INTO constant.county_prices(county_name, county_price) VALUES (%s, %s);
            """,
            "machine_prices": """
            INSERT INTO constant.machine_prices(machine_name, machine_price) VALUES (%s, %s);
            """,
            "mean_salaries": """
            INSERT INTO constant.mean_salaries(industry_name, salary) VALUES (%s, %s);
            """,
            "other_needs": """
            INSERT INTO constant.other_needs(need_name, need_coeff) VALUES (%s, %s);
            """,
            "patent_prices": """
            INSERT INTO constant.patent_prices(patent_name, patent_price) VALUES (%s, %s);
            """
        }
        async with get_connection(self.__db) as cur:
            await cur.execute(queries[params.category], (params.name, params.value))

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
