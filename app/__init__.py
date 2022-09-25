from starlette.applications import Starlette
from starlette.routing import Mount

from app.api import api
from settings import settings

app = Starlette(routes=[Mount("/api/" + settings.APP_VERSION, api)])
