import time
from jose import jwt
from cryptography.hazmat.primitives import serialization
from app.services.key import generate_or_load_keypair, key_id

ACCESS_TOKEN_TTL = 3600
ID_TOKEN_TTL = 3600


def _get_private_key_pem() -> str:
    private_key = generate_or_load_keypair()
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()


def create_access_token(sub: str, client_id: str, scope: str, issuer: str) -> str:
    now = int(time.time())
    claims = {
        "iss": issuer,
        "sub": sub,
        "aud": client_id,
        "scope": scope,
        "iat": now,
        "exp": now + ACCESS_TOKEN_TTL,
        "token_use": "access",
    }
    return jwt.encode(claims, _get_private_key_pem(), algorithm="RS256", headers={"kid": key_id})


def create_id_token(sub: str, client_id: str, issuer: str, nonce: str | None = None) -> str:
    now = int(time.time())
    claims = {
        "iss": issuer,
        "sub": sub,
        "aud": client_id,
        "iat": now,
        "exp": now + ID_TOKEN_TTL,
        "auth_time": now,
        "token_use": "id",
    }
    if nonce:
        claims["nonce"] = nonce
    return jwt.encode(claims, _get_private_key_pem(), algorithm="RS256", headers={"kid": key_id})