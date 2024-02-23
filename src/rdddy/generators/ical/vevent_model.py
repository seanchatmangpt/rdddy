from datetime import datetime

from pydantic import *


class VEVENTModel(BaseModel):
    """A Pydantic model for RFC 5545 compliance."""

    dtstart: datetime = Field(
        default=None,
        title="",
        description="The start date and time of the event.",
        required=True,
    )
    dtend: datetime = Field(
        default=None,
        title="",
        description="The end date and time of the event.",
        required=True,
    )
    summary: str = Field(
        default=None,
        title="",
        description="A brief summary or title of the event.",
        max_length=50,
    )
    description: str = Field(
        default=None, title="", description="A detailed description of the event."
    )
    location: str = Field(
        default=None, title="", description="The location of the event."
    )
    organizer: str = Field(
        default=None, title="", description="The organizer or creator of the event."
    )
    attendees: list[str] = Field(
        default=None, title="", description="A list of attendees for the event."
    )
    categories: list[str] = Field(
        default=None,
        title="",
        description="A list of categories or tags for the event.",
    )
    status: str = Field(
        default="TENTATIVE",
        title="",
        description="The status of the event, e.g., 'TENTATIVE', 'CONFIRMED', or 'CANCELLED'.",
        pattern="^(TENTATIVE|CONFIRMED|CANCELLED)$",
    )
    priority: int = Field(
        default=0,
        title="",
        description="The priority of the event, with 0 being the lowest and 9 being the highest.",
        ge=0,
        le=9,
    )
    url: str = Field(
        default=None,
        title="",
        description="A URL for the event, if available.",
        url=True,
    )
    created: datetime = Field(
        default=None, title="", description="The date and time the event was created."
    )
    last_modified: datetime = Field(
        default=None,
        title="",
        description="The date and time the event was last modified.",
    )
    sequence: int = Field(
        default=0,
        title="",
        description="The sequence number of the event, used for versioning.",
        ge=0,
    )
    uid: str = Field(
        default=None,
        title="",
        description="A unique identifier for the event.",
        uuid=True,
    )
    recurrence_id: datetime = Field(
        default=None,
        title="",
        description="The date and time of a recurring event instance.",
    )
