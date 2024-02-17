from rdddy.messages import *


class StartPhaseCommand(Command):
    phase_name: str


class PhaseStartedEvent(Event):
    phase_name: str


class EvaluatePreconditionQuery(Query):
    phase_name: str


class PreconditionEvaluatedEvent(Event):
    phase_name: str
    result: bool


class ProcessPhaseCommand(Command):
    phase_name: str


class PhaseProcessedEvent(Event):
    phase_name: str


class EvaluatePostconditionQuery(Query):
    phase_name: str


class PostconditionEvaluatedEvent(Event):
    phase_name: str
    result: bool


class PhaseCompletedEvent(Event):
    phase_name: str


class PhaseErrorEvent(Event):
    phase_name: str
    error_message: str
