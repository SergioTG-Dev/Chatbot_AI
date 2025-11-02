from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import field_validator

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @field_validator("SUPABASE_URL", "SUPABASE_KEY", "SUPABASE_SERVICE_ROLE_KEY", "REDIS_URL", "SECRET_KEY")
    @classmethod
    def not_blank(cls, v: str):
        if v is None:
            raise ValueError("Variable de entorno requerida ausente")
        if isinstance(v, str) and not v.strip():
            raise ValueError("Variable de entorno requerida vacía")
        return v

    class Config:
        env_file = str(Path(__file__).resolve().parents[2] / ".env")
        env_file_encoding = "utf-8"

settings = Settings()