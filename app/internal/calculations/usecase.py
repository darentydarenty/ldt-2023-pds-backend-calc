from asgiref.sync import async_to_sync

from .expense_model import ExpensesModel
from .repository import CalculationsRepository
from .models import *

from app.internal.constant.models import *


class CalculationsUseCase:
    _calc_repo: CalculationsRepository
    _exp_model: ExpensesModel

    def __init__(self, calc_repo: CalculationsRepository, model_data: ModelData):
        self._calc_repo = calc_repo
        self._exp_model = ExpensesModel(model_data)

    def calculate(self):
        pass

    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportDAO:
        return await self._calc_repo.get_report_by_tracker_id(tracker_id)

    async def get_all_reports(self) -> list[ReportDAO]:
        return await self._calc_repo.get_all_reports()
