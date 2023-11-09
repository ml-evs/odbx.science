from typing import Optional
from pydantic import Field
from optimade.models.references import Person

__all__ = ["MatadorPerson"]


class MatadorPerson(Person):
    """Container for a person."""

    email: str = Field(
        ...,
        description="""Email address of the submitted, at the time of entry creation.""",
    )

    forwarding_email: Optional[str] = Field(
        None,
        description="""Optional contact email for the person, valid at the last modification time.""",
    )

    identifier: str = Field(
        ...,
        description="""Optional extra identifier for the person, if name or other is not known, for example their university ID.""",
    )

    name: Optional[str] = Field(
        None, description="""The full name of the submitter, if known."""
    )
