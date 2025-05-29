import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from fastmcp import Client

from metabase_mcp_server.app import mcp


@pytest_asyncio.fixture(scope="function")
async def client() -> AsyncGenerator[Client, None]:
    # Run client in its own task to ensure __aenter__ and __aexit__ happen in
    # the same task. This avoids AnyIO's "RuntimeError: Attempted to exit
    # cancel scope in a different task than it was entered in" error.

    stop_event: asyncio.Event = asyncio.Event()
    client_ready: asyncio.Future[Client] = asyncio.Future()

    async def run() -> None:
        async with Client(mcp) as c:
            client_ready.set_result(c)
            await stop_event.wait()

    task = asyncio.create_task(run())
    client_instance = await client_ready
    yield client_instance
    stop_event.set()
    await task


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "filter_headers": [
            ("x-api-key", "DUMMY_AUTHORIZATION"),
        ]
    }
    return config
