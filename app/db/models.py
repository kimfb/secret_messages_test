from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, String, func
from app.db.base import BaseDBModel

class SecretsLog(BaseDBModel):
    __tablename__ = 'secrets_log'

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    first_read: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip: Mapped[str | None] = mapped_column(String, nullable=True)