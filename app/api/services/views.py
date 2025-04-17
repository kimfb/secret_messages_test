from uuid import uuid4
import json

from fastapi import APIRouter, status, Depends, Request, Response
from app.api.shemas.secrets import SecretCreate, SecretRead, SecretResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.db_helper import db_helper
from app.core.redis_helper import get_redis_client, redis_helper
from app.api.services.secret_service import encrypt_secret, decrypt_secret

router_app = APIRouter(tags=['Secrets'], prefix='/secret')

@router_app.post('/create')
async def create_secret(
        secret_in: SecretCreate,
        request: Request,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):
    # await redis_client.set('secret',secret_in.secret)
    # val = await redis_client.get('secret')
    token = str(uuid4())
    enc = encrypt_secret(secret_in.secret)
    await redis_client.setex(token, secret_in.ttl_seconds, json.dumps(enc))
    print(request.client.host)
    return {'token': token}


@router_app.get("/{secret_key}")
async def get_secret(
        #response:  SecretResponse,
        token: str,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):
    req = await redis_client.get(token)
    if not req:
        return {'error': "Нет такого секрета"}
    req = json.loads(req)
    data = decrypt_secret(req['encrypted'], req['key'])







