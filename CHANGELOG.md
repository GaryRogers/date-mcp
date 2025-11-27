# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-27

### Added

- **Four new time-related tools** providing comprehensive time information:
  - `current_time`: Returns the current local time in ISO 8601 format with timezone offset
  - `current_time_utc`: Returns the current UTC time in ISO 8601 format
  - `current_time_location`: Returns the current time in any supported location's timezone
  - `list_available_locations`: Lists all pre-configured and custom locations

- **Global timezone support** with 23 pre-configured locations including:
  - **US cities**: New York, Chicago, Denver, Los Angeles (all major US timezones)
  - **Global hubs**: London, Paris, Berlin, Tokyo, Sydney, Shanghai, Singapore, Dubai, Hong Kong, Toronto, São Paulo, Mexico City, Mumbai, Bangkok, Istanbul, Moscow, Cairo, Lagos, Nairobi

- **Environment variable configuration** via `DATE_MCP_LOCATIONS` to add or override locations:
  - Format: `City=IANA_Timezone,AnotherCity=IANA_Timezone`
  - Supports case-insensitive location lookup
  - Merges with pre-configured locations while allowing overrides

- **Helpful error messages** for unknown locations that include:
  - Sample of 5 available locations
  - Instructions for adding new locations
  - Example mcp.json configuration showing environment variable setup

- **AGENT.md** document with:
  - Development guidelines and ground rules
  - Tool documentation
  - Configuration instructions for custom locations
  - Integration notes for MCP clients

### Changed

- Updated README.md with comprehensive documentation of all six tools
- Enhanced documentation with configuration examples and use case descriptions
- Expanded "Why This Matters" section to cover scheduling and multi-timezone coordination

### Technical Details

- Added `zoneinfo` (Python 3.11+ built-in) for IANA timezone support
- Added `os` module for environment variable configuration
- Implemented case-insensitive location lookup with fallback error handling
- All time outputs comply with ISO 8601 standard with timezone information
- Backward compatible - existing tools (get_day_name, get_iso_date) unchanged

## [0.1.0] - 2025-11-14

### Initial Release

- **Two date tools** providing basic date information:
  - `get_day_name`: Returns the current day of the week
  - `get_iso_date`: Returns the current date in ISO 8601 format (YYYY-MM-DD)

- **MCP Server Implementation**:
  - Standard stdio-based MCP communication
  - Tool discovery via @app.list_tools()
  - Tool execution via @app.call_tool()
  - Minimal dependencies (only requires `mcp>=1.21.1`)

- **Project Structure**:
  - Python 3.11+ requirement
  - Packaged with `uv` for portability
  - Clean separation between server configuration and implementation

- **Documentation**:
  - README.md with installation and usage instructions
  - MCP Inspector integration guide
  - VS Code mcp.json configuration example

- **GitHub Repository**: Ready for public distribution via `uv tool install`
