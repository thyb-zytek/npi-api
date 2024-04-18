from decimal import Decimal

from pydantic import computed_field, field_serializer
from sqlmodel import Field, SQLModel

from core.db import BaseTable
from tools.rpn_calculator import OPERATORS, VARIABLES, RPNCalculator


class CalculationBase(SQLModel):
    expression: str


class CalculationPayload(SQLModel):
    expression: str

    @computed_field
    @property
    def result(self) -> float:
        return RPNCalculator(self.expression).solve()

    @field_serializer('result')
    def serialize_result(self, result: float) -> float:
        return round(result, 10)


class Calculation(CalculationBase, BaseTable, table=True):
    result: Decimal = Field(decimal_places=10)

    @field_serializer('result', when_used="json")
    def serialize_result(self, result: Decimal) -> float:
        return float(result)


class CalculationsHistory(SQLModel):
    data: list[Calculation]
    count: int


class Symbol(SQLModel):
    name: str
    symbol: str


class CalculatorOperator(SQLModel):
    operators: list[Symbol] = Field(
        default_factory=lambda: [Symbol(name=operator[2], symbol=symbol) for symbol, operator in OPERATORS.items()])
    variables: list[Symbol] = Field(
        default_factory=lambda: [Symbol(name=var[1], symbol=symbol) for symbol, var in VARIABLES.items()])
