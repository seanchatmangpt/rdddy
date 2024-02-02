import asyncio

import pytest

from rdddy.messages import *
from rdddy.actor import *
from rdddy.actor_system import ActorSystem


@pytest.fixture
def actor_system(event_loop):
    # Provide the event loop to the actor system
    return ActorSystem(event_loop)


@pytest.mark.asyncio
async def test_handler(actor_system):
    class DummyActor(Actor):
        def __init__(self, actor_system, actor_id=None):
            super().__init__(actor_system, actor_id)
            self.processed_query = None

        async def handle_query(self, query: Query):
            self.processed_query = query

    actor = await actor_system.actor_of(DummyActor)

    query = Query(actor_id=actor.actor_id, content="Query1")

    await asyncio.sleep(0)

    await actor_system.publish(query)

    await asyncio.sleep(0)

    assert actor.processed_query.actor_id == actor.actor_id


@pytest.mark.asyncio
async def test_concurrent_message_processing(actor_system):
    class ConcurrentActor(Actor):
        def __init__(self, actor_system: "ActorSystem", actor_id=None):
            super().__init__(actor_system, actor_id)
            self.processed_message = None

        async def receive(self, message):
            await asyncio.sleep(0)  # Simulate time-consuming processing
            self.processed_message = message

    actor1 = await actor_system.actor_of(ConcurrentActor)
    actor2 = await actor_system.actor_of(ConcurrentActor)

    message1 = Message(actor_id=actor1.actor_id, content="Content1", module="Test")
    message2 = Message(actor_id=actor2.actor_id, content="Content2", module="Test")

    assert actor1.processed_message is None
    assert actor2.processed_message is None

    await asyncio.gather(
        actor1.receive(message1),
        actor2.receive(message2),
    )

    # Implement assertions for concurrent message processing
    assert actor1.processed_message == message1
    assert actor2.processed_message == message2
