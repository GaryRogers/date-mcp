# Date MCP Server

A lightweight Model Context Protocol (MCP) server that provides comprehensive date and time information to AI assistants, built with Python and `uv` for maximum portability.

## Features

- **get_day_name**: Returns the current day of the week (e.g., "Monday")
- **get_iso_date**: Returns the current date in ISO 8601 format (YYYY-MM-DD)
- **current_time**: Returns the current local time in ISO 8601 format with timezone offset
- **current_time_utc**: Returns the current UTC time in ISO 8601 format
- **current_time_location**: Returns the current time in any supported location's timezone (e.g., "New York", "Tokyo", "London")
- **list_available_locations**: Lists all 23 pre-configured locations

Perfect for AI assistants like GitHub Copilot that need reliable, always-accurate date and time information when working on notes, documentation, scheduling, or time-sensitive tasks.

## How It Works

The server uses the standard [MCP Python SDK](https://modelcontextprotocol.io/) to expose six tools for date and time information:

- **Date tools**: Return the current day name and date in ISO 8601 format
- **Time tools**: Return current time in local timezone, UTC, or any configured location
- **Location discovery**: List all available locations for quick reference

All times are returned in ISO 8601 format with proper timezone information. The server supports 23 pre-configured locations including major US cities (New York, Chicago, Denver, Los Angeles) and global financial/cultural centers. Additional locations can be configured via environment variables.

These tools are discovered by MCP clients and can be called by the LLM when needed.

## Why This Matters

AI assistants often struggle with:
- Knowing the current date and time
- Performing date-based calculations and scheduling
- Adding accurate timestamps to content
- Determining time zones for users in different locations

By providing an MCP server with reliable date and time tools, your AI assistant (whether Copilot, Claude, or other MCP-compatible clients) always has access to accurate date/time information without relying on training data or assumptions. This is especially useful for scheduling, coordination across time zones, and time-aware task planning.

## Installing locally

This will install `date-mcp` into `$HOME/.local/bin`

```zsh
uv tool install git+https://github.com/GaryRogers/date-mcp
```

## Using with Visual Studio Code

Edit you `mcp.json` file

- In Visual Studio Code Open the Command Palate (View | Command Palate)
  - Or use `ctrl-shift-p` on Windows or `command-shift-p` on MacOS
- Type `MCP: Open User Configuration`

Example `mcp.json` (basic):

```json
{
	"servers": {
		"date-mcp": {
			"type": "stdio",
			"command": "uvx",
			"args": ["date-mcp"]
		}
	}
}
```

Example `mcp.json` (with custom locations):

```json
{
	"servers": {
		"date-mcp": {
			"type": "stdio",
			"command": "uvx",
			"args": ["date-mcp"],
			"env": {
				"DATE_MCP_LOCATIONS": "Berlin=Europe/Berlin,Barcelona=Europe/Madrid,Austin=America/Chicago"
			}
		}
	}
}
```

### Adding Custom Locations

The server comes with 23 pre-configured locations. To add more or override existing ones:

1. Set the `DATE_MCP_LOCATIONS` environment variable in your `mcp.json` file
2. Use the format: `City=IANA_Timezone,AnotherCity=IANA_Timezone`
3. Find IANA timezone names at [IANA Timezone Database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

**Pre-configured Locations (23 total):**
Chicago, Denver, Los Angeles, New York, Berlin, Cairo, Dubai, Hong Kong, Istanbul, Lagos, London, Mexico City, Moscow, Mumbai, Nairobi, Paris, São Paulo, Shanghai, Singapore, Sydney, Bangkok, Tokyo, Toronto


## Testing with the ModelContextProtocol Inspector

- Start the inspector and point it to the MCP server:
	```zsh
	npx @modelcontextprotocol/inspector uv run date-mcp
	```
	This launches a local web UI (typically at `http://localhost:5173`) where you can interact with the server.
-  In the inspector UI, you'll see all six available tools listed
-  Try the tools:
   - `get_day_name` and `get_iso_date` return day/date information
   - `current_time` and `current_time_utc` return current time
   - `current_time_location` accepts a location parameter (e.g., "Tokyo") to get time in that zone
   - `list_available_locations` shows all configured locations
-  When finished testing, close the browser tab and stop the inspector with <kbd>Ctrl+C</kbd>.
