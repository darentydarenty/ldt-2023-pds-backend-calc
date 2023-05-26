from asgiref.sync import async_to_sync

from .expense_model import ExpensesModel
from .repository import CalculationsRepository
from .models import *

from app.internal.constant.models import *


def convert_report(result: ReportDAO) -> ReportResult:
    return ReportResult(
        tracker_id=result.tracker_id,
        total_expenses=result.total_expenses,
        input_data=CompanyData(
            project_name=result.project_name,
            organization_type=result.organization_type,
            workers_quantity=result.workers_quantity,
            industry=result.industry,
            county=result.county,

            land_area=result.land_area,
            building_area=result.building_area,
            machine_names=result.machine_names,
            machine_quantities=result.machine_quantities,
            patent_type=result.patent_type,
            bookkeeping=result.bookkeeping,
            tax_system=result.tax_system,
            operations=result.operations,
            other_needs=result.other_needs

        ),
        output_data=OutputData(
            service=ServiceCategory(
                service_expenses=result.service_expenses,
                duty_expenses=result.duty_expenses,
                bookkeeping_expenses=result.bookkeeping_expenses,
                patent_expenses=result.patent_expenses,
                machine_expenses=result.machine_expenses,
            ),
            estate=EstateCategory(
                estate_expenses=result.estate_expenses,
                land_expenses=result.land_expenses,
                building_expenses=result.building_expenses,
            ),
            staff=StaffCategory(
                staff_expenses=result.staff_expenses,
                salaries_expenses=result.salaries_expenses,
                pension_expenses=result.pension_expenses,
                medical_expenses=result.medical_expenses
            ),
            tax=TaxCategory(
                tax_expesnses=result.tax_expenses,
                land_tax=result.land_tax,
                estate_tax=result.estate_tax,
                income_tax=result.income_tax
            )
        )
    )


class CalculationsUseCase:
    _calc_repo: CalculationsRepository
    _exp_model: ExpensesModel

    def __init__(self, calc_repo: CalculationsRepository, model_data: ModelData):
        self._calc_repo = calc_repo
        self._exp_model = ExpensesModel(model_data)

    def calculate(self):
        pass

    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportResult:
        result = await self._calc_repo.get_report_by_tracker_id(tracker_id)

        return convert_report(result)

    async def get_all_reports(self) -> list[ReportDAO]:
        return await self._calc_repo.get_all_reports()
