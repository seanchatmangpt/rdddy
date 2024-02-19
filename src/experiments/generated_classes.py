from rdddy.messages import *


class CreateNewRoute(AbstractEvent):
    """Event triggered by CreateNewRoute."""


class InjectHandler(AbstractEvent):
    """Event triggered by InjectHandler."""


class ExecuteHealthCheck(AbstractEvent):
    """Event triggered by ExecuteHealthCheck."""


class ExecuteShazamOperation(AbstractEvent):
    """Event triggered by ExecuteShazamOperation."""


class ExecuteHygenRouteNew(AbstractCommand):
    """Command to execute ExecuteHygenRouteNew."""


class LoadModules(AbstractCommand):
    """Command to execute LoadModules."""


class ConstructRoutes(AbstractCommand):
    """Command to execute ConstructRoutes."""


class RetrieveHealthStatus(AbstractQuery):
    """Query to retrieve RetrieveHealthStatus."""


class RetrieveShazamOperation(AbstractQuery):
    """Query to retrieve RetrieveShazamOperation."""
