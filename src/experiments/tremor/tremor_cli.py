import asyncio
from typing import Optional

from rdddy.actor_system import ActorSystem
from rdddy.async_typer import AsyncTyper

app = AsyncTyper()

from rdddy.abstract_actor import AbstractActor
from rdddy.messages import *
from rdddy.messages import AbstractEvent  # We likely still need this at the base


class GenerateDashboardEvent(AbstractEvent):
    page_name: str
    widget_type: str


class HygenTemplateModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    kwargs: dict = {}  # Field allows arbitrary key-value pairs


class DashboardGeneratorActor(AbstractActor):
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

        print("Generating with Hygen.")
        # Construct Hygen command
        hygen_command = [
            "hygen",
            "page",  # Assuming your template is  named 'page'
            "new",
            event.page_name,  # We  pass the component name to Hygen
        ]

        await run_hygen_async(hygen_command, self.nextjs_root)


async def run_hygen_async(
    template_params: HygenTemplateModel, cwd: Optional[str] = None
):  # Use the new model
    """Executes a Hygen command asynchronously... (Same docstring as earlier)"""
    hygen_command = ["hygen", template_params.name]

    for key, value in template_params.kwargs.items():  # Iterate over kwargs
        hygen_command.extend(["--" + key, str(value)])

    try:
        process = await asyncio.create_subprocess_exec(
            *hygen_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:  # Check for non-zero exit code from Hygen
            return f"Hygen failed with error:\n{stderr.decode()}"
        else:
            return stdout.decode()

    except Exception as e:
        return f"Error running Hygen: {e!s}"


async def main():
    actor_system = ActorSystem()
    generator_actor = await actor_system.actor_of(DashboardGeneratorActor)
    await actor_system.publish(
        GenerateDashboardEvent(page_name="summary", widget_type="line_chart")
    )
    await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
