# client.py
import asyncio
from pathlib import Path
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from lib.llm_agents.base_llm_agent import BaseLLMAgent
from lib.llm_agents.open_ai_llm_agent import OpenAILLMAgent

MCP_SERVER_PATH = Path(__file__).resolve().parent.parent / 'mcp' / 'mcp_server.py'

async def MCPClient_f():

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


class MCPClient:
    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm_agent: BaseLLMAgent = OpenAILLMAgent()

    async def connect_to_server(self) -> None:

        server_params = StdioServerParameters(
            command="python",
            args=["-m", "lib.mcp.mcp_server"],
            env=None,
            cwd='.',
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def proceed_query(self, query: str) -> str:
        messages = [
            {
                'role': 'user',
                'content': query,
            }
        ]

        response = await self.session.list_tools()
        available_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            } for tool in response.tools
        ]

        print(f"{available_tools=}")

        response = self.llm_agent.call(
            messages=messages,
            tools=available_tools,
        )

        print(f"{response.output=}")

    async def cleanup(self) -> None:
        await self.exit_stack.aclose()

