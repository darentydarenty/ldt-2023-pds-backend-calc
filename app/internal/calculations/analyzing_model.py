import numpy as np
import pandas as pd

from .models import *
from ..constant.models import ModelData


class AnalyzingModel:
    """
    Model for defining general functionality of analitical models
    """

    def __init__(self, model_constants: ModelData, companies_data: CompaniesData) -> None:
        """Constructor"""
        self.tax_systems = ['ОСН', 'УСН6%', 'УСН15%', 'ЕСНХ']
        self.update_db(model_constants, companies_data)

    def update_db(self, model_constants: ModelData, companies_data: CompaniesData) -> None:
        """Update all tables (constant + calcs)"""
        self.model_constants = model_constants
        self.update_constants(model_constants=model_constants)
        self.update_companies(companies_data=companies_data)

    def update_constants(self, model_constants: ModelData) -> None:
        """Update tables with model data (constants)"""
        dictionary = model_constants.dict()
        self.MeanSalaries = {item['industry_id']: item.pop('salary') for item in dictionary['mean_salaries']}
        self.CountyPrices = {item['county_id']: item.pop('county_price') for item in dictionary['county_prices']}
        self.MachinePrices = {item['machine_id']: item.pop('machine_price') for item in dictionary['machine_prices']}
        self.NeedsCoeffs = {item['need_id']: item.pop('need_coeff') for item in dictionary['other_needs']}
        self.PatentPrices = {item['patent_id']: item.pop('patent_price') for item in dictionary['patent_prices']}

        self.CountyID = {item['county_id']: item.pop('county_name') for item in dictionary['county_prices']}
        self.IndustryID = {item['industry_id']: item.pop('industry_name') for item in dictionary['mean_salaries']}

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

    def update_companies(self, companies_data: CompaniesData) -> None:
        """Update tables with companies data (calcs)"""
        self.companies_data_df = pd.DataFrame.from_dict(companies_data.dict()['companies_data'])

        if self.companies_data_df.shape[0] == 0:
            self.companies_data_df = pd.DataFrame(columns=ReportDAOKeys)
        try:
            self.companies_data_df['month'] = self.companies_data_df['date_create'].dt.month
            max_industry = self.companies_data_df['industry'].max()
            max_month = self.companies_data_df['month'].max()
            popularity_items = self.companies_data_df[
                (self.companies_data_df['date_create'].dt.year == self.companies_data_df['date_create'].dt.year.max())][
                ['industry', 'month']].value_counts(sort=False).to_dict().items()
            self.popularity_matrix = np.zeros(shape=(max_industry + 1, max_month + 1))
            for (ind, value) in popularity_items:
                self.popularity_matrix[ind] = value
        except AttributeError:
            self.popularity_matrix = np.zeros(shape=(1, 1))
