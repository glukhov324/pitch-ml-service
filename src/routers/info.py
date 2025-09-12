from fastapi import APIRouter

from src.schemas import Msg
from src.config import settings


router = APIRouter(
    prefix="/info"
)


@router.get("/health_check", response_model=Msg)
def health_check():
    
    return Msg(
        msg=f"OK {settings.DEVICE}"
    ).model_dump()