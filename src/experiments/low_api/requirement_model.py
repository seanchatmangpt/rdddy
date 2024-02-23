from pydantic import BaseModel, Field


class Requirement(BaseModel):
    id: str = Field(..., description="Unique identifier for the requirement")
    description: str = Field(..., description="Detailed description of the requirement")
    precondition: str = Field(..., description="Description of the precondition for the requirement")
    process: str = Field(
        ..., description="Description of the process or action to be taken"
    )
    postcondition: str = Field(..., description="Expected postcondition or result of the requirement")
    acceptance_criteria: list[str] = Field(
        ...,
        description="Criteria for accepting the requirement as successfully implemented",
    )


class FunctionalRequirementsSpec(BaseModel):
    project_name: str = Field(..., description="Name of the project or system")
    version: str = Field(..., description="Version of the requirements specification")
    requirements: list[Requirement] = Field(
        ..., description="List of individual functional requirements"
    )
