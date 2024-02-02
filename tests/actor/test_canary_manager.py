import asyncio
import pytest
from unittest.mock import patch, MagicMock

from rdddy.actor import Actor
from rdddy.actor_system import ActorSystem
from actors.canary_manager import (
    ChromeCanaryManager,
    StartCanaryCommand,
    StopCanaryCommand,
    RestartCanaryCommand,
)


# Mock subprocess.Popen to simulate Chrome Canary behavior
class MockPopen:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.returncode = None
        self._mock_stderr = MagicMock()
        self._mock_stderr.readline.side_effect = self._simulate_errors()

    def _simulate_errors(self):
        yield "Normal log line\n"
        yield "[ERROR] Simulated Error\n"
        while True:
            yield ""  # Simulate end of stream after error

    @property
    def stderr(self):
        return self._mock_stderr

    def terminate(self):
        self.returncode = 0

    def poll(self):
        return self.returncode


@pytest.fixture
def actor_system():
    return ActorSystem()


@pytest.mark.asyncio
async def test_chrome_canary_restart(actor_system):
    with patch("subprocess.Popen", MockPopen):
        actor_system = ActorSystem()
        canary_manager = await actor_system.actor_of(ChromeCanaryManager)

        # Start Chrome Canary
        await canary_manager.send(canary_manager.actor_id, StartCanaryCommand())

        # Allow time for the actor to process the logs and restart Chrome Canary
        await asyncio.sleep(0)

        assert canary_manager.restart_count > 0, "Canary should have been restarted"

        # Verify that Chrome Canary was restarted
        # This can be done by checking internal state of canary_manager or using other appropriate method

        # Clean up
        await canary_manager.send(canary_manager.actor_id, StopCanaryCommand())


if __name__ == "__main__":
    pytest.main()
