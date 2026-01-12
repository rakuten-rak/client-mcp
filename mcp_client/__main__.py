import asyncio

from mcp_client.client import MCPClient

async def main():
    
    async with MCPClient("./serverline/server.py") as client:
        print("Connected to the MCP Server")
        
       
        tools = await MCPClient.client_session.list_tools()
        print(f"Available tools: {tools}")
        
        
        prompts = await MCPClient.client_session.list_prompts()
        print(f"Available prompts: {prompts}")
        
      
        resources = await MCPClient.client_session.list_resources()
        print(f"Available resources: {resources}")
        
if __name__ == "__main__":
    asyncio.run(main())