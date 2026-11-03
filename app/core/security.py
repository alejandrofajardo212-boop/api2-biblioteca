from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()   # Argon2

def hashear_password(password: str) -> str:
    return password_hash.hash(password)

def verificar_password(password: str, hash_guardado: str) -> bool:
    return password_hash.verify(password, hash_guardado)

import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import get_settings

settings = get_settings()

def crear_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def crear_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)