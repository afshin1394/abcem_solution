
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env.docker", extra="ignore")

    # Application Settings
    app_name: str
    app_env: str

    # Database Settings
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int

    # Redis Settings
    redis_host: str
    redis_port: int
    redis_db : int



    # Kafka Settings
    kafka_bootstrap_servers: str

    # JWT Settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    logto_app_id: str
    logto_app_secret: str
    logto_endpoint: str



    # Other Settings
    debug: bool = False


    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    @property
    def logto_token_endpoint(self) -> str:
        return f"{self.logto_endpoint}/oidc/token"

# Instantiate settings
settings = Settings()
