from experiments.actor.messages import (
    EvaluatePostconditionQuery,
    EvaluatePreconditionQuery,
    PhaseCompletedEvent,
    PhaseErrorEvent,
    PostconditionEvaluatedEvent,
    PreconditionEvaluatedEvent,
    ProcessPhaseCommand,
    StartPhaseCommand,
)
from rdddy.abstract_actor import AbstractActor
from rdddy.actor_system import ActorSystem


class InitiationActor(AbstractActor):
    async def handle_start_phase_command(self, message: StartPhaseCommand):
        print(f"Initiating phase: {message.phase_name}")
        # Trigger precondition evaluation
        await self.publish(EvaluatePreconditionQuery(phase_name=message.phase_name))


class ProcessingActor(AbstractActor):
    async def handle_precondition_evaluated_event(
        self, message: PreconditionEvaluatedEvent
    ):
        if message.result:
            print(f"Preconditions met for phase: {message.phase_name}, processing...")
            # Simulate phase processing and then evaluate postconditions
            await self.publish(ProcessPhaseCommand(phase_name=message.phase_name))
        else:
            print(f"Preconditions not met for phase: {message.phase_name}, aborting...")
            await self.publish(
                PhaseErrorEvent(
                    phase_name=message.phase_name, error_message="Precondition failed"
                )
            )

    async def handle_process_phase_command(self, message: ProcessPhaseCommand):
        # Simulate phase processing logic here
        print(f"Processing phase: {message.phase_name}")
        # After processing, evaluate postconditions
        await self.publish(EvaluatePostconditionQuery(phase_name=message.phase_name))


class CompletionActor(AbstractActor):
    async def handle_postcondition_evaluated_event(
        self, message: PostconditionEvaluatedEvent
    ):
        if message.result:
            print(f"Phase {message.phase_name} completed successfully.")
            await self.publish(PhaseCompletedEvent(phase_name=message.phase_name))
        else:
            print(f"Postconditions not met for phase: {message.phase_name}.")
            await self.publish(
                PhaseErrorEvent(
                    phase_name=message.phase_name, error_message="Postcondition failed"
                )
            )


# Setup the actor system and actors
async def setup_and_run():
    actor_system = ActorSystem()
    initiation_actor = await actor_system.actor_of(InitiationActor)
    processing_actor = await actor_system.actor_of(ProcessingActor)
    completion_actor = await actor_system.actor_of(CompletionActor)

    # Start the workflow by initiating a phase
    for i in range(5):
        await initiation_actor.publish(StartPhaseCommand(phase_name=f"Phase {i}"))


import asyncio


async def main():
    await setup_and_run()


if __name__ == "__main__":
    asyncio.run(main())
