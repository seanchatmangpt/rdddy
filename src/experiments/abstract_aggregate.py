from slss.actor import Actor


class AbstractAggregate(Actor):
    def __init__(self, actor_system, actor_id=None):
        super().__init__(actor_system, actor_id)

    def apply_event(self, event):
        # Apply the event to the aggregate's state
        pass

    async def emit_event(self, event):
        # Emit the event for event sourcing
        await self.actor_system.publish(event)

    def check_version(self, expected_version):
        # Check if the expected version matches the current version
        return self.version == expected_version

    def validate(self, command):
        # Validate the incoming command
        pass

    async def handle_error(self, error_message):
        # Handle errors or exceptions
        pass

    async def initialize(self):
        # Perform initialization when an aggregate is created
        pass

    async def finalize(self):
        # Clean up resources or perform actions when an aggregate is no longer needed
        pass

    async def load_snapshot(self, snapshot):
        # Load a previously taken snapshot to optimize aggregate initialization
        pass

    async def take_snapshot(self):
        # Capture a snapshot of the aggregate's state for optimization
        pass
