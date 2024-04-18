from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import func, select
from starlette.background import BackgroundTask

from core.background_tasks import cleanup_file
from core.dependencies import SessionDep
from models import (
    Calculation,
    CalculationPayload,
    CalculationsHistory,
    CalculatorOperator,
)

router = APIRouter()


@router.get("/helper", response_model=CalculatorOperator, status_code=status.HTTP_200_OK)
def helper() -> CalculatorOperator:
    return CalculatorOperator()


@router.post("/evaluate", response_model=Calculation, status_code=status.HTTP_201_CREATED)
def calculate(*, session: SessionDep, calculation: CalculationPayload) -> Calculation:
    item = Calculation.model_validate(calculation.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.get("/history", response_model=CalculationsHistory, status_code=status.HTTP_200_OK)
def history(session: SessionDep, skip: int = 0, limit: int = 100) -> CalculationsHistory:
    count_statement = (
        select(func.count())
        .select_from(Calculation)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Calculation)
        .order_by(Calculation.created_at)
        .offset(skip)
        .limit(limit)
    )
    items = session.exec(statement).all()

    return CalculationsHistory(data=items, count=count)


@router.get("/history/{calculation_id}", response_model=Calculation, status_code=status.HTTP_200_OK)
def read_calculation(session: SessionDep, calculation_id: int) -> Calculation:
    item = session.get(Calculation, calculation_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Calculation ({calculation_id}) not found.")
    return item


@router.patch("/history/{calculation_id}", response_model=Calculation, status_code=status.HTTP_200_OK)
def modify_calculation(session: SessionDep, calculation_id: int, calculation: CalculationPayload) -> Calculation:
    item = session.get(Calculation, calculation_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Calculation ({calculation_id}) not found.")
    item.sqlmodel_update(calculation.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
