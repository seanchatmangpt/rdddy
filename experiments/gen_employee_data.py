import pytest
from unittest.mock import patch
from rdddy.generators.gen_python_primitive import (
    GenPythonPrimitive,
)  # replace with the actual import
import pytest
from unittest.mock import patch, MagicMock
from dspy import ChainOfThought, settings, OpenAI


@pytest.fixture
def gen_python_primitive():
    with patch.object(settings, "configure"), patch.object(
        OpenAI, "__init__", return_value=None
    ):
        yield GenPythonPrimitive(list)


# def test_forward_success(
#     mock_literal_eval, mock_chain_of_thought, mock_predict, gen_python_primitive
# ):
#     # Setup mock responses
#     mock_predict.return_value.get.return_value = "['Jupiter', 'Saturn']"
#     mock_chain_of_thought.return_value.get.return_value = "['Jupiter', 'Saturn']"
#     mock_literal_eval.return_value = ["Jupiter", "Saturn"]
#
#     # Call the method
#     result = gen_python_primitive.forward("Create a list of planets")
#     assert result == ["Jupiter", "Saturn"]


@patch("dspy.predict.Predict.forward")
@patch("rdddy.generators.gen_python_primitive.ChainOfThought")
@patch("ast.literal_eval", side_effect=SyntaxError)
def test_forward_syntax_error(
    mock_literal_eval, mock_chain_of_thought, mock_predict, gen_python_primitive
):
    # Setup mock responses
    mock_predict.return_value.get.return_value = "{'Jupiter', 'Saturn'}"
    mock_chain_of_thought.side_effect = [
        MagicMock(get=MagicMock(return_value="{'Jupiter', 'Saturn'}")),  # initial call
        MagicMock(
            get=MagicMock(return_value="{'Jupiter', 'Saturn'}")
        ),  # correction call
    ]
    # Call the method and expect an error
    with pytest.raises(ValueError):
        gen_python_primitive.forward("Create a list with syntax error")

import inspect


from typing import List, Optional
from pydantic import BaseModel

from rdddy.generators.gen_python_primitive import GenPythonPrimitive


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class Employee(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    skills: List[str]
    address: Address
    is_manager: Optional[bool] = False


# Complex string describing an Employee instance
employee_description = f"""
Alex Johnson is 35 years old. His email is alex.johnson@example.com. 
He has skills in Python, JavaScript, and SQL. His address is 123 Main St, Springfield, IL, 62704, USA. 
Alex is not a manager. 
{inspect.getsource(Address)}
{inspect.getsource(Employee)}
"""


def test_forward_success(
    # mock_literal_eval, mock_chain_of_thought, mock_predict, gen_python_primitive
):
    # Setup mock responses
    response = {'first_name': 'Alex', 'last_name': 'Johnson', 'age': 35, 'email': 'alex.johnson@example.com', 'skills': ['Python', 'JavaScript', 'SQL'], 'address': {'street': '123 Main St', 'city': 'Springfield', 'state': 'IL', 'zip_code': '62704', 'country': 'USA'}, 'is_manager': False}
    # mock_predict.return_value.get.return_value = "['Jupiter', 'Saturn']"
    # mock_chain_of_thought.return_value.get.return_value = "['Jupiter', 'Saturn']"
    # mock_literal_eval.return_value = ["Jupiter", "Saturn"]

    # Call the method
    # result = gen_python_primitive.forward("Create a list of planets")
    # assert result == ["Jupiter", "Saturn"]

    module = GenPythonPrimitive(primitive_type=dict)

    result = module.forward(employee_description)

    print(f"{employee_description}: {Employee(**result)}")


# module = GenPythonPrimitive(primitive_type=dict)

# result = module.forward(employee_description)

# print(f"{employee_description}: {Employee(**result)}")
