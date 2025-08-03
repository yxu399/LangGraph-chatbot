from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Clerk
    clerk_secret_key: str
    clerk_webhook_secret: str
    
    # Anthropic
    anthropic_api_key: str
    
    # Application
    debug: bool = True
    environment: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()