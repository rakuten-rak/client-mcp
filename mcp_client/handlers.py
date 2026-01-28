import json
import os

from mcp import ClientSession
from openai import OpenAI

MODEL = "gpt-4o-mini"
MAX_TOKENS = 1000

class OpenAiQueryHandler:
    """Handler OpenAi API interactions and MCP tool executions"""
    
    def __init__ (self,client_session: ClientSession):
        self.client_session = client_session
        if not (api_key := os.getenv("OPENAI_API_KEY")):
            raise ValueError("Error: OPENAI_API_KEY environment variable not set")
        
        self.openai_client = OpenAI(api_key=api_key)
        
    async def process_query(self, query:str) -> str:
        """Process a query using OpenAI and available MCP tools.
        Get initail model's response and decision on tool calls.."""
        messages = [{"role":"user","content":query}]
        initail_response = self.openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS,
            tools=await self._get_tools(),
        )
        current_response_message = initail_response.choices[0].message
        result_parts = []
        if current_response_message.content:
            result_parts.append(current_response_message.content)
            
        # this is going to handle tool calls if any
        if tool_calls := current_response_message.tool_calls:
            messages.append({
                "role":"assistant",
                "content":current_response_message.content or "",
                "tool_calls":tool_calls
            })
            
            # Execute tool calls and get results
            for tool_call in tool_calls:
                tool_result = await self._execute_tool_call(tool_call)
                result_parts.append(tool_result["log"])
                messages.append(tool_result["message"])
                
            # Getting final model's respnose after tool executions
            final_response = self.openai_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS
            )
            
            if content := final_response.choices[0].message.content:
                result_parts.append(content)
                
        return "Assistant : " + "\n".join(result_parts)
        
        
        
        
        
    
    # def __init__(self, api_key: str):
    #     self.client = OpenAI(api_key=api_key)

    # def query(self, prompt: str) -> str:
    #     response = self.client.chat.completions.create(
    #         model=MODEL,
    #         messages=[{"role": "user", "content": prompt}],
    #         max_tokens=MAX_TOKENS
    #     )
    #     return response.choices[0].message['content']