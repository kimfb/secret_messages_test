import uuid
import base64
import bcrypt
import secrets
import os
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def encrypt_secret(secret: str):
    key = Fernet.generate_key()
    fernet = Fernet(key)
    token = fernet.encrypt(secret.encode())

    return {
        'encrypted': token.decode(),
        'key': base64.b64encode(key).decode()
    }

def decrypt_secret(encrypted: str, key_b64: str):
    key = base64.b64decode(key_b64)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted.encode()).decode()


def hash_phrase(phrase: str) -> str:
    return bcrypt.hashpw(phrase.encode(), bcrypt.gensalt()).decode()

def verify_phrase(phrase: str, hashed: str) -> bool:
    return bcrypt.checkpw(phrase.encode(), hashed.encode())


# k = generate_key(os.urandom(16))
# s = encrypt_secret('мой секрет')
# print(s['encrypted'])
# print(s['key'])
# res = decrypt_secret(s['encrypted'], s['key'])
# # print(k)
# print(s)
# print(res)