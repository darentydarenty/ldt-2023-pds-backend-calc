import fastapi.routing

from app.internal.constant.usecase import ConstantUseCase

router = fastapi.routing.APIRouter(prefix="/constant")


class ConstantHandler:
    __const_uc: ConstantUseCase

    def __init__(self, const_uc):
        self.__const_uc = const_uc
        router.add_api_route("/", self.get)

    async def get(self):
        return self.__const_uc.get_data().json()
