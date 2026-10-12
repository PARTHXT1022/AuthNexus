import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport

ACCESS_TOKEN_USER_123 = "eyJhbGciOiJSUzI1NiIsImtpZCI6Im1vY2stb2lkYy1rZXktMSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjkwMDAiLCJzdWIiOiJ1c2VyXzEyMyIsImF1ZCI6InRlc3QtY2xpZW50Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsImlhdCI6MTc5MTExMjE2NCwiZXhwIjoxNzkxMTE1NzY0LCJ0b2tlbl91c2UiOiJhY2Nlc3MifQ.Zu1Fa7dWse53YZXWtibTRJmUth9l4qAQFJjnR_V83nIpn0UbFMSQ8AHZloz56wYbNWrRQxwECsvGvNiipm7bz0_-LKdFKEhWV-H2PDGYSfdxPGMIXUdNFzfzP9GvRbzFC-J6SNO1nvvU7PjKZksZuPA5M-hnXU4mrvVIhE07Wm9yqhthdyMnrnaytLOJAWSFxqoKhE7ix6tnleGubPoAJovl7dAqFAva-3Z9nFCBK_pxr0kUBsyodLkbVAW7s6kTumT_7jp8t4A5u5nU0e5CxaXltR65YhzDu2vPUFvi6Cz4ma9vzRa-jqFUanRVELU26PKNY7cskX3Xl1yX00w__g"

async def main():
    transport = StreamableHttpTransport(
        "http://127.0.0.1:8095/mcp",   
        headers={"Authorization": f"Bearer {ACCESS_TOKEN_USER_123}"},
    )
    async with Client(transport) as client:
        result = await client.call_tool("get_account_usage", {})
        print(result)

asyncio.run(main())