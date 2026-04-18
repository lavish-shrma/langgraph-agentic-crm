from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    DATABASE_URL: str
    GROQ_API_KEY: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
