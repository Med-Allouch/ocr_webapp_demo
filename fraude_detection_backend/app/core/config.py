import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn  


class Settings(BaseSettings):
    PROJECT_NAME: str = "CDC Fraud Detection API"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL Database settings
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "medall")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "health_inssurance_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    DATABASE_URL: Optional[PostgresDsn] = None
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Get database URL from env or construct it."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:4200",  # Frontend URL
        "http://localhost:8080",
        "http://localhost",
    ]
    
    # File storage
    UPLOAD_DIRECTORY: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)