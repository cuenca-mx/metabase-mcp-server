# Metabase MCP Server

This project implements an MCP server to interact with the [Metabase API](https://www.metabase.com/), exposing key functionality via a MCP interface.

## Features

- 🔍 List Metabase cards
- 🗄️ List available databases
- 📊 Execute queries on cards
- 🧾 Run arbitrary queries
- 📝 Create new cards
- 🔖 Create bookmark
- 📁 List collections

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cuenca-mx/metabase-mcp-server.git
cd metabase-mcp-server
```

2. Configure your AI assistant client ([Claude](https://modelcontextprotocol.io/quickstart/user), [Cursor](https://docs.cursor.com/context/model-context-protocol), etc.) by adding the following configuration:

```json
{
    "mcpServers": {
        "metabase": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER/metabase_mcp_server",
                "run",
                "app.py"
            ],
            "env": {
                "METABASE_URL": "https://metabase.domain.com/",
                "METABASE_API_KEY": "your-secret-api-key"
            }
        }
    }
}
```

## Development Setup

This project uses a Makefile to simplify development tasks:

```bash
make install
```

### Environment Variables

Configure required environment variables:

```bash
export $(<env.template)
```

### Running Tests

The project uses `pytest` for unit testing:

```bash
pytest
```

### Debugging with MCP Inspector

Use the [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) for testing and debugging:

```bash
make dev
```
