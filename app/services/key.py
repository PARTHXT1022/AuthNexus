import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from app.config.loader import config

key_path = Path(config.PRIVATE_KEY_PATH)  
key_id = config.KID

key_path.parent.mkdir(parents=True, exist_ok=True)


def generate_or_load_keypair() -> rsa.RSAPrivateKey:
    if key_path.exists():
        return serialization.load_pem_private_key(
            key_path.read_bytes(), password=None
        )

    new_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    key_path.write_bytes(
        new_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return new_key


def _b64url_uint(val: int) -> str:
    byte_len = (val.bit_length() + 7) // 8
    return base64.urlsafe_b64encode(val.to_bytes(byte_len, "big")).rstrip(b"=").decode()


def get_jwks() -> dict:
    private_key = generate_or_load_keypair()   
    numbers = private_key.public_key().public_numbers()
    return {
        "keys": [{
            "kty": "RSA", "use": "sig", "alg": "RS256", "kid": key_id,
            "n": _b64url_uint(numbers.n),
            "e": _b64url_uint(numbers.e),
        }]
    }