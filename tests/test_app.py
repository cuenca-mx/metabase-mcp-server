import json

import pytest
from fastmcp import Client


@pytest.mark.vcr
async def test_list_databases(client: Client) -> None:
    async with client:
        response = await client.call_tool("list_databases")
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert "data" in data
        db = data["data"][0]
        assert db["name"] == "Sample Database"
        assert db["engine"] == "h2"
        assert db["id"] == 1


@pytest.mark.vcr
async def test_list_collections(client: Client) -> None:
    async with client:
        response = await client.call_tool("list_collections")
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert len(data) > 0


@pytest.mark.vcr
async def test_list_cards(client: Client) -> None:
    async with client:
        response = await client.call_tool("list_cards")
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        card = data[0]
        assert card["id"] == 2
        assert card["name"] == "Demo"
        assert card["display"] == "table"
        assert card["type"] == "question"


@pytest.mark.vcr
async def test_execute_card(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "execute_card",
            {
                "card_id": 2,
                "parameters": [
                    {
                        "type": "number",
                        "target": ["variable", ["template-tag", "cantidad"]],
                        "value": 100,
                    }
                ],
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert "data" in data
        assert "rows" in data["data"]
        assert "cols" in data["data"]


@pytest.mark.vcr
async def test_execute_query(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "execute_query",
            {
                "query": "select * from orders where quantity >= 100;",
                "database_id": 1,
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert "data" in data
        assert "rows" in data["data"]
        assert "cols" in data["data"]


@pytest.mark.vcr
async def test_create_card(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "create_card",
            {
                "name": "My Card",
                "description": "My Description",
                "query": "select * from orders where quantity >= 100",
                "collection_id": 1,
                "database_id": 1,
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
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
async def test_create_bookmark(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "create_bookmark",
            {
                "card_id": 4,
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert "created_at" in data


@pytest.mark.vcr
async def test_create_bookmark_already_exists(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "create_bookmark",
            {
                "card_id": 2600,
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert data["error"] == "Bookmark already exists"


@pytest.mark.vcr
async def test_create_bookmark_card_not_found(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "create_bookmark",
            {
                "card_id": 4444,
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert data["error"] == "Card not found"


async def test_convert_timezone_success(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "convert_timezone",
            {
                "datetime_str": "2024-01-15T10:30:00",
                "source_timezone": "America/New_York",
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert data["original"] == "2024-01-15T10:30:00"
        assert data["timezone"] == "America/New_York"
        assert "utc" in data
        assert data["utc"] == "2024-01-15T15:30:00+00:00"


async def test_convert_timezone_failed(client: Client) -> None:
    async with client:
        response = await client.call_tool(
            "convert_timezone",
            {
                "datetime_str": "2024-01-15T10:30:00",
                "source_timezone": "Invalid/Timezone",
            },
        )
        assert response[0].type == "text"
        data = json.loads(response[0].text)
        assert "error" in data
        assert "Failed to convert timezone" in data["error"]
