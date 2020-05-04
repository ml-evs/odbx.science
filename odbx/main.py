""" Lines suffixed with "# odbx" indicate that this line differs from
the reference implementation or does not exist in the reference
implementation.

"""

from lark.exceptions import VisitError
from pydantic import ValidationError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from optimade import __api_version__

import optimade.server.exception_handlers as exc_handlers

from . import routers  # odbx
from .routers import ABOUT

app = FastAPI(title=ABOUT["title"], description=ABOUT["about"], version=__api_version__)

app.add_exception_handler(StarletteHTTPException, exc_handlers.http_exception_handler)
app.add_exception_handler(
    RequestValidationError, exc_handlers.request_validation_exception_handler
)
app.add_exception_handler(ValidationError, exc_handlers.validation_exception_handler)
app.add_exception_handler(VisitError, exc_handlers.grammar_not_implemented_handler)
app.add_exception_handler(Exception, exc_handlers.general_exception_handler)

rich_prefix = ""  # odbx

app.include_router(routers.structures.router, prefix=rich_prefix)  # odbx
app.include_router(routers.home.router, prefix=rich_prefix)  # odbx
