import asyncio

import os

import typer

from rdddy.actor_system import ActorSystem
from rdddy.async_typer import AsyncTyper

app = AsyncTyper()

from rdddy.actor import Actor
from rdddy.messages import *

from rdddy.messages import Event  # We likely still need this at the base


class GenerateDashboardEvent(Event):
    page_name: str
    widget_type: str


class DashboardGeneratorActor(Actor):
    def __init__(self, actor_system: ActorSystem, actor_id=None):
        super().__init__(actor_system, actor_id=actor_id)
        # Retrieve NextJS project root:
        self.nextjs_root = "/Users/candacechatman/dev/nextjs-page"
        # self.nextjs_root = os.getenv("NEXTJS_PROJECT_ROOT")
        if not self.nextjs_root:
            # Handle this error - is this an event to the ActorSystem, a log?
            print("Error: NEXTJS_PROJECT_ROOT environment variable not found.")
            return

    async def handle_generate_dashboard_event(self, event: GenerateDashboardEvent):
        # ... Logic will come later ...
        print(f"Received generation request: {event}")
        try:
            await self.generate_with_hygen(event.page_name, event.widget_type)
        except Exception as e:
            # Add robust error handling later with relevant event publishing
            print(f"Hygen generation failed: {e}")

    async def generate_with_hygen(self, page_name: str, widget_type: str):
        # Construct Hygen command
        hygen_command = [
            "hygen",
            "page",  # Assuming your template is  named 'page'
            "new",
            page_name,  # We  pass the component name to Hygen
        ]

        process = await asyncio.create_subprocess_exec(
            *hygen_command,
            # Capture process output
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Wait for Hygen, collect output for analysis if needed
        await process.communicate()

        # Construct the filepath where Hygen should place the output
        target_filepath = os.path.join(self.nextjs_root, "pages", f"{page_name}.tsx")

        if not os.path.exists(target_filepath):
            raise OSError(f"Could not find {target_filepath}")
        else:
            typer.echo(f"Generated {page_name}")

        # Error – Hygen likely didn't succeed, or your Hygen template is misconfigured

    @app.command()
    async def generate_dashboard(
        page_name: str = "overview", widget_type: str = "line_chart"
    ):
        # ... Logic will come later ....
        typer.echo(
            f"Generating a page page named '{page_name}' with a '{widget_type}' widget!"
        )
        actor_system = ActorSystem()
        generator_actor = await actor_system.actor_of(DashboardGeneratorActor)
        await actor_system.publish(
            GenerateDashboardEvent(page_name=page_name, widget_type=widget_type)
        )


if __name__ == "__main__":
    app()
