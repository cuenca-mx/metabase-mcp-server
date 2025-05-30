from collections.abc import AsyncGenerator
from typing import Any

import pytest
from fastmcp import Client

from metabase_mcp_server.app import mcp


@pytest.fixture(scope="session", autouse=True)
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncGenerator[Client, None]:
    async with Client(mcp) as client:
        yield client


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "filter_headers": [
            ("x-api-key", "DUMMY_AUTHORIZATION"),
        ]
    }
    return config
