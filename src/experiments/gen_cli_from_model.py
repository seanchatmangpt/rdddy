from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

import dspy
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance


class TyperCommand(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the command")
    help: str = Field(..., min_length=1, description="The help text for the command")


class TyperCLI(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the CLI application")
    commands: list[TyperCommand] = Field(
        ..., description="The commands of the CLI application"
    )


# Example description for testing
cli_description = """


DSPy Framework CLI v1.0.0
A Ruby on Rails-style framework CLI for streamlined AI application development.

USAGE:
    dspy [SUBCOMMAND]

SUBCOMMANDS:
    new             Create a new DSPy project with a default directory structure and configuration.
    generate        Generate new components within your DSPy project (e.g., modules, datasets, models).
    server          Start a local server for developing and testing your DSPy application.
    test            Run tests on your DSPy application, including model evaluations and data validations.
    deploy          Deploy your DSPy application to various environments (development, testing, production).
    db              Database operations, such as migrations, seeding, and schema loading.
    data            Manage your datasets, including import, export, and version control.
    eval            Evaluate your models or entire pipelines with custom or predefined metrics.
    help            Displays help information about the available commands.

EXAMPLES:
    # Create a new DSPy project named MyAIApp
    dspy new MyAIApp

    # Generate a new data model within the project
    dspy generate model MyNewModel

    # Run the development server
    dspy server

    # Run tests
    dspy test

    # Deploy your application to production
    dspy deploy --environment=production

    # Perform database migration
    dspy db migrate

    # Import a dataset from a file
    dspy data import --source=./path/to/dataset.csv

    # Evaluate a model with a specific metric
    dspy eval --model=MyModel --metric=f1_score

    # Display help for the 'generate' subcommand
    dspy help generate

For more information on a specific command, use 'dspy [subcommand] --help'.

GLOBAL OPTIONS:
    -h, --help       Prints help information
    -v, --version    Prints version information

ENVIRONMENT VARIABLES:
    DSPY_ENV         Sets the environment for the DSPy CLI (default: development)

CONFIGURATION:
    Configuration for the DSPy CLI and projects can be set in `.dspy.yml` within your project directory or global configuration files.

SUPPORT & DOCUMENTATION:
    For more details, visit the official DSPy documentation at [DSPy Framework Documentation URL].
    For support, reach out to the community forum or issue tracker on our GitHub repository.



"""


def main():
    lm = dspy.OpenAI(max_tokens=3000, model="gpt-4")
    dspy.settings.configure(lm=lm)

    model = GenPydanticInstance(
        root_model=TyperCLI, child_models=[TyperCommand]
    ).forward(cli_description)

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
        "ror_dspy.py"
    )
    env.from_string(pytest_template).stream(cli_data=cli_data.model_dump()).dump(
        "test_ror_dspy.py"
    )

    print("CLI application and tests generated.")


if __name__ == "__main__":
    main()
