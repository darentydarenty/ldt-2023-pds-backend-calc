from pydantic import BaseModel


class CompanyData(BaseModel):
    # company_short
    project_name: str
    organization_type: str
    workers_quantity: int
    industry: str
    county: str

    # company_full
    land_area: int
    building_area: int
    machine_names: list
    machine_quantities: list
    patent_type: str
    bookkeeping: int
    tax_system: str
    operations: int
    other_needs: list


class ReportData(BaseModel):
    # result
    record_id: int
    tracker_id: str
    total_expenses: int | None


class CompanyPredict(BaseModel):
    # result
    total_expenses: int
    # staff category
    staff_expenses: int
    salaries_expenses: int
    pension_expenses: int
    medical_expenses: int
    # estate category
    estate_expenses: int
    land_expenses: int
    building_expenses: int
    # taxes category
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



