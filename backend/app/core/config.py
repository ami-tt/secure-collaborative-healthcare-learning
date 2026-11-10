import json

from typing import List, Union

from pydantic import field_validator

from pydantic_settings import BaseSettings, SettingsConfigDict





class Settings(BaseSettings):

    PROJECT_NAME: str = "Secure Collaborative Healthcare Learning System"

    VERSION: str = "1.0.0"

    API_V1_STR: str = "/api/v1"

    ENVIRONMENT: str = "development"

    DEBUG: bool = True



    # Security & JWT

    SECRET_KEY: str = "default-insecure-dev-key-change-me"

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120



    # Database

    DATABASE_URL: str = "sqlite:///./healthcare_fl.db"



    # CORS

    BACKEND_CORS_ORIGINS: Union[List[str], str] = ["http://localhost:3000", "http://localhost:5173"]



    # Initial Super Admin Seed

    FIRST_SUPERADMIN_EMAIL: str = "admin@securefl.health"

    FIRST_SUPERADMIN_PASSWORD: str = "AdminSecurePassword123!"

    FIRST_SUPERADMIN_NAME: str = "System Administrator"



    @field_validator("BACKEND_CORS_ORIGINS", mode="before")

    @classmethod

    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:

        if isinstance(v, str):

            if v.startswith("[") and v.endswith("]"):

                try:

                    return json.loads(v)

                except Exception:

                    pass

            return [i.strip() for i in v.split(",") if i.strip()]

        elif isinstance(v, (list, tuple)):

            return list(v)

        return []



    model_config = SettingsConfigDict(

        env_file=".env",

        env_file_encoding="utf-8",

        case_sensitive=True,

        extra="ignore"

    )





settings = Settings()
