import dspy
from dspy import Signature
from dspy.signatures.field import InputField, OutputField

from pydantic import BaseModel, Field

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
    """Defines an input field for a DSPy Signature."""

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
    """
    SignatureTemplateSpecModel encapsulates the specifications for input/output behavior of a task in the DSPy framework.

    It provides a structured approach to define how data should be inputted into and outputted from a language model (LM),
    facilitating the creation and integration of complex LM pipelines.

    signature_class = type(model.name, (Signature,), class_dict)
    """

    name: str = Field(
        ...,
        description="Signature class name. Use this to specify additional context or labeling.",
    )
    instructions: str = Field(
        ..., description="Documentation of the task's expected LM function and output."
    )
    input_fields: list[InputFieldTemplateSpecModel]
    output_fields: list[OutputFieldTemplateSpecModel]


def create_signature_class_from_model(model: SignatureTemplateSpecModel) -> type:
    """
    Create a DSPy Signature class from a Pydantic model.

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
    signature_class = type(model.name, (Signature,), class_dict)
    return signature_class


def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    sig_prompt = "I need a signature called QuestionAnswering that allows input of 'context', 'question', and output 'answer'"

    sig_module = GenPydanticInstance(
        root_model=SignatureTemplateSpecModel, child_models=[InputFieldTemplateSpecModel, OutputFieldTemplateSpecModel]
    )

    question_answering_signature = sig_module.forward(sig_prompt)

    # Convert the SignatureModel to a DSPy Signature class
    QuestionAnswering = create_signature_class_from_model(question_answering_signature)

    context = """Chaining language model (LM) calls as composable modules is fueling a new powerful 
    way of programming. However, ensuring that LMs adhere to important constraints remains a key 
    challenge, one often addressed with heuristic “prompt engineering”. We introduce LM Assertions,
     a new programming construct for expressing computational constraints that LMs should satisfy. 
     We integrate our constructs into the recent DSPy programming model for LMs, and present new 
     strategies that allow DSPy to compile programs with arbitrary LM Assertions into systems 
     that are more reliable and more accurate. In DSPy, LM Assertions can be integrated at compile 
     time, via automatic prompt optimization, and/or at inference time, via automatic self- refinement 
     and backtracking. We report on two early case studies for complex question answer- ing (QA), 
     in which the LM program must iteratively retrieve information in multiple hops and synthesize a 
     long-form answer with citations. We find that LM Assertions improve not only compliance with 
     imposed rules and guidelines but also enhance downstream task performance, delivering intrinsic 
     and extrinsic gains up to 35.7% and 13.3%, respectively. Our reference implementation of LM Assertions 
     is integrated into DSPy at dspy.ai."""

    question = "What strategies can DSPy use?"

    answer = (
        dspy.ChainOfThought(QuestionAnswering)
        .forward(context=context, question=question)
        .answer
    )
    print(answer)


if __name__ == "__main__":
    main()
