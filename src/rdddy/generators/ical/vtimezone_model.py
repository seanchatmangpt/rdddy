from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VTIMEZONEModel(BaseModel):
    """A Pydantic model for RFC 5545 compliance."""

    dtstart: datetime = Field(
        default=None,
        title="",
        description="The start date and time for the event.",
        ge=0,
    )
    dtend: datetime = Field(
        default=None, title="", description="The end date and time for the event.", ge=0
    )
    tzoffsetfrom: str = Field(
        default=None,
        title="",
        description="The time zone offset from UTC for the start date and time.",
        min_length=2,
        max_length=5,
    )
    tzoffsetto: str = Field(
        default=None,
        title="",
        description="The time zone offset from UTC for the end date and time.",
        min_length=2,
        max_length=5,
    )
    tzname: str = Field(
        default=None,
        title="",
        description="The name of the time zone.",
        min_length=2,
        max_length=50,
    )
    rrule: str = Field(
        default=None,
        title="",
        description="The recurrence rule for the event.",
        min_length=2,
        max_length=50,
    )
    exdate: datetime = Field(
        default=None,
        title="",
        description="The date and time to exclude from the recurrence rule.",
        ge=0,
    )
    rdate: datetime = Field(
        default=None,
        title="",
        description="The date and time to include in the recurrence rule.",
        ge=0,
    )
    tzid: str = Field(
        default=None,
        title="",
        description="The unique identifier for the time zone.",
        min_length=2,
        max_length=50,
    )
    tzurl: str = Field(
        default=None,
        title="",
        description="The URL for the time zone definition.",
        min_length=2,
        max_length=200,
    )
    last_modified: datetime = Field(
        default=None,
        title="",
        description="The date and time when the time zone was last modified.",
        ge=0,
    )
    created: datetime = Field(
        default=None,
        title="",
        description="The date and time when the time zone was created.",
        ge=0,
    )
    description: str = Field(
        default=None,
        title="",
        description="A description of the time zone.",
        min_length=2,
        max_length=200,
    )
    location: str = Field(
        default=None,
        title="",
        description="The location of the time zone.",
        min_length=2,
        max_length=200,
    )
    tzoffsetfrom: str = Field(
        default=None,
        title="",
        description="The time zone offset from UTC for the start date and time.",
        min_length=2,
        max_length=5,
    )
    tzoffsetto: str = Field(
        default=None,
        title="",
        description="The time zone offset from UTC for the end date and time.",
        min_length=2,
        max_length=5,
    )
