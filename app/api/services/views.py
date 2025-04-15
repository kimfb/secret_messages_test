from fastapi import APIRouter, status, Depends, Response
from app.api.shemas.secrets import SecretCreate, SecretRead, SecretResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.db_helper import db_helper
from app.core.redis_helper import get_redis_client, redis_helper

router_app = APIRouter(tags=['Secrets'], prefix='/secrets')

@router_app.post('/create')
async def create_secret(
        secret_in: SecretCreate,
        response: Response,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):
    await redis_client.set('secret',secret_in.secret)
    val = await redis_client.get('secret')
    print(val)

    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Expires'] = '0'
    response.headers['Pragma'] = 'no-cache'

