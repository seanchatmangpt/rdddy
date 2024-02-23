from typing import Any

import inflection
import jinja2
from pydantic import BaseModel, Field

import dspy
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from typetemp.functional import render


class TemplateSpecificationBaseModel(BaseModel):
    """Template specification base model."""

    def __init__(self, **data: Any):
        super().__init__(**data)


class TemplateSpecificationFieldBaseModel(BaseModel):
    """Template specification field model."""

    def __init__(self, **data: Any):
        super().__init__(**data)


class MetaTemplateSpecificationFieldModel(TemplateSpecificationFieldBaseModel):
    """A Pydantic model for jinja templates that render Pydantic fields."""

    description: str = Field(
        ...,
        description="A detailed description of the field's purpose and usage.",
    )
    field_name: str = Field(
        ...,
        description="The name of the field in the generated template model. "
        "It should fit the description and be unique. No prefixes, suffixes, or abbreviations.",
    )
    default_value: str | None = Field(
        "...",
        description="The default value for the field if not provided.",
    )


class MetaTemplateSpecificationBaseModel(TemplateSpecificationBaseModel):
    """A Pydantic model for jinja templates that render BaseModels."""

    class_name: str = Field(
        ...,
        description="The name of the generated template model.",
    )
    docstring: str = Field(
        ...,
        description="A detailed docstring of the model's purpose and usage.",
    )
    fields: list[MetaTemplateSpecificationFieldModel] = Field(
        ...,
        description="A list of MetaFieldTemplateSpecificationModel instances defining the fields of the model.",
    )


template_str = '''from pydantic import Field
from rdddy.generators.gen_meta_template_spec_model import TemplateSpecificationBaseModel


class {{ model.class_name }}(TemplateSpecificationBaseModel):
    """{{ model.docstring }}"""
    {% for field in model.fields %}
    {{ field.field_name }} = Field(default={{ field.default_value }}, description="{{ field.description }}")
    {% endfor %}

'''


class RootModel(BaseModel):
    root_model_class_name: str = Field(..., description="The name of the root model")
    child_model_class_names: list[str] = Field(
        ..., description="The names of the child models"
    )


def gen_model_tree():
    generate_answer = dspy.ChainOfThought("question -> answer")
    prompt = """The iCalendar specification defines various entities that start with "V" for different components and properties. Here are some common entities that start with "V" in the iCalendar specification:

VEVENT: This is one of the most commonly used components in iCalendar and represents an event.

VTODO: Represents a to-do task or action item.

VJOURNAL: Represents a journal entry or a note.

VFREEBUSY: Represents information about the free or busy time of a calendar user.

VCALENDAR: The top-level component that encapsulates all other iCalendar components.

VTIMEZONE: Represents time zone information.

VAVAILABILITY: Represents availability information for a calendar user.

VALARM: Represents an alarm or reminder associated with an event or to-do.

Create the ICalendar root model and add the child entities
"""
    model_module = GenPydanticInstance(root_model=RootModel)

    icalendar_root_model = model_module.forward(prompt)

    # for child in icalendar_root_model.children:


icalendar_entities = {
    "VEVENT": "This is one of the most commonly used components in iCalendar and represents an event.",
    "VTODO": "Represents a to-do task or action item.",
    "VJOURNAL": "Represents a journal entry or a note.",
    "VFREEBUSY": "Represents information about the free or busy time of a calendar user.",
    "VTIMEZONE": "Represents time zone information.",
    "VAVAILABILITY": "Represents availability information for a calendar user.",
    "VALARM": "Represents an alarm or reminder associated with an event or to-do.",
}


def generate_icalendar_models():
    for entity, description in icalendar_entities.items():
        generate_answer = dspy.ChainOfThought("question -> answer")
        prompt = f"What are the exact fields or attributes of the {entity} in RFC 5545?"
        answer = generate_answer(question=prompt).answer
        print(f"{entity}: {answer}")

        # Define a Pydantic class dynamically for each entity
        model_prompt = f"I need a model named {entity}Model that has all of the relevant fields {description}"

        model_module = GenPydanticInstance(
            root_model=MetaTemplateSpecificationBaseModel,
            child_models=[MetaTemplateSpecificationFieldModel],
        )

        model_inst = model_module.forward(model_prompt)

        print(model_inst)

        # Render the Pydantic class from the specification
        rendered_class_str = render_pydantic_class(model_inst, template_str)

        # Write the rendered class to a Python file
        write_pydantic_class_to_file(
            rendered_class_str,
            f"ical/{inflection.underscore(model_inst.class_name)}.py",
        )

        print(f"{model_inst.class_name} written to {model_inst.class_name}.py")


def render_pydantic_class(model_spec, template_str):
    template = jinja2.Template(template_str)
    return template.render(model=model_spec)


def write_pydantic_class_to_file(class_str, filename):
    with open(filename, "w") as file:
        file.write(class_str)


# Example usage
def main():
    model_prompt = """I need a class named DSLTemplateSpecificationBaseModel,
    so that I can create Pydantic models for Domain Specific Languages. Come up with
    field names that fit a DSL template."""

    model_module = GenPydanticInstance(
        root_model=MetaTemplateSpecificationBaseModel,
        child_models=[MetaTemplateSpecificationFieldModel],
    )

    model_inst = model_module.forward(model_prompt)

    # Render the Pydantic class from the specification
    rendered_class_str = render(template_str, model=model_inst)

    # Write the rendered class to a Python file
    write_pydantic_class_to_file(
        rendered_class_str, f"{inflection.underscore(model_inst.class_name)}.py"
    )


if __name__ == "__main__":
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)
    # main()
    generate_icalendar_models()
