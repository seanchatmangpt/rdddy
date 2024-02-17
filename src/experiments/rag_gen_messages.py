from rdddy.messages import *


class DatasetLoaded(Event):
    """
    Event triggered by DatasetLoaded.
    """

    pass


class PipelineBuilt(Event):
    """
    Event triggered by PipelineBuilt.
    """

    pass


class PipelineOptimized(Event):
    """
    Event triggered by PipelineOptimized.
    """

    pass


class PipelineExecuted(Event):
    """
    Event triggered by PipelineExecuted.
    """

    pass


class PipelineEvaluated(Event):
    """
    Event triggered by PipelineEvaluated.
    """

    pass


class RetrievalEvaluated(Event):
    """
    Event triggered by RetrievalEvaluated.
    """

    pass


class LoadDataset(Command):
    """
    Command to execute LoadDataset.
    """

    pass


class BuildPipeline(Command):
    """
    Command to execute BuildPipeline.
    """

    pass


class OptimizePipeline(Command):
    """
    Command to execute OptimizePipeline.
    """

    pass


class ExecutePipeline(Command):
    """
    Command to execute ExecutePipeline.
    """

    pass


class EvaluatePipeline(Command):
    """
    Command to execute EvaluatePipeline.
    """

    pass


class EvaluateRetrieval(Command):
    """
    Command to execute EvaluateRetrieval.
    """

    pass


class GetDataset(Query):
    """
    Query to retrieve GetDataset.
    """

    pass


class GetPipeline(Query):
    """
    Query to retrieve GetPipeline.
    """

    pass


class GetOptimizedPipeline(Query):
    """
    Query to retrieve GetOptimizedPipeline.
    """

    pass


class GetPipelineExecution(Query):
    """
    Query to retrieve GetPipelineExecution.
    """

    pass


class GetPipelineEvaluation(Query):
    """
    Query to retrieve GetPipelineEvaluation.
    """

    pass


class GetRetrievalEvaluation(Query):
    """
    Query to retrieve GetRetrievalEvaluation.
    """

    pass
