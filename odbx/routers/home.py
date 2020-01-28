""" odbx version of optimade.server.routers.structures.py, including templates. """

from starlette.routing import Router, Route

from ..templates import TEMPLATES


async def homepage(request):

    example_queries = ['elements HAS "Na"', 'chemical_formula_reduced="ClNa"']

    about_txt = 'odbx is a public database of crystal structures from the group of <a href="https://ajm143.github.io">Dr Andrew Morris</a> at the University of Birmingham, currently in public beta with a limited set of structures. Please contact <a href="mailto:web@odbx.science">web@odbx.science</a> with any issues.'

    context = {
        "request": request,
        "odbx_title": "odbx",
        "odbx_blurb": "the open database of xtals",
        "odbx_about": about_txt,
        "example_queries": example_queries,
    }
    return TEMPLATES.TemplateResponse("search.html", context)


router = Router(routes=[Route("/", endpoint=homepage)])
