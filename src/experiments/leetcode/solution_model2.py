from pydantic import BaseModel, Field


class InterviewCodingChallengeModel(BaseModel):
    """A Pydantic model for interview coding challenge pseudocode, solution, and hints."""

    question: str = Field(
        default=...,
        description="The question in natural language for the coding challenge. No psuedo code!",
        min_length=50,
    )
    solution: str = Field(
        default=...,
        description="The solution to the coding challenge pseudocode.",
        min_length=50,
    )
    hints: list[str] = Field(
        default=...,
        title="",
        description="Hints for solving the coding challenge pseudocode.",
        min_length=3,
    )
