from app.services.token_verifier import verify_access_token, TokenVerificationError

token = input("Paste an access_token: ").strip()
try:
    claims = verify_access_token(token, expected_audience="test-client")
    print("Valid. Claims:", claims)
except TokenVerificationError as e:
    print("Rejected:", e)