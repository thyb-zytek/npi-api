from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from sqlmodel import func, select
from starlette.background import BackgroundTask

from core.background_tasks import cleanup_file
from core.dependencies import SessionDep
from models import Calculation, CalculationBase, CalculationsHistory

router = APIRouter()


@router.post("/evaluate", response_model=Calculation, status_code=status.HTTP_201_CREATED)
def calculate(*, session: SessionDep, calculation: CalculationBase) -> Calculation:
    calculation = Calculation.model_validate(calculation)
    session.add(calculation)
    session.commit()
    session.refresh(calculation)
    return calculation


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


@router.get("/history/export", status_code=status.HTTP_200_OK, response_class=FileResponse)
def export(session: SessionDep, skip: int = 0, limit: int = 100) -> FileResponse:
    statement = (
        select(Calculation)
        .order_by(Calculation.created_at)
        .offset(skip)
        .limit(limit)
    )
    items = session.exec(statement).all()
    file_name = "export.csv"
    file_path = f"/tmp/{file_name}"
    with open(file_path, "w") as f:
        f.write("text;result\ntest;0\nessai;1")

    return FileResponse(path=file_path, filename=file_name, media_type='text/csv',
                        background=BackgroundTask(cleanup_file, file_path))
