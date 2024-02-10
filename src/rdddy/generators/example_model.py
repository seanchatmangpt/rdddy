from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr


class ExampleModel(BaseModel):
    """An example Pydantic model for demonstration."""

    email: EmailStr = Field(
        default="default@example.com", title="", description="User's email address"
    )
