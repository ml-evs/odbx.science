""" odbx version of optimade.server.routers.structures.py, including templates. """

import json
from pathlib import Path
from starlette.routing import Router, Route

from ..templates import TEMPLATES

with open(Path(__file__).parent.joinpath("about.json"), "r") as f:
    ABOUT = json.load(f)


async def homepage(request):

    with open(
        Path(__file__).parent.parent.joinpath("data/example_queries.txt"), "r"
    ) as f:
        example_queries = f.readlines()

    context = {
        "request": request,
        "odbx_title": ABOUT["title"],
        "odbx_blurb": ABOUT["blurb"],
        "odbx_about": ABOUT["about"],
        "example_queries": example_queries,
    }
    return TEMPLATES.TemplateResponse("search.html", context)


router = Router(routes=[Route("/", endpoint=homepage)])
