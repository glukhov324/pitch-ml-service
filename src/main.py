from fastapi import FastAPI

from src.routers import asr_router
from src.middlewares import handle_exceptions_middleware
from src.settings import settings



app = FastAPI(
    debug=settings.DEV_MODE,
    title=settings.SERVICE_NAME
)
app.middleware("http")(handle_exceptions_middleware)
app.include_router(asr_router)