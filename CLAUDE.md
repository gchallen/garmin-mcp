# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Model Context Protocol (MCP) server that connects to Garmin Connect to expose fitness and health data to Claude and other MCP-compatible clients. The project is written in Python and uses the `garminconnect` library to authenticate and fetch data from Garmin's API.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv (required)
uv sync

# Run the MCP server directly (requires GARMIN_EMAIL and GARMIN_PASSWORD env vars)
uv run garmin-mcp
```

### Testing with MCP Inspector
```bash
npx @modelcontextprotocol/inspector python /path/to/garmin_mcp/garmin_mcp_server.py
```

## Architecture

The codebase follows a modular architecture with the main entry point at `src/garmin_mcp/__init__.py`. Key components:

1. **Main Server** (`src/garmin_mcp/__init__.py`):
   - Initializes the Garmin client with OAuth authentication
   - Configures all feature modules with the client instance
   - Creates FastMCP server and registers all tools
   - Handles token storage in `~/.garminconnect` directory

2. **Feature Modules**: Each module in `src/garmin_mcp/` handles a specific domain:
   - `activity_management.py`: Activity retrieval and management
   - `health_wellness.py`: Health metrics (steps, heart rate, sleep)
   - `user_profile.py`: User profile information
   - `devices.py`: Device management
   - `gear_management.py`: Gear tracking
   - `weight_management.py`: Body composition data
   - `challenges.py`: Challenge participation
   - `training.py`: Training plans and metrics
   - `workouts.py`: Workout management
   - `data_management.py`: Data export/import
   - `womens_health.py`: Women's health tracking

3. **Module Pattern**: Each module follows this pattern:
   - Has a global `garmin_client` variable configured by the main file
   - Exports `configure(client)` to receive the Garmin client instance
   - Exports `register_tools(app)` to register MCP tools with the FastMCP app
   - Tools are async functions decorated with `@app.tool()`

## Pagination Support

Several tools support pagination to handle large datasets efficiently:

- **get_sleep_data**: Use `part` parameter with values:
  - `"summary"`: Only essential metrics (~450 chars)
  - `"metadata"`: Basic session info
  - `"levels"`: Sleep stage transitions
  - `"metrics"`: Physiological data (HR, SpO2, stress)
  - `"page_1"`, `"page_2"`, etc.: Time-series data in 100-item chunks
  - `"full"`: Complete data (default, may be very large)

- **list_activities**: Supports `offset` and `limit` (max 100) parameters, plus `summary_only` mode

- **get_activities_by_date**: Includes `max_results` (default 50, max 100) and `summary_only` parameters

- **Time-series data tools** (heart rate, stress, steps): Support `hourly_only` parameter for aggregated data

## Important Notes

- Authentication uses OAuth tokens stored locally, with automatic MFA handling if needed
- The server is distributed as a Python package installable via `uvx`
- Date-based versioning follows YEAR.MONTH.MINOR format
- Always use virtual environments when installing Python dependencies