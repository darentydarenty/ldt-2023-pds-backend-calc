import fastapi.routing

from app.internal.constant.usecase import ConstantUseCase


class ConstantHandler:
    __const_uc: ConstantUseCase

    router: fastapi.routing.APIRouter

    def __init__(self, const_uc):
        self.__const_uc = const_uc
        self.router = fastapi.routing.APIRouter(prefix="/constant")

        self.router.add_api_route("/", self.get)

    async def get(self):
        return await self.__const_uc.get_data()
