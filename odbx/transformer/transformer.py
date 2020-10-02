import random
import datetime
import bson
import numpy as np
import pymongo as pm

from typing import List, Union
from optimade.models.structures import Species
from optimade.models import ReferenceResource

from optimade.server.routers import ENTRY_COLLECTIONS

from matador.utils.chem_utils import get_formula_from_stoich, get_concentration
from matador.utils.cell_utils import cart2volume
from matador.crystal import Crystal
from matador.utils.db_utils import WORDS, NOUNS

from odbx.models.dft import (
    MatadorHamiltonian,
    MatadorPseudopotential,
    MatadorCalculator,
    MatadorThermodynamics,
)

from odbx.models.structure import MatadorSpaceGroup, MatadorStructureResourceAttributes
from odbx.models.misc import MatadorPerson

import tqdm


class MatadorOptimadeTransformer:
    def __init__(
        self, structures: list = None, references: list = None,
    ):

        self.wlines = WORDS
        self.nlines = NOUNS

        self.num_words = len(self.wlines)
        self.num_nouns = len(self.nlines)

        documents = structures

        out_cursor = []

        if references is not None:
            for ref in references:
                ref["last_modified"] = datetime.datetime.now()
            # check that all refs can be validated as ReferenceResources
            [
                ReferenceResource(
                    id=ref["id"],
                    attributes={key: ref[key] for key in ref if key != "id"},
                )
                for ref in references
            ]

            last_id = 0
            curs = (
                ENTRY_COLLECTIONS["structures"]
                .collection.find({})
                .sort("_id", pm.DESCENDING)
                .limit(1)
            )
            if len(list(curs)) == 1:
                last_id = int(curs[0]["id"].split("odbx_")[1])

        for ind, doc in tqdm.tqdm(enumerate(documents)):
            crys_doc = Crystal(doc)
            structure = self.create_optimade_structure(crys_doc, last_id + 1 + ind)
            structure["relationships"] = {}
            structure["relationships"]["references"] = {}
            structure["relationships"]["references"]["data"] = [
                {"id": ref["id"], "type": "references"} for ref in references
            ]
            out_cursor.append(structure)

        _ = ENTRY_COLLECTIONS["references"].collection.insert_many(references)
        _ = ENTRY_COLLECTIONS["structures"].collection.insert_many(out_cursor)

    @classmethod
    def construct_dft_hamiltonian(self, doc: Crystal) -> MatadorHamiltonian:
        if "pseudopotentials" not in doc._data:
            doc._data["pseudopotentials"] = self.construct_pseudopotentials(doc)
        spin = doc._data.get("spin_polarized", False)
        spin_treatment = "none"
        if spin:
            spin_treatment = doc._data.get("spin_treatment", "none")
        doc._data["spin_treatment"] = spin_treatment

        ext_pressure = np.zeros((3, 3))
        for i in range(3):
            for j in range(3 - i):
                ext_pressure[i][j] = doc._data["external_pressure"][i][j]
        doc._data["external_pressure"] = ext_pressure.tolist()
        doc._data["kpoint_spacing"] = doc._data["kpoints_mp_spacing"]

        return MatadorHamiltonian(**doc._data)

    @classmethod
    def construct_pseudopotentials(self, doc: Crystal) -> List[MatadorPseudopotential]:
        return sorted(
            [
                MatadorPseudopotential(
                    identifier=doc._data["species_pot"][key],
                    species=key,
                    pp_type="ultrasoft",
                )
                for key in doc._data["species_pot"]
            ],
            key=lambda x: x.species,
        )

    @classmethod
    def construct_thermodynamics(self, doc: Crystal) -> MatadorThermodynamics:
        doc._data["enthalpy"] = doc._data["enthalpy_per_atom"]
        doc._data["total_energy"] = doc._data["total_energy_per_atom"]
        doc._data["formation_energy"] = doc._data.get("formation_energy_per_atom")
        if doc._data["formation_energy"] is None:
            doc._data["formation_energy"] = doc._data.get("formation_enthalpy_per_atom")
        return MatadorThermodynamics(**doc._data)

    @classmethod
    def construct_submitter(self, doc: Crystal) -> Union[MatadorPerson, None]:
        """ Construct a MatadorPerson object, assuming the user field contains a CRSID. """
        return None
        # if "user" in doc._data:
        # user = doc._data["user"]
        # return MatadorPerson(identifier=user, email="web@odbx.science")

    @classmethod
    def construct_calculator(self, doc: Crystal) -> Union[MatadorCalculator, None]:
        """ Construct the container to store calculator info. """
        if "castep_version" in doc._data:
            major = int(doc._data["castep_version"].split(".")[0])
            minor = float("".join(doc._data["castep_version"].split(".")[1:]))
        if "_castep_commit" in doc._data:
            commit = doc._data["_castep_commit"]
        else:
            commit = None
        if "_compiler_architecture" in doc._data:
            arch = doc._data["_compiler_architecture"]
        else:
            arch = None

        return MatadorCalculator(
            name="CASTEP",
            version_major=major,
            version_minor=minor,
            commit_hash=commit,
            architecture=arch,
        )

    @classmethod
    def construct_spacegroup(self, doc: Crystal, tolerance=1e-3) -> MatadorSpaceGroup:
        """ Generate the space group at the standardised tolerance. """
        return MatadorSpaceGroup(
            symbol=doc.get_space_group(symprec=tolerance), spglib_tolerance=tolerance
        )

    def construct_structure_attributes(self, doc: Crystal):

        structure_attributes = {}
        # from optimade StructureResourceAttributes
        structure_attributes["elements"] = doc.elems
        structure_attributes["nelements"] = len(doc.elems)

        concentration = get_concentration(
            doc._data, elements=doc.elems, include_end=True
        )
        structure_attributes["elements_ratios"] = concentration
        structure_attributes["chemical_formula_descriptive"] = doc.formula
        structure_attributes["chemical_formula_reduced"] = doc.formula
        structure_attributes["chemical_formula_hill"] = None

        sorted_stoich = sorted(doc.stoichiometry, key=lambda x: x[1], reverse=True)
        gen = anonymous_element_generator()
        for ind, elem in enumerate(sorted_stoich):
            elem[0] = next(gen)

        structure_attributes["chemical_formula_anonymous"] = get_formula_from_stoich(
            doc.stoichiometry, elements=[elem[0] for elem in sorted_stoich]
        )
        structure_attributes["dimension_types"] = [1, 1, 1]
        structure_attributes["nperiodic_dimensions"] = 3
        structure_attributes["lattice_vectors"] = doc.lattice_cart
        structure_attributes["lattice_abc"] = doc.lattice_abc
        structure_attributes["cell_volume"] = cart2volume(doc.lattice_cart)
        structure_attributes["fractional_site_positions"] = doc.positions_frac
        structure_attributes["cartesian_site_positions"] = doc.positions_abs
        structure_attributes["nsites"] = doc.num_atoms
        structure_attributes["species_at_sites"] = doc.atom_types

        species = []
        for ind, atom in enumerate(doc.elems):
            species.append(
                Species(name=atom, chemical_symbols=[atom], concentration=[1.0])
            )

            structure_attributes["species"] = species
        structure_attributes["assemblies"] = None
        structure_attributes["structure_features"] = []

        # from optimade EntryResourceAttributes
        if "text_id" not in doc._data:
            structure_attributes["local_id"] = " ".join(
                [
                    self.wlines[random.randint(0, self.num_words - 1)].strip(),
                    self.nlines[random.randint(0, self.num_nouns - 1)].strip(),
                ]
            )
        else:
            structure_attributes["local_id"] = " ".join(doc._data["text_id"])
        structure_attributes["last_modified"] = datetime.datetime.now()
        if "_id" in doc._data:
            structure_attributes["immutable_id"] = str(doc._data["_id"])
        else:
            structure_attributes["immutable_id"] = str(bson.objectid.ObjectId())
        # if "date" in doc._data:
        # date = [int(val) for val in doc._data["date"].split("-")]
        # structure_attributes["date"] = datetime.date(
        # year=date[-1], month=date[1], day=date[0]
        # )

        # from matador extensions
        structure_attributes["dft_parameters"] = self.construct_dft_hamiltonian(doc)
        structure_attributes["submitter"] = self.construct_submitter(doc)
        structure_attributes["thermodynamics"] = self.construct_thermodynamics(doc)
        structure_attributes["space_group"] = self.construct_spacegroup(doc)
        structure_attributes["calculator"] = self.construct_calculator(doc)

        structure_attributes["stress_tensor"] = doc._data.get("stress")
        structure_attributes["stress"] = doc._data["pressure"]
        structure_attributes["forces"] = doc._data.get("forces")
        structure_attributes["max_force_on_atom"] = doc._data.get("max_force_on_atom")

        return MatadorStructureResourceAttributes(**structure_attributes)

    def create_optimade_structure(self, doc: Crystal, int_id: int) -> dict:

        structure = self.construct_structure_attributes(doc).dict()
        structure["id"] = f"odbx/{int_id}"

        return structure


def anonymous_element_generator():
    """ Generator that yields the next symbol in the A, B, Aa, ... Az naming scheme. """
    from string import ascii_lowercase
    import itertools

    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            s = list(s)
            s[0] = s[0].upper()
            yield "".join(s)
