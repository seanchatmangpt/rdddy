from rdddy.messages import *


class CreateNewRoute(Event):
    """
    Event triggered by CreateNewRoute.
    """

    pass


class InjectHandler(Event):
    """
    Event triggered by InjectHandler.
    """

    pass


class ExecuteHealthCheck(Event):
    """
    Event triggered by ExecuteHealthCheck.
    """

    pass


class ExecuteShazamOperation(Event):
    """
    Event triggered by ExecuteShazamOperation.
    """

    pass


class ExecuteHygenRouteNew(Command):
    """
    Command to execute ExecuteHygenRouteNew.
    """

    pass


class LoadModules(Command):
    """
    Command to execute LoadModules.
    """

    pass


class ConstructRoutes(Command):
    """
    Command to execute ConstructRoutes.
    """

    pass


class RetrieveHealthStatus(Query):
    """
    Query to retrieve RetrieveHealthStatus.
    """

    pass


class RetrieveShazamOperation(Query):
    """
    Query to retrieve RetrieveShazamOperation.
    """

    pass
