from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MEMORY_NAMESPACE: str = "cdyp7"

    class Config:
        env_prefix = "APP_"


settings = Settings()
