from pydantic import BaseModel


class UserCostData(BaseModel):
    name: str
    cost: float


class CostData(BaseModel):
    average_cost: float
    total_cost: float


class DebtData(BaseModel):
    user_name: str
    debt_amount: float


class CompensationData(BaseModel):
    compensator_name: str
    receiver_name: str
    amount: float


class Result(BaseModel):
    cost_data: CostData
    debt_data: list[DebtData]
    compensations: list[CompensationData]
