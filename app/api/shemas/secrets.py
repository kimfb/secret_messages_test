from typing import Annotated, Optional
from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl_seconds: int = 300

class SecretResponse(BaseModel):
    id: uuid4

class SecretRead(BaseModel):
    secret: str



