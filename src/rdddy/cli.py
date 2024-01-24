"""rdddy CLI."""

import typer
from rdddy.generators import gen_cli

app = typer.Typer()

app.add_typer(gen_cli.app, name="gen")
