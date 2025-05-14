import json
import os
from functools import lru_cache

import boto3

SENTRY_DSN = os.environ['SENTRY_DSN']


@lru_cache(maxsize=1)
def get_secrets_config():
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=os.environ['SECRETS_CONFIG'])[
        'SecretString'
    ]
    config = json.loads(response)
    return config
