import os
from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    ENV: str = Field(default=os.getenv("ENV", "dev"))
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "dev-secret-key-change"))
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60 * 24)

    CORS_ALLOW_ORIGINS: list[str] = Field(
        default_factory=lambda: os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
    )

    DATA_DIR: str = Field(default=os.getenv("DATA_DIR", "/workspace/rural_healthcare_ai_advisor/backend/data"))
    EMERGENCY_RULES_PATH: str = Field(default_factory=lambda: os.path.join(
        os.getenv("DATA_DIR", "/workspace/rural_healthcare_ai_advisor/backend/data"), "rules", "emergency_rules.json"
    ))
    SYNTHETIC_DATASET_PATH: str = Field(default_factory=lambda: os.path.join(
        os.getenv("DATA_DIR", "/workspace/rural_healthcare_ai_advisor/backend/data"), "synthetic_dataset.csv"
    ))
    MULTILINGUAL_PHRASES_PATH: str = Field(default_factory=lambda: os.path.join(
        os.getenv("DATA_DIR", "/workspace/rural_healthcare_ai_advisor/backend/data"), "multilingual_phrases.json"
    ))

    ENCRYPTION_KEY: str = Field(default=os.getenv("ENCRYPTION_KEY", ""))

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

