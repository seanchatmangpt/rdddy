from playwright.async_api import Page

from rdddy.messages import *


# Define commands and events
class StartBrowserCommand(Command):
    browser_id: str = "default"
    custom_args: list[str] = None


class BrowserStartedEvent(Event):
    pass


class StopBrowserCommand(Command):
    browser_id: str = "default"


class RestartBrowserCommand(Command):
    browser_id: str = "default"


# Example command class for updating configuration
class UpdateBrowserConfigCommand(Command):
    browser_id: str = "default"
    new_args: dict = {}


class BrowserStatusEvent(Event):
    status: str


class Click(Command):
    """Matches the pyppeteer page click exactly"""

    selector: str
    options: dict = None


class Goto(Command):
    """Matches the pyppeteer page goto exactly"""

    url: str
    options: dict = None


class TypeText(Command):
    """Matches the pyppeteer page type exactly"""

    selector: str
    text: str
    options: dict = None


class SendChatGPT(Command):
    prompt: str
    page: Page


class ChatGPTResponse(Event):
    """Contents are the response from the site"""


class FindElement(Command):
    """Find an element by selector"""

    selector: str


class ElementFound(Event):
    """Element found in the page"""


class NavigateBack(Command):
    """Navigate back in the browser history"""


class NavigateForward(Command):
    """Navigate forward in the browser history"""


class ReloadPage(Command):
    """Reload the current page"""


class GetPageContent(Command):
    """Get the HTML content of the current page"""


class PageContent(Event):
    """HTML content of the page"""

    content: str


class ExecuteScript(Command):
    """Execute JavaScript code on the page"""

    script: str


class ScriptResult(Event):
    """Result of the executed JavaScript code"""

    result: Any  # You can specify the data type based on the expected result


class CloseBrowser(Command):
    """Close the browser"""


class BrowserClosed(Event):
    """Browser has been closed"""


class SetViewportSize(Command):
    """Set the viewport size of the browser"""

    width: int
    height: int


class ViewportSizeSet(Event):
    """Viewport size has been set successfully"""
