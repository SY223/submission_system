#From video 47:00

from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Assignment Submission"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = ""

    DATABASE_URL_ASYNC: str = ""
    DATABASE_URL: str = ""

    UPLOAD_DIR_ASSIGNMENTS: str = "uploads/assignments"

    #Pydantic Version 2 Settings Config
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
