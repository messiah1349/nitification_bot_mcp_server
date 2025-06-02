# client.py
import asyncio
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

MCP_SERVER_PATH = Path(__file__).resolve().parent.parent / 'mcp' / 'mcp_server.py'

async def MCPClient():

    # This will run your server.py as a subprocess
    server_params = StdioServerParameters(
        command="python",  # or "uv" if using uv
        args=["-m", "lib.mcp.mcp_server"],  # path to your server file
        env=None,
        cwd='.',
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [tool.name for tool in tools.tools])
            
            # Call a tool
            result = await session.call_tool("get_deeds_for_user", {"user_id": "1"})
            print("Result:", result)

