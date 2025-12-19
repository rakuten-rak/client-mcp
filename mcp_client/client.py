import sys
from contextlib import AsyncExitStack
from typing import Any,Awaitable,Callable,ClassVar,Self
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """MCP Client to intereact with MCP Server...
    
    Usage:
        async with MCPClient (server_path) as client:
            # Call client methods here....
            # """
            
            
            
            
    client_session:ClassVar[ClientSession]
    def __init__(self,server_path:str):
        self.server_path = server_path
        self.exit_stack = AsyncExitStack()
    async def __aenter__(self) -> Self:
        cls = type(self)
        cls.client_session = await self.connect_to_server()
        return self
    async def __aexit__(self,*_) -> None:
        await self.exit_stack.aclose()
        
    async def connect_to_server(self) -> ClientSession:
        try:
            read,write = await self.exit_stack.enter_async_context(
                stdio_client(
                    server=StdioServerParameters(
                        command="sh",
                        args=[
                            "-c",
                            f"{sys.executable} {self.server_path} 2>/dev/null",
                        ],
                        env=None
                    )
                )
            )
            client_session = await self.exit_stack.enter_async_context(
                ClientSession(read,write)
            )
            await client_session.initialize()
            return client_session
        except Exception:
            raise RuntimeError("Error: Failed to connect to server")
         
    