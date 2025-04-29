import redis.asyncio as redis
from redis.asyncio import Redis, ConnectionPool
from typing import AsyncGenerator

from app.core.config import settings


class RedisHelper:
    def __init__(self):
        self.pool: ConnectionPool | None = None


    async def connect(self):
        self.pool = redis.ConnectionPool(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.db,
            #password=settings.redis.password,
            decode_responses=settings.redis.decode_responses,
            max_connections=settings.redis.max_connections,
            socket_timeout=settings.redis.socket_timeout,
            socket_connect_timeout=settings.redis.socket_connect_timeout
        )

    async def close(self):
        if self.pool:
            await self.pool.disconnect(inuse_connections=True)


    def get_client(self):
        if not self.pool:
            raise RuntimeError('Redis pool не инициализирован. Вызовите connect()')
        return Redis(connection_pool=self.pool)

redis_helper = RedisHelper()


async def get_redis_client():# -> AsyncGenerator[Redis, None]:
    """Зависимость FastAPI."""
    # await redis_helper.connect()
    client = redis_helper.get_client()
    yield client

