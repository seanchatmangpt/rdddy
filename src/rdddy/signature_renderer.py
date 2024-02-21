from pydantic import BaseModel, Field

import dspy
from dspy import Signature
from dspy.signatures.field import InputField, OutputField
from typetemp.template.typed_template import TypedTemplate

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance


class InputFieldTemplateSpecModel(BaseModel):
    """Defines an input field for a DSPy Signature."""

    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str | None = Field(
        None,
        description="Optional additional context or labeling for the input field.",
    )
    desc: str = Field(
        ...,
        description="Description of the input field's purpose or the nature of content it should contain.",
    )


class OutputFieldTemplateSpecModel(BaseModel):
    """Defines an output field for a DSPy Signature."""

    name: str = Field(
        ...,
        description="The key used to access and pass the input within the Signature.",
    )
    prefix: str | None = Field(
        None,
        description="Optional additional context or labeling for the output field.",
    )
    desc: str = Field(
        ...,
        description="Description of the output field's purpose or the nature of content it should contain.",
    )


class SignatureTemplateSpecModel(BaseModel):
    '''
    Generate a Signature for the DSPy Framework.

    Examples:
    ```python
class CheckCitationFaithfulness(dspy.Signature):
    """Verify that the text is based on the provided context."""

    context = dspy.InputField(desc="facts here are assumed to be true")
    text = dspy.InputField()
    faithfulness = dspy.OutputField(desc="True/False indicating if text is faithful to context")

class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""

    context = dspy.InputField(desc="contains cited relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="Descriptive answer to the question")

class CheckForCitations(dspy.Signature):
    """Verify the text has proper citations."""

    context = dspy.InputField(desc="facts here are assumed to be true")
    text = dspy.InputField()
    cited = dspy.OutputField(desc="True/False indicating if citations are present")
    ```
    '''
    class_name: str = Field(
        ...,
        description="Signature class name. Use this to specify additional context or labeling.",
    )
    instructions: str = Field(
        ..., description="Documentation of the task's expected LM function and output."
    )
    input_fields: list[InputFieldTemplateSpecModel]
    output_fields: list[OutputFieldTemplateSpecModel]


def create_signature_class_from_model(model: SignatureTemplateSpecModel) -> type:
    """Create a DSPy Signature class from a Pydantic model.

    :param model: The Pydantic model to convert.
    :return: A DSPy Signature class.
    """
    class_dict = {"__doc__": model.instructions, "__annotations__": {}}

    # Process input fields
    for field in model.input_fields:
        input_field = InputField(prefix=field.prefix, desc=field.desc)
        class_dict[field.name] = input_field
        class_dict["__annotations__"][field.name] = InputField

    # Process output fields
    for field in model.output_fields:
        output_field = OutputField(prefix=field.prefix, desc=field.desc)
        class_dict[field.name] = output_field
        class_dict["__annotations__"][field.name] = OutputField

    # Dynamically create the Signature class
    signature_class = type(model.class_name, (Signature,), class_dict)
    return signature_class


class GenDSPySignatureTemplate(TypedTemplate):
    """
    Generates and renders DSPy Signature classes to disk using Jinja2 templates.
    """
    source = '''from dspy import Signature
from dspy.signatures.field import InputField, OutputField


class {{ signature.class_name }}(Signature):
    """
    {{ signature.instructions }}
    """
    {% for input_field in signature.input_fields %}
    {{ input_field.name }} = InputField(desc="{{ input_field.desc }}")
    {% endfor %}

    {% for output_field in signature.output_fields %}
    {{ output_field.name }} = OutputField(desc="{{ output_field.desc }}")
    {% endfor %}
    '''
    to = "signatures/{{ signature.class_name | underscore }}.py"

business_sig_prompts = [
    "I need a signature called CustomerFeedbackAnalysis that inputs 'customer_comments' and outputs 'sentiment_analysis'",
    "I need a signature called SalesPrediction that inputs 'historical_sales_data', 'current_market_trends' and outputs 'future_sales_estimate'",
    "I need a signature called EmployeePerformanceEvaluation that inputs 'employee_activities', 'project_outcomes' and outputs 'performance_rating'",
    "I need a signature called MarketSegmentation that inputs 'customer_demographics', 'purchase_history' and outputs 'segment_labels'",
    "I need a signature called ProductRecommendation that inputs 'customer_profile', 'browsing_history' and outputs 'recommended_products'",
    "I need a signature called InventoryOptimization that inputs 'current_inventory_levels', 'sales_forecasts' and outputs 'reorder_recommendations'",
    "I need a signature called RiskAssessment that inputs 'investment_portfolio', 'market_risks' and outputs 'risk_level'",
    "I need a signature called CustomerLifetimeValuePrediction that inputs 'customer_purchase_history', 'engagement_metrics' and outputs 'lifetime_value_estimate'",
    "I need a signature called CompetitorAnalysis that inputs 'competitor_product_offerings', 'market_position' and outputs 'competitive_advantages'",
    "I need a signature called OperationalEfficiencyImprovement that inputs 'current_operational_metrics', 'process_bottlenecks' and outputs 'improvement_recommendations'"
]

sig_module = GenPydanticInstance(
    root_model=SignatureTemplateSpecModel,
    child_models=[InputFieldTemplateSpecModel, OutputFieldTemplateSpecModel],
)

# Assuming we have a function `generate_signature_from_prompt` that takes a sig_prompt and processes it.
def generate_signature_from_prompt(sig_prompt):
    # This function is a placeholder for the actual logic that would generate a signature model from a prompt.
    sig_instance = sig_module.forward(sig_prompt)

    GenDSPySignatureTemplate(signature=sig_instance)()

    print(sig_instance)






def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    # Now, let's call this function for each prompt in the list.
    for prompt in business_sig_prompts:
        generate_signature_from_prompt(prompt)

    print(f"{len(business_sig_prompts)} signatures generated.")



if __name__ == "__main__":
    main()
