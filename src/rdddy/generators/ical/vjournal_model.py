from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VJOURNALModel(BaseModel):
    """A Pydantic model for RFC 5545 compliance."""
    
    dtstamp: datetime = Field(default=None, title="", description="The date and time stamp for the journal entry.")
    
    uid: str = Field(default=None, title="", description="A unique identifier for the journal entry.")
    
    dtstart: datetime = Field(default=None, title="", description="The start date and time for the journal entry.")
    
    summary: str = Field(default=None, title="", description="A brief summary of the journal entry.", min_length=2, max_length=50)
    
    description: str = Field(default=None, title="", description="A detailed description of the journal entry.")
    

    
    