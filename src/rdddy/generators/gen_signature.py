import dspy
from jinja2 import Template
import os

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.signature_factory import (
    SignatureTemplateSpecModel,
    InputFieldTemplateSpecModel,
    OutputFieldTemplateSpecModel,
)


def render_signature_class(model, template_str):
    template = Template(template_str)
    rendered_class = template.render(model=model)
    return rendered_class


def write_signature_class_to_file(class_str, file_name):
    with open(file_name, "w") as file:
        file.write(class_str)


# Example usage
signature_model_instance = ...  # Your SignatureModel instance
template_str = '''import dspy

class {{ model.name }}(dspy.Signature):
    """
    {{ model.instructions }}
    """
    {% for field in model.input_fields %}
    {{ field.name }} = dspy.InputField({%- if field.prefix %} prefix="{{ field.prefix }}", {%- endif %} desc="{{ field.desc }}")
    {% endfor %}
    {% for field in model.output_fields %}
    {{ field.name }} = dspy.OutputField({%- if field.prefix %} prefix="{{ field.prefix }}", {%- endif %} desc="{{ field.desc }}")
    {% endfor %}
'''


def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    sig_prompt = "I need a signature called GenPythonClass that allows input of 'prompt', and output 'source'. The signature needs to create python classes from the prompt."

    sig_module = GenPydanticInstance(
        root_model=SignatureTemplateSpecModel,
        child_models=[InputFieldTemplateSpecModel, OutputFieldTemplateSpecModel],
    )

    sig_inst = sig_module.forward(sig_prompt)
    print(f'prompt:\n{lm.history[0].get("prompt")}')
    print(f'response:\n{lm.history[0]["response"].choices[0]["text"]}')
    rendered_class_str = render_signature_class(sig_inst, template_str)
    write_signature_class_to_file(rendered_class_str, "output_signature.py")


if __name__ == "__main__":
    main()
