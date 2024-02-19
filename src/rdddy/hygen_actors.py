import asyncio
from typing import Optional

from loguru import logger
from pydantic import Field

import dspy
from rdddy.abstract_actor import AbstractActor
from rdddy.actor_system import ActorSystem
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.messages import *


class GenerateDashboardEvent(AbstractEvent):
    page_name: str
    widget_type: str


class HygenCLIArgs(BaseModel):
    """The arguments for the Hygen CLI"""

    model_config = ConfigDict(extra="allow")

    name: str = Field(
        ...,
        description="The name associated with the template generation, often used as a filename or identifier.",
    )
    route: str = Field(
        None,
        description="The route or path where the generated file(s) should be located.",
    )
    description: str = Field(None, description="The description of the page")
    items: str = Field(
        None,
        description="A string representing items or configurations specific to the generation process.",
    )


class HygenTemplateModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    generator: str = Field(
        ..., description="Specifies the Hygen generator to be used for code generation."
    )
    action: str = Field(..., description="Defines the action that the generator should perform.")
    cli_args: HygenCLIArgs = Field(
        ...,
        description="Additional key-value pairs providing specific arguments for the template generation process.",
    )


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
        try:
            module = GenPydanticInstance(root_model=HygenTemplateModel, child_models=[HygenCLIArgs])
            hygen_inst = module.forward(
                "I need a hygen template to create an about component, use the page generator. and the 'new' action. the route is about"
            )

            output = await run_hygen_async(hygen_inst, self.nextjs_root)
            logger.debug(output)
        except Exception as e:
            logger.error(e)


async def run_hygen_async(
    template_params: HygenTemplateModel, cwd: Optional[str] = None, overwrite: bool = True
):  # Use the new model
    """Executes a Hygen command asynchronously... (Same docstring as earlier)"""
    hygen_command = ["hygen", template_params.generator, template_params.action]

    for (
        key,
        value,
    ) in template_params.cli_args.model_dump().items():  # Iterate over kwargs
        hygen_command.extend(["--" + key, str(value)])

    logger.debug(f"Running hygen command: {hygen_command}")

    try:
        process = await asyncio.create_subprocess_exec(
            *hygen_command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
        )

        response = b"yes" if overwrite else b"no"

        process.stdin.write(response)
        await process.stdin.drain()
        process.stdin.close()

        stdout, stderr = await process.communicate()

        if (
            process.returncode != 0 or "Error" in stdout.decode()
        ):  # Check for non-zero exit code from Hygen
            raise ChildProcessError(f"Hygen failed with error:\n{stderr.decode()}{stdout.decode()}")
        else:
            return stdout.decode()
    except ChildProcessError as e:
        raise e


async def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)
    actor_system = ActorSystem()
    generator_actor = await actor_system.actor_of(DashboardGeneratorActor)
    await actor_system.publish(
        GenerateDashboardEvent(page_name="summary", widget_type="line_chart")
    )
    await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
