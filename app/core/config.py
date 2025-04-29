from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    name: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseModel):
    host: str
    port: int
    db: int
    password: str
    decode_responses: bool = True
    max_connections: int = 100
    socket_timeout: float | None = None
    socket_connect_timeout: float | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        case_sensitive=False,
        env_prefix='APP_',
    )
    # PostgreSQL
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    # Redis
    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    # db: PostgresConfig
    # redis: RedisConfig

    @property
    def db(self) -> PostgresConfig:
        return PostgresConfig(
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            name=self.db_name,
        )

    @property
    def redis(self) -> RedisConfig:
        return RedisConfig(
            host=self.redis_host,
            port=self.redis_port,
            db=self.redis_db,
            password=self.redis_password
        )

settings = Settings()


