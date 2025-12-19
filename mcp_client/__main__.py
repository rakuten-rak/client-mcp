import asyncio

from mcp_client.client import MCPClient

async def main():
    # Fixed path - should match your actual server location
    async with MCPClient("./serverline/server.py") as client:
        print("Connected to the MCP Server")
        
        # Example: List available tools
        tools = await MCPClient.client_session.list_tools()
        print(f"Available tools: {tools}")
        
        # Example: List available prompts
        prompts = await MCPClient.client_session.list_prompts()
        print(f"Available prompts: {prompts}")
        
        # Example: List available resources
        resources = await MCPClient.client_session.list_resources()
        print(f"Available resources: {resources}")
        
if __name__ == "__main__":
    asyncio.run(main())