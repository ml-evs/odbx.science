""" odbx version of optimade.server.routers.structures.py, including templates. """

from typing import Union

from fastapi import APIRouter, Depends
from starlette.requests import Request

from optimade.models import (
    ErrorResponse,
    StructureResource,
    StructureResponseMany,
    StructureResponseOne,
)
from optimade.server.config import CONFIG
from optimade.server.deps import EntryListingQueryParams, SingleEntryQueryParams
from optimade.server.entry_collections import MongoCollection, client
from optimade.server.mappers import StructureMapper

from optimade.server.routers.utils import get_entries, get_single_entry

from ..odbx_templates import TEMPLATES

router = APIRouter()


@router.get("/")
def homepage(request: Request):
    context = {
        "request": request,
        "odbx_title": "odbx",
        "odbx_blurb": "the open database of xtals",
        "odbx_about": 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham.',
    }

    return TEMPLATES.TemplateResponse("home.html", context)
