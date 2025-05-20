import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

import httpx
from fastmcp import Context, FastMCP
from mcp.types import TextContent
from pydantic_settings import BaseSettings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp-server-metabase")


class Config(BaseSettings):
    metabase_url: str
    metabase_api_key: str
    timeout: int = 30


config = Config()


@dataclass
class AppContext:
    client: httpx.AsyncClient


@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    client = httpx.AsyncClient(
        base_url=config.metabase_url.rstrip("/"),
        timeout=config.timeout,
        headers={"x-api-key": config.metabase_api_key},
    )
    async with client:
        yield AppContext(client=client)


mcp = FastMCP(
    name="mcp-metabase",
    instructions="""
        This server provides a set of tools to interact with Metabase,
        a business intelligence and analytics platform.
    """,
    lifespan=app_lifespan,
    dependencies=[
        "httpx",
        "pydantic-settings",
    ],
)


@mcp.tool(name="list_databases", description="List all databases in Metabase")
async def list_databases(ctx: Context) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    response = await client.get("/api/database")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="list_collections", description="List all collections in Metabase"
)
async def list_collections(ctx: Context) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    response = await client.get("/api/collection")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(name="list_cards", description="List all cards in Metabase")
async def list_cards(ctx: Context) -> TextContent:
    """Since there are many cards, the response is limited to only
    bookmarked/favorite cards"""
    client = ctx.request_context.lifespan_context.client
    response = await client.get("/api/card/?f=bookmarked")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="execute_card", description="Run the query associated with a Card."
)
async def execute_card(
    ctx: Context, card_id: int, parameters: list[dict[str, Any]]
) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    response = await client.post(
        f"/api/card/{card_id}/query",
        json={"parameters": parameters},
    )
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="execute_query",
    description=(
        "Execute a query and retrieve the results in the usual format."
    ),
)
async def execute_query(
    ctx: Context, query: str, database_id: int
) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    response = await client.post(
        "/api/dataset",
        json={
            "type": "native",
            "native": {"query": query, "template_tags": {}},
            "database": database_id,
        },
    )
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="create_card",
    description=(
        "Create a new Card. Card type can be question, metric, or model."
    ),
)
async def create_card(
    ctx: Context,
    name: str,
    description: str,
    query: str,
    collection_id: int,
    database_id: int,
) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    response = await client.post(
        "/api/card",
        json={
            "name": name,
            "display": "table",
            "visualization_settings": {},
            "dataset_query": {
                "database": database_id,
                "native": {"query": query, "template_tags": {}},
                "type": "native",
            },
            "description": description,
            "collection_id": collection_id,
            "type": "question",
        },
    )
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="create_bookmark",
    description="Create a new bookmark for user.",
)
async def create_bookmark(
    ctx: Context,
    card_id: int,
) -> TextContent:
    client = ctx.request_context.lifespan_context.client
    try:
        response = await client.post(f"/api/bookmark/card/{card_id}")
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            return TextContent(
                type="text",
                text=json.dumps({"error": "Bookmark already exists"}),
            )
        elif e.response.status_code == 404:
            return TextContent(
                type="text",
                text=json.dumps({"error": "Card not found"}),
            )
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


if __name__ == "__main__":  # pragma: no cover
    mcp.run()
