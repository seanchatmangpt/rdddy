from rdddy.messages import *


class DatasetLoaded(AbstractEvent):
    """Event triggered by DatasetLoaded."""


class PipelineBuilt(AbstractEvent):
    """Event triggered by PipelineBuilt."""


class PipelineOptimized(AbstractEvent):
    """Event triggered by PipelineOptimized."""


class PipelineExecuted(AbstractEvent):
    """Event triggered by PipelineExecuted."""


class PipelineEvaluated(AbstractEvent):
    """Event triggered by PipelineEvaluated."""


class RetrievalEvaluated(AbstractEvent):
    """Event triggered by RetrievalEvaluated."""


class LoadDataset(AbstractCommand):
    """Command to execute LoadDataset."""


class BuildPipeline(AbstractCommand):
    """Command to execute BuildPipeline."""


class OptimizePipeline(AbstractCommand):
    """Command to execute OptimizePipeline."""


class ExecutePipeline(AbstractCommand):
    """Command to execute ExecutePipeline."""


class EvaluatePipeline(AbstractCommand):
    """Command to execute EvaluatePipeline."""


class EvaluateRetrieval(AbstractCommand):
    """Command to execute EvaluateRetrieval."""


class GetDataset(AbstractQuery):
    """Query to retrieve GetDataset."""


class GetPipeline(AbstractQuery):
    """Query to retrieve GetPipeline."""


class GetOptimizedPipeline(AbstractQuery):
    """Query to retrieve GetOptimizedPipeline."""


class GetPipelineExecution(AbstractQuery):
    """Query to retrieve GetPipelineExecution."""


class GetPipelineEvaluation(AbstractQuery):
    """Query to retrieve GetPipelineEvaluation."""


class GetRetrievalEvaluation(AbstractQuery):
    """Query to retrieve GetRetrievalEvaluation."""
