import asyncio
import logging

from rdddy.abstract_actor import AbstractActor
from rdddy.actor_system import ActorSystem
from rdddy.messages import AbstractCommand, AbstractEvent, AbstractQuery

logger = logging.getLogger(__name__)


class WorkshopState:
    """Represents the state of the event storming workshop.
    You can expand this class to include more workshop-related data.
    """

    def __init__(self):
        self.events = []


class EventStormFacilitatorAgent(AbstractActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)
        self.workshop_state = WorkshopState()

    async def handle_start_workshop(self, message: AbstractCommand):
        """Handle the command to start the event storming workshop."""
        logger.info("Starting the event storming workshop.")
        # Perform any initialization tasks here
        await self.publish(AbstractEvent(actor_id=self.actor_id, content="Workshop started"))

    async def handle_simulate_event(self, message: AbstractCommand):
        """Handle the command to simulate an event in the workshop."""
        event_description = message.content
        logger.info(f"Simulating event: {event_description}")
        # Add the event to the workshop state
        self.workshop_state.events.append(event_description)
        await self.send(
            self,
            AbstractEvent(actor_id=self.actor_id, content=f"Event simulated: {event_description}"),
        )

    async def handle_query_workshop(self, message: AbstractQuery):
        """Handle the query to get information about the workshop state."""
        logger.info("Querying workshop information.")
        # Create a response with workshop state information
        response_content = f"Events in workshop: {', '.join(self.workshop_state.events)}"
        await self.publish(AbstractEvent(actor_id=self.actor_id, content=response_content))

    async def handle_exit_workshop(self, message: AbstractCommand):
        """Handle the command to exit the event storming workshop."""
        logger.info("Exiting the event storming workshop.")
        # Perform any cleanup tasks here
        await self.send(self, AbstractEvent(actor_id=self.actor_id, content="Workshop exited"))


class ParticipantAgent(AbstractActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)

    async def handle_join_workshop(self, message: AbstractCommand):
        """Handle the command for a participant to join the workshop."""
        logger.info(f"{self.actor_id} is joining the event storming workshop.")
        await self.publish(AbstractEvent(actor_id=self.actor_id, content="Joined the workshop"))

    async def handle_simulate_event(self, message: AbstractCommand):
        """Handle the command for a participant to simulate an event."""
        event_description = message.content
        logger.info(f"{self.actor_id} is simulating event: {event_description}")
        await self.publish(
            AbstractEvent(actor_id=self.actor_id, content=f"Event simulated: {event_description}"),
        )

    async def handle_query_workshop(self, message: AbstractQuery):
        """Handle the query to get information about the workshop state."""
        logger.info(f"{self.actor_id} is querying workshop information.")
        # Add logic to query the workshop state and respond


class UserInterfaceAgent(AbstractActor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)

    async def handle_user_input(self, message: AbstractCommand):
        """Handle user input from the command line interface."""
        user_command = message.content
        print(user_command)
        # Add logic to process user input and send appropriate commands or queries to other agents


import anyio


async def main():
    actor_system = ActorSystem()
    facilitator_agent = await actor_system.actor_of(EventStormFacilitatorAgent)
    participant_agent1 = await actor_system.actor_of(ParticipantAgent)
    participant_agent2 = await actor_system.actor_of(ParticipantAgent)
    ui_agent = await actor_system.actor_of(UserInterfaceAgent)

    await actor_system.publish(AbstractCommand(content="Hello World"))

    await asyncio.sleep(1)


if __name__ == "__main__":
    anyio.run(main)
