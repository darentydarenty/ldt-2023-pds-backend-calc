from copy import deepcopy

from aiopg import Connection
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from app.internal.calculations.models import ReportDAO, ReportByTrackerCmd
from app.pkg.connectors import Postgresql
from app.pkg.connectors.postgresql import get_connection


class CalculationsRepository:
    def __init__(self, postgresql: Postgresql, conn: Connection):
        self.__db = postgresql
        self.__conn = conn
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
                    cf.machine_quantities, cf.operations, pp.patent_name, cf.tax_system,
                    
                   cp.county_name as county, ms.industry_name as industry,
                   cs.organization_type, cs.project_name, cs.workers_quantity
                FROM
                    calcs.result res
                JOIN calcs.estate e on res.record_id = e.record_id
                JOIN calcs.company_full cf on res.record_id = cf.record_id
                JOIN calcs.company_short cs on res.record_id = cs.record_id
                JOIN calcs.services s on res.record_id = s.record_id
                JOIN calcs.staff st on res.record_id = st.record_id
                JOIN calcs.taxes t on res.record_id = t.record_id
                
                JOIN constant.county_prices cp ON cs.county = cp.county_id
                JOIN constant.mean_salaries ms ON cs.industry = ms.industry_id
                JOIN constant.patent_prices pp ON cf.patent_type = pp.patent_id
                
                WHERE
                    res.tracker_id = %s;
                """

        async with self.__conn.cursor(cursor_factory=RealDictCursor) as cur:
        # async with self.get_connection(self.__db) as cur:
        #
            await cur.execute(query, tracker_id)

            data = await cur.fetchone()

            return ReportDAO(**data)

    async def create_first_report(self):
        pass

    async def update_report(self):
        pass
