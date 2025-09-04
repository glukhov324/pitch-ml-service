from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
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
    LOG_FORMAT: str = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    LOG_FOLDER: str = "logs"
    LOG_FILE: str = "logs.log"
    LOG_LEVEL: int = logging.INFO

    # Models
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"
    COMPUTE_TYPE: str
    WHISPER_ARCH: str
    BATCH_SIZE: int


settings = Settings()