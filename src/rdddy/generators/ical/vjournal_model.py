from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VJOURNALModel(BaseModel):
    """A Pydantic model for RFC 5545 VJOURNAL compliance."""
    dtstamp: datetime = Field(default=None, title="", description="The date and time stamp for the creation of the VJOURNAL.", required)
    uid: str = Field(default=None, title="", description="A unique identifier for the VJOURNAL.", required)
    dtstart: datetime = Field(default=None, title="", description="The start date and time for the VJOURNAL.", required)
    summary: str = Field(default=None, title="", description="A summary of the VJOURNAL.", required)
    description: str = Field(default=None, title="", description="A detailed description of the VJOURNAL.")
    location: str = Field(default=None, title="", description="The location of the VJOURNAL.")
    categories: List[str] = Field(default=None, title="", description="A list of categories for the VJOURNAL.")
    status: str = Field(default=None, title="", description="The status of the VJOURNAL.")
    priority: int = Field(default=None, title="", description="The priority of the VJOURNAL.", ge=0, le=9)
    url: str = Field(default=None, title="", description="A URL associated with the VJOURNAL.")
    created: datetime = Field(default=None, title="", description="The creation date and time of the VJOURNAL.")
    last_modified: datetime = Field(default=None, title="", description="The last modified date and time of the VJOURNAL.")
    organizer: str = Field(default=None, title="", description="The organizer of the VJOURNAL.")
    attendees: List[str] = Field(default=None, title="", description="A list of attendees for the VJOURNAL.")
    related_to: str = Field(default=None, title="", description="A related event or task for the VJOURNAL.")

