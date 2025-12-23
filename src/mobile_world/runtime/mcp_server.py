"""MCP server for Mobile World controller operations."""

import asyncio
import concurrent.futures
import os
from collections.abc import Callable
from threading import Lock
from typing import Any

import dotenv
from fastmcp.client import Client
from loguru import logger

dotenv.load_dotenv()


DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
MODELSCOPE_API_KEY = os.getenv("MODELSCOPE_API_KEY")
MCP_CONFIG = {
    "mcpServers": {
        "amap": {
            "transport": "sse",
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
            "headers": {"Authorization": f"Bearer {DASHSCOPE_API_KEY}"},
        },
        "gitHub": {
            "transport": "http",
            "url": "https://mcp.api-inference.modelscope.net/c3c76357651542/mcp",
            "headers": {"Authorization": f"Bearer {MODELSCOPE_API_KEY}"},
        },
        "jina": {
            "transport": "http",
            "url": "https://mcp.api-inference.modelscope.net/25a924b9ce914b/mcp",
            "headers": {"Authorization": f"Bearer {MODELSCOPE_API_KEY}"},
        },
        "stockstar": {
            "transport": "sse",
            "url": "https://dashscope.aliyuncs.com/api/v1/mcps/stockstar/sse",
            "headers": {"Authorization": f"Bearer {DASHSCOPE_API_KEY}"},
        },
        "arXiv": {
            "transport": "http",
            "url": "https://mcp.api-inference.modelscope.net/d9b238e019f04e/mcp",
            "headers": {"Authorization": f"Bearer {MODELSCOPE_API_KEY}"},
        },
    }
}
CLIENT = None
client_lock = Lock()


class SyncMCPClient:
    """MCP client with sync interface. Uses persistent connection for stdio transports."""

    def __init__(self, url: str | None = None, config: dict | None = None):
        self.url = url
        self.config = config
        self.tools: list[dict[str, Any]] | None = None

        self.client = Client(config) if config else None

    async def list_tools(self) -> list[dict[str, Any]]:
        if self.client:
            try:
                async with self.client:
                    tools_result = await self.client.list_tools()
                    return [t.model_dump() for t in tools_result]

            except Exception as e:
                logger.warning(f"Failed to list tools from client: {e}")
                return []
        return []

    def _run_async_func(self, func: Callable[..., Any]) -> Any:
        try:
            asyncio.get_running_loop()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, func())
                return future.result()
        except RuntimeError:
            return asyncio.run(func())

    def list_tools_sync(self) -> list[dict[str, Any]]:
        with client_lock:
            if self.tools is not None:
                return self.tools
            self.tools = self._run_async_func(self.list_tools)
            return self.tools

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if self.client:
            try:
                async with self.client:
                    result_content = await self.client.call_tool(name, arguments, timeout=60)
                    return [t.model_dump() for t in result_content]
            except Exception as e:
                logger.warning(f"Failed to call tool {name} from client: {e} {self.config}")
                return {"result": f"Failed to call tool {name}: {e}"}
        return {"result": "No client configured"}

    def call_tool_sync(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        with client_lock:
            return self._run_async_func(lambda: self.call_tool(name, arguments))


def init_mcp_clients() -> SyncMCPClient:
    with client_lock:
        global CLIENT
        if CLIENT is None:
            CLIENT = SyncMCPClient(config=MCP_CONFIG)
        return CLIENT
