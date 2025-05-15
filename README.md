# Metabase MCP Server

This project implements an MCP server to interact with the [Metabase API](https://www.metabase.com/), exposing key functionality via a MCP interface.

## Features

- 🔍 List Metabase cards
- 🗄️ List available databases
- 📊 Execute queries on cards
- 🧾 Run arbitrary queries
- 📝 Create new cards

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Environment Variables

Make sure to configure the environment variables:

```bash
export $(<env.template)
```
