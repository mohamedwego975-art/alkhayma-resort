from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(default="postgresql+asyncpg://postgres:changeme123@localhost:5433/resort_db")
    redis_url: str = "redis://localhost:6379"
    environment: str = "development"
    
    # JWT Settings
    secret_key: str = Field(default="your-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Payment Gateways
    paymob_api_key: str = "test_paymob_api_key"
    paymob_integration_id: str = "test_integration_id"
    paymob_hmac_secret: str = "test_hmac_secret"
    
    stripe_secret_key: str = "sk_test_your_stripe_key"
    stripe_webhook_secret: str = "whsec_test_secret"
    
    # Webhooks
    n8n_webhook_url: str | None = None
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
