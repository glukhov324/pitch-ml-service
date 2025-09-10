from fastapi import APIRouter
from src.schemas import Msg


router = APIRouter(
    prefix="/info"
)


@router.get("/health_check", response_model=Msg)
def health_check():
    return Msg(
        msg="OK"
    ).model_dump()