from datetime import datetime

from pydantic import *


class VFREEBUSYModel(BaseModel):
    """A Pydantic model for RFC 5545 VFREEBUSY compliance."""

    dtstart: datetime = Field(
        default=...,
        title="",
        description="The start date and time for the VFREEBUSY period.",
    )
    dtend: datetime = Field(
        default=...,
        title="",
        description="The end date and time for the VFREEBUSY period.",
    )
    dtstamp: datetime = Field(
        default=...,
        title="",
        description="The date and time when the VFREEBUSY was created.",
    )
    organizer: str = Field(
        default="", title="", description="The organizer of the VFREEBUSY period."
    )
    uid: str = Field(
        default="",
        title="",
        description="The unique identifier for the VFREEBUSY period.",
    )
    url: str = Field(
        default="", title="", description="The URL for the VFREEBUSY period."
    )
    freebusy: str = Field(
        default="",
        title="",
        description="The free or busy time periods for the VFREEBUSY period.",
    )
    attendee: str = Field(
        default="", title="", description="The attendees for the VFREEBUSY period."
    )
    comment: str = Field(
        default="",
        title="",
        description="Any comments or notes for the VFREEBUSY period.",
    )
    contact: str = Field(
        default="",
        title="",
        description="The contact information for the VFREEBUSY period.",
    )
    request_status: str = Field(
        default="", title="", description="The status of the VFREEBUSY request."
    )
    sequence: int = Field(
        default=0,
        title="",
        description="The sequence number for the VFREEBUSY period.",
    )
    x_prop: str = Field(
        default="",
        title="",
        description="Any additional properties for the VFREEBUSY period.",
    )
    x_component: str = Field(
        default="",
        title="",
        description="Any additional components for the VFREEBUSY period.",
    )
