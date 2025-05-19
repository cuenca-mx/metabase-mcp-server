import json

import pytest
from mcp.server.fastmcp import FastMCP

from mcp_server_metabase.app import (
    AppContext,
    Metabase,
    app_lifespan,
    create_bookmark,
    create_card,
    execute_card,
    execute_query,
    list_cards,
    list_collections,
    list_databases,
)

from .conftest import Context


@pytest.mark.vcr
async def test_make_request_success(metabase_client: Metabase) -> None:
    response = await metabase_client.make_request("GET", "/api/card/?f=all")
    assert response.status_code == 200


@pytest.mark.vcr
async def test_list_databases(mcp_context: Context) -> None:
    response = await list_databases(mcp_context)
    data = json.loads(response.text)
    assert "data" in data
    db = data["data"][0]
    assert db["name"] == "Sample Database"
    assert db["engine"] == "h2"
    assert db["id"] == 1


@pytest.mark.vcr
async def test_list_collections(mcp_context: Context) -> None:
    response = await list_collections(mcp_context)
    data = json.loads(response.text)
    assert len(data) > 0


@pytest.mark.vcr
async def test_list_cards(mcp_context: Context) -> None:
    response = await list_cards(mcp_context)
    data = json.loads(response.text)
    card = data[0]
    assert card["id"] == 2
    assert card["name"] == "Demo"
    assert card["display"] == "table"
    assert card["type"] == "question"


@pytest.mark.vcr
async def test_execute_card(mcp_context: Context) -> None:
    response = await execute_card(
        mcp_context,
        card_id=2,
        parameters=[
            {
                "type": "number",
                "target": ["variable", ["template-tag", "cantidad"]],
                "value": 100,
            }
        ],
    )
    data = json.loads(response.text)
    assert "data" in data
    assert "rows" in data["data"]
    assert "cols" in data["data"]


@pytest.mark.vcr
async def test_execute_query(mcp_context: Context) -> None:
    response = await execute_query(
        mcp_context,
        query="select * from orders where quantity >= 100;",
        database_id=1,
    )
    data = json.loads(response.text)
    assert "data" in data
    assert "rows" in data["data"]
    assert "cols" in data["data"]


@pytest.mark.vcr
async def test_create_card(mcp_context: Context) -> None:
    response = await create_card(
        mcp_context,
        name="My Card",
        description="My Description",
        query="select * from orders where quantity >= 100",
        collection_id=1,
        database_id=1,
    )
    data = json.loads(response.text)
    assert data["name"] == "My Card"
    assert data["description"] == "My Description"
    assert data["query_type"] == "native"
    assert data["database_id"] == 1
    assert data["collection_id"] == 1
    assert data["type"] == "question"
    assert data["display"] == "table"
    assert data["dataset_query"]["database"] == 1
    assert data["dataset_query"]["type"] == "native"
    assert (
        data["dataset_query"]["native"]["query"]
        == "select * from orders where quantity >= 100"
    )


@pytest.mark.vcr
async def test_create_bookmark(mcp_context: Context) -> None:
    response = await create_bookmark(
        mcp_context,
        card_id=4,
    )
    data = json.loads(response.text)
    assert "created_at" in data


@pytest.mark.vcr
async def test_create_bookmark_already_exists(mcp_context: Context) -> None:
    response = await create_bookmark(
        mcp_context,
        card_id=2600,
    )
    data = json.loads(response.text)
    assert data["error"] == "Bookmark already exists"


@pytest.mark.vcr
async def test_create_bookmark_card_not_found(mcp_context: Context) -> None:
    response = await create_bookmark(
        mcp_context,
        card_id=4444,
    )
    data = json.loads(response.text)
    assert data["error"] == "Card not found"


async def test_app_lifespan_real_instance() -> None:
    server = FastMCP("test")
    async with app_lifespan(server) as ctx:
        assert isinstance(ctx, AppContext)
        assert ctx.metabase is not None
        assert ctx.metabase._base_url == "https://metabase.domain.com"
        await ctx.metabase.close()


async def test_app_lifespan_missing_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("METABASE_URL", raising=False)
    monkeypatch.delenv("METABASE_API_KEY", raising=False)
    server = FastMCP("test")
    with pytest.raises(
        ValueError, match="METABASE_URL and METABASE_API_KEY must be set"
    ):
        async with app_lifespan(server):
            pass
