from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class VTODOModel(BaseModel):
    """A model for RFC 5545 compliance."""
    
    summary: str = Field(default=None, title="", description="A summary of the task.")
    
    due_date: datetime = Field(default=None, title="", description="The due date of the task.")
    

    
    