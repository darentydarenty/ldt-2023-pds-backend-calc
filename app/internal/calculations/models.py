import datetime

from pydantic import BaseModel


ReportDAOKeys = [ 'tracker_id', 'total_expenses', 'date_create', 'report_name', 'salaries_expenses', 'staff_expenses',
                  'pension_expenses', 'medical_expenses', 'estate_tax', 'land_tax', 'tax_expenses', 'income_tax',
                  'service_expenses', 'duty_expenses', 'bookkeeping_expenses', 'patent_expenses', 'machine_expenses',
                  'estate_expenses', 'land_expenses', 'building_expenses', 'land_area', 'building_area',
                  'machine_names', 'machine_quantities', 'patent_type', 'bookkeeping', 'tax_system',
                  'operations', 'other_needs', 'project_name', 'industry', 'organization_type', 'workers_quantity', 'county' ]


class ReportData(BaseModel):
    # result
    record_id: int
    tracker_id: str
    total_expenses: int | None


class CompanyData(BaseModel):
    # company_short
    project_name: str | None
    organization_type: str | None
    workers_quantity: int | None
    industry: str | None
    county: str | None

    # company_full
    land_area: int | None
    building_area: int | None
    machine_names: list[str] | None
    machine_quantities: list[int] | None
    patent_type: str | None
    bookkeeping: bool | None
    tax_system: str | None
    operations: int | None
    other_needs: list[str] | None


class ModelCompanyData(BaseModel):
    # company_short
    project_name: str | None
    organization_type: str | None
    workers_quantity: int | None
    industry: int | None
    county: int | None

    # company_full
    land_area: int | None
    building_area: int | None
    machine_names: list[int] | None
    machine_quantities: list[int] | None
    patent_type: int | None
    bookkeeping: int | None
    tax_system: str | None
    operations: int | None
    other_needs: list[int] | None


class StaffExpenses(BaseModel):
    record_id: int

    staff_expenses: int
    salaries_expenses: int
    pension_expenses: int
    medical_expenses: int


class EstateExpenses(BaseModel):
    record_id: int

    estate_expenses: int
    land_expenses: int
    building_expenses: int


class TaxExpenses(BaseModel):
    record_id: int

    tax_expenses: int
    land_tax: int
    estate_tax: int
    income_tax: int


class ServiceExpenses(BaseModel):
    record_id: int

    service_expenses: int
    duty_expenses: int
    bookkeeping_expenses: int
    patent_expenses: int
    machine_expenses: int


class CompanyPredict(BaseModel):
    # result
    total_expenses: int
    # staff
    staff_expenses: int
    salaries_expenses: int
    pension_expenses: int
    medical_expenses: int
    # estate
    estate_expenses: int
    land_expenses: int
    building_expenses: int
    # taxes
    tax_expenses: int
    land_tax: int
    estate_tax: int
    income_tax: int
    # services
    service_expenses: int
    duty_expenses: int
    bookkeeping_expenses: int
    patent_expenses: int
    machine_expenses: int


"""
Categories to load in DB
"""


class ServiceCategory(BaseModel):
    service_expenses: int
    duty_expenses: int
    bookkeeping_expenses: int
    patent_expenses: int
    machine_expenses: int


class TaxCategory(BaseModel):
    tax_expenses: int
    land_tax: int
    estate_tax: int
    income_tax: int


class EstateCategory(BaseModel):
    estate_expenses: int
    land_expenses: int
    building_expenses: int


class StaffCategory(BaseModel):
    staff_expenses: int
    salaries_expenses: int
    pension_expenses: int
    medical_expenses: int


"""
Data for report
"""


class OutputData(BaseModel):
    service: ServiceCategory
    estate: EstateCategory
    staff: StaffCategory
    tax: TaxCategory


class ReportResult(BaseModel):
    tracker_id: str
    total_expenses: int
    output: OutputData
    input: CompanyData


class CalculationRequest(BaseModel):
    user_id: int | None
    company: CompanyData


class CompanyShortDAO(BaseModel):
    record_id: int

    user_id: int | None

    project_name: str | None
    organization_type: str | None
    workers_quantity: int | None
    industry: str | None
    county: str | None


class CompanyFullDAO(BaseModel):
    record_id: int

    land_area: int | None
    building_area: int | None
    machine_names: list | None
    machine_quantities: list | None
    patent_type: str | None
    bookkeeping: bool | None
    tax_system: str | None
    operations: int | None
    other_needs: list | None


class ReportDAO(BaseModel):
    # base
    tracker_id: str
    total_expenses: int
    date_create: datetime.datetime
    report_name: str

    # staff
    salaries_expenses: int
    staff_expenses: int
    pension_expenses: int
    medical_expenses: int

    # taxes
    estate_tax: int
    land_tax: int
    tax_expenses: int
    income_tax: int

    # services
    service_expenses: int
    duty_expenses: int
    bookkeeping_expenses: int
    patent_expenses: int
    machine_expenses: int

    # estate
    estate_expenses: int
    land_expenses: int
    building_expenses: int

    # company full
    land_area: int | None
    building_area: int | None
    machine_names: list[str] | None
    machine_quantities: list[int] | None
    patent_name: str | None
    bookkeeping: bool | None
    tax_system: str | None
    operations: int | None
    other_needs: list[str] | None

    # company short
    project_name: str | None
    industry: str | None
    organization_type: str | None
    workers_quantity: int | None
    county: str | None



class ReportByTrackerCmd(BaseModel):
    tracker_id: str


class ReportListUnit(BaseModel):
    name: str
    summary: int
    time_stamp: datetime.datetime
    report_id: str


class ReportList(BaseModel):
    results: list[ReportListUnit]


"""dataClasses for graphs"""
# Types describing graphs


class PiePlotGraph(BaseModel):
    labels: list[str]
    datasets: list[dict]


class LinePlotGraph(BaseModel):
    labels: list[str]
    datasets: list[dict]
# Fixed structure with needed output graphs


class GraphsData(BaseModel):
    expenses_distribution: PiePlotGraph
    taxes_distribution: PiePlotGraph
    popularity_chart: LinePlotGraph


"""Структура гипотезы, только строка потому что больше нечего впихнуть"""
# Type with insight


class Insight(BaseModel):
    insight: str


"""Выходные типы данных для обоих моделей"""
# Fixed structure with needed insights


class InsightsData(BaseModel):
    usual_expenses_insight: Insight
    usual_county_insight: Insight
    workers_quantity_insight: Insight
    best_tax_system_insight: Insight


class ModelReportDAO(BaseModel):
    # result
    tracker_id: str
    total_expenses: int
    date_create: datetime.datetime
    report_name: str
    # staff
    salaries_expenses: int
    staff_expenses: int
    pension_expenses: int
    medical_expenses: int
    # taxes
    estate_tax: int
    land_tax: int
    tax_expenses: int
    income_tax: int
    # services
    service_expenses: int
    duty_expenses: int
    bookkeeping_expenses: int
    patent_expenses: int
    machine_expenses: int
    # estate
    estate_expenses: int
    land_expenses: int
    building_expenses: int
    # company full
    land_area: int | None
    building_area: int | None
    machine_names: list[int] | None
    machine_quantities: list[int] | None
    patent_type: int | None
    bookkeeping: bool | None
    tax_system: str | None
    operations: int | None
    other_needs: list[int] | None
    # company short
    project_name: str | None
    industry: int | None
    organization_type: str | None
    workers_quantity: int | None
    county: int | None


class CompaniesData(BaseModel):
    companies_data: list[ModelReportDAO]
