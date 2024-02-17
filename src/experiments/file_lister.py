import asyncio
import os
import typer

app = typer.Typer()


def print_files_in_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            typer.echo(file_path)


@app.command()
def list_files(
    directory_path: str = typer.Argument(
        "/Users/candacechatman/dev/ReactiveMessagingPatterns_ActorModel/src/co/vaughnvernon/reactiveenterprise",
        help="Directory path to list files from.",
    )
):
    """
    List files in the specified directory.
    """
    if os.path.exists(directory_path):
        typer.echo("Files in the directory:")
        print_files_in_directory(directory_path)
    else:
        typer.echo(f"The directory '{directory_path}' does not exist.")


@app.command()
def convert(
    name: str = typer.Option(help="The name of the template."),
    prompt: str = typer.Option(help="The prompt for the template."),
    max_tokens: int = 2000,
):
    """
    Create a Python file with a SmartTemplate and convert_* function for a specific task.

    Args:
        name (str): The name of the SmartTemplate to use.
        prompt (str): The prompt for the
        max_tokens (int): Maximum tokens to generate. Defaults to
    """
    asyncio.run(_convert(name, prompt, max_tokens))


async def _convert(name: str, prompt: str, max_tokens: int):
    """ """
    pwd = os.path.dirname(__file__)
    env.loader = FileSystemLoader(f"{pwd}/templates")
    template = env.get_template("smart_template.j2")

    prompt = await spr(
        prompt=f"Hyperdetailed assistant prompt to generate {prompt}", encode=False
    )

    file_content = await template.render_async(
        name=name, prompt=prompt, max_tokens=max_tokens
    )

    with open(f"convert_{name}.py", "w") as file:
        file.write(file_content)

    typer.echo(f"Created convert_{name}.py.")


if __name__ == "__main__":
    app()
