from pydantic import BaseModel


class ReportData(BaseModel):
    # result
    record_id: int
    tracker_id: str
    total_expenses: int | None


class CompanyData(BaseModel):
    # company_short
    project_name:       str | None
    organization_type:  str | None
    workers_quantity:   int | None
    industry:           int | None
    county:             int | None

    # company_full
    land_area:          int | None
    building_area:      int | None
    machine_names:      list | None
    machine_quantities: list | None
    patent_type:        int | None
    bookkeeping:        int | None
    tax_system:         str | None
    operations:         int | None
    other_needs:        list | None


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


class InputData(BaseModel):
    __root__: CompanyData


class ReportResult(BaseModel):
    tracker_id: str
    total_expenses: int
    output: OutputData
    input: InputData


class ReportDAO(BaseModel):

    # base
    tracker_id: str
    total_expenses: int
    date_create: str
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
    patent_type: str | None
    bookkeeping: bool | None
    tax_system: str | None
    operations: int | None
    other_needs: list[str] | None

    # company short
    project_name: str | None
    industry: str | None
    organization_type: str | None
    workers_quantity: int
    county: str | None


class ReportByTrackerCmd(BaseModel):
    tracker_id: str