from starlette.applications import Starlette
from starlette.routing import Mount

from settings import settings
from app.api import api


app = Starlette(
    routes=[
        Mount("/api/" + settings.APP_VERSION, api)
    ]
)
