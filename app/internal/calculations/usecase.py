import datetime
import uuid

from asgiref.sync import async_to_sync

from .expense_model import ExpensesModel
from .repository import CalculationsRepository
from .models import *

from app.internal.constant.models import *


def convert_report(result: ReportDAO) -> ReportResult:
    return ReportResult(
        tracker_id=result.tracker_id,
        total_expenses=result.total_expenses,
        input=CompanyData(
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
        output=OutputData(
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
                tax_expenses=result.tax_expenses,
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

    async def calculate(self, params: CalculationRequest):
        tracker_id = str(uuid.uuid4())
        record_id = await self._calc_repo.insert_record_raw(
            tracker_id=tracker_id,
            report_name=f"Отчёт {datetime.datetime.now().strftime('YYYY-MM-ddTHH:mm:ss')}",
        )

        await self._calc_repo.insert_company_info(
            company_full=CompanyFullDAO(
                record_id=record_id,

                land_area=params.company.land_area,
                building_area=params.company.building_area,
                machine_names=params.company.machine_names,
                machine_quantities=params.company.machine_quantities,
                patent_type=params.company.patent_type,
                bookkeeping=params.company.bookkeeping,
                tax_system=params.company.tax_system,
                operations=params.company.operations,
                other_needs=params.company.other_needs,
            ),
            company_short=CompanyShortDAO(
                record_id=record_id,
                user_id=params.user_id,

                project_name=params.company.project_name,
                organisation_type=params.company.organization_type,
                workers_quantity=params.company.workers_quantity,
                industry=params.company.industry,
                county=params.company.county,
            )
        )




    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportResult:
        result = await self._calc_repo.get_report_by_tracker_id(tracker_id)

        return convert_report(result)

    async def get_all_reports(self, user_id: int | None = None) -> list[ReportResult]:
        result = await self._calc_repo.get_all_reports(user_id)

        return [convert_report(r) for r in result]
