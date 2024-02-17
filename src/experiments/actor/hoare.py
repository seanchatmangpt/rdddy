from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from experiments.actor.messages import *


class InitiationActor(Actor):
    async def handle_start_phase_command(self, message: StartPhaseCommand):
        print(f"Starting phase: {message.phase_name}")
        # Simulate checking a condition to decide if we proceed
        if message.phase_name == "Hello":
            # Emit an event to indicate the precondition is evaluated and successful
            await self.publish(
                PreconditionEvaluatedEvent(phase_name=message.phase_name, result=True)
            )
        else:
            await self.publish(
                PhaseErrorEvent(
                    phase_name=message.phase_name, error_message="Precondition failed"
                )
            )

    async def handle_evaluate_precondition_query(
        self, message: EvaluatePreconditionQuery
    ):
        # Directly using the message content to decide success or failure here for simplicity
        if message.phase_name == "Hello":
            await self.publish(
                PreconditionEvaluatedEvent(phase_name=message.phase_name, result=True)
            )
        else:
            await self.publish(
                PhaseErrorEvent(
                    phase_name=message.phase_name, error_message="Precondition failed"
                )
            )


class CompletionActor(Actor):
    async def handle_evaluate_postcondition_query(
        self, message: EvaluatePostconditionQuery
    ):
        # If message is "Hello", the postcondition check passes
        if message.phase_name == "Hello":
            await self.publish(
                PostconditionEvaluatedEvent(phase_name=message.phase_name, result=True)
            )
            await self.publish(PhaseCompletedEvent(phase_name=message.phase_name))
        # If message is "Goodbye", the postcondition check fails
        elif message.phase_name == "Goodbye":
            await self.publish(
                PhaseErrorEvent(
                    phase_name=message.phase_name, error_message="Postcondition failed"
                )
            )


# Setup and usage within an ActorSystem context
async def setup_and_run():
    actor_system = ActorSystem()
    initiation_actor = await actor_system.actor_of(InitiationActor)
    completion_actor = await actor_system.actor_of(CompletionActor)

    await actor_system.publish(StartPhaseCommand(phase_name="Hello"))
    await actor_system.publish(StartPhaseCommand(phase_name="Goodbye"))


import asyncio


async def main():
    await setup_and_run()


if __name__ == "__main__":
    asyncio.run(main())
