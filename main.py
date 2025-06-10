import asyncio
from lib.mcp_client.mcp_client import MCPClient

async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()
        await client.proceed_query('how many deeds has user with user id = 1')
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
