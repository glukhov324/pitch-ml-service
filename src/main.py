from fastapi import FastAPI

from src.routers import speech_router, text_router, info_router
from src.middlewares import handle_exceptions_middleware
from src.config import settings



app = FastAPI(
    debug=settings.DEV_MODE,
    title=settings.SERVICE_NAME
)
app.middleware("http")(handle_exceptions_middleware)

app.include_router(
    router=info_router,
    tags=["Info"],
    prefix=settings.API_V1_STR
)

app.include_router(
    router=speech_router,
    tags=["Speech Analytics"],
    prefix=settings.API_V1_STR
)

app.include_router(
    router=text_router,
    tags=["Text Analytics"],
    prefix=settings.API_V1_STR
)