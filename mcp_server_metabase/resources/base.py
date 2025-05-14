from typing import Dict

from fast_agave.blueprints import RestApiBlueprint
from fast_agave_authed.middlewares.decorators import (
    authentication_exempt,
    authorization_exempt,
)

app = RestApiBlueprint()


@app.get('/')
@authentication_exempt
@authorization_exempt
async def mcp_server_metabase() -> Dict:
    return dict(greeting="I'm mcp-server-metabase!!!")
