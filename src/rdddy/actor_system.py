import asyncio
from typing import TYPE_CHECKING, TypeVar, Any
from loguru import logger
import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler.eventloop import AsyncIOScheduler

if TYPE_CHECKING:
    from rdddy.actor import Actor
    from rdddy.messages import Message

T = TypeVar("T", bound="Actor")


class ActorSystem:
    def __init__(self, loop: asyncio.AbstractEventLoop = None) -> None:
        self.actors = {}
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.scheduler = AsyncIOScheduler(loop=self.loop)
        self.event_stream = rx.subject.Subject()

    async def actor_of(self, actor_class, **kwargs) -> "Actor":
        actor = actor_class(self, **kwargs)
        self.actors[actor.actor_id] = actor
        await actor.start(self.scheduler)
        return actor

    async def publish(self, message: "Message"):
        self.event_stream.on_next(message)
        actors = list(self.actors.values())
        for actor in actors:
            await self.send(actor.actor_id, message)

    async def remove_actor(self, actor_id):
        actor = self.actors.pop(actor_id, None)
        if actor:
            logger.info(f"Removing actor {actor_id}")
        else:
            logger.warning(f"Actor {actor_id} not found for removal")
        logger.debug(f"Current actors count: {len(self.actors)}")

    async def send(self, actor_id: int, message: "Message"):
        logger.debug(f"Sending message {message} to actor {actor_id}")
        actor = self.actors.get(actor_id)
        if actor:
            actor.mailbox.on_next(message)
            await asyncio.sleep(0)

    async def wait_for_event(self, event_type: type) -> Any:
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def on_next(event):
            if isinstance(event, event_type):
                future.set_result(event)
                subscription.dispose()

        subscription = self.event_stream.pipe(
            ops.filter(lambda event: isinstance(event, event_type))
        ).subscribe(on_next)

        return await future

    def __getitem__(self, actor_name):
        return self.actors.get(actor_name)
