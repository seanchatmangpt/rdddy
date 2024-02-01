import inspect

from jinja2 import Environment, FileSystemLoader


from pydantic import BaseModel, Field
from typing import List

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.generators.gen_python_primitive import GenPythonPrimitive


class Command(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the command")
    help: str = Field(..., min_length=1, description="The help text for the command")


class TyperCLI(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the CLI application")
    commands: List[Command] = Field(
        ..., description="The commands of the CLI application"
    )


# Example description for testing
cli_description = f"""


We are building a Typer CLI application named 'DSPyGenerator'. It should include the following commands:

1. Command Name: generate_module
   Help: Generates a new DSPy module with a specified name.

2. Command Name: generate_signature
   Help: Creates a new signature class for defining input-output behavior in DSPy modules.

3. Command Name: generate_chainofthought
   Help: Generates a ChainOfThought module with a standard question-answering signature.

4. Command Name: generate_retrieve
   Help: Generates a Retrieve module for use in information retrieval tasks within DSPy.

5. Command Name: generate_teleprompter
   Help: Creates a teleprompter setup for optimizing DSPy programs.

6. Command Name: generate_example
   Help: Generates an example structure for use in training and testing DSPy modules.

7. Command Name: generate_assertion
   Help: Generates a template for creating LM Assertions in DSPy programs.

"""

model = GenPydanticInstance(root_model=TyperCLI, child_models=[Command]).forward(
    cli_description
)

# Example CLI data
cli_data = model


# --- Jinja Templates ---
cli_template = """
import typer
app = typer.Typer()

{% for command in cli_data.commands %}
@app.command(name="{{ command.name }}")
def {{ command.name }}():
    \"\"\"{{ command.help }}\"\"\"
    # Command logic goes here
    print("This is the {{ command.name }} command.")

{% endfor %}

if __name__ == "__main__":
    app()


"""

pytest_template = """
import pytest
from typer.testing import CliRunner
from metadspy.cli import app  # Updated import statement

runner = CliRunner()

{% for command in cli_data.commands %}
def test_{{ command.name }}():
    result = runner.invoke(app, ["{{ command.name }}"])
    assert result.exit_code == 0
    assert "This is the {{ command.name }} command." in result.output  # Replace with specific expected output

{% endfor %}
"""

# --- Render Templates ---
env = Environment(loader=FileSystemLoader("."))
env.from_string(cli_template).stream(cli_data=cli_data.model_dump()).dump(
    "generated_cli.py"
)
env.from_string(pytest_template).stream(cli_data=cli_data.model_dump()).dump(
    "test_generated_cli.py"
)

print("CLI application and tests generated.")
