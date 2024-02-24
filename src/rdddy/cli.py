import dspy

import typer
from typer import Typer

from rdddy.generators.gen_pydantic_class import GenPydanticClass

app = Typer()




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
