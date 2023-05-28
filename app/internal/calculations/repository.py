from .models import *

from app.internal.calculations.models import ReportDAO, ReportByTrackerCmd
from app.pkg.connectors import Postgresql
from app.pkg.connectors.postgresql import get_connection


class CalculationsRepository:
    def __init__(self, postgresql: Postgresql):
        self.__db = postgresql
        self.get_connection = get_connection

    async def get_report_by_tracker_id(self, tracker_id: str) -> ReportDAO:
        query = """
                SELECT
                    
                    res.tracker_id,
                    res.total_expenses, res.date_create, res.report_name,
                    
                    st.salaries_expenses, st.medical_expenses, st.pension_expenses, st.staff_expenses,
                    
                    e.building_expenses, e.estate_expenses, e.land_expenses,
                    
                    s.bookkeeping_expenses, s.duty_expenses, s.machine_expenses, s.patent_expenses, s.service_expenses,
                    
                    t.estate_tax, t.income_tax, t.land_tax, t.tax_expenses,
                    array(
                        SELECT
                            need_name
                        FROM
                            constant.other_needs ion
                        WHERE
                           ion.need_id =  ANY(cf.other_needs)
                    ) as other_needs,
                     
                     cf.bookkeeping, cf.building_area, cf.land_area, array(
                        SELECT
                            machine_name
                        FROM
                            constant.machine_prices imp
                        WHERE imp.machine_id = ANY(cf.machine_names)
                    ) as machine_names,
                    cf.machine_quantities, cf.operations, pp.patent_name as patent_type, cf.tax_system,
                    
                   cp.county_name as county, ms.industry_name as industry,
                   cs.organization_type, cs.project_name, cs.workers_quantity
                FROM
                    calcs.result res
                    
                LEFT JOIN calcs.estate e on res.record_id = e.record_id
                LEFT JOIN calcs.company_full cf on res.record_id = cf.record_id
                LEFT JOIN calcs.company_short cs on res.record_id = cs.record_id
                LEFT JOIN calcs.services s on res.record_id = s.record_id
                LEFT JOIN calcs.staff st on res.record_id = st.record_id
                LEFT JOIN calcs.taxes t on res.record_id = t.record_id


                LEFT JOIN constant.county_prices cp ON cs.county = cp.county_id
                LEFT JOIN constant.mean_salaries ms ON cs.industry = ms.industry_id
                LEFT JOIN constant.patent_prices pp ON cf.patent_type = pp.patent_id
                
                WHERE
                    res.tracker_id = %s;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, (tracker_id,))

            data = await cur.fetchone()
            print(data)

            return ReportDAO(**data)

    async def get_all_reports(self, user_id: int | None = None) -> list[ReportDAO]:
        query = """
                SELECT
                    res.tracker_id,
                    res.total_expenses, res.date_create, res.report_name,
                    
                    st.salaries_expenses, st.medical_expenses, st.pension_expenses, st.staff_expenses,
                    
                    e.building_expenses, e.estate_expenses, e.land_expenses,
                    
                    s.bookkeeping_expenses, s.duty_expenses, s.machine_expenses, s.patent_expenses, s.service_expenses,
                    
                    t.estate_tax, t.income_tax, t.land_tax, t.tax_expenses,
                    array(
                        SELECT
                            need_name
                        FROM
                            constant.other_needs ion
                        WHERE
                           ion.need_id =  ANY(cf.other_needs)
                    ) as other_needs,
                     
                     cf.bookkeeping, cf.building_area, cf.land_area, array(
                        SELECT
                            machine_name
                        FROM
                            constant.machine_prices imp
                        WHERE imp.machine_id = ANY(cf.machine_names)
                    ) as machine_names,
                    cf.machine_quantities, cf.operations, pp.patent_name, cf.tax_system,
                    
                   cp.county_name as county, ms.industry_name as industry,
                   cs.organization_type, cs.project_name, cs.workers_quantity
                FROM
                    calcs.result res
                    
                LEFT JOIN calcs.estate e on res.record_id = e.record_id
                LEFT JOIN calcs.company_full cf on res.record_id = cf.record_id
                LEFT JOIN calcs.company_short cs on res.record_id = cs.record_id
                LEFT JOIN calcs.services s on res.record_id = s.record_id
                LEFT JOIN calcs.staff st on res.record_id = st.record_id
                LEFT JOIN calcs.taxes t on res.record_id = t.record_id


                LEFT JOIN constant.county_prices cp ON cs.county = cp.county_id
                LEFT JOIN constant.mean_salaries ms ON cs.industry = ms.industry_id
                LEFT JOIN constant.patent_prices pp ON cf.patent_type = pp.patent_id
                """
        if user_id is not None:
            query = f"{query} WHERE cs.user_id = %s;"
        async with get_connection(self.__db) as cur:
            if user_id is None:
                await cur.execute(query)
            else:
                await cur.execute(query, (user_id,))
            data = await cur.fetchall()

            return [ReportDAO(**r) for r in data]

    async def get_company_for_model(self, tracker_id: str) -> ModelCompanyData:
        query = """
                SELECT
                    cf.*, cs.*
                FROM
                    calcs.result r
                JOIN calcs.company_full cf on r.record_id = cf.record_id
                JOIN calcs.company_short cs on r.record_id = cs.record_id
                WHERE
                    r.tracker_id = %s;
                """
        async with get_connection(self.__db) as cur:
            await cur.execute(query, (tracker_id,))
            data = await cur.fetchone()
            return ModelCompanyData(**data)

    async def get_reports_for_model(self) -> list[ModelReportDAO]:
        query = """
                SELECT
                    
                    res.tracker_id,
                    res.total_expenses, res.date_create, res.report_name,
                    
                    st.salaries_expenses, st.medical_expenses, st.pension_expenses, st.staff_expenses,
                    
                    e.building_expenses, e.estate_expenses, e.land_expenses,
                    
                    s.bookkeeping_expenses, s.duty_expenses, s.machine_expenses, s.patent_expenses, s.service_expenses,
                    
                    t.estate_tax, t.income_tax, t.land_tax, t.tax_expenses,
                    cf.other_needs,
                     
                    cf.bookkeeping, cf.building_area, cf.land_area, cf.machine_names,
                    cf.machine_quantities, cf.operations, cf.patent_type, cf.tax_system,
                    
                   cs.county, cs.industry,
                   cs.organization_type, cs.project_name, cs.workers_quantity
                FROM
                    calcs.result res
                    
                LEFT JOIN calcs.estate e on res.record_id = e.record_id
                LEFT JOIN calcs.company_full cf on res.record_id = cf.record_id
                LEFT JOIN calcs.company_short cs on res.record_id = cs.record_id
                LEFT JOIN calcs.services s on res.record_id = s.record_id
                LEFT JOIN calcs.staff st on res.record_id = st.record_id
                LEFT JOIN calcs.taxes t on res.record_id = t.record_id;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query)
            data = await cur.fetchall()
            return [ModelReportDAO(**r) for r in data]

    async def insert_record_raw(self,
                                tracker_id: str,
                                report_name: str) -> int:
        query = """
                INSERT INTO
                    calcs.result
                    (tracker_id, total_expenses, date_create, report_name) 
                VALUES 
                    (%s, DEFAULT, DEFAULT, %s)
                RETURNING record_id;
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, (tracker_id, report_name))
            data = await cur.fetchone()
            return int(data["record_id"])

    async def insert_company_info(self,
                                  company_full: CompanyFullDAO,
                                  company_short: CompanyShortDAO) -> list[tuple]:
        queries = {
            """
            INSERT INTO
                calcs.company_short
                (record_id, user_id, project_name, industry, organization_type, workers_quantity, county)
                
            VALUES
                (%(record_id)s, %(user_id)s, %(project_name)s,
                 (SELECT
                    industry_id
                FROM constant.mean_salaries
                WHERE industry_name = %(industry)s),
                 
                 %(organization_type)s,
                 %(workers_quantity)s,
                 (
                 SELECT
                    county_id
                FROM
                    constant.county_prices
                WHERE
                    county_name = %(county)s)
                )
            RETURNING county, industry;
                 
            """: company_short.dict(),
            """
            INSERT INTO
                calcs.company_full
                (record_id, land_area,
                building_area, machine_names,
                machine_quantities, patent_type,
                bookkeeping, tax_system,
                operations, other_needs)
                VALUES 
                (
                %(record_id)s, %(land_area)s,
                %(building_area)s, array(
                        SELECT
                            machine_id
                        FROM
                            constant.machine_prices
                        WHERE
                            machine_name = ANY(%(machine_names)s)
                    ),
                %(machine_quantities)s, (
                    SELECT 
                        patent_id
                    FROM 
                        constant.patent_prices
                    WHERE
                        patent_name = %(patent_type)s
                    ),
                %(bookkeeping)s, %(tax_system)s,
                %(operations)s, array(
                        SELECT
                            need_id
                        FROM
                            constant.other_needs
                        WHERE
                            need_name = ANY(%(other_needs)s)
                    )
                )
                RETURNING machine_names, other_needs, patent_type;
            """: company_full.dict()
        }
        result = []
        async with get_connection(self.__db) as cur:
            for query, param in queries.items():
                await cur.execute(query, param)
                data: dict = await cur.fetchone()
                result.extend([(k, v) for k, v in data.items()])

            return result

    async def insert_service_expenses(self, params: ServiceExpenses):
        query = """
                INSERT INTO
                    calcs.services
                    (record_id, service_expenses,
                    duty_expenses, bookkeeping_expenses,
                    patent_expenses, machine_expenses)
                VALUES 
                    (%(record_id)s, %(service_expenses)s,
                    %(duty_expenses)s, %(bookkeeping_expenses)s,
                    %(patent_expenses)s, %(machine_expenses)s);
                """
        async with get_connection(self.__db) as cur:
            await cur.execute(query, params.dict())

    async def insert_staff_expenses(self, params: StaffExpenses):
        query = """
                INSERT INTO
                    calcs.staff
                    (record_id, staff_expenses,
                    salaries_expenses, pension_expenses,
                    medical_expenses) 
                VALUES (
                    %(record_id)s, %(staff_expenses)s,
                    %(salaries_expenses)s, %(pension_expenses)s,
                    %(medical_expenses)s
                )
                
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, params.dict())

    async def insert_estate_expenses(self, params: EstateExpenses):
        query = """
                        INSERT INTO
                            calcs.estate
                            (record_id, estate_expenses,
                            land_expenses, building_expenses) 
                        VALUES (
                            %(record_id)s, %(estate_expenses)s,
                            %(land_expenses)s, %(building_expenses)s
                        )

                        """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, params.dict())

    async def insert_taxes_expanses(self, params: TaxExpenses):
        query = """
                INSERT INTO
                    calcs.taxes
                    (record_id, tax_expenses,
                    land_tax, estate_tax,
                    income_tax)
                VALUES (
                    %(record_id)s, %(tax_expenses)s,
                    %(land_tax)s, %(estate_tax)s,
                    %(income_tax)s
                )
                """
        async with get_connection(self.__db) as cur:
            await cur.execute(query, params.dict())

    async def update_report(self, record_id: int, total_expenses: int):
        query = """
                UPDATE calcs.result SET total_expenses = %s WHERE record_id=%s
                """

        async with get_connection(self.__db) as cur:
            await cur.execute(query, (total_expenses, record_id))

