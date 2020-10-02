# pylint: disable=line-too-long
from lark.exceptions import VisitError

from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from optimade import __api_version__
import optimade.server.exception_handlers as exc_handlers
from optimade.server.config import CONFIG
from optimade.server.entry_collections import MongoCollection
from optimade.server.middleware import (
    EnsureQueryParamIntegrity,
    CheckWronglyVersionedBaseUrls,
    HandleApiHint,
    AddWarnings,
)
from optimade.server.routers import (
    info,
    links,
    references,
    structures,
    landing,
    versions,
)

# from optimade.server.schemas import ENTRY_SCHEMAS
from optimade.server.routers.utils import BASE_URL_PREFIXES

from .models.structure import MatadorStructureResource
from .routers import ABOUT


app = FastAPI(
    title=ABOUT["title"],
    description=ABOUT["about"],
    version=__api_version__,
    docs_url=f"{BASE_URL_PREFIXES['major']}/extensions/docs",
    redoc_url=f"{BASE_URL_PREFIXES['major']}/extensions/redoc",
    openapi_url=f"{BASE_URL_PREFIXES['major']}/extensions/openapi.json",
)

if not CONFIG.use_real_mongo:
    import optimade.server.data as data
    from optimade.server.routers import ENTRY_COLLECTIONS

    def load_entries(endpoint_name: str, endpoint_collection: MongoCollection):
        print(f"loading test {endpoint_name}...")

        endpoint_collection.collection.insert_many(getattr(data, endpoint_name, []))
        print(f"done inserting test {endpoint_name}...")

    for name, collection in ENTRY_COLLECTIONS.items():
        load_entries(name, collection)

# Set the info endpoint to use MatadorStructureResource
# ENTRY_SCHEMAS.structure_model = MatadorStructureResource

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
app.add_exception_handler(NotImplementedError, exc_handlers.not_implemented_handler)
app.add_exception_handler(Exception, exc_handlers.general_exception_handler)


for endpoint in (info, links, references, structures, landing, versions):
    app.include_router(endpoint.router)
# Add various versioned endpoints
for version in ("major", "minor", "patch"):
    for endpoint in (info, links, references, structures, landing):
        app.include_router(endpoint.router, prefix=BASE_URL_PREFIXES[version])
