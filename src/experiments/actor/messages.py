from rdddy.messages import *


class StartPhaseCommand(AbstractCommand):
    phase_name: str


class PhaseStartedEvent(AbstractEvent):
    phase_name: str


class EvaluatePreconditionQuery(AbstractQuery):
    phase_name: str


class PreconditionEvaluatedEvent(AbstractEvent):
    phase_name: str
    result: bool


class ProcessPhaseCommand(AbstractCommand):
    phase_name: str


class PhaseProcessedEvent(AbstractEvent):
    phase_name: str


class EvaluatePostconditionQuery(AbstractQuery):
    phase_name: str


class PostconditionEvaluatedEvent(AbstractEvent):
    phase_name: str
    result: bool


class PhaseCompletedEvent(AbstractEvent):
    phase_name: str


class PhaseErrorEvent(AbstractEvent):
    phase_name: str
    error_message: str
