import argparse
import sys
import asyncio
import platform
import pathlib

def parse_args():
    parser = argparse.ArgumentParser(description="MCP Client CLI")
    parser.add_argument(
        "server_path",
        # type=str,
        type=pathlib.Path,
        help="Path to the MCP server script",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        
        # "--list-tools",
        # "--menu-tools",
        "--members",
        action="store_true",
        # help="List available tools from the MCP server",
        help="List the MCP Server's tools, prompts, and resources",
    )
    return parser.parse_args()