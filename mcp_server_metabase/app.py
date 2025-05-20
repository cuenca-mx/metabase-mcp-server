import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

import httpx
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import TextContent

from .config import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp-server-metabase")


class Metabase:
    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._client = httpx.AsyncClient(
            timeout=300,  # 5 minutes, some queries can take a while
            headers={"x-api-key": self._api_key},
        )

    async def make_request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        url = f"{self._base_url}/{path.lstrip('/')}"
        response = await self._client.request(method, url, json=json)
        response.raise_for_status()
        return response

    async def close(self) -> None:
        await self._client.aclose()


@dataclass
class AppContext:
    metabase: Metabase


@asynccontextmanager
async def app_lifespan(_server: FastMCP) -> AsyncIterator[AppContext]:
    metabase = Metabase(
        base_url=config.metabase_url,
        api_key=config.metabase_api_key,
    )
    try:
        yield AppContext(metabase=metabase)
    finally:
        await metabase.close()


mcp = FastMCP("mcp-metabase", lifespan=app_lifespan)


@mcp.tool(name="list_databases", description="List all databases in Metabase")
async def list_databases(ctx: Context) -> TextContent:
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request("GET", "/api/database")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="list_collections", description="List all collections in Metabase"
)
async def list_collections(ctx: Context) -> TextContent:
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request("GET", "api/collection")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(name="list_cards", description="List all cards in Metabase")
async def list_cards(ctx: Context) -> TextContent:
    """Since there are many cards, the response is limited to only
    bookmarked/favorite cards"""
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request("GET", "/api/card/?f=bookmarked")
    return TextContent(type="text", text=json.dumps(response.json(), indent=2))


@mcp.tool(
    name="execute_card", description="Run the query associated with a Card."
)
async def execute_card(
    ctx: Context, card_id: int, parameters: list[dict[str, Any]]
) -> TextContent:
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request(
        "POST",
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
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request(
        "POST",
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
    metabase = ctx.request_context.lifespan_context.metabase
    response = await metabase.make_request(
        "POST",
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
    metabase = ctx.request_context.lifespan_context.metabase
    try:
        response = await metabase.make_request(
            "POST",
            f"/api/bookmark/card/{card_id}",
        )
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
