import json
import os
from typing import Generator

import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_secretsmanager


@pytest.fixture
def create_secret():
    default_config = dict(
        DATABASE_URI=os.environ['DATABASE_URI'],
    )
    with mock_secretsmanager():
        client = boto3.client('secretsmanager')
        client.create_secret(
            Name=os.environ['SECRETS_CONFIG'],
            SecretString=json.dumps(default_config),
        )
        yield


@pytest.fixture
def client(create_secret) -> Generator[TestClient, None, None]:
    from {{cookiecutter.top_level_package}}.app import app

    client = TestClient(app)
    yield client
