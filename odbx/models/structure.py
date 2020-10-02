import datetime
from pydantic import BaseModel, Field, conint, validator
from typing import List, Optional, Tuple, Union
from optimade.models import (
    StructureResource,
    StructureResourceAttributes,
)
from odbx.models.dft import MatadorThermodynamics, MatadorHamiltonian, MatadorCalculator
from odbx.models.misc import MatadorPerson
from odbx.models.utils import check_shape

__all__ = ["MatadorSpaceGroup", "MatadorStructureResourceAttributes"]


Vector3D = Tuple[Union[float, None], Union[float, None], Union[float, None]]


class MatadorSpaceGroup(BaseModel):
    """ Container for an spglib calculated space group. """

    symbol: str = Field(
        ...,
        description="""The International Hermann-Mauguin (HM) space group symbol, as reported by spglib.""",
    )

    spglib_tolerance: float = Field(
        ..., description="""The symmetry tolerance used to compute the space group."""
    )

    number: Optional[conint(gt=0, lt=231)] = Field(
        None, description="""The ITA space group number from 1-230."""
    )


class MatadorStructureResourceAttributes(StructureResourceAttributes):
    """ Extends the OPTIMADE spec for matador-specific keys. """

    lattice_abc: Tuple[Vector3D, Vector3D] = Field(
        ...,
        description="""The lattice parameters of the structure, in Angstrom and degrees.""",
    )

    fractional_site_positions: List[Vector3D] = Field(
        ...,
        description="""A list of the fractional positions of sites in the structure.""",
    )

    cell_volume: float = Field(
        ...,
        description="""The volume of the simulation cell used in the calculation, in Angstrom³.""",
    )

    dft_parameters: MatadorHamiltonian = Field(
        ...,
        description="""The parameters/Hamiltonian used in the relaxation of this structure.""",
    )

    thermodynamics: MatadorThermodynamics = Field(
        ..., description="""Container for the energies computed for the structure."""
    )

    calculator: MatadorCalculator = Field(
        ..., description="""The calculator used for the calculation."""
    )

    space_group: MatadorSpaceGroup = Field(
        ...,
        description="""The computed space group of the structure, calculated by spglib with symmetry tolerance of 0.001.""",
    )

    submitter: Optional[MatadorPerson] = Field(
        None, description="""The person nominally responsible for the calculation. """
    )

    stress: float = Field(
        ..., description="""The computed stress on the structure (Tr(p)/3)."""
    )

    stress_tensor: Tuple[Vector3D, Vector3D, Vector3D] = Field(
        None, description="""The computed stress tensor on the structure."""
    )

    forces: Optional[List[Vector3D]] = Field(
        None, description="""The forces on each atom in the structure, in eV/A. """
    )

    max_force_on_atom: Optional[float] = Field(
        None,
        description="""The norm of the maximum force on an atom in the structure in eV/A.""",
    )

    tags: Optional[List[str]] = Field(
        None, description="""List of free text tags associated with the structure.""",
    )

    calculation_date: Optional[datetime.datetime] = Field(
        None, description="""Date on which calculation was performed."""
    )

    @validator("stress_tensor", whole=True)
    def check_stress(cls, v):
        check_shape(v, (3, 3), "stress_tensor")

    @validator("forces", whole=True)
    def check_forces(cls, v, values):
        check_shape(v, (values.get("nsites"), 3), "forces")


class MatadorStructureResource(StructureResource):
    attributes: MatadorStructureResourceAttributes
