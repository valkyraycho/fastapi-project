from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    DATABASE_TEST_URL: str = ""
    JWT_SECRET: str = ""  # generate with `openssl rand -hex 32``
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = ""

    DOMAIN: str = ""
    TESTING: bool = False


Config = Settings()
REDIS_URL = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
broker_url = REDIS_URL
result_backend = REDIS_URL
broker_connection_retry_on_startup = True
