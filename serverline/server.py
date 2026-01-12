import os
from pathlib import Path
# from fastmcp import FastMCP, Context
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-server")

@mcp.tool()
async def echo(message: str) -> str:
    """Echo back the message"""
    return message

@mcp.prompt()
async def greeting_prompt(name: str) -> str:
    """A simple greeting prompt"""
    return f"Greet {name} kindly"

@mcp.resource("file://./greeting.txt")
def greeting_file() -> str:
    """The greeting text file"""
    greeting_path = Path(__file__).parent / "greeting.txt"
    
    try:
        # Create greeting.txt if it doesn't exist
        if not greeting_path.exists():
            with open(greeting_path, "w", encoding="utf-8") as file:
                file.write("Hello! Welcome to Dana-MCP!")
        
        with open(greeting_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"Error reading greeting file: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")