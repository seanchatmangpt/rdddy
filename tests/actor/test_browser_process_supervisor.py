import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from rdddy.actor_system import ActorSystem
from rdddy.browser.browser_domain import *
from rdddy.browser.browser_process_supervisor import BrowserProcessSupervisor


class MockAsyncProcess:
    def __init__(self):
        self.returncode = None
        self._populate_stderr()
        self._mock_stderr = MagicMock()
        self._mock_stderr.readline.side_effect = self._simulate_errors()

    def _simulate_errors(self):
        yield "Normal log line\n"
        yield "[ERROR] Simulated Error\n"
        while True:
            yield ""

    async def _populate_stderr(self):
        await self._mock_stderr.put("Normal log line\n")
        await self._mock_stderr.put("[ERROR] Simulated Error\n")
        # Simulate end of stream after error by not putting any more items

    async def communicate(self):
        return "", ""

    @property
    def stderr(self):
        return self

    async def readline(self):
        return await self._mock_stderr.get()

    def terminate(self):
        self.returncode = 0

    def poll(self):
        return self.returncode


@pytest.fixture
def actor_system():
    return ActorSystem()


@pytest.mark.asyncio
async def test_chrome_browser_restart(actor_system):
    mock_process = MockAsyncProcess()

    with patch("asyncio.create_subprocess_exec", return_value=mock_process):
        supervisor = await actor_system.actor_of(BrowserProcessSupervisor)

        await actor_system.publish(StartBrowserCommand())

        # Allow time for the actor to process the logs and restart Chrome Browser
        await asyncio.sleep(0.1)  # Adjust sleep time if necessary

        await actor_system.wait_for_message(RestartBrowserCommand)

        assert supervisor.restart_count > 0, "Browser should have been restarted"

        # Verify that Chrome Browser was restarted
        # This can be done by checking internal state of supervisor or using other appropriate method

        # Clean up
