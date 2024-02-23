from datetime import datetime

from pydantic import *


class VAVAILABILITYModel(BaseModel):
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
        max_length=255,
    )
    description: str = Field(
        default=None, title="", description="A detailed description of the event."
    )
    location: str = Field(
        default=None, title="", description="The location of the event."
    )
    rrule: str = Field(
        default=None, title="", description="A recurrence rule for the event."
    )
    exdate: datetime = Field(
        default=None,
        title="",
        description="A list of dates to exclude from the recurrence rule.",
    )
    uid: str = Field(
        default=None,
        title="",
        description="A unique identifier for the event.",
        required=True,
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
        default=0, title="", description="The sequence number of the event.", ge=0
    )
    status: str = Field(
        default="CONFIRMED",
        title="",
        description="The status of the event.",
        allowed_values=["CONFIRMED", "TENTATIVE", "CANCELLED"],
    )
    organizer: str = Field(
        default=None, title="", description="The organizer of the event."
    )
    attendees: list[str] = Field(
        default=None, title="", description="A list of attendees for the event."
    )
    categories: list[str] = Field(
        default=None, title="", description="A list of categories for the event."
    )
    url: str = Field(default=None, title="", description="A URL for the event.")
