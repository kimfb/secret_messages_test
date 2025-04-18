from datetime import datetime
from http.client import responses

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from app.core.db_helper import db_helper
from app.api.shemas.secrets import SecretCreate
from app.db.models import SecretsLog, Secrets

async def create_secret_db(
        session: AsyncSession,
        # secret: SecretCreate,
        secret_enc: dict,
        token: str,
        request: Request
):

    secret_cur = select(Secrets).where(
        Secrets.secret == secret_enc['encrypted']
    )
    res = await session.execute(secret_cur)
    secret_cur = res.scalar_one_or_none()

    if secret_cur is not None:
        return {'error': "Секрет уже существует"}

    secret_new = Secrets(
        token=token,
        secret=secret_enc['encrypted']
    )

    log_new = SecretsLog(
        ip=request.client.host,
        secret=secret_new
    )
    session.add(secret_new)
    session.add(log_new)
    await session.commit()
    return secret_new



