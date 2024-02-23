from datetime import datetime

from pydantic import *


class VALARMModel(BaseModel):
    """A Pydantic model for RFC 5545 compliance."""

    action: str = Field(
        default=None, title="", description="The action associated with the alarm."
    )
    trigger: str = Field(
        default=None, title="", description="The trigger for the alarm."
    )
    duration: str = Field(
        default=None, title="", description="The duration of the alarm."
    )
    repeat: int = Field(
        default=None,
        title="",
        description="The number of times the alarm should be repeated.",
        ge=0,
    )
    description: str = Field(
        default=None, title="", description="A description of the alarm."
    )
    summary: str = Field(default=None, title="", description="A summary of the alarm.")
    attendees: list[str] = Field(
        default=None, title="", description="A list of attendees for the alarm."
    )
    acknowledged: datetime = Field(
        default=None,
        title="",
        description="The date and time the alarm was acknowledged.",
    )
    related_to: str = Field(
        default=None, title="", description="The related event or to-do for the alarm."
    )
    uid: str = Field(
        default=None, title="", description="The unique identifier for the alarm."
    )
    created: datetime = Field(
        default=None, title="", description="The date and time the alarm was created."
    )
    last_modified: datetime = Field(
        default=None,
        title="",
        description="The date and time the alarm was last modified.",
    )
    sequence: int = Field(
        default=None, title="", description="The sequence number for the alarm.", ge=0
    )
    x_prop: str = Field(
        default=None,
        title="",
        description="Any additional custom properties for the alarm.",
    )
    attach: list[str] = Field(
        default=None, title="", description="A list of attachments for the alarm."
    )
