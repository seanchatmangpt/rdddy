from rdddy.generators.gen_pydantic_instance import (
    GenPydanticInstance,
)
import pytest
from unittest.mock import patch, MagicMock
from dspy import settings, OpenAI, DSPyAssertionError
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError


class APIEndpoint(BaseModel):
    method: str = Field(..., description="HTTP method of the API endpoint")
    url: str = Field(..., description="URL of the API endpoint")
    description: str = Field(
        ..., description="Description of what the API endpoint does"
    )
    response: str = Field(..., description="Response from the API endpoint")
    query_params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")


VALID_PYDANTIC_MODEL_STRING = """{
    "method": "GET",
    "url": "/forecast/today",
    "description": "API endpoint for retrieving meteorological conditions",
    "response": "Structured summary of weather conditions",
    "query_params": {"geographical_area": "string"}
}"""

VALID_PROMPT = """
Imagine a digital portal where users can inquire about meteorological conditions. 
This portal is accessible through a web interface that interacts with a backend service. 
The service is invoked by sending a request to a specific endpoint. 
This request is crafted using a standard protocol for web communication. 
The endpoint's location is a mystery, hidden within the path '/forecast/today'. 
Users pose their inquiries by specifying a geographical area of interest, 
though the exact format of this specification is left to the user's imagination. 
Upon successful request processing, the service responds with a structured 
summary of the weather, encapsulating details such as temperature, humidity, 
and wind speed. However, the structure of this response and the means of 
accessing the weather summary are not explicitly defined.
"""


VALID_PYDANTIC_MODEL_DICT = {
    "method": "GET",
    "url": "/forecast/today",
    "description": "API endpoint for retrieving meteorological conditions",
    "response": "Structured summary of weather conditions",
    "query_params": {"geographical_area": "string"},
}

INVALID_STR = "{ 'name': 'Alice', 'age': 30, 'city': 'Wonderland' }"


@pytest.fixture
def gen_pydantic_model():
    with patch.object(settings, "configure"), patch.object(
        OpenAI, "__init__", return_value=None
    ):
        yield GenPydanticInstance(
            APIEndpoint
        )  # Replace APIEndpoint with your Pydantic model


@patch("dspy.predict.Predict.forward")
@patch("rdddy.generators.gen_module.ChainOfThought")
@patch("ast.literal_eval")
def test_forward_success(
    mock_literal_eval, mock_chain_of_thought, mock_predict, gen_pydantic_model
):
    # Mock responses for a successful forward pass
    mock_predict.return_value.get.return_value = (
        VALID_PYDANTIC_MODEL_STRING  # Replace with a valid string for your model
    )
    mock_chain_of_thought.return_value.get.return_value = VALID_PYDANTIC_MODEL_STRING
    mock_literal_eval.return_value = (
        VALID_PYDANTIC_MODEL_DICT  # Replace with a valid dict for your model
    )

    # Call the method
    result = gen_pydantic_model.forward(
        prompt=VALID_PROMPT
    )  # Replace with a valid prompt
    assert isinstance(
        result, APIEndpoint
    )  # Replace APIEndpoint with your Pydantic model class


@patch("dspy.predict.Predict.forward")
@patch("rdddy.generators.gen_module.ChainOfThought")
@patch("ast.literal_eval", side_effect=SyntaxError)
def test_forward_syntax_error(
    mock_literal_eval, mock_chain_of_thought, mock_predict, gen_pydantic_model
):
    # Setup mock responses for a syntax error case
    mock_predict.return_value.get.return_value = INVALID_STR
    mock_chain_of_thought.side_effect = [
        MagicMock(get=MagicMock(return_value=INVALID_STR)),  # initial call
        MagicMock(get=MagicMock(return_value=INVALID_STR)),  # correction call
    ]

    # Call the method and expect an error
    with pytest.raises(DSPyAssertionError):
        gen_pydantic_model.forward(prompt="///")  # Replace with an invalid prompt
