import uuid
import base64
import bcrypt


from cryptography.fernet import Fernet


def encrypt_secret(secret: str) -> dict:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    token = fernet.encrypt(secret.encode())

    return {
        'encrypted': token.decode(),
        'key': base64.b64encode(key).decode()
    }

def decrypt_secret(encrypted: str, key_b64: str) -> str:
    key = base64.b64decode(key_b64)
    fernet = Fernet(key)
    return fernet.decrypt(encrypted.encode()).decode()


def hash_phrase(phrase: str) -> str:
    return bcrypt.hashpw(phrase.encode(), bcrypt.gensalt()).decode()

def verify_phrase(phrase: str, hashed: str) -> bool:
    return bcrypt.checkpw(phrase.encode(), hashed.encode())

