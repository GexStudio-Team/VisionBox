from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "VisionBots API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"
    DATABASE_URL: str = "sqlite:///./visionbots.db"
    CORS_ORIGINS: str = "http://localhost:5173"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
