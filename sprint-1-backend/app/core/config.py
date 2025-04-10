# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration settings
    """
    # Database configuration
    DATABASE_URL: str = "postgresql://user:password@localhost/documentdb"
    
    # File upload settings
    UPLOAD_DIR: str = "uploaded_files"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_FILE_TYPES: list = ['pdf', 'jpg', 'jpeg', 'png']
    
    # Extraction settings
    EXTRACTION_MODE: str = "placeholder"  # Can be changed to actual mode later
    
    class Config:
        """
        Configuration for loading environment variables
        """
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a singleton settings instance
settings = Settings()