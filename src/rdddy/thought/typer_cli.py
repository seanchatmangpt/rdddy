import json

from pydantic import BaseModel, Field

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance

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


class Command(BaseModel):
    """Typer CLI command"""

    name: str = Field(..., min_length=1, description="The name of the command")
    help: str = Field(..., min_length=1, description="The help text for the command")


class TyperCLI(BaseModel):
    """Typer CLI name and commands"""

    name: str = Field(..., min_length=1, description="The name of the CLI application")
    commands: list[Command] = Field(
        ..., description="The commands of the CLI application"
    )


def main():
    dot = GenPydanticInstance(root_model=TyperCLI, models=[Command, TyperCLI])

    cli = dot.forward(prompt=cli_description)

    print(cli)


if __name__ == "__main__":
    main()
