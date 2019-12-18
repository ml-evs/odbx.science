""" odbx version of optimade.server.routers.structures.py, including templates. """

import re
from typing import Union
from pathlib import Path

from fastapi import APIRouter, Depends
from starlette.requests import Request

from optimade.models import (
    ErrorResponse,
    StructureResource,
    StructureResponseOne,
    EntryResponseOne,
)
from optimade.server.config import CONFIG
from optimade.server.deps import SingleEntryQueryParams
from optimade.server.entry_collections import MongoCollection, client

from optimade.server.routers.utils import get_single_entry
from ..odbx_mappers import StructureMapper
from ..odbx_templates import TEMPLATES
from ..utils import optimade_to_basic_cif

router = APIRouter()


with open(Path(__file__).resolve().parent.joinpath("test.cif"), "r") as f:
    cif_string = "".join(
        [line for line in f.readlines() if not line.strip().startswith("#")]
    ).replace("'", "\\'")

structures_coll = MongoCollection(
    collection=client[CONFIG.mongo_database][CONFIG.structures_collection],
    resource_cls=StructureResource,
    resource_mapper=StructureMapper,
)


@router.get(
    "/structures/{entry_id:path}",
    response_model=Union[StructureResponseOne, ErrorResponse],
    response_model_exclude_unset=True,
    tags=["Structure"],
)
def get_single_structure(
    request: Request, entry_id: str, params: SingleEntryQueryParams = Depends()
):

    response = get_single_entry(
        collection=structures_coll,
        entry_id=entry_id,
        request=request,
        params=params,
        response=EntryResponseOne,
    )

    context = {"request": request, "entry_id": entry_id}

    if response.meta.data_returned < 1:
        return TEMPLATES.TemplateResponse("structure_not_found.html", context)

    exp = re.compile("[A-Z][^A-Z]")
    split_formula = re.findall(
        exp, response.data.attributes.chemical_formula_descriptive
    )
    print(response.data.attributes.chemical_formula_descriptive)
    print(split_formula)

    context.update(
        {
            "odbx_title": "odbx",
            "odbx_blurb": "the open database of xtals",
            "odbx_about": 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham.',
            "odbx_cif_string": optimade_to_basic_cif(response.data),
            "structure_info": dict(response),
            "split_formula": split_formula,
        }
    )

    return TEMPLATES.TemplateResponse("structure.html", context)
