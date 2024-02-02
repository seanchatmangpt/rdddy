import dspy
import inflection
import jinja2
from pydantic import BaseModel, Field

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from typetemp.functional import render
from typing import List, Optional


class FieldTemplateSpecificationModel(BaseModel):
    field_name: str = Field(
        ...,
        title="Field Name",
        description="The name of the field in the model.",
    )
    field_type: str = Field(
        ...,
        title="Field Type",
        description="The data type of the field, e.g., 'str', 'int', 'EmailStr', or 'datetime'.",
    )
    default_value: str | None = Field(
        "...",
        title="Default Value",
        description="The default value for the field if not provided.",
    )
    description: str = Field(
        ...,
        title="Description",
        description="A detailed description of the field's purpose and usage.",
    )
    constraints: str | None = Field(
        None,
        title="Constraints",
        description="Constraints or validation rules for the field, if any. Specify as a string, e.g., 'min_length=2, max_length=50' or 'ge=0, le=120'.",
    )


class ConfigTemplateSpecificationModel(BaseModel):
    class Config:
        title = "Model Configuration"
        description = "Configuration settings for a Pydantic BaseModel."

    title: str = Field(
        ...,
        description="The title for the BaseModel configuration.",
    )
    description: str = Field(
        ...,
        description="A detailed description of the BaseModel configuration's purpose and usage.",
    )
    allow_population_by_field_name: bool = Field(
        True,
        description="Whether to allow populating a model using field names.",
    )
    underscore_attrs_are_private: bool = Field(
        False,
        description="Whether to treat underscore-prefixed attributes as private (no validation).",
    )
    alias_generator: str = Field(
        ...,
        description="The alias generator to use for field aliasing.",
    )


class ValidatorTemplateSpecificationModel(BaseModel):
    validator_name: str = Field(
        ...,
        title="Validator Name",
        description="The name of the validator.",
    )
    description: str = Field(
        ...,
        title="Description",
        description="A detailed description of the validator's purpose and usage.",
    )
    parameters: List[str] = Field(
        [],
        title="Parameters",
        description="A list of parameter names accepted by the validator.",
    )


class PydanticClassTemplateSpecificationModel(BaseModel):
    class_name: str = Field(
        ...,
        title="Model Class Name",
        description="The class name of the Pydantic model.",
    )
    description: str = Field(
        ...,
        title="Description",
        description="A detailed description of the Pydantic model's purpose and usage.",
    )
    fields: List[FieldTemplateSpecificationModel] = Field(
        ...,
        title="Fields",
        description="A list of field specifications for the model. Each field specifies the name, type, default value, description, and constraints.",
    )



template_str = '''from pydantic import BaseModel, Field, validator, root_validator, EmailStr, UrlStr
from typing import List, Optional
from datetime import datetime


class {{ model.class_name }}(BaseModel):
    """{{ model.description }}"""
    {% for field in model.fields %}
    {{ field.field_name }}: {{ field.field_type }} = Field(default={{ field.default_value }}, title="{{ field.title }}", description="{{ field.description }}"{% if field.constraints %}, {{ field.constraints }}{% endif %})
    {% endfor %}

    {% if model.validators|length > 0 %}
    {% for validator in model.validators %}
    @validator('{{ validator.parameters|join("', '") }}')
    def {{ validator.validator_name }}(cls, value):
        # {{ validator.description }}
        return value
    {% endfor %}
    {% endif %}
    {% if model.config %}
    class Config:
        {% if model.config.allow_population_by_field_name %}allow_population_by_field_name = True{% endif %}
        {% if model.config.underscore_attrs_are_private %}underscore_attrs_are_private = True{% endif %}
        {% if model.config.alias_generator %}alias_generator = {{ model.config.alias_generator }}{% endif %}
    {% endif %}
'''

def render_pydantic_class(model_spec, template_str):
    template = jinja2.Template(template_str)
    return template.render(model=model_spec)


def write_pydantic_class_to_file(class_str, filename):
    with open(filename, 'w') as file:
        file.write(class_str)


# Example usage
def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    model_prompt = "I need a verbose contact model named ContactModel from the friend of a friend ontology with 10 fields, each with length constraints"

    model_module = GenPydanticInstance(root_model=PydanticClassTemplateSpecificationModel,
                                     child_models=[FieldTemplateSpecificationModel
                                                   ])

    model_inst = model_module.forward(model_prompt)

    # Render the Pydantic class from the specification
    rendered_class_str = render(template_str, model=model_inst)

    # Write the rendered class to a Python file
    write_pydantic_class_to_file(rendered_class_str, f"{inflection.underscore(model_inst.class_name)}.py")


if __name__ == '__main__':
    main()
