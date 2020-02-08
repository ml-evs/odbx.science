from pydantic import BaseModel, Field, List, Optional, conint, validator
from optimade.models import StructureResourceAttributes

__all__ = [
    'MatadorSpaceGroup',
    'MatadorStructureResourceAttributes'
]


class MatadorSpaceGroup(BaseModel):
    """ Container for an spglib calculated space group. """

    symbol: str = Field(
        ...,
        description="""The International (HM) space group symbol, as reported by spglib.""",
    )

    spglib_tolerance: float = Field(
        ...,
        description="""The symmetry tolerance used to compute the space group."""
    )

    number: Optional[conint(gt=0, lt=231)] = Field(
        ...,
        description="""The space group number from 1-230."""
    )


class MatadorStructureResourceAttributes(StructureResourceAttributes):
    """ Extends the OPTiMaDe spec for matador-specific keys. """

    lattice_abc: List[List[float]] = Field(
        ...,
        description="""The lattice parameters of the structure, in Angstrom and degrees.""",
    )

    fractional_site_positions: List[List[float]] = Field(
        ...,
        description="""Fractional positions."""
    )

    cell_volume: float = Field(
        ...,
        description="""The volume of the simulation cell used in the calculation, in Angstrom³.""",
    )

    parameters: MatadorHamiltonian = Field(
        ...,
        description="""The ers/Hamiltonian used in the relaxation of this structure.""",
    )

    thermodynamics: MatadorThermodynamics = Field(
        ...,
        description="""Container for the energies computed for the structure."""
    )

    space_group: MatadorSpaceGroup = Field(
        ...,
        description="""The computed space group of the structure, calculated by spglib with symmetry tolerance of 0.001.""",
    )

    submitter: MatadorPerson = Field(
        ...,
        description="""The person nominally responsible for the calculation. """
    )

    stress: float = Field(
        ...,
        description="""The computed stress on the structure (Tr(p)/3)."""
    )

    stress_tensor: Optional[List[List[float]]] = Field(
        ...,
        description="""The computed stress tensor on the structure."""
    )

    forces: Optional[List[List[float]]] = Field(
        ...,
        description="""The forces on each atom in the structure, in eV/A. """
    )

    max_force_on_atom: Optional[float] = Field(
        ...,
        description="""The norm of the maximum force on an atom in the structure in eV/A.""",
    )

    tags: List[str] = Field(
        default=[],
        description="""List of free text tags associated with the structure.""",
    )

    date: Optional[datetime.datetime] = Field(
        ...,
        description="""Date on which calculation was performed."""
    )

    @validator("stress_tensor", whole=True)
    def check_stress(cls, v):
        check_shape(v, (3, 3), "stress_tensor")

    @validator("forces", whole=True)
    def check_forces(cls, v, values):
        check_shape(v, (values.get("nsites"), 3), "forces")
