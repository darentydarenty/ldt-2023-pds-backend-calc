from pydantic import BaseModel


class ReportData(BaseModel):
    # result
    record_id: int
    tracker_id: str
    total_expenses: int | None


class CompanyData(BaseModel):
    # company_short
    project_name: str
    organization_type: str
    workers_quantity: int
    industry: int
    county: int

    # company_full
    land_area: int
    building_area: int
    machine_names: list
    machine_quantities: list
    patent_type: int
    bookkeeping: int
    tax_system: str
    operations: int
    other_needs: list

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

class MachinePricesDAO(BaseModel):
    machine_id:    int
    machine_name:  str
    machine_price: int


class MeanSalariesDAO(BaseModel):
    industry_id:   int
    industry_name: str
    salary:        int


class OtherNeedsDAO(BaseModel):
    need_id:    int
    need_name:  str
    need_coeff: float


class PatentPricesDAO(BaseModel):
    patent_id:    int
    patent_name:  str
    patent_price: float


class CountyPricesDAO(BaseModel):
    county_id:    int
    county_name:  str
    county_price: float


class ModelData(BaseModel):
    machine_prices: list[MachinePricesDAO]
    mean_salaries:  list[MeanSalariesDAO]
    other_needs:    list[OtherNeedsDAO]
    patent_prices:  list[PatentPricesDAO]
    county_prices:  list[CountyPricesDAO]


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



