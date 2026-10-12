import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

TOKEN_ACME = "eyJhbGciOiJSUzI1NiIsImtpZCI6Im1vY2stb2lkYy1rZXktMSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAiLCJzdWIiOiJ1c2VyXzEyMyIsImF1ZCI6InRlc3QtY2xpZW50Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsImlhdCI6MTc5MTgyNzgwNiwiZXhwIjoxNzkxODMxNDA2LCJ0b2tlbl91c2UiOiJhY2Nlc3MifQ.SPXOJ7FIVPoz_8eQuhqGcJB8D3aZU1NlbcC02Iv-tQnCu3tnkFl_GuAhtZSQH5gfYOIEzJg30zsAo3CGZGZtW99c7sAhxPFP-GT1EOCP2SFHQxM1Bone463amGhK8pzXqjJZEB0mjVCW8Mq3ZwBpqya2-xnHEKzQq4pStuZCEd38-6BQg7ra_XgjqNzFN8xaHv_MtMiOMq3NPoGwrmH9nYoPoXVg0H-pwmY0txcpRJfg5sKOO9ZFrbgrLFsV2uWcop_cOIIlpQU0bJ9g5KHzwRkdUrajfKM2IfWqh_LwAlzjTsaxUawFohcn8msz50ULlszQsoljPBGPmZmhv095uA"
TOKEN_BETA = "eyJhbGciOiJSUzI1NiIsImtpZCI6Im1vY2stb2lkYy1rZXktMSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vMTI3LjAuMC4xOjgwMDAiLCJzdWIiOiJ1c2VyXzQ1NiIsImF1ZCI6InRlc3QtY2xpZW50LXR3byIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUiLCJpYXQiOjE3OTE4MjgwOTksImV4cCI6MTc5MTgzMTY5OSwidG9rZW5fdXNlIjoiYWNjZXNzIn0.eCE0EP82WQn3Lqkmz65d-9J_ewdVmNEJWDYkHbqbO0OpvRHao781SId_CcBDVIDkttuBvVOj1DjklrlxhRCr3IlVrDm8IMXUVzT8lUXrVO3Zyx3XYeI7qYRcUUcMloJ4B8O-i06djvsfRSABkmNUFQ5GP4T5xw7MMmoB2qnaEjx8-7YmHJ0ofVr92TxcG-D51-_J9sMPdjVbB25aI5M56G1o3ndcDmI9LwU2msk2Tt5OJaZ1Cr1zvYJA9oI2K8k6OlRoW_LPfCcu3KEFdsc-Ec2PI4Bm39C2ksmmTgNIDNRooyoAiaZo7IhRQYkwjSuBJ3Y1DmMZ85t3mSoQeWGm9Q"
URL = "http://127.0.0.1:8095/mcp"

def make_client(token: str | None) -> Client:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return Client(StreamableHttpTransport(URL, headers=headers))

async def call(label: str, token: str | None, tool: dict, args: dict | None = None):
    print(f"\n---------{label}---------")
    try:
        async with make_client(token) as client:
            result = await client.call_tool(tool, args or {})
            print(result.data)
    except Exception as e:
        print("REJECTED:", type(e).__name__, "-", str(e)[:200])

async def main():
    await call("ACME Token -> usage", TOKEN_ACME, "get_account_usage")
    await call("Beta token -> usage", TOKEN_BETA, "get_account_usage")
    await call("Acme token -> churn", TOKEN_ACME, "get_churn_risk_score")
    await call("Beta token -> churn", TOKEN_BETA, "get_churn_risk_score")

    await call(
        "ATTACK: Acme token + tenant_id=beta-inc argument",
        TOKEN_ACME, "get_account_usage", {"tenant_id": "beta-inc"},
    )

    await call("No token at all", None, "get_account_usage")
    await call("Garbage token", "not.a.real.token", "get_account_usage")

asyncio.run(main())