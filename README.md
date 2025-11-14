# Date MCP Server

A lightweight Model Context Protocol (MCP) server that provides current date and day information to AI assistants, built with Python and `uv` for maximum portability.

## Features

- **get_day_name**: Returns the current day of the week (e.g., "Monday")
- **get_iso_date**: Returns the current date in ISO 8601 format (YYYY-MM-DD)

Perfect for AI assistants like GitHub Copilot that need reliable, always-accurate date information when working on notes, documentation, or time-sensitive tasks.

## How It Works

The server uses the standard [MCP Python SDK](https://modelcontextprotocol.io/) to expose two simple tools:

- **get_day_name()**: Uses `datetime.now().strftime("%A")` to return the current day
- **get_iso_date()**: Uses `datetime.now().strftime("%Y-%m-%d")` to return the current date

These tools are discovered by MCP clients and can be called by the LLM when needed.

## Why This Matters

AI assistants often struggle with:
- Knowing the current date
- Performing date-based calculations
- Adding accurate timestamps to content

By providing an MCP server with reliable date tools, your AI assistant (whether Copilot, Claude, or other MCP-compatible clients) always has access to accurate date information without relying on training data or assumptions.

## Installing locally

This will install `date-mcp` into `$HOME/.local/bin`

```zsh
uv tool install ~/source/date-mcp
```

## Using with Visual Studio Code

Edit you `mcp.json` file

- In Visual Studio Code Open the Command Palate (View | Command Palate)
  - Or use `ctrl-shit-p` on Windows or `command-shift-p` on MacOS
- Type `MCP: Open User Configuration`

Example `mcp.json`:

```json
{
	"servers": {
		"date-mcp": {
			"type": "stdio",
			"command": "uvx",
			"args": [
				"date-mcp"
			]
		}
	},
	"inputs": []
}
```


## Testing with the ModelContextProtocol Inspector

- Start the inspector and point it to the MCP server:
	```zsh
	npx @modelcontextprotocol/inspector uv run date-mcp
	```
	This launches a local web UI (typically at `http://localhost:5173`) where you can interact with the server.
-  In the inspector UI, you'll see the available tools listed. Click on `get_day_name` and `get_iso_date` to invoke them and verify they return the current weekday and ISO date respectively.
-  When finished testing, close the browser tab and stop the inspector with <kbd>Ctrl+C</kbd>.
