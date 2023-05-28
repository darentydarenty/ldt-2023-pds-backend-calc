import numpy as np

from app.internal.calculations.models import CompanyPredict, ModelCompanyData
from app.internal.constant.models import ModelData


class ExpensesModel:
    """
    Model for estimating necessary investments
    """

    def __init__(self, ModelConstants: ModelData) -> None:
        """Constructor"""
        self.duty_charge = {'ООО': 4000, 'ИП': 800}  # пошлина
        self.pred_duration = 12  # длительность предсказания в месяцах
        self.pension_coeff = 0.22
        self.medical_coeff = 0.051
        self.land_coeff = 0.015
        self.building_coeff = 0.02
        self.income_coeff = 0.13
        self.building_cost = 80000
        self.needs_full_cost = 40000

        self.update_db(ModelConstants)

    def update_db(self, ModelConstants: ModelData) -> None:
        """Update object tables with coeffs"""
        dictionary = ModelConstants.dict()
        self.MeanSalaries = {item['industry_id']: item.pop('salary') for item in dictionary['mean_salaries']}
        self.CountyPrices = {item['county_id']: item.pop('county_price') for item in dictionary['county_prices']}
        self.MachinePrices = {item['machine_id']: item.pop('machine_price') for item in dictionary['machine_prices']}
        self.NeedsCoeffs = {item['need_id']: item.pop('need_coeff') for item in dictionary['other_needs']}
        self.PatentPrices = {item['patent_id']: item.pop('patent_price') for item in dictionary['patent_prices']}

        self.IndustryID = {item['industry_id']: item.pop('industry_name') for item in dictionary['mean_salaries']}
        self.PatentID = {item['patent_id']: item.pop('patent_name') for item in dictionary['patent_prices']}

        land_costs = list(self.CountyPrices.values())
        try:
            self.CountyPrices['mean'] = np.round(sum(land_costs) / len(land_costs), 2)
        except ZeroDivisionError:
            self.CountyPrices['mean'] = 0
        machine_costs = list(self.MachinePrices.values())
        try:
            self.MachinePrices['mean'] = int(sum(machine_costs) / len(machine_costs))
        except ZeroDivisionError:
            self.MachinePrices['mean'] = 0

    def _bookkeeping_formula(self, employees, operations, tax_system):
        mul_coeff = {
            'УСН6%': 3000000,
            'УСН15%': 4300000,
            'ОСН': 9000000,
            'ЕСНХ': 4300000
        }
        add_coeff = {
            'УСН6%': 1000,
            'УСН15%': 2000,
            'ОСН': 4000,
            'ЕСНХ': 2000
        }
        return employees * 500 + np.sqrt(operations * mul_coeff[tax_system]) + add_coeff[tax_system]

    def _check_dictionary(self, data):
        def _check_additive_value(value):
            if value is None:
                return 0
            return value

        def _check_multiplicative_value(value):
            if value is None:
                return 1
            return value

        def _check_machines(data):
            if data['machine_names'] is None and data['machine_quantities'] is None:
                data['machine_names'] = []
                data['machine_quantities'] = []
            if data['machine_names'] is None:
                data['machine_names'] = [None] * len(data['machine_quantities'])
            if data['machine_quantities'] is None:
                data['machine_quantities'] = [None] * len(data['machine_names'])
            return data

        data = _check_machines(data)
        data['organization_type'] = 'ООО' if data['organization_type'] is None else data['organization_type']
        data['workers_quantity'] = _check_additive_value(data['workers_quantity'])
        data['industry'] = list(self.IndustryID.keys())[list(self.IndustryID.values()).index(26)] if data['industry'] is None else data['industry']
        data['county'] = 'mean' if data['county'] is None else data['county']
        data['land_area'] = _check_additive_value(data['land_area'])
        data['building_area'] = _check_additive_value(data['building_area'])
        data['machine_names'] = [('mean' if machine is None else machine) for machine in data['machine_names']]
        data['machine_quantities'] = [(0 if value is None else value) for value in data['machine_quantities']]
        data['patent_type'] = list(self.PatentID.keys())[list(self.PatentID.values()).index('Без патента')] if data[
                                                                                                                   'patent_type'] is None else \
        data['patent_type']
        data['bookkeeping'] = _check_additive_value(data['bookkeeping'])
        data['tax_system'] = 'ОСН' if data['tax_system'] is None else data['tax_system']
        data['operations'] = _check_additive_value(data['operations'])
        data['other_needs'] = [] if data['other_needs'] is None else data['other_needs']
        return data

    def predict_dict(self, company_data: dict) -> dict:
        """Get prediction with detalization"""
        company_data = self._check_dictionary(company_data)
        DutyCharge = self.duty_charge[company_data['organization_type']]
        Salaries = self.MeanSalaries[company_data['industry']] * company_data['workers_quantity'] * self.pred_duration
        PensionExpenses = Salaries * self.pension_coeff
        MedicalExpenses = Salaries * self.medical_coeff
        LandExpenses = self.CountyPrices[company_data['county']] * company_data['land_area']
        MachinePrices = np.array([self.MachinePrices[MachineName] for MachineName in company_data['machine_names']])
        MachinesExpenses = sum(MachinePrices * np.array(company_data['machine_quantities']))
        OtherNeedsCoeffs = [self.NeedsCoeffs[NeedName] for NeedName in company_data['other_needs']]
        BuildingExpenses = (self.building_cost + self.needs_full_cost * sum(OtherNeedsCoeffs)) * company_data[
            'building_area']
        PatentExpenses = self.PatentPrices[company_data['patent_type']]
        BookKeepingExpenses = self.pred_duration * self._bookkeeping_formula(company_data['workers_quantity'],
                                                                             company_data['operations'],
                                                                             company_data['tax_system']) if \
        company_data['bookkeeping'] else 0
        LandTax = LandExpenses * self.land_coeff if company_data['tax_system'] != 'ЕСНХ' else 0
        BuildingTax = BuildingExpenses * self.building_coeff
        IncomeTax = Salaries * self.income_coeff if company_data['tax_system'] == 'ОСН' or company_data[
            'tax_system'] == 'ЕСНХ' else 0

        PersonnelExpenses = Salaries + PensionExpenses + MedicalExpenses
        RealtyExpenses = LandExpenses + BuildingExpenses
        TaxExpenses = LandTax + BuildingTax + IncomeTax
        ServiceExpenses = DutyCharge + BookKeepingExpenses + PatentExpenses + MachinesExpenses

        TotalExpenses = PersonnelExpenses + RealtyExpenses + TaxExpenses + ServiceExpenses

        output = {
            'total_expenses': int(TotalExpenses),
            'staff_expenses': int(PersonnelExpenses),
            'estate_expenses': int(RealtyExpenses),
            'tax_expenses': int(TaxExpenses),
            'service_expenses': int(ServiceExpenses),
            'salaries_expenses': int(Salaries),
            'pension_expenses': int(PensionExpenses),
            'medical_expenses': int(MedicalExpenses),
            'land_expenses': int(LandExpenses),
            'building_expenses': int(BuildingExpenses),
            'land_tax': int(LandTax),
            'estate_tax': int(BuildingTax),
            'income_tax': int(IncomeTax),
            'duty_expenses': int(DutyCharge),
            'bookkeeping_expenses': int(BookKeepingExpenses),
            'patent_expenses': int(PatentExpenses),
            'machine_expenses': int(MachinesExpenses)
        }
        return output

    def predict(self, company_data: ModelCompanyData) -> CompanyPredict:
        tmp_dict = company_data.dict()
        return CompanyPredict(**self.predict_dict(tmp_dict))
