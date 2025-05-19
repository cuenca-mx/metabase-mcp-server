import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio

from mcp_server_metabase.app import Metabase

METABASE_URL = os.environ["METABASE_URL"]
METABASE_API_KEY = os.environ["METABASE_API_KEY"]


@pytest_asyncio.fixture(scope="session")
async def metabase_client() -> AsyncGenerator[Metabase, None]:
    client = Metabase(base_url=METABASE_URL, api_key=METABASE_API_KEY)
    try:
        yield client
    finally:
        await client.close()


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "filter_headers": [
            ("x-api-key", "DUMMY_AUTHORIZATION"),
        ]
    }
    return config


class LifespanContext:
    def __init__(self, metabase: Metabase) -> None:
        self.metabase = metabase


class RequestContext:
    def __init__(self, metabase: Metabase) -> None:
        self.lifespan_context = LifespanContext(metabase)


class Context:
    def __init__(self, metabase: Metabase) -> None:
        self.request_context = RequestContext(metabase)


@pytest.fixture
def mcp_context(metabase_client: Metabase) -> Context:
    return Context(metabase_client)
