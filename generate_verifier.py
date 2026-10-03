import base64, hashlib, secrets
v = base64.urlsafe_b64encode(secrets.token_bytes(64)).rstrip(b'=').decode()
c = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b'=').decode()
print("VERIFIER:", v)
print("CHALLENGE:", c)