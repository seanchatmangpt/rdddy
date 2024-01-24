import asyncio

import pytest
from denz.actor import Actor, Message
from denz.actor_system import ActorSystem


@pytest.fixture
def actor_system():
    return ActorSystem()


@pytest.mark.asyncio
async def test_actor_system_initialization(actor_system):
    assert actor_system.actors == []


@pytest.mark.asyncio
async def test_actor_creation(actor_system):
    actor = actor_system.actor_of(Actor)
    assert actor in actor_system.actors


@pytest.mark.asyncio
async def test_broadcasting(actor_system):
    class TestActor(Actor):
        async def receive(self, message):
            self.received_message = message

    actor1 = actor_system.actor_of(TestActor)
    actor2 = actor_system.actor_of(TestActor)

    message = Message(actor_id="Sender", content="Content", module="Test")

    await actor_system.publish(message)

    await asyncio.sleep(0.1)  # Allow time for message processing

    assert actor1.received_message == message
    assert actor2.received_message == message
