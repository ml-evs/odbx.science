from .utils import MatadorOptimadeTransformer
from .dft import *  # noqa
from .misc import *  # noqa
from .structure import *  # noqa


""" This module includes all the odbx-specific extensions
of the OPTiMaDe specification.

"""

__all__ = [  # noqa
    "MatadorPseudopotentialType",
    "MatadorSpinTreatment",
    "MatadorSupportedXCFunctionals",
    "MatadorPseudopotential",
    "MatadorHamiltonian",
    "MatadorCalculator",
    "MatadorThermodynamics",
]


if __name__ == "__main__":
    import pymongo as pm
    from matador.scrapers import castep2dict

    cli = pm.MongoClient()
    db = cli.crystals

    in_cursor, s = castep2dict("/home/me388/NaP*/*.castep", db=True)
    out_coll = db.structures
    # db.structures.drop()
    MatadorOptimadeTransformer(out_coll, in_cursor=in_cursor)
