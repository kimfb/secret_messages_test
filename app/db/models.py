from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Boolean, String, func
from uuid import UUID
from app.db.base import BaseDBModel

class SecretsLog(BaseDBModel):
    __tablename__ = 'secrets_log'

    id: Mapped[int] = mapped_column(primary_key=True)
    secret_id: Mapped[int] = mapped_column(ForeignKey('secrets.id'), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    first_read: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)

    secret: Mapped['Secrets'] = relationship(back_populates='log')


class Secrets(BaseDBModel):
    __tablename__ = 'secrets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[UUID]
    secret: Mapped[str]
    # phrase: Mapped[str]

    log: Mapped['SecretsLog'] = relationship(
        back_populates='secret',
        uselist=False,
    )