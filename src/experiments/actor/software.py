import asyncio

from experiments.actor.messages import PhaseErrorEvent
from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from rdddy.messages import *


# Define the messages for each step in the scenario
class RequirementSpecificationCommand(Command):
    requirements: dict[str, str]


class ModelGeneratedEvent(Event):
    mdl_id: str


class ModelValidatedEvent(Event):
    mdl_id: str
    validation_status: bool


class ModelAdaptationCommand(Command):
    mdl_id: str
    external_inputs: dict[str, str]


class DecisionMadeEvent(Event):
    mdl_id: str
    decision_actions: list[str]


class OptimizationCompletedEvent(Event):
    mdl_id: str


class DeploymentStartedCommand(Command):
    mdl_id: str


class ModelDeployedEvent(Event):
    mdl_id: str


class ModelMonitoringCommand(Command):
    mdl_id: str


# Actors will be defined here, each handling relevant messages
# For brevity, only the structure of actors is outlined


class ProjectManagementActor(Actor):
    async def handle_requirement_specification_command(
        self, message: RequirementSpecificationCommand
    ):
        # Log the receipt of requirements and trigger model generation
        print(f"Received project requirements: {message.requirements}")
        await self.publish(ModelGeneratedEvent(mdl_id="model_123"))


class ModelGenerationActor(Actor):
    async def handle_model_generated_event(self, message: ModelGeneratedEvent):
        # Generate model based on received event (simulate model generation)
        print(f"Model {message.mdl_id} generated.")
        await self.publish(
            ModelValidatedEvent(mdl_id=message.mdl_id, validation_status=True)
        )


class ModelValidationActor(Actor):
    async def handle_model_validated_event(self, message: ModelValidatedEvent):
        # Validate the model (simulation)
        print(f"Model {message.mdl_id} validation status: {message.validation_status}")
        if message.validation_status:
            await self.publish(
                DecisionMadeEvent(mdl_id=message.mdl_id, decision_actions=["proceed"])
            )
        else:
            await self.publish(
                PhaseErrorEvent(
                    phase_name="Validation", error_message="Validation Failed"
                )
            )


class AdaptationActor(Actor):
    async def handle_model_adaptation_command(self, message: ModelAdaptationCommand):
        # Adapt the model based on external inputs (simulate adaptation)
        print(f"Adapting model {message.mdl_id} with inputs: {message.external_inputs}")
        await self.publish(OptimizationCompletedEvent(mdl_id=message.mdl_id))


class DecisionMakingActor(Actor):
    async def handle_decision_made_event(self, message: DecisionMadeEvent):
        # Make decision based on DMN (simulate decision-making)
        print(f"Decision for model {message.mdl_id}: {message.decision_actions}")
        if "proceed" in message.decision_actions:
            await self.publish(DeploymentStartedCommand(mdl_id=message.mdl_id))


class OptimizationActor(Actor):
    async def handle_optimization_completed_event(
        self, message: OptimizationCompletedEvent
    ):
        # Optimization logic (simulation)
        print(f"Optimization completed for model {message.mdl_id}.")
        await self.publish(ModelDeployedEvent(mdl_id=message.mdl_id))


class DeploymentActor(Actor):
    async def handle_deployment_started_command(
        self, message: DeploymentStartedCommand
    ):
        # Handle deployment (simulate deployment process)
        print(f"Deployment started for model {message.mdl_id}.")
        await self.publish(ModelMonitoringCommand(mdl_id=message.mdl_id))


class MonitoringActor(Actor):
    async def handle_model_monitoring_command(self, message: ModelMonitoringCommand):
        # Monitor the model (simulate monitoring)
        print(f"Monitoring initiated for model {message.mdl_id}.")
        # Based on monitoring, you could trigger new adaptation or optimization cycles


# Setup and execution logic for the actors and the actor system
async def setup_and_run():
    actor_system = ActorSystem()
    await actor_system.actors_of(
        [
            ProjectManagementActor,
            ModelGenerationActor,
            ModelValidationActor,
            AdaptationActor,
            DecisionMakingActor,
            OptimizationActor,
            DeploymentActor,
            MonitoringActor,
        ]
    )
    # Instantiate and start all actors
    # Example: project_management_actor = await actor_system.actor_of(ProjectManagementActor)
    # Trigger the start of the scenario by sending a RequirementSpecificationCommand
    await actor_system.publish(
        RequirementSpecificationCommand(
            requirements={"model-deployment-started": "hello"}
        )
    )


async def main():
    await setup_and_run()


if __name__ == "__main__":
    asyncio.run(main())
