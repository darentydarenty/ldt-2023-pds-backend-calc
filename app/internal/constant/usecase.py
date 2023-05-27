import asyncio
import functools

from asgiref.sync import async_to_sync

from .repository import ConstantRepository
from .models import *


class ConstantUseCase:
    _data: ModelData | None

    __const_repo: ConstantRepository

    def __init__(self, const_repo: ConstantRepository):
        self.__const_repo = const_repo
        self._data = None

    async def load(self):

        result = await self.__const_repo.get_data()

        self._data = ModelData(
            county_prices=result[0],
            machine_prices=result[1],
            mean_salaries=result[2],
            other_needs=result[3],
            patent_prices=result[4]
        )

    async def _async_get_data(self) -> ModelData:
        result = await self.__const_repo.get_data()
        self._data = ModelData(
            county_prices=result[0],
            machine_prices=result[1],
            mean_salaries=result[2],
            other_needs=result[3],
            patent_prices=result[4]
        )
        return self._data

    async def get_industries(self) -> IndustriesResponse:
        result = await self.__const_repo.get_industries()

        return IndustriesResponse(
            industries=result
        )

    async def get_fields(self):
        result = await self.__const_repo.get_fields()
        return {
            "data": result
        }

    def get_data(self) -> ModelData:
        return self._data