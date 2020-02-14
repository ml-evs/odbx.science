""" odbx version of optimade.server.routers.structures.py, including templates. """

from typing import Union
from pathlib import Path

from fastapi import APIRouter, Depends
from starlette.requests import Request

from optimade.models import (
    ErrorResponse,
    StructureResource,
    StructureResponseOne,
    StructureResponseMany,
)
from optimade.server.config import CONFIG
from optimade.server.query_params import SingleEntryQueryParams, EntryListingQueryParams
from optimade.server.entry_collections import MongoCollection
from optimade.server.routers.utils import get_single_entry, get_entries

from matador.utils.chem_utils import get_stoich_from_formula

from ..mappers import StructureMapper
from ..templates import TEMPLATES
from ..utils import optimade_to_basic_cif
from ..entry_collections import CLIENT, OdbxMongoCollection

router = APIRouter()


with open(Path(__file__).resolve().parent.joinpath("test.cif"), "r") as f:
    cif_string = "".join(
        [line for line in f.readlines() if not line.strip().startswith("#")]
    ).replace("'", "\\'")

structures_coll = OdbxMongoCollection(
    collection=CLIENT[CONFIG.mongo_database][CONFIG.structures_collection],
    resource_cls=StructureResource,
    resource_mapper=StructureMapper,
)


@router.get(
    "/structures",
    response_model=Union[StructureResponseMany, ErrorResponse],
    response_model_exclude_unset=True,
    tags=["Structure"],
)
@router.get(
    "/structures/?",
    response_model=Union[StructureResponseMany, ErrorResponse],
    response_model_exclude_unset=True,
    tags=["Structure"],
)
def get_structures(request: Request, params: EntryListingQueryParams = Depends()):

    context = {"request": request}

    try:
        response = get_entries(
            collection=structures_coll,
            response=StructureResponseMany,
            request=request,
            params=params,
        )

    except Exception as exc:
        context.update(query_error=exc, query_str=str(request.url).split("filter=")[-1])

        return TEMPLATES.TemplateResponse("error.html", context)

    context.update(query=response.meta.query.representation)

    if response.meta.data_returned < 1:
        return TEMPLATES.TemplateResponse("no_structures_found.html", context)

    context.update(
        {
            "odbx_title": "odbx",
            "odbx_blurb": "the open database of xtals",
            "odbx_about": 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham.',
            "data_available": response.meta.data_returned,
            "results": response.data,
            "n_results": len(response.data),
        }
    )

    return TEMPLATES.TemplateResponse("structures.html", context)


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
        response=StructureResponseOne,
    )

    context = {"request": request, "entry_id": entry_id}

    if response.meta.data_returned < 1:
        return TEMPLATES.TemplateResponse("structure_not_found.html", context)

    stoichiometry = get_stoich_from_formula(
        response.data.attributes.chemical_formula_descriptive
    )
    for ind, (elem, num) in enumerate(stoichiometry):
        if num - int(num) > 1e-5:
            raise RuntimeError("Unable to cast formula to correct format")
        stoichiometry[ind][1] = int(num)

    context.update(
        {
            "odbx_title": "odbx",
            "odbx_blurb": "the open database of xtals",
            "odbx_about": 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham.',
            "odbx_cif_string": optimade_to_basic_cif(response.data),
            "structure_info": dict(response),
            "stoichiometry": stoichiometry,
        }
    )

    return TEMPLATES.TemplateResponse("structure.html", context)
