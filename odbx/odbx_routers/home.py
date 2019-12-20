""" odbx version of optimade.server.routers.structures.py, including templates. """

from starlette.routing import Router, Route

from ..odbx_templates import TEMPLATES


async def homepage(request):

    example_queries = ['elements HAS "Na"', 'chemical_formula_reduced="ClNa"']

    context = {
        "request": request,
        "odbx_title": "odbx",
        "odbx_blurb": "the open database of xtals",
        "odbx_about": 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham, currently in public beta. Please contact <a href="mailto:web@odbx.science">web@odbx.science</a> with any issues.',
        "example_queries": example_queries,
    }
    return TEMPLATES.TemplateResponse("search.html", context)


router = Router(routes=[Route("/", endpoint=homepage)])
