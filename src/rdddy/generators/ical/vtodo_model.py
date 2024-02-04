from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VTODOModel(BaseModel):
    """A Pydantic model for RFC 5545 compliance."""
    dtstamp: datetime = Field(default=None, title="", description="The date and time stamp for the creation of the VTODO.", required)
    uid: str = Field(default=None, title="", description="A unique identifier for the VTODO.", required)
    dtstart: datetime = Field(default=None, title="", description="The start date and time for the VTODO.", required)
    due: datetime = Field(default=None, title="", description="The due date and time for the VTODO.", required)
    summary: str = Field(default=None, title="", description="A summary of the VTODO.", required)
    description: str = Field(default=None, title="", description="A detailed description of the VTODO.")
    priority: int = Field(default=0, title="", description="The priority of the VTODO, with 0 being the lowest and 9 being the highest.", ge=0, le=9)
    status: str = Field(default=NEEDS-ACTION, title="", description="The status of the VTODO, with options such as 'NEEDS-ACTION', 'COMPLETED', or 'CANCELLED'.", in=['NEEDS-ACTION', 'COMPLETED', 'CANCELLED'])
    categories: List[str] = Field(default=None, title="", description="A list of categories for the VTODO.")
    location: str = Field(default=None, title="", description="The location of the VTODO.")
    url: str = Field(default=None, title="", description="A URL associated with the VTODO.")
    rrule: str = Field(default=None, title="", description="A recurrence rule for the VTODO, specified as a string.")
    exdate: List[datetime] = Field(default=None, title="", description="A list of dates to exclude from the recurrence rule.")
    duration: str = Field(default=None, title="", description="The duration of the VTODO, specified as a string.")
    attach: List[str] = Field(default=None, title="", description="A list of attachments for the VTODO.")

