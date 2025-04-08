from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class PostgresConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class RedisConfig(BaseModel):
    host: str
    port: int = 6379
    db: int = 0
    password: str | None = None
    decode_responses: bool = True
    max_connections: int = 100
    socket_timeout: float | None = None
    socket_connect_timeout: float | None = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix='APP__',
    )
    db: PostgresConfig
    redis: RedisConfig

settings = Settings()
