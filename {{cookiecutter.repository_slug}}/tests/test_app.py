from starlette.testclient import TestClient


def test_{{ cookiecutter.top_level_package }}_app(client: TestClient) -> None:
    resp = client.get('/')
    assert resp.json()['greeting'] == "I'm {{cookiecutter.repository_name}}!!!"
