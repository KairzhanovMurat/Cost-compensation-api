import pytest
from src import services, schemas

users_data_1 = [
    schemas.UserCostData(name="Alice", cost=100),
    schemas.UserCostData(name="Bob", cost=150),
    schemas.UserCostData(name="Charlie", cost=50)
]

users_data_2 = [
    schemas.UserCostData(name="Dave", cost=200),
    schemas.UserCostData(name="Eve", cost=250),
    schemas.UserCostData(name="Frank", cost=150)
]

users_data_3 = [
    schemas.UserCostData(name="George", cost=100),
    schemas.UserCostData(name="Helen", cost=100),
    schemas.UserCostData(name="Ian", cost=100)
]


@pytest.mark.parametrize("users_data, expected_average, expected_total", [
    (users_data_1, 100, 300),
    (users_data_2, 200, 600),
    (users_data_3, 100, 300),
])
def test_get_cost_data(users_data, expected_average, expected_total):
    calc = services.Calculator(users_data)
    cost_data = calc.get_cost_data()
    assert cost_data.average_cost == expected_average
    assert cost_data.total_cost == expected_total


@pytest.mark.parametrize("users_data, expected_debts", [
    (users_data_1, [
        schemas.DebtData(user_name="Charlie", debt_amount=50),
        schemas.DebtData(user_name="Alice", debt_amount=0),
        schemas.DebtData(user_name="Bob", debt_amount=-50)

    ]),
    (users_data_2, [
        schemas.DebtData(user_name="Frank", debt_amount=50),
        schemas.DebtData(user_name="Dave", debt_amount=0),
        schemas.DebtData(user_name="Eve", debt_amount=-50),

    ]),
    (users_data_3, [
        schemas.DebtData(user_name="George", debt_amount=0),
        schemas.DebtData(user_name="Helen", debt_amount=0),
        schemas.DebtData(user_name="Ian", debt_amount=0)
    ])
])
def test_get_debts(users_data, expected_debts):
    calc = services.Calculator(users_data)
    debts = calc.get_debts()
    assert len(debts) == len(expected_debts)
    for i in range(len(debts)):
        assert debts[i].user_name == expected_debts[i].user_name
        assert debts[i].debt_amount == pytest.approx(expected_debts[i].debt_amount, rel=1e-2)


@pytest.mark.parametrize("users_data, expected_compensations", [
    (users_data_1, [
        schemas.CompensationData(compensator_name="Charlie", receiver_name="Bob", amount=50)
    ]),
    (users_data_2, [
        schemas.CompensationData(compensator_name="Frank", receiver_name="Eve", amount=50)
    ]),
    (users_data_3, [])
])
def test_calculate_compensations(users_data, expected_compensations):
    calc = services.Calculator(users_data)
    compensations = calc.calculate_compensations()
    assert len(compensations) == len(expected_compensations)
    for i in range(len(compensations)):
        assert compensations[i].compensator_name == expected_compensations[i].compensator_name
        assert compensations[i].receiver_name == expected_compensations[i].receiver_name
        assert compensations[i].amount == pytest.approx(expected_compensations[i].amount, rel=1e-2)


@pytest.mark.parametrize("users_data", [
    (users_data_1),
    (users_data_2),
    (users_data_3),
])
def test_get_result(users_data):
    calc = services.Calculator(users_data)
    result = calc.get_result()

    assert isinstance(result.cost_data, schemas.CostData)

    assert isinstance(result.debt_data, list)
    assert all(isinstance(debt, schemas.DebtData) for debt in result.debt_data)

    assert isinstance(result.compensations, list)
    assert all(isinstance(comp, schemas.CompensationData) for comp in result.compensations)
