from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from app.mcp_server.data import MOCK_ACCOUNTS
from app.services.token_verifier import verify_access_token, TokenVerificationError

mcp = FastMCP(
    "saas-metrics-server"
)

def _authenticate() -> dict:
    headers = get_http_headers(include_all=True)
    auth_header = headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        raise TokenVerificationError("missing bearer token")
    token = auth_header.removeprefix("Bearer ")
    return verify_access_token(token, expected_audience="test-client")

def _get_tenant_account() -> tuple[dict | None, dict | None]:
    try:
        claims = _authenticate()
    except TokenVerificationError as e:
        return None, {"status": "error", "error": f"auth failed: {e}"}

    tenant_id = claims.get("tenant_id")
    if not tenant_id:
        return None, {"status": "error", "error": "token has no tenant_i claim"}

    account = MOCK_ACCOUNTS.get(tenant_id)
    if account is None:
        return None, {"status": "error", "error": f"no account for tenant {tenant_id}"}
    return account, None 
    
@mcp.tool()
def get_account_usage() -> dict:
    account, error = _get_tenant_account()
    if error:
        return error

    return {
        "status": "ok",
        "data": {
            "account_name": account["account_name"],
            "monthly_active_users": account["monthly_active_users"],
            "mrr": account["mrr"],
            "last_login_days_ago": account["last_login_days_ago"],
        }
    }


@mcp.tool()
def get_churn_risk_score() -> dict:
    account, error = _get_tenant_account()
    if error:
        return error

    score = account["churn_risk_score"]
    level = "high" if score >= 0.5 else "medium" if score >= 0.25 else "low"
    return {
        "status": "ok",
        "data": {
            "account_name": account["account_name"],
            "churn_risk_score": score,
            "risk_level": level,
        },
    }

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8095)