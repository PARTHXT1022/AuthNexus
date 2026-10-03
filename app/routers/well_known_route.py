from fastapi import APIRouter
from app.services.key import get_jwks
from app.config.loader import config

issuer_url = config.ISSUER

router = APIRouter(
    prefix="/api/v1",
    tags = ["Discovery"]
)

@router.get("/.well-known/jwks.json")
def json():
    return get_jwks()

@router.get("/.well-known/openid_configuration")
def discovery():
    return {
        "issuer": issuer_url,
        "authorization_endpoint": f"{issuer_url}/authorize",
        "token_endpoint": f"{issuer_url}/token",
        "jwks_uri": f"{issuer_url}/.well-known/jwks.json",
        "response_types_supported": ["code"],
        "code_challenge_methods_supported": ["S256"],
        "grant_types_supported": ["authorization_code"],
        "id_token_signing_alg_values_supported": ["RS256"],
    } 
