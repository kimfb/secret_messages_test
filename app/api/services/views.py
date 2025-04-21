from uuid import uuid4
import json

from fastapi import APIRouter, status, Depends, Request, Response
from app.api.shemas.secrets import SecretCreate, SecretRead, SecretResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.db_helper import db_helper
from app.core.redis_helper import get_redis_client, redis_helper
from app.api.services.secret_service import encrypt_secret, decrypt_secret, hash_phrase, verify_phrase
from app.api.services.crud_service import create_secret_db, get_secret_db, get_passphrase, delete_secret_db


router_app = APIRouter(tags=['Secrets'], prefix='/secret')

@router_app.post('/create')
async def create_secret(
        secret_in: SecretCreate,
        request: Request,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):

    token = str(uuid4())
    enc_secret = encrypt_secret(secret_in.secret)
    hashed_phrase = hash_phrase(secret_in.passphrase)
    await redis_client.setex(token, secret_in.ttl_seconds, json.dumps(enc_secret))

    await create_secret_db(
        session=session_db,
        request=request,
        token=token,
        hashed_phrase=hashed_phrase
        )
    return {'secret_key': token}


@router_app.get("/{secret_key}")
async def get_secret(
        request:  Request,
        secret_key: str,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):
    req = await redis_client.get(secret_key)
    if not req:
         return {'error': "Нет такого секрета"}
    await redis_client.delete(secret_key)
    req = json.loads(req)

    await get_secret_db(session=session_db, token=secret_key, request=request)
    return decrypt_secret(req['encrypted'], req['key'])


@router_app.delete('/{secret_key}')
async def delete_secret(
        request:  Request,
        secret_key: str,
        passphrase: str,
        session_db: AsyncSession = Depends(db_helper.session_getter),
        redis_client: Redis = Depends(get_redis_client)
):

    hashed_passphrase = await get_passphrase(token=secret_key, session=session_db)
    verified = verify_phrase(passphrase, hashed_passphrase)
    if not verified:
        return {'error': 'incorrect passphrase'}
    await redis_client.delete(secret_key)
    await delete_secret_db(token=secret_key, session=session_db)

    return {'message': 'данные удалены'}





