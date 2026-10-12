from pydantic import BaseModel

class Keys(BaseModel):
    KEY_DIR: str = "D:/Saas_security_application/app/keys"
    PRIVATE_KEY_PATH: str = "D:/Saas_security_application/app/keys/private_keys/private_key.pem"
    KID: str = "mock-oidc-key-1"
    ISSUER: str = "http://127.0.0.1:8000"