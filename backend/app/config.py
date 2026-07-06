import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/legalos"
    SECRET_KEY: str = "d1f885e34be34cf5e28a49c25f483c6f6bb8fbcce8a7bcfae81b6727284b3917"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    OPENAI_API_KEY: str = "mock-key-for-now"
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    QDRANT_URL: str = "http://localhost:6333"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
