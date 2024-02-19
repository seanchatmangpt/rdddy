import asyncio

from experiments.abstract_aggregate import AbstractAggregate
from rdddy.actor_system import ActorSystem
from rdddy.messages import AbstractCommand, AbstractEvent


# Domain Events
class WorkshopStarted(AbstractEvent):
    workshop_id: str


class ParticipantAdded(AbstractEvent):
    workshop_id: str
    participant_id: str


# ... Other domain events ...


# Domain Commands
class StartWorkshop(AbstractCommand):
    workshop_id: str


class AddParticipant(AbstractCommand):
    workshop_id: str
    participant_id: str


# ... Other domain commands ...


# Aggregate Root
class WorkshopAggregate(AbstractAggregate):
    def __init__(self, actor_system, workshop_id):
        super().__init__(actor_system, workshop_id)
        self.participants = []
        self.events = []

    async def start_workshop(self, command: StartWorkshop):
        # Start workshop logic
        # Emit WorkshopStarted event
        print("Starting workshop")
        await self.emit_event(WorkshopStarted(workshop_id=command.workshop_id))

    def add_participant(self, command: AddParticipant):
        # Add participant logic
        # Emit ParticipantAdded event
        self.emit_event(
            ParticipantAdded(workshop_id=command.workshop_id, participant_id=command.participant_id)
        )


# Simulation
async def simulate_workshop():
    actor_system = ActorSystem()

    # Create WorkshopAggregate
    workshop_aggregate = await actor_system.actor_of(WorkshopAggregate, workshop_id="workshop-123")

    # Send commands to the aggregate
    start_command = StartWorkshop(workshop_id="workshop")
    await actor_system.publish(start_command)


if __name__ == "__main__":
    asyncio.run(simulate_workshop())
