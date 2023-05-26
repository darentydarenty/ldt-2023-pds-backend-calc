from pydantic import BaseModel


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


class IndustriesResponse(BaseModel):
    industries: list[str]

