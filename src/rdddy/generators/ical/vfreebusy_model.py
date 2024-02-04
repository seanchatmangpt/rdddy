from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VFREEBUSYModel(BaseModel):
    """A Pydantic model for RFC 5545 VFREEBUSY compliance."""
    dtstart: datetime = Field(default=None, title="", description="The start date and time for the VFREEBUSY period.")
    dtend: datetime = Field(default=None, title="", description="The end date and time for the VFREEBUSY period.")
    dtstamp: datetime = Field(default=None, title="", description="The date and time when the VFREEBUSY was created.")
    organizer: str = Field(default=None, title="", description="The organizer of the VFREEBUSY period.")
    uid: str = Field(default=None, title="", description="The unique identifier for the VFREEBUSY period.")
    url: str = Field(default=None, title="", description="The URL for the VFREEBUSY period.")
    dtstamp: datetime = Field(default=None, title="", description="The date and time when the VFREEBUSY was last modified.")
    freebusy: str = Field(default=None, title="", description="The free or busy time periods for the VFREEBUSY period.")
    attendee: str = Field(default=None, title="", description="The attendees for the VFREEBUSY period.")
    comment: str = Field(default=None, title="", description="Any comments or notes for the VFREEBUSY period.")
    contact: str = Field(default=None, title="", description="The contact information for the VFREEBUSY period.")
    request_status: str = Field(default=None, title="", description="The status of the VFREEBUSY request.")
    sequence: int = Field(default=None, title="", description="The sequence number for the VFREEBUSY period.")
    x_prop: str = Field(default=None, title="", description="Any additional properties for the VFREEBUSY period.")
    x_component: str = Field(default=None, title="", description="Any additional components for the VFREEBUSY period.")

