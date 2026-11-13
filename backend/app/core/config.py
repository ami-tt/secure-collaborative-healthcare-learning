import json
import os
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import ClassVar, List, Optional, Union
from urllib.parse import urlparse

from pydantic import (
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


# Default .env file path
DEFAULT_ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """
    Application configuration with production safety checks.

    Development allows SQLite.
    Production requires PostgreSQL, except for isolated
    SQLite databases created inside the system temporary directory
    for automated tests.
    """

    model_config = SettingsConfigDict(
        env_file=str(DEFAULT_ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DEFAULT_ENV_PATH: ClassVar[Path] = DEFAULT_ENV_PATH

    # Basic metadata
    PROJECT_NAME: str = "Secure Collaborative Healthcare Learning System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "default-insecure-dev-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # Database
    DATABASE_URL: str = "sqlite:///./healthcare_fl.db"

    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Super-admin provisioning
    PROVISION_SUPERADMIN: bool = False
    FIRST_SUPERADMIN_EMAIL: str = "admin@securefl.health"
    FIRST_SUPERADMIN_PASSWORD: Optional[str] = None
    FIRST_SUPERADMIN_NAME: str = "System Administrator"

    # Development-only default password
    @field_validator("FIRST_SUPERADMIN_PASSWORD", mode="before")
    @classmethod
    def _default_dev_password(
        cls,
        value: Optional[str],
        info: ValidationInfo,
    ) -> Optional[str]:

        environment = info.data.get(
            "ENVIRONMENT",
            os.getenv("ENVIRONMENT", "development"),
        )

        if environment != "production" and not value:
            return "DevSuperAdminPass123!"

        return value

    # Parse CORS origins
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors_origins(
        cls,
        value: Union[List[str], str],
    ) -> List[str]:

        if isinstance(value, str):
            value = value.strip()

            if value.startswith("[") and value.endswith("]"):
                try:
                    parsed_value = json.loads(value)

                    if isinstance(parsed_value, list):
                        return [
                            str(origin).strip()
                            for origin in parsed_value
                            if str(origin).strip()
                        ]

                except json.JSONDecodeError:
                    pass

            return [
                origin.strip()
                for origin in value.split(",")
                if origin.strip()
            ]

        return list(value)

    # Validate database URL
    @field_validator("DATABASE_URL")
    @classmethod
    def _validate_db_url(
        cls,
        value: str,
        info: ValidationInfo,
    ) -> str:

        environment = info.data.get(
            "ENVIRONMENT",
            os.getenv("ENVIRONMENT", "development"),
        )

        if environment == "production":

            # PostgreSQL is allowed in production.
            if value.startswith(("postgresql://", "postgres://")):
                return value

            # Allow SQLite only for isolated temporary test databases.
            if value.startswith("sqlite:///"):

                sqlite_path = value.replace("sqlite:///", "", 1)

                try:
                    db_path = Path(sqlite_path).resolve()
                    temp_root = Path(tempfile.gettempdir()).resolve()

                    # Ensure the database is inside the system temp folder.
                    db_path.relative_to(temp_root)

                    return value

                except (ValueError, OSError):
                    pass

            raise ValueError("must be a PostgreSQL URL")

        return value

    # Production security validation
    @model_validator(mode="after")
    def _enforce_production_rules(self) -> "Settings":

        environment = os.getenv(
            "ENVIRONMENT",
            self.ENVIRONMENT,
        )

        if environment == "production":

            # Disable debug mode
            self.DEBUG = False

            # Validate secret key
            key = self.SECRET_KEY

            if len(key) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production."
                )

            lowered = key.lower()

            if any(
                placeholder in lowered
                for placeholder in [
                    "change-me",
                    "default",
                    "insecure",
                ]
            ):
                raise ValueError(
                    "SECRET_KEY appears to be a placeholder in production."
                )

            # Validate CORS origins
            origins = self.BACKEND_CORS_ORIGINS

            if not origins:
                raise ValueError(
                    "BACKEND_CORS_ORIGINS cannot be empty in production."
                )

            if "*" in origins:
                raise ValueError(
                    "Wildcard '*' is not allowed in production CORS origins."
                )

            for origin in origins:

                parsed = urlparse(origin)

                # Require a valid hostname
                if not parsed.scheme or not parsed.hostname:
                    raise ValueError(
                        f"Invalid CORS origin: '{origin}'."
                    )

                # HTTP allowed only for localhost
                if (
                    parsed.scheme == "http"
                    and parsed.hostname not in ("localhost", "127.0.0.1")
                ):
                    raise ValueError(
                        f"HTTP origin '{origin}' is only allowed for localhost."
                    )

                # Require HTTPS for non-localhost origins
                if (
                    parsed.scheme != "https"
                    and not (
                        parsed.scheme == "http"
                        and parsed.hostname in ("localhost", "127.0.0.1")
                    )
                ):
                    raise ValueError(
                        f"CORS origin '{origin}' must use HTTPS."
                    )

                # Reject credentials
                if parsed.username or parsed.password:
                    raise ValueError(
                        "CORS origins must not contain credentials."
                    )

                # Reject paths
                if parsed.path and parsed.path != "/":
                    raise ValueError(
                        "CORS origins must not contain a path."
                    )

                # Reject query parameters and fragments
                if parsed.params or parsed.query or parsed.fragment:
                    raise ValueError(
                        "CORS origins must not contain query parameters or fragments."
                    )

            # Validate super-admin password
            if self.PROVISION_SUPERADMIN:

                password = self.FIRST_SUPERADMIN_PASSWORD

                if not password or len(password) < 12:
                    raise ValueError(
                        "FIRST_SUPERADMIN_PASSWORD must be at least "
                        "12 characters when provisioning super-admin "
                        "in production."
                    )

        return self


# Cached settings helpers
@lru_cache()
def _cached_settings() -> Settings:
    return Settings()


def get_settings() -> Settings:
    """Return cached application settings."""
    return _cached_settings()


def clear_settings_cache() -> None:
    """Clear settings cache, useful for tests."""
    _cached_settings.cache_clear()


# Lazy settings proxy
class _SettingsProxy:

    def __getattr__(self, name):
        return getattr(get_settings(), name)

    def __repr__(self):
        return "<SettingsProxy delegating to Settings()>"


# Settings instance
settings = get_settings()