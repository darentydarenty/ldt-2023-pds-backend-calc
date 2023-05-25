from app.pkg.connectors import Postgresql


class CalculationsRepository:
    def __init__(self, postgresql: Postgresql):
        self.__db = postgresql


    async def get_report_by_tracker_id(self, tracker_id: str):
        pass

    async def create_first_report(self):
        pass

    async def update_report(self):
        pass