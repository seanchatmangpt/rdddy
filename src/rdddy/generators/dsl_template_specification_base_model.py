from pydantic import Field
from rdddy.generators.gen_meta_template_spec_model import TemplateSpecificationBaseModel


class DSLTemplateSpecificationBaseModel(TemplateSpecificationBaseModel):
    """A Pydantic model for jinja templates that render DSL models."""

    dsl_name = Field(default=None, description="The name of the DSL being defined")
    dsl_description = Field(
        default=None,
        description="A detailed description of the DSL's purpose and usage.",
    )
    dsl_syntax = Field(default=None, description="The syntax of the DSL being defined")
