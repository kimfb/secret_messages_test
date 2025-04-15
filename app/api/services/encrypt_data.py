import uuid
import base64
import os
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def generate_key_from_passphrase(passphase: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    return base64.urlsafe_b64encode(kdf.derive(passphase.encode()))

def encrypt_secret(secret: str, passpharase: str):
    salt = os.urandom(16)
    key = generate_key_from_passphrase(passpharase, salt)
    fernet = Fernet(key)
    token = fernet.encrypt(secret.encode())

    return {
        'encrypted': token.decode(),
        'salt': base64.b64encode(salt).decode()
    }

def decrypt_secret(encrypted: str, passphrase: str, salt_b64: str):
    salt = base64.b64decode(salt_b64)
    key = generate_key_from_passphrase(passphrase, salt)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted.encode()).decode()


# k = generate_key_from_passphrase('соль', os.urandom(16))
# s = encrypt_secret('мой секрет', 'соль')
# res = decrypt_secret(s['encrypted'], 'сол', s['salt'])
# # print(k)
# print(s)
# print(res)