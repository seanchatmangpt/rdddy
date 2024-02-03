from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VEVENTModel(BaseModel):
    """A model for RFC 5545 compliance."""
    
    DTSTART: datetime = Field(default=None, title="", description="The start date and time of the event.")
    
    DTEND: datetime = Field(default=None, title="", description="The end date and time of the event.")
    
    SUMMARY: str = Field(default=None, title="", description="A brief summary or title of the event.")
    
    LOCATION: str = Field(default=None, title="", description="The location of the event.")
    
    DESCRIPTION: str = Field(default=None, title="", description="A detailed description of the event.")
    
    UID: str = Field(default=None, title="", description="A unique identifier for the event.")
    

    
    