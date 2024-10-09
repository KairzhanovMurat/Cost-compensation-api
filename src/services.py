from .schemas import UserCostData, CostData, DebtData, Result, CompensationData


class Calculator:
    def __init__(self, users: list[UserCostData]):
        self.users = users
        self.temp_debts: list = []

    @property
    def average_cost(self) -> float:
        return sum([user.cost for user in self.users]) / len(self.users) if self.users else 0

    @property
    def total_cost(self) -> float:
        return sum([user.cost for user in self.users])

    def get_cost_data(self) -> CostData:
        return CostData(average_cost=self.average_cost, total_cost=self.total_cost)

    def _get_user_debts(self, user: UserCostData) -> DebtData:
        debt = self.average_cost - user.cost
        return DebtData(user_name=user.name, debt_amount=debt)

    def get_debts(self) -> list[DebtData]:
        debts = [self._get_user_debts(user) for user in self.users]
        debts.sort(key=lambda debt: debt.debt_amount, reverse=True)
        return debts

    def compensate(self, max_debt: DebtData, min_debt: DebtData) -> CompensationData | None:
        if len(self.temp_debts) <= 1:
            self.temp_debts.clear()
            return

        if max_debt.debt_amount == min_debt.debt_amount:
            self.temp_debts.remove(max_debt)
            self.temp_debts.remove(min_debt)
            return None

        compensation = min(abs(min_debt.debt_amount), max_debt.debt_amount)

        max_debt.debt_amount -= compensation
        min_debt.debt_amount += compensation

        if max_debt.debt_amount == 0:
            self.temp_debts.remove(max_debt)
        if min_debt.debt_amount == 0:
            self.temp_debts.remove(min_debt)

        return CompensationData(
            compensator_name=max_debt.user_name,
            receiver_name=min_debt.user_name,
            amount=compensation
        )

    def calculate_compensations(self) -> list[CompensationData]:
        self.temp_debts = self.get_debts()
        compensations = []
        while self.temp_debts:
            max_debt = self.temp_debts[0]
            min_debt = self.temp_debts[-1]
            compensation = self.compensate(max_debt, min_debt)
            if compensation:
                compensations.append(compensation)
        return compensations

    def get_result(self):
        cost_data = self.get_cost_data()
        debt_data = self.get_debts()
        compensations = self.calculate_compensations()
        return Result(cost_data=cost_data, debt_data=debt_data,
                      compensations=compensations)
