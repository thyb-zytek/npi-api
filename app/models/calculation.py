from sqlmodel import SQLModel

from core.db import BaseTable


class CalculationBase(SQLModel):
    expression: str


class Calculation(CalculationBase, BaseTable, table=True):
    result: float | None = None


class CalculationsHistory(SQLModel):
    data: list[Calculation]
    count: int
