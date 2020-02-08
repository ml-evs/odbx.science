from typing import Optional, List
from enum import Enum
from pydantic import Field, validator, BaseModel

__all__ = [
    "MatadorPseudopotentialType",
    "MatadorSpinTreatment",
    "MatadorSupportedXCFunctionals",
    "MatadorPseudopotential",
    "MatadorHamiltonian",
    "MatadorCalculator",
    "MatadorThermodynamics",
]


class MatadorSpinTreatment(str, Enum):
    none = "none"
    scalar = "scalar"
    vector = "vector"


class MatadorSupportedXCFunctionals(str, Enum):
    lda = "LDA"
    pbe = "PBE"
    pbesol = "PBESOL"
    rscan = "RSCAN"
    pbe0 = "PBE0"
    hse06 = "HSE06"


class MatadorPseudopotentialType(str, Enum):
    ultrasoft = "ultrasoft"
    norm_conserving = "norm_conserving"
    paw = "paw"


class MatadorPseudopotential(BaseModel):
    """ Container for psuedopotentials. """

    identifier: str = Field(
        ...,
        description="""Textual identifier of the pseudopotential, e.g. descriptive filename or CASTEP generator string.""",
    )

    species: str = Field(
        ..., description="""The species that this pseudopotential represents."""
    )

    pp_type: Optional[MatadorPseudopotentialType] = Field(
        ...,
        description="""The overall type of the pseudopotential, must be one of ["ultrasoft", "norm-conserving", "paw"].""",
    )

    raw: Optional[str] = Field(
        ...,
        description="""The contents of the pseudopotential file used in the calculation.""",
    )

    scheme_desc: Optional[str] = Field(
        ...,
        description="""Descrition of psedopotential generation scheme e.g. 'vanderbilt-usp' or 'paw'""",
    )

    library: Optional[str] = Field(
        ...,
        description="""Optional library name for source of pseudopotential, e.g. 'C18' or 'SSSP-acc'.""",
    )


class MatadorHamiltonian(BaseModel):
    """ Container for any parameters that alter the Hamiltonian under which the structure was relaxed, or convergence parameters that alter the final results. """

    cut_off_energy: float = Field(
        ...,
        description="""The cutoff energy used in the calcution, in eV."""
    )

    xc_functional: MatadorSupportedXCFunctionals = Field(
        ...,
        description="""The name of the exchange-correlation functional used for the calculation. Acronymn must in supported list. """,
    )

    pseudopotentials: List[MatadorPseudopotential] = Field(
        ...,
        description="""List of pseudopotentials used for each chemical species in the structure. Must be presented in alphabetical order of the chemical species.""",
    )

    spin_treatment: MatadorSpinTreatment = Field(
        ...,
        description="""Enum to store the spin treatment for the calculation, where the allowed values reflect the CASTEP keywords.""",
    )

    external_pressure: List[List[float]] = Field(
        ...,
        description="""The external pressure tensor applied during relaxation."""
    )

    kpoint_spacing: float = Field(
        ...,
        description="""The maximum k-point spacing of the MP grid used in the calculation, in 2pi Angstrom units (as used by e.g. CASTEP). """,
    )

    geom_method: Optional[str] = Field(
        ...,
        description="""Free text name of the method used to relax the structure."""
    )

    geom_force_tol: Optional[float] = Field(
        ...,
        description="""The target force attempted by the relaxer."""
    )

    @validator("external_pressure", whole=True)
    def check_pressure(cls, v):
        check_shape(v, (3, 3), "external_pressure")


class MatadorCalculator(BaseModel):

    name: str = Field(
        ...,
        description="The name of the software package used for the calculation"
    )

    version_major: int = Field(
        ...,
        description="The major version number of the software package as an integer.",
    )

    version_minor: float = Field(
        ...,
        description="The minor version number as a float."
    )

    commit_hash: Optional[str] = Field(
        ...,
        description="The commit hash of the version, if available."
    )

    architecture: Optional[str] = Field(
        ...,
        description="Description of the compiler and architecture."
    )


class MatadorThermodynamics(BaseModel):

    enthalpy: float = Field(
        ...,
        description="""The computed enthalpy per atom in eV, referenced against the vacuum. """,
    )

    total_energy: float = Field(
        ...,
        description="""The computed total energy per atom in eV, reference against the vacuum.""",
    )

    formation_energy: Optional[float] = Field(
        ...,
        description="""The computed formation energy per atom in eV."""
    )

    hull_distance: Optional[float] = Field(
        ...,
        description="""The computed distance from the convex hull in eV."""
    )

    relative_enthalpy: Optional[float] = Field(
        ...,
        description="""The relative enthalpy per atom in eV, versus some appropriate reference calculation. """,
    )
