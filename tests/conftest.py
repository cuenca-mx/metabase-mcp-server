import os
from typing import Any

import pytest

from mcp_server_metabase.app import Metabase

METABASE_URL = os.environ["METABASE_URL"]
METABASE_API_KEY = os.environ["METABASE_API_KEY"]


@pytest.fixture
def metabase_client():
    return Metabase(base_url=METABASE_URL, api_key=METABASE_API_KEY)


@pytest.fixture(scope="session")
def vcr_config() -> dict[str, Any]:
    config: dict[str, Any] = {
        "filter_headers": [
            ("x-api-key", "DUMMY_AUTHORIZATION"),
        ]
    }
    return config


class LifespanContext:
    def __init__(self, metabase):
        self.metabase = metabase


class RequestContext:
    def __init__(self, metabase):
        self.lifespan_context = LifespanContext(metabase)


class Context:
    def __init__(self, metabase):
        self.request_context = RequestContext(metabase)


@pytest.fixture
def mcp_context(metabase_client):
    return Context(metabase_client)
