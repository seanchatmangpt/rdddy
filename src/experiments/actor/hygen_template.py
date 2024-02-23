import os

from loguru import logger
from pydantic import Field

import dspy
from rdddy.abstract_actor import AbstractActor
from rdddy.actor_system import ActorSystem
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.messages import *

template_content_desc = """
---
to: app/emails/<%= name %>.html
---

Hello <%= name %>,
<%= message %>
(version <%= version %>)
"""


class HygenTemplateSpecificationCommand(AbstractCommand):
    template_name: str = Field(..., description="The name of the template to generate.")
    template_path: str = Field(
        ..., description="The path where the template should be created."
    )
    template_content: str = Field(
        ..., description=template_content_desc, min_length=200
    )


class TemplateGeneratedEvent(AbstractEvent):
    template_name: str = Field(..., description="The name of the generated template.")
    success: bool = Field(
        ..., description="Indicates whether the template was successfully generated."
    )


class TemplateValidatedEvent(AbstractEvent):
    template_name: str = Field(..., description="The name of the validated template.")
    is_valid: bool = Field(
        ..., description="Indicates the validation result of the template."
    )


class TemplateDeploymentStartedEvent(AbstractEvent):
    template_name: str = Field(
        ..., description="The name of the template being deployed."
    )


class TemplateDeploymentCompletedEvent(AbstractEvent):
    template_name: str = Field(..., description="The name of the deployed template.")
    success: bool = Field(
        ..., description="Indicates whether the template was successfully deployed."
    )


class HygenTemplateGeneratorActor(AbstractActor):
    async def handle_hygen_template_specification_command(
        self, command: HygenTemplateSpecificationCommand
    ):
        # Generate the Hygen template
        try:
            self.write_to_file(
                f"{command.template_path}/{command.template_name}.ejs.t",
                command.template_content,
            )
            logger.debug(
                f"Hygen template {command.template_name} generated successfully."
            )
            await self.publish(
                TemplateGeneratedEvent(
                    template_name=command.template_name, success=True
                )
            )
        except Exception as e:
            logger.debug(f"Failed to generate template {command.template_name}: {e}")
            await self.publish(
                TemplateGeneratedEvent(
                    template_name=command.template_name, success=False
                )
            )

    def write_to_file(self, file_path: str, content: str):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            file.write(content)


class TemplateValidationActor(AbstractActor):
    async def handle_template_generated_event(self, event: TemplateGeneratedEvent):
        if event.success:
            # Simulate validation logic
            logger.debug(f"Validating template: {event.template_name}")
            # Assume validation passes for this example
            await self.publish(
                TemplateValidatedEvent(template_name=event.template_name, is_valid=True)
            )


class TemplateDeploymentActor(AbstractActor):
    async def handle_template_validated_event(self, event: TemplateValidatedEvent):
        if event.is_valid:
            logger.debug(f"Deploying template: {event.template_name}")
            # Simulate deployment logic
            # Assume deployment succeeds for this example
            await self.publish(
                TemplateDeploymentCompletedEvent(
                    template_name=event.template_name, success=True
                )
            )


async def setup_and_run():
    actor_system = ActorSystem()
    # Initialize and register all actors
    await actor_system.actors_of(
        [HygenTemplateGeneratorActor, TemplateValidationActor, TemplateDeploymentActor]
    )

    module = GenPydanticInstance(root_model=HygenTemplateSpecificationCommand)
    hygen_inst = module.forward(
        "I need a hygen template to create an about component, use the page generator. and the 'new' action. the route is about"
    )

    await actor_system.publish(hygen_inst)
    # Trigger the template generation process
    # await actor_system.publish(HygenTemplateSpecificationCommand(
    #     template_name="exampleTemplate",
    #     template_path="_templates/example/new",
    #     template_content="---\nto: app/example/<%= name %>.js\n---\nconsole.log('Hello, <%= name %>!')"
    # ))


async def main():
    lm = dspy.OpenAI(max_tokens=2000)
    dspy.settings.configure(lm=lm)

    await setup_and_run()


# if __name__ == '__main__':
# asyncio.run(main())
