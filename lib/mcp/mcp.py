from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from lib.backend.backend_requester import BackendRequester, Response, ResponseStr
from lib.common.constants import BACKEND_HOST, BACKEND_PORT

mcp = FastMCP("notification_bot_backend")

backend_requester = BackendRequester(BACKEND_HOST, BACKEND_PORT)


@mcp.tool()
async def get_deeds_for_user(user_id: int) -> Response:
    '''return for user by it's id list of deeds with full available information'''
    response = await backend_requester.get_deed_for_user(user_id)
    return response

# add other functions
