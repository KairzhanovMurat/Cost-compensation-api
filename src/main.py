from fastapi import FastAPI
from .schemas import UserCostData, Result
from .services import Calculator
import uvicorn

app = FastAPI(docs_url="/")


@app.post("/calculate")
def calculate_average_waste(users: list[UserCostData]) -> Result:
    calculator = Calculator(users)
    return calculator.get_result()


if __name__ == "__main__":
    uvicorn.run("main:app")
