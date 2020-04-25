# pylint: disable=line-too-long

from lark.exceptions import VisitError

from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from optimade import __api_version__
import optimade.server.exception_handlers as exc_handlers

from optimade.server.middleware import EnsureQueryParamIntegrity
from optimade.server.routers import info, links, references, structures, landing
from optimade.server.routers.utils import BASE_URL_PREFIXES
from .routers import ABOUT


# for prefix in BASE_URL_PREFIXES:
# BASE_URL_PREFIXES[prefix] = (BASE_URL_PREFIXES[prefix]).replace(
# "//", "/"
# )


app = FastAPI(
    title=ABOUT["title"],
    description=ABOUT["about"],
    version=__api_version__,
    docs_url=f"{BASE_URL_PREFIXES['major']}/extensions/docs",
    redoc_url=f"{BASE_URL_PREFIXES['major']}/extensions/redoc",
    openapi_url=f"{BASE_URL_PREFIXES['major']}/extensions/openapi.json",
)


# Add various middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.add_middleware(EnsureQueryParamIntegrity)

# Add various exception handlers
app.add_exception_handler(StarletteHTTPException, exc_handlers.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exc_handlers.request_validation_exception_handler
)
app.add_exception_handler(ValidationError, exc_handlers.validation_exception_handler)
app.add_exception_handler(VisitError, exc_handlers.grammar_not_implemented_handler)
app.add_exception_handler(NotImplementedError, exc_handlers.not_implemented_handler)
app.add_exception_handler(Exception, exc_handlers.general_exception_handler)


# Add various endpoints to `/vMAJOR`
app.include_router(info.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(links.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(references.router, prefix=BASE_URL_PREFIXES["major"])
app.include_router(structures.router, prefix=BASE_URL_PREFIXES["major"])


# Add the router for the landing page for all prefixes
app.include_router(landing.router)
app.include_router(landing.router, prefix=BASE_URL_PREFIXES["major"])


def add_optional_versioned_base_urls(app: FastAPI):
    """Add the following OPTIONAL prefixes/base URLs to server:
    ```
        /vMajor.Minor
        /vMajor.Minor.Patch
    ```
    """
    for version in ("minor", "patch"):
        app.include_router(info.router, prefix=BASE_URL_PREFIXES[version])
        app.include_router(links.router, prefix=BASE_URL_PREFIXES[version])
        app.include_router(references.router, prefix=BASE_URL_PREFIXES[version])
        app.include_router(structures.router, prefix=BASE_URL_PREFIXES[version])
        app.include_router(landing.router, prefix=BASE_URL_PREFIXES[version])
