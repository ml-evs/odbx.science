# pylint: disable=line-too-long
import os
import json
from pathlib import Path

from lark.exceptions import VisitError

from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from optimade import __api_version__, __version__
import optimade.server.exception_handlers as exc_handlers

from optimade.server.config import CONFIG
from optimade.server.middleware import (
    EnsureQueryParamIntegrity,
    CheckWronglyVersionedBaseUrls,
    HandleApiHint,
    AddWarnings,
)
from optimade.server.routers import index_info, links, versions
from optimade.server.routers.utils import BASE_URL_PREFIXES
from .routers import ABOUT


if CONFIG.debug:  # pragma: no cover
    print("DEBUG MODE")


app = FastAPI(
    title=ABOUT["title"],
    description=ABOUT["about"],
    version=__api_version__,
    docs_url=f"{BASE_URL_PREFIXES['major']}/extensions/docs",
    redoc_url=f"{BASE_URL_PREFIXES['major']}/extensions/redoc",
    openapi_url=f"{BASE_URL_PREFIXES['major']}/extensions/openapi.json",
)


if CONFIG.index_links_path.exists():
    import bson.json_util
    from optimade.server.routers.links import links_coll
    from optimade.server.routers.utils import mongo_id_for_database

    print("loading index links...")
    with open(CONFIG.index_links_path) as f:
        data = json.load(f)

        processed = []

        for db in data:
            db["_id"] = {"$oid": mongo_id_for_database(db["id"], db["type"])}
            processed.append(db)

        print("inserting index links into collection...")
        links_coll.collection.insert_many(
            bson.json_util.loads(bson.json_util.dumps(processed))
        )
        print("done inserting index links...")


# Add various middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(EnsureQueryParamIntegrity)
app.add_middleware(CheckWronglyVersionedBaseUrls)
app.add_middleware(HandleApiHint)
app.add_middleware(AddWarnings)


# Add various exception handlers
app.add_exception_handler(StarletteHTTPException, exc_handlers.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exc_handlers.request_validation_exception_handler
)
app.add_exception_handler(ValidationError, exc_handlers.validation_exception_handler)
app.add_exception_handler(VisitError, exc_handlers.grammar_not_implemented_handler)
app.add_exception_handler(Exception, exc_handlers.general_exception_handler)


# Add various endpoints to unversioned URL
app.include_router(index_info.router)
app.include_router(links.router)
app.include_router(versions.router)

for version in ("major", "minor", "patch"):
    app.include_router(index_info.router, prefix=BASE_URL_PREFIXES[version])
    app.include_router(links.router, prefix=BASE_URL_PREFIXES[version])
