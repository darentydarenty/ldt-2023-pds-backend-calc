import asyncio

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
        self.router.add_api_route("/all",
                                  self.get_all_reports,
                                  methods=["GET"])
        self.router.add_api_route("/create",
                                  self.make_calculation,
                                  methods=["POST"])

    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportResult:
        return await self._calc_uc.get_report_by_tracker_id(tracker_id)

    async def get_all_reports(self, user_id: int | None) -> list[ReportResult]:
        return await self._calc_uc.get_all_reports(user_id)

    async def make_calculation(self, params: CalculationRequest):
        return await self._calc_uc.calculate(params)

