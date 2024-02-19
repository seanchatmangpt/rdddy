import pyperclip
import typer

from typetemp.template.render_funcs import render_str
from utils.create_prompts import spr

app = typer.Typer()


class TemplateSpec:
    def __init__(
        self,
        name: str,
        prompt: str,
        max_tokens: int = 2000,
        output_format: str = "python",
    ):
        self.name = name
        self.prompt = prompt
        self.max_tokens = max_tokens
        self.output_format = output_format


@app.command(help="Generate a SmartTemplate from a prompt.")
def smart(
    name: str = typer.Option(..., "--name", "-n"),
    prompt: str = typer.Option(..., "--prompt", "-p"),
    output_format: str = typer.Option("python", "--output", "-o"),
    max_tokens: int = 2000,
):
    asyncio.run(_render_smart_template(name, prompt, max_tokens, output_format))


@app.command(
    help="Generate a TypedTemplate from a prompt. Can use the clipboard to copy the content."
)
def static(
    name: str = typer.Option(..., "--name", "-n"),
    paste: bool = typer.Option(False, "--paste", is_flag=True),
):
    asyncio.run(_render_typed_template(name, paste))


async def _render_smart_template(name: str, prompt: str, max_tokens: int, output_format: str):
    """Renders a SmartTemplate to the filesystem"""
    prompt = await spr(
        prompt=f"ChatGPT Assistant that {prompt}",
        encode=False,
        max_tokens=40,
        model="3i",
    )

    template_name = render_str("{{ name | underscore }}_smart_template.py", name=name)

    # await smart_template_template.render(
    #     name,
    #     prompt=prompt,
    #     # config=LLMConfig(max_tokens=max_tokens, model="chatgpt"),
    #     output_format=output_format,
    #     to=template_name,
    # )

    typer.echo(f"Created {template_name}.")


async def _render_typed_template(name, paste):
    """Renders a TypedTemplate to the filesystem"""
    template_name = render_str("{{ name | underscore }}_typed_template.py", name=name)

    if paste is not None:
        content = pyperclip.paste()
    else:
        content = None

    typer.echo(f"Created {template_name}.")


import asyncio


async def main():
    await _render_smart_template("git_commit", "Short commit message", 20, "text")


if __name__ == "__main__":
    asyncio.run(main())
