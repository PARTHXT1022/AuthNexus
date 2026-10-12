import time
import requests
from jose import jwt, JWTError
from app.config.loader import config

jwks_cache: dict | None = None
jwks_fetched_at: float = 0
JWKS_CACHE_TTL = 300

def get_jwks() -> dict:
    global jwks_cache, jwks_fetched_at
    if jwks_cache is None or (time.time() - jwks_fetched_at) > JWKS_CACHE_TTL:
        resp = requests.get(f"{config.ISSUER}/.well-known/jwks.json", timeout=5)
        resp.raise_for_status()
        jwks_cache = resp.json()
        jwks_fetched_at = time.time()

    return jwks_cache

class TokenVerificationError(Exception):
    pass

def verify_access_token(token: str, expected_audience: str) -> dict:
    try:
        header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise TokenVerificationError(f"malformed token: {e}")

    jwks = get_jwks()

    key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)

    if key is None:
        raise TokenVerificationError("no matching key for this token's kid")

    try:
        claims = jwt.decode(
            token,
            key, 
            algorithms=["RS256"],
            audience=expected_audience,
            issuer=config.ISSUER
        )

    except JWTError as e:
        raise TokenVerificationError(f"signature/claims verification failed: {e}")

    if claims.get("token_use") != "access":
        raise TokenVerificationError("an ID token was presented where an access token is required")

    return claims