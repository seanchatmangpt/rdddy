import asyncio

# Assuming the actor classes are defined in a module named `autospider_actors`
from autospider.actors import (
    CompletionActor,
    ExecutionActor,
    InitiationActor,
    PreconditionActor,
    ProcessingActor,
)
from autospider.messages import StartScrapingCommand
from rdddy.actor_system import ActorSystem


async def setup_and_run():
    # Create the Actor System
    actor_system = ActorSystem()

    # Initialize actors
    initiation_actor = await actor_system.actor_of(InitiationActor)
    precondition_actor = await actor_system.actor_of(PreconditionActor)
    processing_actor = await actor_system.actor_of(ProcessingActor)
    execution_actor = await actor_system.actor_of(ExecutionActor)
    completion_actor = await actor_system.actor_of(CompletionActor)

    # Start the scraping process by sending a StartScrapingCommand
    # Replace 'http://example.com' with the actual URL you want to scrape
    await actor_system.publish(StartScrapingCommand(url="http://example.com"))
    await asyncio.sleep(60)


async def main():
    await setup_and_run()


if __name__ == "__main__":
    asyncio.run(main())
