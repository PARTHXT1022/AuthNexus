import secrets
import time
import base64
import hashlib
from typing import Optional
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import RedirectResponse
from app.config.loader import config
from app.services.jwt_service import create_access_token, create_id_token

router = APIRouter(
    prefix='/api/v1',
    tags=["Key Routes"]
)

CODE_TTL = 60
REFRESH_TOKEN_TTL = 60 * 60 * 24 * 14  
issuer_url = config.ISSUER

AUTH_CODE_STORE: dict[str, dict] = {}
REFRESH_TOKEN_STORE: dict[str, dict] = {}


def issue_refresh_token(sub: str, client_id: str) -> str:
    token = secrets.token_urlsafe(32)
    REFRESH_TOKEN_STORE[token] = {
        "sub": sub,
        "client_id": client_id,
        "expires_at": time.time() + REFRESH_TOKEN_TTL,
        "revoked": False,
    }
    return token


@router.get("/authorize")
def authorize(
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str,
    code_challenge_method: str,
    scope: str = "openid profile"
):
    if response_type != "code":
        raise HTTPException(400, detail="only 'code' response_type is supported")
    if code_challenge_method != "S256":
        raise HTTPException(400, detail="only S256 PKCE method is supported")

    issued_code = secrets.token_urlsafe(24)
    AUTH_CODE_STORE[issued_code] = {
        "client_id": client_id,          
        "redirect_uri": redirect_uri,    
        "code_challenge": code_challenge,
        "sub": "user_123",
        "expires_at": time.time() + CODE_TTL,
        "used": False,
    }
    # return RedirectResponse(f"{redirect_uri}?code={issued_code}&state={state}")
    return {
        "code": issued_code,
        "state": state,
        "note": "In production this would be a 307 redirect to redirect_uri with these as query params."
    }

@router.post("/token")
def token(
    grant_type: str = Form(...),
    client_id: str = Form(...),
    code: Optional[str] = Form(None),
    redirect_uri: Optional[str] = Form(None),
    code_verifier: Optional[str] = Form(None),
    refresh_token: Optional[str] = Form(None),
):
    if grant_type == "authorization_code":
        if not (code and redirect_uri and code_verifier):
            raise HTTPException(400, {"error": "invalid_request", "detail": "code, redirect_uri, code_verifier required"})

        entry = AUTH_CODE_STORE.get(code)

        if entry is None:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "unknown code"})
        if entry["used"]:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "code already used"})
        if time.time() > entry["expires_at"]:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "code expired"})
        if entry["redirect_uri"] != redirect_uri or entry["client_id"] != client_id:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "client/redirect mismatch"})

        computed_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode("ascii")).digest()
        ).rstrip(b"=").decode()

        if computed_challenge != entry["code_challenge"]:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "PKCE verification failed"})

        entry["used"] = True

        access_token = create_access_token(sub=entry["sub"], client_id=client_id, scope="openid profile", issuer=issuer_url)
        id_token = create_id_token(sub=entry["sub"], client_id=client_id, issuer=issuer_url)
        new_refresh_token = issue_refresh_token(sub=entry["sub"], client_id=client_id)

        return {
            "access_token": access_token,
            "id_token": id_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }

    elif grant_type == "refresh_token":
        if not refresh_token:
            raise HTTPException(400, {"error": "invalid_request", "detail": "refresh_token required"})

        entry = REFRESH_TOKEN_STORE.get(refresh_token)
        if entry is None or entry["revoked"]:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "unknown or revoked refresh token"})
        if time.time() > entry["expires_at"]:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "refresh token expired"})
        if entry["client_id"] != client_id:
            raise HTTPException(400, {"error": "invalid_grant", "detail": "client mismatch"})

        entry["revoked"] = True  

        new_access_token = create_access_token(sub=entry["sub"], client_id=client_id, scope="openid profile", issuer=issuer_url)
        new_refresh_token = issue_refresh_token(sub=entry["sub"], client_id=client_id)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "Bearer",
            "expires_in": 3600,
        }

    else:
        raise HTTPException(400, {"error": "unsupported_grant_type"})