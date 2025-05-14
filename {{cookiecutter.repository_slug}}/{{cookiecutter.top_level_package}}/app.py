import sentry_sdk
from fast_agave.middlewares import FastAgaveErrorHandler
from fast_agave_authed.middlewares import AuthedMiddleware
from fastapi import FastAPI
from mongoengine import connect
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from .config import SENTRY_DSN, get_secrets_config
from .resources import app as resources

secrets = get_secrets_config()
sentry_sdk.init(dsn=SENTRY_DSN)

connect(host=secrets['DATABASE_URI'])
app = FastAPI(title='{{cookiecutter.repository_name}}')

SentryAsgiMiddleware._run_asgi2 = SentryAsgiMiddleware._run_asgi3  # type: ignore  # noqa: E501

app.add_middleware(AuthedMiddleware)
app.add_middleware(FastAgaveErrorHandler)
app.add_middleware(SentryAsgiMiddleware)


app.include_router(resources)


@app.on_event('startup')
async def on_startup() -> None:  # pragma: no cover
    # Eliminar este método si no hay algo que inicializar
    ...
