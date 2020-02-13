""" Lines suffixed with "# odbx" indicate that this line differs from
the reference implementation or does not exist in the reference
implementation.

"""

import json
from pathlib import Path

from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from starlette.staticfiles import StaticFiles  # odbx

from optimade.server.entry_collections import MongoCollection
from optimade.server.config import CONFIG
from optimade.server.routers import info, links, references, structures, landing
from optimade.server.middleware import RedirectSlashedURLs
from optimade.server.routers.utils import get_providers, BASE_URL_PREFIXES

import optimade.server.exception_handlers as exc_handlers

from . import routers  # odbx

config_version = "0.10.0"

app = FastAPI(
    title="OPTiMaDe API",
    description=(
        "The [Open Databases Integration for Materials Design (OPTiMaDe) consortium]"
        "(http://http://www.optimade.org/) aims to make materials databases interoperational "
        "by developing a common REST API."
    ),
    version=config_version,
    docs_url="/optimade/extensions/docs",
    redoc_url="/optimade/extensions/redoc",
    openapi_url="/optimade/extensions/openapi.json",
)

app.add_middleware(RedirectSlashedURLs)

app.add_exception_handler(StarletteHTTPException, exc_handlers.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exc_handlers.request_validation_exception_handler
)
app.add_exception_handler(ValidationError, exc_handlers.validation_exception_handler)
app.add_exception_handler(Exception, exc_handlers.general_exception_handler)

app.include_router(info.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(links.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(references.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(structures.router, prefix=BASE_URL_PREFIXES["major"])

# add landing page
app.include_router(landing.router, prefix="/optimade")
app.include_router(landing.router, prefix=BASE_URL_PREFIXES["major"])

rich_prefix = ""  # odbx
app.include_router(routers.structures.router, prefix=rich_prefix)  # odbx
app.include_router(routers.home.router, prefix=rich_prefix)  # odbx

js_dir = Path(__file__).parent.joinpath("js")  # odbx
css_dir = Path(__file__).parent.joinpath("css")  # odbx
app.mount("/js", StaticFiles(directory=js_dir), name="js")  # odbx
app.mount("/css", StaticFiles(directory=css_dir), name="css")  # odbx


def update_schema(app):
    """Update OpenAPI schema in file 'local_openapi.json'"""
    with open("local_openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)


@app.on_event("startup")
async def startup_event():
    update_schema(app)
