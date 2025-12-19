import asyncio

from mcp_client.client import MCPClient

async def main():
    async with MCPClient("./serverline/server.py"):
        print("connected to the MCP Server")
        
if __name__ == "__main__":
    asyncio.run(main())