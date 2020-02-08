from typing import Optional, Dict
from pydantic import Schema, EmailStr
from optimade.models.references import Person

__all__ = ["MatadorPerson"]


class MatadorPerson(Person):
    """ Container for a person. """

    email: EmailStr = Schema(
        ...,
        description="""Email address of the submitted, at the time of entry creation.""",
    )

    forwarding_email: Optional[EmailStr] = Schema(
        ...,
        description="""Optional contact email for the person, valid at the last modification time.""",
    )

    identifier: str = Schema(
        ...,
        description="""Optional extra identifier for the person, if name or other is not known, for example their university ID.""",
    )

    name: Optional[str] = Schema(
        ..., description="""The full name of the submitter, if known."""
    )
