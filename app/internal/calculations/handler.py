import fastapi.routing

from .usecase import CalculationsUseCase
from .models import *


class CalculationsHandler:
    router: fastapi.routing.APIRouter
    _calc_uc: CalculationsUseCase

    def __init__(self, calc_uc: CalculationsUseCase):
        self._calc_uc = calc_uc
        self.router = fastapi.routing.APIRouter(prefix="/calc")

        self.router.add_api_route("/info",
                                  self.get_report_by_tracker_id,
                                  methods=["GET"])

    async def get_report_by_tracker_id(self, tracker_id: str):
        result = await self._calc_uc.get_report_by_tracker_id(tracker_id)
        print(result)
        return result


