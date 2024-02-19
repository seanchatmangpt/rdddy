from rdddy.messages import *


class StartScrapingCommand(AbstractCommand):
    """Command to initiate scraping for a given URL."""

    url: str


class EvaluateScrapingPreconditionQuery(AbstractQuery):
    """Query to evaluate if the preconditions for scraping a URL are met."""

    url: str


class ScrapingPreconditionEvaluatedEvent(AbstractEvent):
    """Event indicating the result of scraping preconditions evaluation."""

    phase_name: str = "Scraping Precondition Evaluation"
    url: str
    result: bool


class ExecuteScrapingCommand(AbstractCommand):
    """Command to execute the scraping process for a given URL."""

    url: str


class ScrapingErrorEvent(AbstractEvent):
    """Event indicating an error occurred during the scraping process."""

    phase_name: str
    url: str
    error_message: str


class EvaluateScrapingPostconditionQuery(AbstractQuery):
    """Query to evaluate if the postconditions after scraping a URL are met."""

    url: str


class ScrapingPostconditionEvaluatedEvent(AbstractEvent):
    """Event indicating the result of scraping postconditions evaluation."""

    phase_name: str = "Scraping Postcondition Evaluation"
    url: str
    result: bool


class ScrapingCompletedEvent(AbstractEvent):
    """Event indicating the completion of the scraping process."""

    phase_name: str = "Scraping Completed"
    url: str
    scraped_data: dict  # Assuming scraped data is stored as a dictionary
