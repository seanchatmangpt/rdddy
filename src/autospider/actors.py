from autospider.messages import (
    EvaluateScrapingPostconditionQuery,
    EvaluateScrapingPreconditionQuery,
    ExecuteScrapingCommand,
    ScrapingCompletedEvent,
    ScrapingErrorEvent,
    ScrapingPostconditionEvaluatedEvent,
    ScrapingPreconditionEvaluatedEvent,
    StartScrapingCommand,
)
from rdddy.abstract_actor import AbstractActor


class InitiationActor(AbstractActor):
    async def handle_start_scraping_command(self, message: StartScrapingCommand):
        print(f"Received StartScrapingCommand: Starting scraping for URL {message.url}")
        # Example: Trigger precondition evaluation
        await self.publish(EvaluateScrapingPreconditionQuery(url=message.url))


class PreconditionActor(AbstractActor):
    async def handle_evaluate_scraping_precondition_query(
        self, message: EvaluateScrapingPreconditionQuery
    ):
        print(f"Evaluating scraping precondition for URL {message.url}")
        # Example: Pretend the precondition is always met
        await self.publish(ScrapingPreconditionEvaluatedEvent(url=message.url, result=True))


class ProcessingActor(AbstractActor):
    async def handle_scraping_precondition_evaluated_event(
        self, message: ScrapingPreconditionEvaluatedEvent
    ):
        if message.result:
            print(f"Precondition met for URL {message.url}, executing scraping...")
            await self.publish(ExecuteScrapingCommand(url=message.url))
        else:
            print(f"Precondition not met for URL {message.url}, aborting...")
            await self.publish(
                ScrapingErrorEvent(url=message.url, error_message="Precondition failed")
            )


class ExecutionActor(AbstractActor):
    async def handle_execute_scraping_command(self, message: ExecuteScrapingCommand):
        print(f"Executing scraping for URL {message.url}")
        # Example: After execution, evaluate postconditions
        await self.publish(EvaluateScrapingPostconditionQuery(url=message.url))

    async def handle_evaluate_scraping_post_condition_query(
        self, message: EvaluateScrapingPostconditionQuery
    ):
        await self.publish(ScrapingPostconditionEvaluatedEvent(url=message.url, result=True))


class CompletionActor(AbstractActor):
    async def handle_scraping_postcondition_evaluated_event(
        self, message: ScrapingPostconditionEvaluatedEvent
    ):
        if message.result:
            print(f"Scraping completed successfully for URL {message.url}.")
            await self.publish(
                ScrapingCompletedEvent(url=message.url, scraped_data={"hello": "world"})
            )
        else:
            print(f"Postconditions not met for URL {message.url}.")
            await self.publish(
                ScrapingErrorEvent(url=message.url, error_message="Postcondition failed")
            )
