import asyncio

import typer

from rdddy.async_typer import AsyncTyper

from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from experiments.actor.messages import (
    StartPhaseCommand,
    EvaluatePreconditionQuery,
    PreconditionEvaluatedEvent,
    ProcessPhaseCommand,
    PhaseErrorEvent,
    EvaluatePostconditionQuery,
    PostconditionEvaluatedEvent,
    PhaseCompletedEvent,
)


class InitiationActor(Actor):
    async def handle_start_phase_command(self, message: StartPhaseCommand):
        print(f"Initiating phase: {message.phase_name}")
        # Trigger precondition evaluation
        await self.publish(EvaluatePreconditionQuery(phase_name=message.phase_name))


class ProcessingActor(Actor):
    async def handle_evaluate_precondition_query(
        self, message: EvaluatePreconditionQuery
    ):
        await self.publish(
            PreconditionEvaluatedEvent(phase_name=message.phase_name, result=True)
        )

    async def handle_precondition_evaluated_event(
        self, message: PreconditionEvaluatedEvent
    ):
        typer.echo("")
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


class CompletionActor(Actor):
    async def handle_postcondition_evaluated_event(
        self, message: EvaluatePostconditionQuery
    ):
        if message.phase_name:
            print(f"Phase {message.phase_name} completed successfully.")
            await self.publish(PhaseCompletedEvent(phase_name=message.phase_name))
            summary = summarization_module.forward(str(message))
            typer.echo(summary)
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
    # for i in range(5):
    i = 1
    await actor_system.publish(StartPhaseCommand(phase_name=f"Phase {i}"))
    # await asyncio.sleep(1)

    while True:
        await asyncio.sleep(0.1)


app = AsyncTyper()

import dspy


class SummarizationModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_summary = dspy.ChainOfThought("text -> report")

    def forward(self, text):
        # Asynchronously generate a summary
        summary = self.generate_summary(text=text).report
        return summary


# Instantiate the summarization module
summarization_module = SummarizationModule()


@app.command()
async def summarize(text: str):
    """
    Asynchronous CLI command to generate summaries for the provided text.
    """
    await setup_and_run()
    # typer.echo("Generating summary")
    # summary = summarization_module.forward(text)
    # typer.echo(summary)
    # typer.echo("Summary generated")
    #


async def main():
    lm = dspy.OpenAI(max_tokens=500)
    dspy.settings.configure(lm=lm)
    # app()
    await setup_and_run()


import asyncio


if __name__ == "__main__":
    asyncio.run(main())


# if __name__ == '__main__':
#     main()
