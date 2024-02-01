from rdddy.generators.gen_python_primitive import (
    GenPythonPrimitive,
)  # replace with the actual import
import pytest
from unittest.mock import patch, MagicMock
from dspy import ChainOfThought, settings, OpenAI, DSPyAssertionError


@pytest.fixture
def gen_python_primitive():
    with patch.object(settings, "configure"), patch.object(
        OpenAI, "__init__", return_value=None
    ):
        yield GenPythonPrimitive(list)


@patch("dspy.predict.Predict.forward")
@patch("rdddy.generators.gen_module.ChainOfThought")
@patch("ast.literal_eval")
def test_forward_success(
    mock_literal_eval, mock_chain_of_thought, mock_predict, gen_python_primitive
):
    # Setup mock responses
    mock_predict.return_value.get.return_value = "['Jupiter', 'Saturn']"
    mock_chain_of_thought.return_value.get.return_value = "['Jupiter', 'Saturn']"
    mock_literal_eval.return_value = ["Jupiter", "Saturn"]

    # Call the method
    result = gen_python_primitive.forward(prompt="Create a list of planets")
    assert result == ["Jupiter", "Saturn"]


@patch("dspy.predict.Predict.forward")
@patch("rdddy.generators.gen_module.ChainOfThought")
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
    with pytest.raises(DSPyAssertionError):
        gen_python_primitive.forward(prompt="Create a list with syntax error")
