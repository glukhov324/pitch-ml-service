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
    API_V1_STR: str = Field("/api/v1")

    # Logging
    LOG_FORMAT: str = Field(f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    LOG_FOLDER: str = Field("logs")
    LOG_FILE: str = Field("logs.log")
    LOG_LEVEL: int = logging.INFO

    # Models
    DEVICE: str = Field("cuda" if torch.cuda.is_available() else "cpu")
    NUM_WORKERS: int = Field(2)
    NUM_THREADS: int = Field(2)
    WHISPER_MODEL_SIZE: str = Field("medium")
    WHISPER_COMPUTE_TYPE: str = Field("int8")
    WHISPER_BEAM_SIZE: int = Field(5)
    FLOAT_ROUND_RATE: int = Field(2)
    SER_MODEL_NAME: str
    SER_SAMPLING_RATE: int




settings = Settings()