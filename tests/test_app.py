from starlette.testclient import TestClient


def test_mcp_server_metabase_app(client: TestClient) -> None:
    resp = client.get('/')
    assert resp.json()['greeting'] == "I'm mcp-server-metabase!!!"
