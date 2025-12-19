from fastmcp import FastMCP, Context

mcp = FastMCP("mcp-server")

@mcp.tool()
async def echo(message:str) -> str:
    """Echo back thne message"""
    return message

@mcp.prompt()
async def greeting_prompt(name:str) -> str:
    """A Simple greeting prompt"""
    return f"Greet {name} kindly"

@mcp.resource("file://./greeting.txt")
def greeting_file() -> str:
    """The Greeting text file"""
    with open("greeting.txt","r",encoding="utf-8") as file:
        return file.read()
    
if __name__ == "__main__":
    mcp.run(transport="stdio")
    


