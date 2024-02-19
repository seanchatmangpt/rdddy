# async_concurrent_nanofiction.py

import asyncio
import datetime
import random


class SyntheticLog:
    def __init__(self, timestamp, message):
        self.timestamp = timestamp
        self.message = message

    def __str__(self):
        return f"[{self.timestamp}] {self.message}"


# Asynchronous function to simulate the upgrade process
async def upgrade_component(upgrading_component, upgraded_component, delay):
    await asyncio.sleep(delay)  # Simulate time taken for upgrade
    current_date = datetime.datetime.now()
    return SyntheticLog(
        current_date,
        f"{upgrading_component} initiates upgrade of {upgraded_component}.",
    )


# Asynchronous generator to produce synthetic logs
async def synthetic_log_generator():
    upgrade_sequence = ["Denz", "DomainDef", "LivingCharter"]
    for i in range(1, 10):
        upgrading_component = upgrade_sequence[i % len(upgrade_sequence)]
        upgraded_component = upgrade_sequence[(i - 1) % len(upgrade_sequence)]

        # Simulate a random delay for each upgrade process
        # delay = random.uniform(0.5, 2.0)
        yield await upgrade_component(upgrading_component, upgraded_component, 0)

        if upgrading_component == "LivingCharter":
            feature = random.choice(
                [
                    "VOC Analysis",
                    "QFD Implementation",
                    "FMEA Process",
                    "DOE and CTQs",
                    "Control Plan",
                ]
            )
            yield SyntheticLog(datetime.datetime.now(), f"LivingCharter automates {feature}.")

        elif upgrading_component == "DomainDef":
            yield SyntheticLog(
                datetime.datetime.now(),
                f"DomainDef enhances model precision for {upgraded_component}.",
            )

        elif upgrading_component == "Denz":
            yield SyntheticLog(
                datetime.datetime.now(),
                f"Denz optimizes reactive DDD framework for {upgraded_component}.",
            )


# Main asynchronous function to gather and display logs
async def main():
    logs = []
    async for log in synthetic_log_generator():
        logs.append(log)

    for log in logs:
        print(log)


# Run the asynchronous main function
asyncio.run(main())
asyncio.run(main())
asyncio.run(main())
asyncio.run(main())
asyncio.run(main())
asyncio.run(main())
