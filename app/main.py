import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.db_helper import db_helper
from app.core.redis_helper import redis_helper
from app.db.models import SecretsLog
from app.db.base import BaseDBModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_helper.connect()
    async with db_helper.engine.begin() as con:
        await con.run_sync(BaseDBModel.metadata.create_all)
    yield
    await redis_helper.close()

app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)