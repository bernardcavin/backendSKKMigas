import secrets
from typing import Annotated, Any, Literal
import os
from pydantic import (
    AnyUrl,
    BeforeValidator,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class OracleDsn(AnyUrl):
    allowed_schemes = {'oracle+cx_oracle'}
    user_required = True

def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = ""
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    LOCAL_SQLALCHEMY_DATABASE_URI: str = 'sqlite:///./demo.db'
    
    UPLOAD_DIR: str = "uploads"
    
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def upload_dir(self) -> str:
        # Use HTTPS for anything other than local development
        return os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')), 
            self.UPLOAD_DIR
            )

    app_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_POSTGRES_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    ORACLE_USER: str
    ORACLE_PASSWORD: str = ""
    ORACLE_SERVER: str
    ORACLE_PORT: int = 1512
    ORACLE_SERVICE_NAME: str = ""
        
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_ORACLE_DATABASE_URI(self) -> str:
        return f"oracle+cx_oracle://{self.ORACLE_USER}:{self.ORACLE_PASSWORD}@{self.ORACLE_SERVER}:{self.ORACLE_PORT}/?service_name={self.ORACLE_SERVICE_NAME}"
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT == "local":
            return str(self.LOCAL_SQLALCHEMY_DATABASE_URI)
        elif self.ENVIRONMENT == "staging":
            return str(self.SQLALCHEMY_POSTGRES_DATABASE_URI)
        elif self.ENVIRONMENT == "production":
            return str(self.SQLALCHEMY_ORACLE_DATABASE_URI)
        else:
            raise ValueError(f"Invalid environment: {self.ENVIRONMENT}")

settings = Settings()  # type: ignore