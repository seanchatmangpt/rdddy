from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class HelloWorld(BaseModel):
    """A simple Pydantic model for displaying a message."""
    message: str = Field(default="Hello, World!", title="", description="A simple message to be displayed.")

