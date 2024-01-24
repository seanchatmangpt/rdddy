import asyncio
from loguru import logger
from typing import TYPE_CHECKING, Any
import reactivex as rx
from reactivex import operators as ops

from rdddy.messages import *

if TYPE_CHECKING:
    from rdddy.actor_system import ActorSystem


class Actor:
    def __init__(self, actor_system: "ActorSystem", actor_id=None):
        self.actor_system = actor_system
        self.actor_id = actor_id or id(self)
        self.mailbox = rx.subject.Subject()
        self.handlers = self.map_handlers()

    async def start(self, scheduler):
        self.mailbox.pipe(ops.observe_on(scheduler)).subscribe(
            on_next=self.on_next,  # Synchronous wrapper for async handler
            on_error=self.on_error,
            on_completed=self.on_completed,
        )
        logger.info(f"Actor {self.actor_id} started")

    def on_next(self, message: Message):
        # Schedule the async handler as a new task
        logger.debug(f"Actor {self.actor_id} received message: {message}")
        asyncio.create_task(self.receive(message))

    def on_error(self, error):
        logger.error(f"Error in actor {self.actor_id} mailbox: {error}")

    def on_completed(self):
        logger.info(f"Actor {self.actor_id} mailbox stream completed")

    async def receive(self, message: Message):
        handler = self.handlers.get(type(message))
        if handler:
            await handler(message)

    async def send(self, recipient_id: int, message: Message):
        await self.actor_system.send(recipient_id, message)

    async def publish(self, message: Message):
        await self.actor_system.publish(message)

    def map_handlers(self):
        handlers = {}
        for name, method in inspect.getmembers(self):
            if callable(method) and hasattr(method, "__annotations__"):
                annotations = method.__annotations__
                for arg in annotations.values():
                    try:
                        if issubclass(arg, Message):
                            handlers[arg] = method
                    except TypeError:
                        pass
        del handlers[Message]
        return handlers
