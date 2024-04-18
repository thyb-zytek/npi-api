from fastapi import APIRouter

from api.v1 import calculator

__version__ = 1

router = APIRouter()

router.include_router(calculator.router, prefix="/rpn", tags=["RPN Calculator"])
