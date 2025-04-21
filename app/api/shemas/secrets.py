from typing import Annotated, Optional
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl_seconds: int = 300


class SecretDelete(BaseModel):
    id: uuid4
    passphrase: str | None = None

class SecretRead(BaseModel):
    secret: str



