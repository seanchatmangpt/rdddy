import dspy

import typer
from jinja2 import Environment
from pydantic import BaseModel, Field
from typer import Typer

from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from typetemp.extension.inflection_extension import InflectionExtension


app = Typer()


def setup_jinja_env():
    env = Environment()
    env.add_extension(InflectionExtension)

    env.filters['to_kwarg'] = lambda input_name: f"{input_name}={input_name}"
    return env


class DSPyModuleTemplate(BaseModel):
    '''
    class {{ model.class_name | camelize }}(dspy.Module):
    """{{ model.docstring }}"""

        def forward(self, {{ model.inputs | join(', ') }}):
            pred = dspy.Predict("{{ model.inputs | join(', ') }} -> {{ model.output }}")

            result = pred({{ model.inputs | map('to_kwarg') | join(', ') }}).{{ model.output }}
            return result
    '''
    class_name: str = Field(..., description="Class name of the DSPy Module. Do not include DSPy in the class_name")
    docstring: str = Field(..., description="Documentation for the DSPy Module")
    inputs: list[str] = Field(..., description="Inputs for dspy.Module")
    output: str = Field(..., description="Output for dspy.Module")


dspy_module_template = '''import dspy
from typer import Typer

app = Typer()


lm = dspy.OpenAI(max_tokens=500)
dspy.settings.configure(lm=lm)


class {{ model.class_name | camelize }}(dspy.Module):
    """{{ model.docstring }}"""
    
    def forward(self, {{ model.inputs | join(', ') }}):
        pred = dspy.Predict("{{ model.inputs | join(', ') }} -> {{ model.output }}")
        
        result = pred({{ model.inputs | map('to_kwarg') | join(', ') }}).{{ model.output }}
        return result

def main():
{% for input in model.inputs %}
    {{ input }} = ""  # Initialize your inputs here. Adjust as necessary.
{% endfor %}
    {{ model.class_name | underscore }} = {{ model.class_name | camelize }}()
    print({{ model.class_name | underscore }}.forward({{ model.inputs | map('to_kwarg') | join(', ') }}))


@app.command()
def module_test({{ model.inputs | join(', ') }}):
    """{{ model.docstring }}"""
    {{ model.class_name | underscore }} = {{ model.class_name | camelize }}()

    print({{ model.class_name | underscore }}.forward({{ model.inputs | map('to_kwarg') | join(', ') }}))


if __name__ == "__main__":
    app()
    # main()
    
'''


@app.command(name="module")
def gen_module(prompt: str):
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    env = setup_jinja_env()

    template = env.from_string(dspy_module_template)

    tmpl_model = GenPydanticInstance(root_model=DSPyModuleTemplate)(prompt)

    source = template.render(model=tmpl_model)

    with open(f"new_module_{id(tmpl_model)}.py", "w") as file:
        file.write(source)

    print(source)


@app.command(name="model", short_help="Generates a Pydantic model class.")
def pydantic_model_gen(prompt: str):
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)

    style = "All fields must be fields annotated attributes Field classes with descriptions"
    module = dspy.Predict("reqs, style -> pydantic_class_source")
    source = module(reqs=prompt, style=style).pydantic_class_source
    print(source)


@app.command(name="models", short_help="Generates a Pydantic root model with child models.")
def pydantic_root_child_model_gen(prompt: str):
    lm = dspy.OpenAI(max_tokens=1000, model="gpt-4")
    dspy.settings.configure(lm=lm)

    # Define the style for generating complex models including root and child relationships
    style = "Generate root and child Pydantic models. Include fields with types, default values, and descriptions."

    # Use DSPy to predict the Pydantic class source code for both root and child models based on the prompt
    module = dspy.Predict("reqs, style -> pydantic_root_and_child_classes_source")
    source = module(reqs=prompt, style=style).pydantic_root_and_child_classes_source

    # Print the generated Pydantic class source code
    print(source)



README = "DSPy is a framework for algorithmically optimizing LM prompts and weights"


@app.command(name="help")
def dspy_help(
    question: str
):
    history = ""
    history = chatbot(question, history=history, context=README)


def chatbot(question, history, context):
    qa = dspy.ChainOfThought("question, context -> answer")
    response = qa(question=question, context=context).answer
    history += response
    print(f"Chatbot: {response}")
    confirmed = False
    while not confirmed:
        confirm = typer.prompt("Did this answer your question? [y/N]", default="N")

        if confirm.lower() in ["y", "yes"]:
            confirmed = True
        else:
            want = typer.prompt("How can I help more?")

            question = f"{history}\n{want}"
            question = question[-1000:]

            response = qa(question=question, context=README).answer
            history += response
            print(f"Chatbot: {response}")

    return history


@app.command()
def init(name: str):
    print(f"Initializing DPSy project: {name}")


if __name__ == "__main__":
    app()
