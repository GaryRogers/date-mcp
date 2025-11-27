# Agent Guidelines for date-mcp

## Repository Purpose

This repository implements a **Model Context Protocol (MCP) server** that provides date and time information tools. The server exposes six tools:

1. **get_day_name** - Returns the current day of the week (e.g., "Monday")
2. **get_iso_date** - Returns the current date in ISO 8601 format (YYYY-MM-DD)
3. **current_time** - Returns the current local time in ISO 8601 format with timezone offset
4. **current_time_utc** - Returns the current time in UTC in ISO 8601 format
5. **current_time_location** - Returns the current time in a specified location's timezone
6. **list_available_locations** - Lists all supported locations for the current_time_location tool

The MCP server communicates via standard I/O (stdio) and is designed to be integrated with AI applications and LLM clients as a tool provider.

## Project Structure

```
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # User-facing documentation
├── src/
│   └── date_mcp/
│       ├── __init__.py     # Package initialization
│       ├── main.py         # Entry point
│       └── server.py       # MCP server implementation
```

## Development Ground Rules

### Code Quality
- Keep the codebase minimal and focused on MCP server functionality
- Maintain clear separation between tool definitions and tool implementations
- Use type hints throughout the codebase
- Follow PEP 8 style guidelines

### Tool Development
- Each tool must have a clear `description` and `inputSchema`
- Tool handlers must return `list[TextContent]` with proper text responses
- Raise `ValueError` for unknown or invalid tool calls
- Keep tool logic simple and deterministic (no external dependencies unless necessary)

### Testing & Validation
- Ensure tools return consistent, predictable output
- Test server startup and stdio communication
- Verify tool descriptions are accurate and helpful

### Dependencies
- Minimize external dependencies
- Use `mcp` library as the core dependency
- Any new dependencies must be justified and added to `pyproject.toml`

### Documentation
- Keep comments focused on the "why" not the "what"
- Update README.md when adding new tools or features
- Maintain this AGENT.md as the source of truth for development guidelines

### Breaking Changes
- Changing tool names or schemas breaks client compatibility
- Tool removal is a breaking change
- Coordinate any breaking changes carefully

## Configuration

### Adding Custom Locations

The server comes with 23 pre-configured locations (US major cities, capitals, and major financial centers). To add custom locations or override existing ones, use the `DATE_MCP_LOCATIONS` environment variable.

**Format:**
```
DATE_MCP_LOCATIONS="City=IANA_Timezone,AnotherCity=IANA_Timezone"
```

**Example in mcp.json:**
```json
{
  "servers": {
    "date-mcp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["date-mcp"],
      "env": {
        "DATE_MCP_LOCATIONS": "Berlin=Europe/Berlin,Barcelona=Europe/Madrid,Sydney=Australia/Sydney"
      }
    }
  }
}
```

**Finding IANA Timezone Names:**
- Use the `list_available_locations` tool to see currently configured locations
- For unknown locations, the `current_time_location` tool will return an error message with suggestions on how to configure them
- Full IANA timezone database: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

**Pre-configured Locations:**
Chicago, Denver, Los Angeles, New York, Berlin, Cairo, Dubai, Hong Kong, Istanbul, Lagos, London, Mexico City, Moscow, Mumbai, Nairobi, Paris, São Paulo, Shanghai, Singapore, Sydney, Bangkok, Tokyo, Toronto

### Future Enhancements
When extending this server:
- Add new tools following the existing pattern (list_tools + call_tool handlers)
- Consider tool parameters for customization (e.g., timezone support)
- Maintain backward compatibility with existing tools when possible
- Update documentation for any new capabilities

## Integration Notes

This MCP server is designed to work with:
- AI applications using the Model Context Protocol
- LLM clients that support MCP tool calling
- Any system that communicates via stdio-based MCP

When integrating, clients should:
- Launch the server via the Python entry point
- Communicate using the MCP protocol via stdin/stdout
- Handle tool responses as plain text

