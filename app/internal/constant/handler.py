import asyncio

import fastapi.routing

from app.internal.constant.usecase import ConstantUseCase


class ConstantHandler:
    __const_uc: ConstantUseCase

    router: fastapi.routing.APIRouter

    def __init__(self, const_uc):
        self.__const_uc = const_uc
        self.router = fastapi.routing.APIRouter(prefix="/constant")

        self.router.add_api_route("/", self.get)
        self.router.add_api_route("/industries", self.get_industries)
        self.router.add_api_route("/fields", self.get_fields)

    async def get(self):
        return await self.__const_uc._async_get_data()

    async def get_industries(self):

        return await self.__const_uc.get_industries()

    async def get_fields(self):
        return await self.__const_uc.get_fields()
