import numpy as np

from app.internal.calculations.analyzing_model import AnalyzingModel
from .expense_model import ExpensesModel
from .models import *


class GraphsModel(AnalyzingModel):
    """
    Model for making graphs and diagrams about company
    """
    def make_graphs(self, company_data: ModelCompanyData) -> GraphsData:
        """Make graphs about client's company and other companies"""
        model = ExpensesModel(self.model_constants)
        company_predict = model.predict(company_data).dict()
        temp_company_data = company_data.dict()


        ### Распределение расходов
        _staff_exp = np.floor(100*company_predict['staff_expenses']/company_predict['total_expenses'])
        _estate_exp = np.floor(100*company_predict['estate_expenses']/company_predict['total_expenses'])
        _service_exp = np.floor(100*company_predict['service_expenses']/company_predict['total_expenses'])
        _tax_exp = 100-(_staff_exp+_estate_exp+_service_exp)
        expenses_distribution = {
            'labels':['Персонал', 'Недвижимость', 'Налоги', 'Услуги'],
            'datasets':[{'staff_expenses':    _staff_exp},
                        {'estate_expenses':   _estate_exp},
                        {'tax_expenses':      _tax_exp},
                        {'service_expenses':  _service_exp}]}


        ### Распределение типов налоговых систем
        global_tax_systems = self.companies_data_df[self.companies_data_df['industry']==temp_company_data['industry']]['tax_system'].value_counts().to_dict()
        sum_global_tax_systems = sum(global_tax_systems.values())
        pie_dataset = []
        try:
            _usn6_system = np.floor(100*global_tax_systems['УСН6%']/sum_global_tax_systems)
        except KeyError:
            _usn6_system = 0
        try:
            _usn15_system = np.floor(100*global_tax_systems['УСН15%']/sum_global_tax_systems)
        except KeyError:
            _usn15_system = 0
        try:
            _esnh_system = np.floor(100*global_tax_systems['ЕСНХ']/sum_global_tax_systems)
        except KeyError:
            _esnh_system = 0
        try:
            _osn_system = global_tax_systems['ЕСНХ']
            _osn_system = (100-(_usn6_system + _usn15_system + _esnh_system))
        except KeyError:
            _osn_system = 0
        pie_dataset.append({'УСН6%':_usn6_system})
        pie_dataset.append({'УСН15%':_usn15_system})
        pie_dataset.append({'ЕСНХ':_esnh_system})
        pie_dataset.append({'ОСН':_osn_system})
        taxes_distribution = {
            'labels':['ОСН', 'УСН6%', 'УСН15%', 'ЕСНХ'],
            'datasets':pie_dataset}
        if sum_global_tax_systems==0:
          taxes_distribution = {
            'labels':   ['EMPTY'],
            'datasets': [{'EMPTY':0}]}

        ### График популярности индустрии
        months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        if self.popularity_matrix.shape != (1,1) or temp_company_data["industry"] is not None:
            most_popular = self.popularity_matrix.sum(axis=1)
            most_popular_idx = np.argsort(most_popular)[::-1][:3].tolist()
            line_dataset = [{self.IndustryID[i]: self.popularity_matrix[i].tolist()[1:]} for i in most_popular_idx if i>0 and i!=temp_company_data['industry']]
            line_dataset.append({'Ваша отрасль: '+self.IndustryID[temp_company_data['industry']]:  self.popularity_matrix[temp_company_data['industry']].tolist()[1:]})
            popularity_chart = {
                'labels':   list(months.values())[:self.popularity_matrix.shape[1]-1],
                'datasets': line_dataset }
        else:
            popularity_chart = {
                'labels':   ['EMPTY'],
                'datasets': [{'EMPTY':[]}]}

        output = {
            'expenses_distribution': PiePlotGraph(**expenses_distribution),
            'taxes_distribution': PiePlotGraph(**taxes_distribution),
            'popularity_chart': LinePlotGraph(**popularity_chart)
        }
        return GraphsData(**output)
