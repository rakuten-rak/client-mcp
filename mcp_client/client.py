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
        
    async def list_all_members(self)->None:
        """List all tools, prompts, and resources from the MCP server."""
        print("MCP Server Members:")
        print("=" * 50)
        sections = {
            "Tools": self.client_session.list_tools,
            "Prompts": self.client_session.list_prompts,
            "Resources": self.client_session.list_resources,
        }
        for section_name, list_method in sections.items():\
            await self._list_section(section_name, list_method)
            # print(f"\n{section_name}:")
            # print("-" * 20)
        print("\n" + "=" * 50)
            # members = await list_method()
            # for member in members:
                # print(member)
        members = await self.client_session.list_members()
        for member in members:
            print(member)
    async def _list_section(
        self,
        section_name: str,
        # list_method: Callable[[], Awaitable[list[str]]],
        list_method: Callable[[], Awaitable[Any]],
    ) -> None:
        print(f"\n{section_name}:")
        print("-" * 20)
        members = await list_method() # own
        for member in members: #own
            print(member)
        try:
            items = getattr(await list_method(), section_name.lower()) #lower optional
                            # if items := "items" in dir(members) else "tools")
            if items:
                print(f"\n {section_name.upper()} ({len(items)}):")
                print("-" * 20)
                for item in items:
                    description = (item.description or "No description")
                    print(f"- {item.name}: {description}")
            else:
                # print(f"No {section_name.lower()} available.")
                print(f"\n {section_name.upper()} (0): None available.")
        except Exception as e:  
            print(f"Error retrieving {section_name.lower()}: {e}") # you can change from lower to upper optional..
                                                   
                                                #    if hasattr(item, "description")
                                                #    else "No description")
                                                