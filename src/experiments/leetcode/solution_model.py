import inflection
from dspy import OpenAI, settings

from rdddy.generators.gen_pydantic_class import (
    PydanticClassTemplateSpecificationModel,
    FieldTemplateSpecificationModel,
    class_template_str,
)
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from typetemp.functional import render


# Define the function to generate and write a Pydantic class based on a prompt
def generate_pydantic_class(prompt: str, filename: str):
    # Initialize the LM with DSPy settings
    lm = OpenAI(max_tokens=3000)
    settings.configure(lm=lm)

    # Define the GenPydanticInstance module with the appropriate root and child models
    model_module = GenPydanticInstance(
        root_model=PydanticClassTemplateSpecificationModel,
        child_models=[FieldTemplateSpecificationModel],
    )

    # Generate the Pydantic model instance from the prompt
    model_inst = model_module.forward(prompt)

    # Render the Pydantic class from the specification
    rendered_class_str = render(class_template_str, model=model_inst)

    # Define a helper function to write the rendered class to a Python file
    def write_pydantic_class_to_file(class_str: str, file_path: str):
        with open(file_path, "w") as file:
            file.write(class_str)

    # Write the rendered class to the specified filename
    write_pydantic_class_to_file(rendered_class_str, filename)

    print(f"Pydantic model written to {filename}")


# Example usage
if __name__ == "__main__":
    # Define your prompt here
    prompt = (
        "I need a model for interview coding challenge questions, answers, and hints"
    )

    # Specify the filename for the generated Pydantic model
    filename = "solution_model2.py"

    # Generate the Pydantic class and write it to a file
    generate_pydantic_class(prompt, filename)
