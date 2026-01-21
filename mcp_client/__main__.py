import asyncio
from mcp_client.cli import parse_args
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
        
    async def main() -> None:    
        """Run the MCP Client with the specified options."""
        args = parse_args()
        if not args.server_path.exists():
            print(f"Error: Server script '{args.server_path}' not found....")
            return
        
        try:
            async with MCPClient(str(args.server_path)) as client:
                if args.members:
                    await client.list_all_members()
        except RuntimeError as e:
            print(e)
        
if __name__ == "__main__":
    asyncio.run(main())