from pydantic_settings import BaseSettings
from pydantic import Field, computed_field


class Settings(BaseSettings):
    # Database parts (assembled into database_url)
    database_url_env: str | None = Field(default=None, alias="DATABASE_URL")
    db_user: str = Field(default="postgres")
    db_pass: str = Field(default="changeme123")
    db_name: str = Field(default="resort_db")
    db_host: str = Field(
        default="db"
    )  # Changed from localhost for Docker compatibility
    db_port: int = Field(default=5432)

    redis_url: str = Field(default="redis://localhost:6379/0")
    environment: str = Field(default="development")

    # Security
    secret_key: str = Field(
        default="your-64-char-secret-key-here-change-in-production-minimum-64-characters-long"
    )
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60)
    refresh_token_expire_days: int = Field(default=30)

    # CORS - env: comma-separated string (e.g. ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000)
    allowed_origins_env: str | None = Field(default=None, alias="ALLOWED_ORIGINS")

    # Payment Gateways
    paymob_api_key: str = Field(default="test_paymob_api_key")
    paymob_integration_id: str = Field(default="test_integration_id")
    paymob_hmac_secret: str = Field(default="test_hmac_secret")
    stripe_secret_key: str = Field(default="sk_test_your_stripe_key")
    stripe_webhook_secret: str = Field(default="whsec_test_secret")

    # Webhooks
    n8n_webhook_url: str | None = Field(default=None)

    @computed_field
    @property
    def database_url(self) -> str:
        """Assemble database URL from parts - supports both PostgreSQL and SQLite for development."""
        # Load from env directly if present to override computed URL
        if getattr(self, "database_url_env", None):
            return self.database_url_env

        # Use SQLite for quick development if USE_SQLITE is set
        if getattr(self, "use_sqlite", False):
            return "sqlite+aiosqlite:///./alkhayma_dev.db"
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    # Development settings - PostgreSQL by default as per project requirements
    use_sqlite: bool = Field(default=False)  # Use PostgreSQL as specified in documentation
    log_level: str = Field(default="DEBUG")

    _default_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
    ]

    @computed_field
    @property
    def allowed_origins(self) -> list[str]:
        """CORS allowed origins (from env comma-separated or default)."""
        if self.allowed_origins_env:
            return [x.strip() for x in self.allowed_origins_env.split(",") if x.strip()]
        return self._default_origins.copy()

    @computed_field
    @property
    def cors_origins(self) -> list[str]:
        """Alias for allowed_origins for backward compatibility."""
        return self.allowed_origins

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
