from app.pkg.connectors import Postgresql


class CalculationsRepository:
    def __init__(self, postgresql: Postgresql):
        self.__db = postgresql

