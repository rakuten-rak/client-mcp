import sys
import platform
from contextlib import AsyncExitStack
from typing import Any, Awaitable, Callable, ClassVar, Self, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """MCP Client to interact with MCP Server.
    
    Usage:
        async with MCPClient(server_path) as client:
            # Call client methods here
            pass
    """
    
    client_session: ClassVar[ClientSession]
    
    def __init__(self, server_path: str):
        self.server_path = server_path
        self.exit_stack = AsyncExitStack()
        
    async def __aenter__(self) -> Self:
        cls = type(self)
        cls.client_session = await self.connect_to_server()
        return self
        
    async def __aexit__(self, *_) -> None:
        await self.exit_stack.aclose()
        
    async def connect_to_server(self) -> ClientSession:
        try:
            # Cross-platform command setup
            if platform.system() == "Windows":
                # Windows doesn't have 'sh', use python directly
                server_params = StdioServerParameters(
                    command=sys.executable,
                    args=[self.server_path],
                    env=None
                )
            else:
                # Unix/Linux/Mac can use sh
                server_params = StdioServerParameters(
                    command="sh",
                    args=[
                        "-c",
                        f"{sys.executable} {self.server_path} 2>/dev/null",
                    ],
                    env=None
                )
            
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server=server_params)
            )
            client_session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await client_session.initialize()
            return client_session
        except Exception as e:
            raise RuntimeError(f"Error: Failed to connect to server - {e}")