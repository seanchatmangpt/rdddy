import pathlib

import typer

import dspy
from typetemp.functional import render
from utils.create_prompts import create_pydantic_class

turbo = dspy.OpenAI(max_tokens=2000)
dspy.settings.configure(lm=turbo)

app = typer.Typer()

# Get the absolute path to the directory where this script is located
module_dir = pathlib.Path(__file__).parent.absolute()

# Path to the templates directory
templates_dir = module_dir / "templates"


@app.command(name="module")
def generate_module(
    name: str = typer.Argument(..., help="Name of the module to generate"),
    output_key: str = typer.Option(
        ..., "--output-key", "-o", help="The output key for the module"
    ),
    input_key: str = typer.Option(
        ..., "--input-key", "-i", help="The primary input key for the module"
    ),
    additional_inputs: str = typer.Option(
        None, "--additional-inputs", help="Comma-separated additional input keys"
    ),
):
    """Generates a new DSPy module with a specified name."""
    template_path = templates_dir / "module_template.j2"

    # Handling additional input keys
    input_keys = [input_key] + (
        additional_inputs.split(",") if additional_inputs else []
    )

    rendered = render(
        template_path, name=name, output_key=output_key, input_key_or_keys=input_keys
    )

    typer.echo(rendered)


@app.command(name="signature")
def generate_signature():
    """Creates a new signature class for defining input-output behavior in DSPy modules."""
    # Command logic goes here
    print("This is the generate_signature command.")


@app.command(name="chainofthought")
def generate_chainofthought():
    """Generates a ChainOfThought module with a standard question-answering signature."""
    # Command logic goes here
    print("This is the generate_chainofthought command.")


@app.command(name="retrieve")
def generate_retrieve():
    """Generates a Retrieve module for use in information retrieval tasks within DSPy."""
    # Command logic goes here
    print("This is the generate_retrieve command.")


@app.command(name="teleprompter")
def generate_teleprompter():
    """Creates a teleprompter setup for optimizing DSPy programs."""
    # Command logic goes here
    print("This is the generate_teleprompter command.")


@app.command(name="example")
def generate_example():
    """Generates an example structure for use in training and testing DSPy modules."""
    # Command logic goes here
    print("This is the generate_example command.")


@app.command(name="assertion")
def generate_assertion():
    """Generates a template for creating LM Assertions in DSPy programs."""
    # Command logic goes here
    print("This is the generate_assertion command.")


def write_to_file(content, filename):
    with open(filename, "w") as f:
        f.write(content)


prompt = """ FastAPI route import """


def main():
    # app()

    # # model = PydanticSHACLGenerator().forward(prompt)
    # write_to_file(model, 'fastapi_route.py')
    print(create_pydantic_class())


if __name__ == "__main__":
    main()
