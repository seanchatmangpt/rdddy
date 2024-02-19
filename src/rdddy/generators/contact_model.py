from datetime import datetime

from pydantic import *


class ContactModel(BaseModel):
    """A Pydantic model representing a contact in the friend of a friend ontology."""

    name: str = Field(
        default="",
        title="",
        description="The name of the contact.",
        min_length=2,
        max_length=50,
    )
    email: EmailStr = Field(
        default=...,
        title="",
        description="The email address of the contact.",
        min_length=5,
        max_length=50,
    )
    phone_number: str = Field(
        default="",
        title="",
        description="The phone number of the contact.",
        min_length=10,
        max_length=15,
    )
    address: str = Field(
        default="",
        title="",
        description="The address of the contact.",
        min_length=10,
        max_length=100,
    )
    birthday: datetime = Field(
        default=...,
        title="",
        description="The birthday of the contact.",
        ge=1900,
        le=2021,
    )
    relationship: str = Field(
        default="",
        title="",
        description="The relationship of the contact to the user.",
        min_length=2,
        max_length=50,
    )
    notes: str = Field(
        default="",
        title="",
        description="Any additional notes or information about the contact.",
        max_length=500,
    )
    social_media: str = Field(
        default="",
        title="",
        description="The social media accounts of the contact.",
        max_length=100,
    )
    company: str = Field(
        default="",
        title="",
        description="The company the contact works for.",
        min_length=2,
        max_length=50,
    )
    job_title: str = Field(
        default="",
        title="",
        description="The job title of the contact.",
        min_length=2,
        max_length=50,
    )
