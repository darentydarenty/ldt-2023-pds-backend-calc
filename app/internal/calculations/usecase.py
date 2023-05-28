import asyncio
import datetime
import uuid

from asgiref.sync import async_to_sync

from .expense_model import ExpensesModel
from .graph_model import GraphsModel
from .insight_model import InsightsModel
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


def convert_report_digest(result: ReportDAO) -> ReportListUnit:
    return ReportListUnit(
        name=result.report_name,
        summary=result.total_expenses,
        time_stamp=result.date_create,
        report_id=result.tracker_id
    )


class CalculationsUseCase:
    _calc_repo: CalculationsRepository
    _model_data: ModelData
    _exp_model: ExpensesModel

    def __init__(self, calc_repo: CalculationsRepository, model_data: ModelData):
        self._calc_repo = calc_repo
        self._model_data = model_data
        self._exp_model = ExpensesModel(model_data)

    async def calculate(self, params: CalculationRequest) -> ReportResult:
        tracker_id = str(uuid.uuid4())
        record_id = await self._calc_repo.insert_record_raw(
            tracker_id=tracker_id,
            report_name=f"Отчёт {(datetime.datetime.now() + datetime.timedelta(hours=3)).strftime('%Y-%m-%d')}",
        )

        indexes_list = await self._calc_repo.insert_company_info(
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
                organization_type=params.company.organization_type,
                workers_quantity=params.company.workers_quantity,
                industry=params.company.industry,
                county=params.company.county,
            )
        )
        indexes_dict = dict(indexes_list)
        company4model = ModelCompanyData(
            **params.company.dict(
                exclude={'machine_names', 'county', 'industry', 'other_needs', 'patent_type'},
            ),
            machine_names=indexes_dict['machine_names'],
            county=indexes_dict['county'],
            industry=indexes_dict['industry'],
            other_needs=indexes_dict['other_needs'],
            patent_type=indexes_dict['patent_type']
        )
        prediction_result = self._exp_model.predict(company4model)

        await asyncio.gather(
            self._calc_repo.update_report(
                                        record_id=record_id,
                                        total_expenses=prediction_result.total_expenses,
                                          ),
            self._calc_repo.insert_estate_expenses(
                EstateExpenses(
                    record_id=record_id,
                    estate_expenses=prediction_result.estate_expenses,
                    land_expenses=prediction_result.land_expenses,
                    building_expenses=prediction_result.building_expenses,
                )
            ),
            self._calc_repo.insert_service_expenses(
                ServiceExpenses(
                    record_id=record_id,
                    service_expenses=prediction_result.service_expenses,
                    duty_expenses=prediction_result.duty_expenses,
                    bookkeeping_expenses=prediction_result.bookkeeping_expenses,
                    patent_expenses=prediction_result.patent_expenses,
                    machine_expenses=prediction_result.machine_expenses,
                )
            ),
            self._calc_repo.insert_staff_expenses(
                StaffExpenses(
                    record_id=record_id,
                    staff_expenses=prediction_result.staff_expenses,
                    salaries_expenses=prediction_result.salaries_expenses,
                    pension_expenses=prediction_result.pension_expenses,
                    medical_expenses=prediction_result.medical_expenses,

                )
            ),
            self._calc_repo.insert_taxes_expanses(
                TaxExpenses(
                    record_id=record_id,
                    tax_expenses=prediction_result.tax_expenses,
                    land_tax=prediction_result.land_tax,
                    estate_tax=prediction_result.estate_tax,
                    income_tax=prediction_result.income_tax,
                )
            )
        )

        return await self.get_report_by_tracker_id(tracker_id)

    async def get_plots(self, tracker_id: str) -> GraphsData:
        companies = await self._calc_repo.get_reports_for_model()
        input_company = await self._calc_repo.get_company_for_model(tracker_id)
        graph_model = GraphsModel(self._model_data, CompaniesData(companies_data=companies))
        return graph_model.make_graphs(input_company)

    async def get_insights(self, tracker_id) -> InsightsData:
        companies = await self._calc_repo.get_reports_for_model()
        input_company = await self._calc_repo.get_company_for_model(tracker_id)
        insight_model = InsightsModel(self._model_data, CompaniesData(companies_data=companies))
        return insight_model.make_insights(input_company)

    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportResult:
        result = await self._calc_repo.get_report_by_tracker_id(tracker_id)

        return convert_report(result)

    async def get_all_reports(self, user_id: int | None = None) -> ReportList:
        result = await self._calc_repo.get_all_reports(user_id)

        report_list = [convert_report_digest(r) for r in result]

        return ReportList(
            results=report_list,
        )
