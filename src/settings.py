from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List
import logging
import torch



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Server
    HOST: str = Field("0.0.0.0")
    PORT: int = Field(5000)
    DEV_MODE: bool = Field(False)
    SERVICE_NAME: str = Field("Speech Service")

    # Logging
    LOG_FORMAT: str = Field(f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    LOG_FOLDER: str = Field("logs")
    LOG_FILE: str = Field("logs.log")
    LOG_LEVEL: int = logging.INFO

    # Models
    DEVICE: str = Field("cuda" if torch.cuda.is_available() else "cpu")
    COMPUTE_TYPE: str
    WHISPER_ARCH: str
    BATCH_SIZE: int
    AVAILABLE_LANGUAGES: List[str]




settings = Settings()