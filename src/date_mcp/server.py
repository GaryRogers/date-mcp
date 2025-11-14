"""
MCP server that provides current date information tools.
Exposes two tools: get_day_name and get_iso_date
"""

import asyncio
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Initialize MCP server
app = Server("date-mcp")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_day_name",
            description="Get the name of the current day of the week",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_iso_date",
            description="Get the current date in ISO 8601 format (YYYY-MM-DD)",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "get_day_name":
        day_name = datetime.now().strftime("%A")
        return [TextContent(type="text", text=day_name)]
    elif name == "get_iso_date":
        iso_date = datetime.now().strftime("%Y-%m-%d")
        return [TextContent(type="text", text=iso_date)]
    else:
        raise ValueError(f"Unknown tool: {name}")


def main():
    """Initialize and run the MCP server."""
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
