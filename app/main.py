import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.services.views import router_app
from app.core.db_helper import db_helper
from app.core.redis_helper import redis_helper
from app.db.models import SecretsLog
from app.db.base import BaseDBModel
from app.api.services.middleWare_set import MiddlewareNoCache


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_helper.connect()
    async with db_helper.engine.begin() as con:
        await con.run_sync(BaseDBModel.metadata.create_all)
    yield
    await redis_helper.close()

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_app)
app.add_middleware(MiddlewareNoCache)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)