"""
MCP server that provides date and time information tools.
Exposes six tools: get_day_name, get_iso_date, current_time, current_time_utc, 
current_time_location, and list_available_locations
"""

import asyncio
import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, GetPromptResult, PromptMessage


# Base location to timezone mapping (capitals and major financial centers)
LOCATION_MAP = {
    "New York": "America/New_York",
    "Chicago": "America/Chicago",
    "Denver": "America/Denver",
    "Los Angeles": "America/Los_Angeles",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Shanghai": "Asia/Shanghai",
    "Singapore": "Asia/Singapore",
    "Dubai": "Asia/Dubai",
    "Hong Kong": "Asia/Hong_Kong",
    "Toronto": "America/Toronto",
    "São Paulo": "America/Sao_Paulo",
    "Mexico City": "America/Mexico_City",
    "Mumbai": "Asia/Kolkata",
    "Bangkok": "Asia/Bangkok",
    "Istanbul": "Europe/Istanbul",
    "Moscow": "Europe/Moscow",
    "Cairo": "Africa/Cairo",
    "Lagos": "Africa/Lagos",
    "Nairobi": "Africa/Nairobi",
}

INSTRUCTIONS = """
This server provides tools for retrieving date and time information.
- Use 'get_day_name' to find out the day of the week.
- Use 'current_time_location' for specific city times.
- Always prefer ISO 8601 format for dates.
"""

# Load environment variable overrides
_env_locations = os.getenv("DATE_MCP_LOCATIONS", "")
if _env_locations:
    for entry in _env_locations.split(","):
        entry = entry.strip()
        if "=" in entry:
            city, tz = entry.split("=", 1)
            LOCATION_MAP[city.strip()] = tz.strip()


def get_timezone_from_location(location: str) -> str:
    """
    Get timezone for a location (case-insensitive).
    Raises ValueError with helpful suggestions if not found.
    """
    # Try exact match first, then case-insensitive
    if location in LOCATION_MAP:
        return LOCATION_MAP[location]
    
    # Case-insensitive search
    for city, tz in LOCATION_MAP.items():
        if city.lower() == location.lower():
            return tz
    
    # Not found - provide helpful error message
    sample_cities = list(LOCATION_MAP.keys())[:5]
    sample_list = ", ".join(sample_cities)
    
    error_msg = (
        f"Unknown location: '{location}'. Available locations include: {sample_list}, and more.\n\n"
        f"To add '{location}', configure the DATE_MCP_LOCATIONS environment variable in your mcp.json:\n\n"
        f'{{\n'
        f'  "servers": {{\n'
        f'    "date-mcp": {{\n'
        f'      "type": "stdio",\n'
        f'      "command": "uvx",\n'
        f'      "args": ["date-mcp"],\n'
        f'      "env": {{\n'
        f'        "DATE_MCP_LOCATIONS": "{location}=<IANA_TIMEZONE>"\n'
        f'      }}\n'
        f'    }}\n'
        f'  }}\n'
        f'}}\n\n'
        f"For example, to add Vienna: DATE_MCP_LOCATIONS=\"Vienna=Europe/Vienna\"\n"
        f"For multiple locations: DATE_MCP_LOCATIONS=\"Vienna=Europe/Vienna,Sydney=Australia/Sydney\""
    )
    raise ValueError(error_msg)


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
        ),
        Tool(
            name="current_time",
            description="Get the current time in local timezone in ISO 8601 format with timezone offset",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="current_time_utc",
            description="Get the current time in UTC in ISO 8601 format",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="current_time_location",
            description="Get the current time in a specified location's timezone in ISO 8601 format",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name (e.g., 'New York', 'London', 'Tokyo')"
                    }
                },
                "required": ["location"]
            }
        ),
        Tool(
            name="list_available_locations",
            description="List all available locations for current_time_location tool",
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
    elif name == "current_time":
        # Local time with timezone offset in ISO 8601 format
        now = datetime.now(timezone.utc).astimezone()
        current_time = now.isoformat()
        return [TextContent(type="text", text=current_time)]
    elif name == "current_time_utc":
        # UTC time in ISO 8601 format
        now = datetime.now(timezone.utc)
        current_time = now.isoformat().replace("+00:00", "Z")
        return [TextContent(type="text", text=current_time)]
    elif name == "current_time_location":
        # Time in specified location's timezone
        location = arguments.get("location")
        if not location:
            raise ValueError("location parameter is required")
        
        tz_name = get_timezone_from_location(location)
        tz = ZoneInfo(tz_name)
        now = datetime.now(tz)
        current_time = now.isoformat()
        return [TextContent(type="text", text=current_time)]
    elif name == "list_available_locations":
        # List all available locations
        sorted_locations = sorted(LOCATION_MAP.keys())
        locations_text = "\n".join(sorted_locations)
        return [TextContent(type="text", text=locations_text)]
    else:
        raise ValueError(f"Unknown tool: {name}")


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="date-summary",
            description="Get a summary of the current date and time",
            arguments=[]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Handle prompt requests."""
    if name == "date-summary":
        return GetPromptResult(
            description="Date Summary",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text="Please provide a summary of the current date, time in UTC, and day of the week."
                    )
                )
            ]
        )
    raise ValueError(f"Unknown prompt: {name}")


def main():
    """Initialize and run the MCP server."""
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="date-mcp",
                    server_version="0.3.0",
                    capabilities=app.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                    instructions=INSTRUCTIONS
                )
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
