from datetime import datetime

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import Request

from app.db.models import SecretsLog, Secrets

async def create_secret_db(
        session: AsyncSession,
        hashed_phrase: str,
        token: str,
        request: Request
):

    secret_new = Secrets(
        token=token,
        phrase=hashed_phrase
    )

    log_new = SecretsLog(
        ip_creator=request.client.host,
        secret=secret_new
    )
    session.add(secret_new)
    await session.commit()
    return {
        'status': 'Данные сохранены',
        'token': token}



async def get_secret_db(
        session: AsyncSession,
        token: str
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

    if not secret:
        return {"error": 'нет данных'}

    secret_log = secret.log
    secret_log.first_read = datetime.now()

    await session.commit()
    return {'status': 'Данные прочитаны'}




async def delete_secret_db(
        token: str,
        session: AsyncSession,
        request: Request
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
        secret_log.ip_deleted_by = request.client.host
        await session.commit()

        return {'status': 'данные удалены'}

    return {'error': 'нет данных'}



async def get_passphrase(
        token: str,
        session: AsyncSession
):
    stmt = select(Secrets).where(
        Secrets.token == token
    )
    res = await session.execute(stmt)
    hashed_phrase = res.scalar_one_or_none().phrase
    print(hashed_phrase)
    return hashed_phrase
