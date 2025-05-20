from typing import Any

import pytest
import pytest_asyncio
from fastmcp import Client

from metabase_mcp_server.app import mcp


@pytest_asyncio.fixture(scope="function")
async def client() -> Client:
    return Client(mcp)


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "filter_headers": [
            ("x-api-key", "DUMMY_AUTHORIZATION"),
        ]
    }
    return config
