from datetime import datetime

from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr

class PydanticClassTemplateSpecificationModel(BaseModel):
    """This model represents a contact from the friend of a friend ontology."""
    name: str = Field(default=None, title="", description="The name of the contact.", min_length=2, max_length=50)
    email: EmailStr = Field(default=None, title="", description="The email address of the contact.")
    phone_number: str = Field(default=None, title="", description="The phone number of the contact.", min_length=10, max_length=15)
    address: str = Field(default=None, title="", description="The address of the contact.", min_length=5, max_length=100)
    birthday: datetime = Field(default=None, title="", description="The birthday of the contact.", ge=1900, le=2021)
    gender: str = Field(default=None, title="", description="The gender of the contact.", in=['male', 'female', 'other'])
    occupation: str = Field(default=None, title="", description="The occupation of the contact.", min_length=2, max_length=50)
    relationship_status: str = Field(default=None, title="", description="The relationship status of the contact.", in=['single', 'married', 'divorced', 'widowed'])
    interests: List[str] = Field(default=None, title="", description="A list of the contact's interests.")
    notes: str = Field(default=None, title="", description="Any additional notes about the contact.", max_length=500)

