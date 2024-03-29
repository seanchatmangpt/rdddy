import asyncio
from asyncio.subprocess import Process

from loguru import logger

from rdddy.abstract_actor import AbstractActor
from rdddy.actor_system import ActorSystem
from rdddy.browser.browser_domain import *
from rdddy.browser.browser_worker import BrowserWorker


class BrowserProcessSupervisor(AbstractActor):
    def __init__(self, actor_system):
        super().__init__(actor_system)
        self.processes: dict[str, Process] = {}  # Tracks browser processes by ID
        self.default_args = ["--remote-debugging-port=9222"]  # Default browser args
        self.health_check_running = False

    async def start_browser_process(self, cmd: StartBrowserCommand):
        if cmd.browser_id in self.processes:
            await self.stop_browser_process(
                StopBrowserCommand(browser_id=cmd.browser_id)
            )
        args = self.default_args if cmd.custom_args is None else cmd.custom_args
        self.processes[cmd.browser_id] = await asyncio.create_subprocess_exec(
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await self.start_health_check()
        logger.info(f"Started browser process with ID {cmd.browser_id}.")

    async def stop_browser_process(self, cmd: StopBrowserCommand):
        process = self.processes.pop(cmd.browser_id, None)
        if process:
            try:
                process.terminate()
                await self.stop_health_check()
                logger.info(f"Stopped browser process with ID {cmd.browser_id}.")
            except ProcessLookupError:
                logger.info(f"Process already terminated {cmd.browser_id}.")

    async def restart_browser_process(self, cmd: RestartBrowserCommand):
        await self.publish(StopBrowserCommand(browser_id=cmd.browser_id))
        await asyncio.sleep(5)
        await self.publish(StartBrowserCommand(browser_id=cmd.browser_id))

    async def update_browser_config(self, cmd: UpdateBrowserConfigCommand):
        logger.info(
            f"Updating browser configuration for ID {cmd.browser_id}: {cmd.new_args}"
        )
        await self.publish(RestartBrowserCommand())

    async def start_health_check(self):
        self.health_check_running = True

        while self.health_check_running:
            for browser_id, process in self.processes.items():
                if process.returncode is None:
                    logger.info(f"Browser process {browser_id} is alive.")
                    await self.publish(BrowserStatusEvent(status="alive"))
                else:
                    logger.warning(
                        f"Browser process {browser_id} is unresponsive. Restarting..."
                    )
                    await self.publish(BrowserStatusEvent(status="dead"))
                    await self.publish(RestartBrowserCommand())
            await asyncio.sleep(10)  # Sleep for 60 seconds before the next check

    async def stop_health_check(self):
        self.health_check_running = False

    async def handle_browser_status_event(self, event: BrowserStatusEvent):
        print(event)


# Example usage
async def main():
    actor_system = ActorSystem()
    proc_supervisor = await actor_system.actor_of(BrowserProcessSupervisor)
    browser_actor = await actor_system.actor_of(BrowserWorker)

    # Start Chrome Browser
    await actor_system.publish(StartBrowserCommand())

    # await actor_system.publish(StopBrowserCommand())

    # Perform browser actions using BrowserActor
    logger.info("Main function done.")

    # Stop Chrome Browser
    await asyncio.sleep(500)


if __name__ == "__main__":
    asyncio.run(main())
