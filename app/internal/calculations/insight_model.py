from app.internal.calculations.analyzing_model import AnalyzingModel
from .expense_model import ExpensesModel
from .models import *


class InsightsModel(AnalyzingModel):
    """
    Model for making insights about company
    """

    def make_insights(self, company_data: ModelCompanyData) -> InsightsData:
        """Make insights on existing model, it's data and predict"""
        model = ExpensesModel(self.model_constants)
        company_predict = model.predict(company_data).dict()
        # placeholders
        workers_quantity_insight = {'insight': 'EMPTY'}
        usual_expenses_insight = {'insight': 'EMPTY'}
        usual_county_insight = {'insight': 'EMPTY'}
        best_tax_system_insight = {'insight': 'EMPTY'}

        ### Выбор оптимальной налоговой системы
        temp_company_data = company_data.dict()
        best_tax_system = current_tax_system = temp_company_data['tax_system']
        best_total_expenses = current_total_expenses = company_predict['total_expenses']
        for tax_system in [i for i in self.tax_systems if i != current_tax_system]:
            temp_company_data['tax_system'] = tax_system
            total_expenses = model.predict(ModelCompanyData(**temp_company_data)).dict()['total_expenses']
            if total_expenses < best_total_expenses:
                best_total_expenses = total_expenses
                best_tax_system = tax_system
        best_tax_system_insight = {
            'insight': ('Вы используете оптимальную налоговую систему'
                        if best_tax_system == current_tax_system else
                        f'Расходы на налоги с системой {best_tax_system} станут на {current_total_expenses - best_total_expenses} руб. меньше')}

        # check DB len
        if self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']].shape[0] > 0:
            ### Количество сотрудников
            temp_company_data = company_data.dict()
            current_workers_quantity = company_data.dict()['workers_quantity']
            mean_workers_quantity = int(
                self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']][
                    'workers_quantity'].mean())
            workers_quantity_insight = 'EMPTY'
            if mean_workers_quantity < current_workers_quantity:
                workers_quantity_insight = f'В среднем на предприятиях вашей отрасли работает на {int((current_workers_quantity - mean_workers_quantity) / (current_workers_quantity * 0.01))}% сотрудников меньше'
            elif mean_workers_quantity > current_workers_quantity:
                workers_quantity_insight = f'В среднем на предприятиях вашей отрасли работает на {int((mean_workers_quantity - current_workers_quantity) / (current_workers_quantity * 0.01))}% сотрудников больше'
            workers_quantity_insight = {'insight': workers_quantity_insight}

            ### Разницы по фичам staff_expenses, estate_expenses, service_expenses
            usual_expenses_insight = ''
            mean_staff_expenses = int(
                self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']][
                    'staff_expenses'].mean())
            current_staff_expenses = company_predict['staff_expenses']
            if mean_staff_expenses < current_staff_expenses:
                usual_expenses_insight += f'В среднем предприятия вашей отрасли тратят на персонал на {int((current_staff_expenses - mean_staff_expenses) / (current_staff_expenses * 0.01))}% меньше, '
            elif mean_staff_expenses > current_staff_expenses:
                usual_expenses_insight += f'В среднем предприятия вашей отрасли тратят на персонал на {int((mean_staff_expenses - current_staff_expenses) / (current_staff_expenses * 0.01))}% больше, '
            else:
                usual_expenses_insight += 'В среднем предприятия вашей отрасли тратят на персонал столько же, '
            mean_estate_expenses = int(
                self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']][
                    'estate_expenses'].mean())
            current_estate_expenses = company_predict['estate_expenses']
            if mean_estate_expenses < current_estate_expenses:
                usual_expenses_insight += f'на недвижимость на {int((current_estate_expenses - mean_estate_expenses) / (current_estate_expenses * 0.01))}% меньше, '
            elif mean_estate_expenses >= current_estate_expenses:
                usual_expenses_insight += f'на недвижимость на {int((mean_estate_expenses - current_estate_expenses) / (current_estate_expenses * 0.01))}% больше, '
            else:
                usual_expenses_insight += 'на недвижимость столько же, '
            mean_service_expenses = int(
                self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']][
                    'service_expenses'].mean())
            current_service_expenses = company_predict['service_expenses']
            if mean_service_expenses < current_service_expenses:
                print("DEBUG", mean_service_expenses, current_service_expenses)
                usual_expenses_insight += f'а на услуги на {int((current_service_expenses - mean_service_expenses) / (current_service_expenses * 0.01))}% меньше'
            elif mean_service_expenses >= current_service_expenses:
                usual_expenses_insight += f'а на услуги на {int((mean_service_expenses - current_service_expenses) / (current_service_expenses * 0.01))}% больше'
            else:
                usual_expenses_insight += 'а на услуги столько же'
            usual_expenses_insight = {'insight': usual_expenses_insight}

            ### Разницы по округам
            best_counties = self.companies_data_df[self.companies_data_df['industry'] == temp_company_data['industry']][
                'county'].value_counts().to_dict()
            best_counties = sorted(best_counties, key=best_counties.get, reverse=True)[:3]  # top 3
            if len(best_counties) > 0:
                best_counties_price = [self.CountyPrices[i] for i in best_counties]
                current_county = company_data.dict()['county']
                current_county = 'mean' if current_county is None else current_county
                current_county_price = self.CountyPrices[current_county]
                best_county_ind = best_counties_price.index(min(best_counties_price))
                mean_best_counties_price = sum(best_counties_price) / len(best_counties_price)
                if (current_county in best_counties) and (current_county_price < mean_best_counties_price):
                    usual_county_insight = 'Вы выбрали оптимальный административный округ для такого предприятия'
                elif (current_county in best_counties):
                    usual_county_insight = f'Расположение вашего предприятия популярно в отрасли, другим популярным административным округом является {self.CountyID[best_counties[best_county_ind]]}, где стоимость земли меньше на {int((current_county_price - best_counties_price[best_county_ind]) / (current_county_price * 0.01))}%'
                elif (current_county_price < mean_best_counties_price):
                    county_str = ', '.join([self.CountyID[i] for i in best_counties])
                    usual_county_insight = 'Расположение вашего предприятия непопулярно в отрасли, обычно предприятия располагаются в ' + county_str + f', где стоимость земли больше на {int((mean_best_counties_price - current_county_price) / (current_county_price * 0.01))}%'
                else:
                    county_str = ', '.join([self.CountyID[i] for i in best_counties])
                    usual_county_insight = 'Расположение вашего предприятия непопулярно в отрасли, обычно предприятия располагаются в ' + county_str + f', где стоимость земли меньше на {int((current_county_price - mean_best_counties_price) / (current_county_price * 0.01))}%'
                usual_county_insight = {'insight': usual_county_insight}

        output = {
            'usual_expenses_insight': Insight(**usual_expenses_insight),
            'usual_county_insight': Insight(**usual_county_insight),
            'workers_quantity_insight': Insight(**workers_quantity_insight),
            'best_tax_system_insight': Insight(**best_tax_system_insight)
        }
        return InsightsData(**output)
