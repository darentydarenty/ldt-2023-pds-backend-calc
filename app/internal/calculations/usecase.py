from .repository import CalculationsRepository


class CalculationsUseCase:
    _calc_repo: CalculationsRepository

    def __init__(self, calc_repo: CalculationsRepository):
        self._calc_repo = calc_repo

    def calculate(self):
        pass
