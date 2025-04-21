from datetime import datetime
from http.client import responses
from logging import setLoggerClass
from xmlrpc.client import DateTime

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Request
from app.core.db_helper import db_helper
from app.api.shemas.secrets import SecretCreate
from app.db.models import SecretsLog, Secrets

async def create_secret_db(
        session: AsyncSession,
        # secret: SecretCreate,
        hashed_phrase: str,
        token: str,
        request: Request
):

    # secret_cur = select(Secrets).where(
    #     Secrets.secret == secret_enc['encrypted']
    # )
    # res = await session.execute(secret_cur)
    # secret_cur = res.scalar_one_or_none()
    #
    # if secret_cur is not None:
    #     return {'error': "Секрет уже существует"}

    secret_new = Secrets(
        token=token,
        phrase=hashed_phrase
    )

    log_new = SecretsLog(
        ip=request.client.host,
        secret=secret_new
    )
    session.add(secret_new)
    #session.add(log_new)
    await session.commit()
    return 'Данные сохранены'


async def get_secret_db(
        session: AsyncSession,
        token: str,
        request: Request
):
    stmt = (
     select(Secrets)
     .join(Secrets.log)
     .options(selectinload(Secrets.log))
     .where(
        Secrets.token == token,
        SecretsLog.first_read == None,
        SecretsLog.deleted == False,
    ))

    res = await session.execute(stmt)
    secret = res.scalar_one_or_none()
    if secret:
        secret_log = secret.log
        secret_log.first_read = datetime.now()

        await session.commit()
        return {'message': 'ok'}

    return {"error": 'нет данных'}


async def delete_secret_db(
        token: str,
        session: AsyncSession,
):
    stmt = (
        select(SecretsLog)
        .join(Secrets)
        .options(selectinload(SecretsLog.secret))
        .where(
            Secrets.token == token,
            SecretsLog.deleted == False,
        )
    )
    res = await session.execute(stmt)
    secret_log = res.scalar_one_or_none()
    if secret_log:
        secret_log.deleted_at = datetime.now()
        secret_log.deleted = True
        await session.commit()

        return {'message': 'ok'}

    return {'error': 'нет данных'}



async def get_passphrase(
        session: AsyncSession,
        token: str
):
    stmt = select(Secrets).where(
        Secrets.token == token
    )
    res = await session.execute(stmt)
    hashed_phrase = res.scalar_one_or_none().phrase
    print(hashed_phrase)
    return hashed_phrase
